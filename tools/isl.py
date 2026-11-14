#!/usr/bin/env python3
"""Formatter and linter for MICROS RES 3700 ISL scripts.

Formatting::

    isl.py fmt FILE...             print formatted source
    isl.py fmt --write FILE...     rewrite files in place
    isl.py fmt --check FILE...     exit 1 if any file would change
    isl.py fmt -                   stdin -> stdout (editor integration)
    isl.py fmt --lines A-B FILE    format only lines A..B (1-based, inclusive)

Linting::

    isl.py lint FILE...            file:line:col: severity LNNN message
    isl.py lint --fix FILE...      format in place, then report what remains
    isl.py lint --format json FILE...
    isl.py lint --strict FILE...   fail on warnings too
    isl.py lint --lines A-B FILE   report only findings on lines A..B

Both take --indent N (spaces per level, default 2). Standard library only.
Also holds the vocabulary used by gen_isl_grammar.py. See
skills/micros-isl-3700/SKILL.md for the style guide and rule list.
"""


from __future__ import annotations

import argparse
import difflib
import json
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
displayinput displayinverse displayislts displaymsinput displayreararea
displaytouchscreen dllcall dllcall_cdecl dllfree dllload editdetail errorbeep
errormessage exitcancel exitcontinue exitoncancel exitwitherror fclose fopen
format formatbuffer formatq fread freadbfr freadln fseek fwrite fwritebfr
fwriteln getenterorclear getrxmsg include infomessage input inputkey linefeed
listdisplay listinput listprint loaddbkybdmacro loadkybdmacro loadmaginfo
lowercase makeascii mid msleep printline prompt prorate regidleevent
retainglobalvar return rxmsg savechkinfo saverefinfo setisltskey setisltskeyx
setsignonleft setsignonright setstring split splitq system test_dsvc
touchscreen txmsg uppercase usecompatformat useislformat usefiltereddetail
useunfiltereddetail useisltimeouts usestdtimeouts var voiddetail waitforclear
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



def format_range(text: str, start: int, end: int, indent: int = DEFAULT_INDENT) -> str:
    """Format only lines start..end (1-based, inclusive).

    The whole file is formatted so the block context is right; only lines inside
    the range are taken from the result. Lines outside it are left untouched.
    """
    old = text.split('\n')
    new = format_source(text, indent).split('\n')
    sm = difflib.SequenceMatcher(None, [x.strip() for x in old], [x.strip() for x in new],
                                 autojunk=False)
    out = list(old)
    for tag, i1, i2, j1, _j2 in sm.get_opcodes():
        if tag != 'equal':
            continue
        for k in range(i2 - i1):
            if start <= i1 + k + 1 <= end:
                out[i1 + k] = new[j1 + k].rstrip() if not old[i1 + k].strip() else new[j1 + k]
    return '\n'.join(out)


def parse_lines(spec: str) -> tuple[int, int]:
    a, _, b = spec.partition('-')
    start = int(a)
    return start, int(b or a)


def _read(path: str) -> str:
    return sys.stdin.read() if path == '-' else Path(path).read_text(encoding='utf-8')


# ---------------------------------------------------------------- linting

@dataclass
class Diag:
    path: str
    line: int
    col: int
    severity: str     # error | warning
    code: str
    message: str
    fixable: bool = False

    def text(self) -> str:
        return (f'{self.path}:{self.line}:{self.col}: {self.severity} '
                f'{self.code} {self.message}')


def split_args(s: str) -> list[str]:
    """Split a call argument string on top-level commas."""
    args, cur, depth, in_str = [], [], 0, False
    for ch in s:
        if in_str:
            cur.append(ch)
            in_str = ch != '"'
            continue
        if ch == '"':
            in_str = True
        elif ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        elif ch == ',' and depth == 0:
            args.append(''.join(cur).strip())
            cur = []
            continue
        cur.append(ch)
    tail = ''.join(cur).strip()
    if tail or args:
        args.append(tail)
    return args


def parse_params(s: str | None) -> list[tuple[str, bool]]:
    """Return [(mode, is_array)] for a sub parameter list; mode is var/ref."""
    if not s or not s.strip():
        return []
    params = []
    for part in split_args(s):
        words = part.split()
        mode = words[0].lower() if words else ''
        params.append((mode, '[' in part))
    return params


def logical_text(lines: list[Line], start: int) -> str:
    """Join a statement and its continuation lines (comments dropped)."""
    parts = []
    i = start
    while i < len(lines):
        ln = lines[i]
        piece = ln.code_raw.rstrip()
        if ln.continues and piece.endswith('\\'):
            piece = piece[:-1]
        parts.append(piece.strip())
        if not ln.continues:
            break
        i += 1
    return ' '.join(parts)


