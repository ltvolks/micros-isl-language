#!/usr/bin/env python3
"""Formatter for MICROS RES 3700 ISL scripts (also holds the shared vocabulary).

    isl_fmt.py FILE...            print formatted source
    isl_fmt.py --write FILE...    rewrite files in place
    isl_fmt.py --check FILE...    exit 1 if any file would change
    isl_fmt.py -                  stdin -> stdout (editor integration)
    isl_fmt.py --indent N         spaces per level (default 2)

Standard library only. See skills/micros-isl-3700/SKILL.md for the style guide.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_INDENT = 2

# ---------------------------------------------------------------- vocabulary

BLOCK_OPEN = {'event', 'sub', 'if', 'for', 'forever', 'while',
              'startprint', 'startprintwithstatus'}
BLOCK_MIDDLE = {'else', 'elseif'}
# closer -> openers it may close
BLOCK_CLOSE = {
    'endevent': {'event'},
    'endsub': {'sub'},
    'endif': {'if'},
    'endfor': {'for', 'forever'},
    'endwhile': {'while'},
    'endprint': {'startprint', 'startprintwithstatus'},
    'endprintff': {'startprint', 'startprintwithstatus'},
    'endprintnoff': {'startprint', 'startprintwithstatus'},
}
LOOPS = {'for', 'forever', 'while'}

# Statement-leading words known to ISL on 3700 (isl-reference commands.md and
# functions.md). Unknown words are reported as warnings, not errors.
KNOWN_COMMANDS = set("""
break call cleararray clearchkid clearchkinfo clearislts clearkybdmacro
clearreararea continueoncancel debug discardglobalvar display display_rear_area
displayinput displayinverse displayislts displaymsinput displayrearea
displaytouchscreen dllcall dllcall_cdecl dllfree dllload editdetail errorbeep
errormessage exitcancel exitcontinue exitoncancel exitwitherror fclose fopen
format formatbuffer formatq fread freadbfr freadln fseek fwrite fwritebfr
fwriteln getenterorclear getrxmsg include infomessage input inputkey linefeed
listdisplay listinput listprint loaddbkybdmacro loadkybdmacro loadmaginfo
lowercase makeascii mid msleep printline prompt prorate regidleevent
retainglobalvar return rxmsg savechkinfo saverefinfo setisltskey setisltskeyx
setsignonleft setsignonright setstring split splitq system test_dsvc
touchscreen txmsg uppercase usecompatformat useisformat usefilteredetail
useunfilteredetail useisltimeouts usestdtimeouts var voiddetail waitforclear
waitforconfirm waitforenter waitforrxmsg window windowedit windowinput
windoweditwithsave windowinputwithsave windowclear windowclose windowscrolldown
windowscrollup beep
""".split()) | BLOCK_OPEN | BLOCK_MIDDLE | set(BLOCK_CLOSE)

# Event names (isl-reference events.md plus names seen in real scripts).
KNOWN_EVENTS = set("""
begin_check clockin clockout dsc dsc_error_correct_items dsc_void dtl_changed
exit final_tender idle_no_trans init inq pickup_check pretender print_header
print_trailer rxmsg signin signout srvc_total svc svc_error_correct_items
svc_void tmed tndr tndr_error_correct_items tndr_void trans_cncl
""".split())
NUMERIC_EVENTS = {'inq', 'tmed'}

BANNER_RE = re.compile(r'^//\s*\*{8,}\s*$')
TOKEN_RE = re.compile(r'[A-Za-z_@][\w]*')
ASSIGN_RE = re.compile(r'^[@\w]+\s*(\[.*?\])?\s*=(?!=)')
EVENT_RE = re.compile(r'^event\s+([A-Za-z_]\w*)\s*(?::\s*(\S+))?', re.I)
SUB_RE = re.compile(r'^sub\s+(\w+)\s*(?:\((.*)\))?\s*$', re.I)


# ---------------------------------------------------------------- scanning

@dataclass
class Line:
    number: int                 # 1-based
    raw: str
    code: str = ''              # code part, comment removed, strings blanked
    code_raw: str = ''          # code part with strings intact
    comment: str = ''           # text from // onward ('' if none)
    lead: str = ''              # original leading whitespace
    token: str = ''             # first word, lowercased
    blank: bool = False
    comment_only: bool = False
    continuation: bool = False  # continues the previous logical line
    continues: bool = False     # ends with a backslash
    stmt: int = 0               # index of the line starting this logical line
    extra: dict = field(default_factory=dict)


def split_comment(text: str) -> tuple[str, str, str]:
    """Return (code_raw, code_blanked, comment) for one physical line."""
    in_str = False
    blanked: list[str] = []
    for i, ch in enumerate(text):
        if in_str:
            if ch == '"':
                in_str = False
                blanked.append('"')
            else:
                blanked.append(' ')
            continue
        if ch == '"':
            in_str = True
            blanked.append('"')
            continue
        if ch == '/' and text[i:i + 2] == '//':
            return text[:i], ''.join(blanked), text[i:]
        blanked.append(ch)
    return text, ''.join(blanked), ''


def scan(text: str) -> list[Line]:
    lines: list[Line] = []
    prev_continues = False
    stmt = 0
    for n, raw in enumerate(text.split('\n'), 1):
        raw = raw.rstrip('\r')
        stripped = raw.strip()
        ln = Line(number=n, raw=raw)
        ln.lead = raw[:len(raw) - len(raw.lstrip(' \t'))]
        if not stripped:
            ln.blank = True
            ln.stmt = len(lines)
            prev_continues = False
            lines.append(ln)
            continue
        code_raw, code, comment = split_comment(raw)
        ln.code_raw, ln.code, ln.comment = code_raw, code, comment
        ln.comment_only = not code.strip()
        ln.continues = (not ln.comment_only) and code.rstrip().endswith('\\')
        if prev_continues:
            ln.continuation = True
        else:
            stmt = len(lines)
        ln.stmt = stmt
        if not ln.comment_only and not ln.continuation:
            m = TOKEN_RE.match(code.strip())
            ln.token = m.group(0).lower() if m else ''
        prev_continues = ln.continues
        lines.append(ln)
    # a trailing '' from the final newline is not a line
    if lines and lines[-1].blank and lines[-1].raw == '':
        lines.pop()
    return lines


def expand_width(ws: str) -> int:
    return len(ws.expandtabs(4))


# ---------------------------------------------------------------- formatting

def format_source(text: str, indent: int = DEFAULT_INDENT) -> str:
    lines = scan(text)
    out: list[str] = []
    levels: dict[int, int] = {}      # stmt line index -> output level
    depth = 0
    blanks = 0
    for idx, ln in enumerate(lines):
        if ln.blank:
            blanks += 1
            if out and blanks <= 2:
                out.append('')
            continue
        blanks = 0
        text_line = ln.raw.strip()
        if ln.continuation:
            first = lines[ln.stmt]
            rel = max(0, expand_width(ln.lead) - expand_width(first.lead))
            out.append(' ' * (levels.get(ln.stmt, depth) * indent + rel)
                       + text_line.rstrip())
            continue
        if ln.comment_only:
            level = depth
        elif ln.token in BLOCK_CLOSE:
            depth = max(0, depth - 1)
            level = depth
        elif ln.token in BLOCK_MIDDLE:
            level = max(0, depth - 1)
        else:
            level = depth
        levels[idx] = level
        out.append(' ' * (level * indent) + text_line.rstrip())
        if not ln.comment_only and ln.token in BLOCK_OPEN:
            depth += 1
    while out and out[-1] == '':
        out.pop()
    return '\n'.join(out) + '\n' if out else ''



def _read(path: str) -> str:
    return sys.stdin.read() if path == '-' else Path(path).read_text(encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog='isl_fmt', description='Format ISL scripts')
    p.add_argument('files', nargs='+', help='ISL files, or - for stdin')
    p.add_argument('--indent', type=int, default=DEFAULT_INDENT, help='spaces per level (default 2)')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--write', action='store_true', help='rewrite files in place')
    g.add_argument('--check', action='store_true', help='exit 1 if changes needed')
    args = p.parse_args(argv)
    changed = 0
    for path in args.files:
        src = _read(path)
        out = format_source(src, args.indent)
        if path == '-':
            sys.stdout.write(out)
            continue
        if out != src:
            changed += 1
            if args.write:
                Path(path).write_text(out, encoding='utf-8')
                print(f'formatted {path}')
            elif args.check:
                print(f'would reformat {path}')
        if not (args.write or args.check):
            sys.stdout.write(out)
    return 1 if (args.check and changed) else 0


if __name__ == '__main__':
    raise SystemExit(main())