def lint_source(text: str, path: str = '<stdin>', indent: int = DEFAULT_INDENT
                ) -> list[Diag]:
    lines = scan(text)
    diags: list[Diag] = []

    def add(ln: Line, sev: str, code: str, msg: str, col: int = 1,
            fixable: bool = False) -> None:
        diags.append(Diag(path, ln.number, col, sev, code, msg, fixable))

    stack: list[tuple[str, Line]] = []
    subs: dict[str, tuple[Line, list[tuple[str, bool]]]] = {}
    calls: list[tuple[Line, str, list[str]]] = []
    wildcard_seen: dict[str, Line] = {}     # event name -> its * event
    has_rxmsg_event = False
    timeouts_handled = False
    waits: list[Line] = []

    for idx, ln in enumerate(lines):
        if ln.blank or ln.comment_only or ln.continuation:
            continue
        tok = ln.token
        stmt = logical_text(lines, idx)
        low = stmt.lower()

        if tok in ('event', 'sub') and stack:
            # events and subs are top-level: whatever is still open was never
            # closed. Report once and resync so one slip does not cascade.
            for t, opened in stack:
                add(opened, 'error', 'L002',
                    f'{t} is never closed (next {tok} starts on line {ln.number})')
            stack.clear()
        if tok in BLOCK_OPEN:
            stack.append((tok, ln))
        elif tok in BLOCK_CLOSE:
            if not stack:
                add(ln, 'error', 'L002', f'{tok} without a matching block')
            elif stack[-1][0] not in BLOCK_CLOSE[tok]:
                top = stack[-1]
                add(ln, 'error', 'L002',
                    f'{tok} does not match {top[0]} opened on line {top[1].number}')
                stack.pop()
            else:
                stack.pop()
        elif tok in BLOCK_MIDDLE:
            if not stack or stack[-1][0] != 'if':
                add(ln, 'error', 'L002', f'{tok} outside an if block')
        elif tok == 'break':
            if not any(t in LOOPS for t, _ in stack):
                add(ln, 'error', 'L002', 'break outside a for/forever/while loop')

        if tok == 'event':
            _lint_event(ln, stmt, lines, add)
            m = EVENT_RE.match(stmt)
            if m:
                name = m.group(1).lower()
                arg = (m.group(2) or '').strip()
                if name == 'rxmsg':
                    has_rxmsg_event = True
                    if arg.lower() == '_timeout':
                        timeouts_handled = True
                star = wildcard_seen.get(name)
                if star is not None and arg != '*':
                    add(ln, 'error', 'L003',
                        f'event {name} follows the * event on line {star.number}; '
                        'the * event must come after the specific ones')
                if arg == '*' and star is None:
                    wildcard_seen[name] = ln
        elif tok == 'sub':
            m = SUB_RE.match(stmt)
            if not m:
                add(ln, 'error', 'L002', 'malformed sub declaration')
            else:
                name = m.group(1).lower()
                if name in subs:
                    add(ln, 'error', 'L006',
                        f'duplicate sub {m.group(1)} (first defined on line '
                        f'{subs[name][0].number}; the first one wins)')
                else:
                    subs[name] = (ln, parse_params(m.group(2)))
                _lint_docstring(ln, lines, idx, add, f'sub {m.group(1)}')
        elif tok == 'call':
            m = re.match(r'call\s+(\w+)\s*(?:\((.*)\))?\s*$', stmt, re.I)
            if m:
                args = split_args(m.group(2)) if m.group(2) else []
                calls.append((ln, m.group(1).lower(), args))
        elif tok in ('waitforrxmsg', 'getrxmsg'):
            waits.append(ln)
        elif tok == 'useisltimeouts':
            timeouts_handled = True
        elif tok and tok not in KNOWN_COMMANDS and not ASSIGN_RE.match(stmt):
            add(ln, 'warning', 'L001', f'unknown command "{tok}" (not in the '
                'ISL reference; 9700-only or a typo?)')
        _ = low

    for _t, ln in stack:
        add(ln, 'error', 'L002', f'{_t} is never closed')

    # L009 calls against known subs
    for ln, name, args in calls:
        if name not in subs:
            add(ln, 'warning', 'L009', f'call to unknown sub "{name}"')
            continue
        params = subs[name][1]
        if len(args) != len(params):
            add(ln, 'error', 'L009', f'{name} takes {len(params)} argument(s), '
                f'{len(args)} given')
            continue
        for a, (mode, is_arr) in zip(args, params):
            if mode == 'ref' and (a.startswith('"') or re.match(r'^[\d$-]', a)):
                add(ln, 'error', 'L009', f'ref parameter given a literal: {a}')
            if is_arr and '[' not in a and not a.startswith('@'):
                add(ln, 'error', 'L009', f'array parameter needs "name[]": {a}')

    # L006/L007 file-level messaging checks
    for ln in waits:
        if ln.token == 'waitforrxmsg' and not has_rxmsg_event:
            add(ln, 'warning', 'L006', 'waitforrxmsg but the file defines no '
                'event rxmsg handlers')
    if waits and not timeouts_handled:
        add(waits[0], 'warning', 'L007', 'waits for a reply but no '
            'UseISLTimeOuts / event rxmsg : _timeout handling found')

    # L008 whitespace / indentation (fixable by formatting)
    formatted = format_source(text, indent).split('\n')
    # map formatted non-blank lines back by walking both in step
    orig_nonblank = [ln for ln in lines if not ln.blank]
    fmt_nonblank = [f for f in formatted if f.strip()]
    if len(orig_nonblank) == len(fmt_nonblank):
        for ln, want in zip(orig_nonblank, fmt_nonblank):
            if ln.raw.rstrip() != want:
                has_tab = '\t' in ln.lead
                add(ln, 'warning', 'L008',
                    'tab indentation' if has_tab else
                    f'indentation should be {len(want) - len(want.lstrip())} spaces'
                    if ln.raw.rstrip().lstrip() == want.lstrip()
                    else 'whitespace differs from formatted output',
                    fixable=True)
            elif ln.raw != ln.raw.rstrip():
                add(ln, 'warning', 'L008', 'trailing whitespace',
                    col=len(ln.raw.rstrip()) + 1, fixable=True)
    for ln in lines:
        if ln.blank and ln.raw:
            add(ln, 'warning', 'L008', 'trailing whitespace', fixable=True)
    run = 0
    for ln in lines:
        run = run + 1 if ln.blank else 0
        if run == 3:
            add(ln, 'warning', 'L008', 'more than two consecutive blank lines', fixable=True)
    if text and not text.endswith('\n'):
        add(lines[-1], 'warning', 'L008', 'no newline at end of file',
            col=len(lines[-1].raw) + 1, fixable=True)

    diags.sort(key=lambda d: (d.line, d.col, d.code))
    return diags


def _lint_event(ln: Line, stmt: str, lines: list[Line], add) -> None:
    m = EVENT_RE.match(stmt)
    if not m:
        add(ln, 'error', 'L001', 'malformed event declaration')
        return
    name = m.group(1).lower()
    arg = m.group(2)
    if name not in KNOWN_EVENTS:
        add(ln, 'error', 'L001', f'unknown event "{m.group(1)}"'
            + (' (there is no plain Event Void)' if name == 'void' else ''))
    if name in NUMERIC_EVENTS and not (arg and (arg.isdigit() or arg == '*')):
        add(ln, 'error', 'L001', f'event {name} needs a number or *')
    if name == 'rxmsg' and not arg:
        add(ln, 'error', 'L001', 'event rxmsg needs a message id')
    if name == 'inq':
        text = ln.comment[2:].strip() if ln.comment else ''
        if not text:
            add(ln, 'warning', 'L004',
                'inquire needs a trailing // description (shown in the symbol list)',
                col=len(ln.raw.rstrip()) + 1)
    label = f'event {m.group(1)}' + (f' : {arg}' if arg else '')
    _lint_docstring(ln, lines, ln.stmt, add, label)


def _lint_docstring(ln: Line, lines: list[Line], idx: int, add, label: str) -> None:
    prev = lines[idx - 1].raw.strip() if idx > 0 else ''
    if not BANNER_RE.match(prev):
        add(ln, 'warning', 'L005',
            f'{label} has no docstring banner (// ****...) on the line above')


# ---------------------------------------------------------------- CLI

def cmd_fmt(args) -> int:
    changed = 0
    for path in args.files:
        src = _read(path)
        if args.lines:
            out = format_range(src, *parse_lines(args.lines), indent=args.indent)
        else:
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


def cmd_lint(args) -> int:
    all_diags: list[Diag] = []
    for path in args.files:
        src = _read(path)
        if args.fix and path != '-':
            out = format_source(src, args.indent)
            if out != src:
                Path(path).write_text(out, encoding='utf-8')
                src = out
        found = lint_source(src, path, args.indent)
        if args.lines:
            lo, hi = parse_lines(args.lines)
            found = [d for d in found if lo <= d.line <= hi]
        all_diags += found
    if args.format == 'json':
        print(json.dumps([d.__dict__ for d in all_diags], indent=2))
    else:
        for d in all_diags:
            print(d.text())
    errors = sum(d.severity == 'error' for d in all_diags)
    warnings = len(all_diags) - errors
    if args.format != 'json' and all_diags:
        print(f'{errors} error(s), {warnings} warning(s)', file=sys.stderr)
    return 1 if errors or (args.strict and warnings) else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='isl', description='Format and lint MICROS ISL scripts')
    sub = p.add_subparsers(dest='cmd', required=True)

    def common(sp):
        sp.add_argument('files', nargs='+', help='ISL files, or - for stdin')
        sp.add_argument('--indent', type=int, default=DEFAULT_INDENT,
                        help='spaces per level (default 2)')
        sp.add_argument('--lines', metavar='A-B', help='only these 1-based lines')

    f = sub.add_parser('fmt', help='format scripts')
    common(f)
    g = f.add_mutually_exclusive_group()
    g.add_argument('--write', action='store_true', help='rewrite files in place')
    g.add_argument('--check', action='store_true', help='exit 1 if changes needed')
    f.set_defaults(func=cmd_fmt)

    lp = sub.add_parser('lint', help='report problems')
    common(lp)
    lp.add_argument('--fix', action='store_true', help='re-format files first')
    lp.add_argument('--format', choices=['text', 'json'], default='text')
    lp.add_argument('--strict', action='store_true', help='fail on warnings too')
    lp.set_defaults(func=cmd_lint)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
