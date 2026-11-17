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

# System variables (sysvars.md) and the read-only subset (marked "Read-Only" there).
KNOWN_SYSVARS = set("""
alphascreen autosvc backupservername beverage_reqd bootserialnum bootserialstr
cashier cashier_name ccauth_count ccdate ccnumber center chgtip chk
chk_autofire_time chk_delayed_order chk_future_order chk_open_time ckemp
ckemp_chkname ckemp_fname ckemp_lname ckemplopt ckid cknum ckseqnum com_active
customerinfo customerinfoline customerseq date day dbmemlen dbmemsize depdsci
dsc dsci dscittl dtl_autofire_time dtl_charge_tip_amount dtl_charge_tip_name
dtl_dining_course dtl_dsc_ittl dtl_dsc_sttl dtl_famgrp dtl_famgrp_objnum
dtl_has_charge_tip dtl_has_printed dtl_id dtl_is_auto_discount dtl_is_combo
dtl_is_combo_main dtl_is_combo_parent dtl_is_combo_side dtl_is_cond
dtl_is_coupon dtl_is_default_cond dtl_is_om dtl_is_om_base dtl_is_om_container
dtl_is_om_section dtl_is_om_specialty dtl_is_om_topping dtl_is_on_hold
dtl_is_void dtl_majgrp dtl_majgrp_objnum dtl_mlvl dtl_name dtl_name_two
dtl_object dtl_objnum dtl_ord_dev_output dtl_plvl dtl_prefix dtl_prep_time
dtl_prtgstchk dtl_prtrcpt dtl_qty dtl_seat dtl_selected dtl_sequence dtl_slvl
dtl_status dtl_taxtype dtl_ttl dtl_type dtl_typedef dwoff dwon emplopt
employee fieldstatus file_bfrsize file_errno file_errstr file_separator
filter_active filter_mask groupseqnum grpnum gst gstrmng gstthistender
guestseqnum hour idle_seconds inbackupmode ineditclosedcheck inputstatus
inreopenclosedcheck instandalonemode jnl key_cancel key_clear key_down_arrow
key_end key_enter key_exit key_home key_left_arrow key_page_down key_page_up
key_right_arrow key_up_arrow lastauthemp lastauthemp_fname lastauthemp_lname
line line_executed magstatus max_lines_to_run maxdtlr maxdtlt minute mlvl
month numdsc numdtlr numdtlt numsi numsvc numtax order_type_name ordertype
ordr parent_dtl_id platform pmsbuffer pmsnumber pmsseqnum prefix_dtl_name
prevpay printing printstatus rcpt redoff redon returnstatus rvc rvcname rxmsg
script seat second servername show_pms_messages si slvl srvprd strict_args
sustaincustomtext svc svci svcittl system tax taxrate tblid tblnum tblobjnum
test_dsvc_ttl time tmdnum tmdtypedef tndttl touchscreen trace trailer
trainingmode trdtlr trdtlt tremp tremp_chkname tremp_fname tremp_lname ttldue
txbl userentry uwsserialnum vald validate_mag_track varspace varused version
voidstatus warnings_are_fatal wcols weekday wrows wsid wsname wstype year
yearday
""".split())

READONLY_SYSVARS = set("""
alphascreen autosvc backupservername cashier cashier_name ccdate ccnumber
center chgtip chk chk_autofire_time chk_delayed_order chk_future_order
chk_open_time ckemp ckemp_chkname ckemp_fname ckemp_lname ckemplopt cknum
ckseqnum customerinfoline day depdsci dsci dscittl dtl_autofire_time
dtl_charge_tip_amount dtl_charge_tip_name dtl_dining_course dtl_dsc_ittl
dtl_dsc_sttl dtl_famgrp dtl_famgrp_objnum dtl_has_charge_tip dtl_id
dtl_is_auto_discount dtl_is_combo dtl_is_combo_main dtl_is_combo_parent
dtl_is_combo_side dtl_is_coupon dtl_is_void dtl_majgrp dtl_majgrp_objnum
dtl_mlvl dtl_name dtl_name_two dtl_object dtl_ord_dev_output dtl_plvl
dtl_prep_time dtl_prtgstchk dtl_prtrcpt dtl_qty dtl_seat dtl_selected
dtl_sequence dtl_slvl dtl_status dtl_ttl dtl_type dtl_typedef dwoff dwon
emplopt fieldstatus file_errstr filter_active filter_mask grpnum gst gstrmng
hour inbackupmode ineditclosedcheck inputstatus inreopenclosedcheck
instandalonemode jnl key_cancel key_clear key_down_arrow key_end key_enter
key_exit key_home key_left_arrow key_page_down key_page_up key_right_arrow
key_up_arrow lastauthemp lastauthemp_fname lastauthemp_lname line
line_executed magstatus maxdtlr maxdtlt minute mlvl month numdsc numdtlr
numdtlt numsi numsvc numtax order_type_name ordertype ordr parent_dtl_id
platform pmsseqnum prevpay printstatus rcpt redoff redon rvc rvcname rxmsg
seat second servername si slvl srvprd svc svci svcittl tax taxrate tblid
tblnum tmdnum tmdtypedef trainingmode trdtlr trdtlt tremp tremp_chkname
tremp_fname tremp_lname ttldue txbl userentry uwsserialnum vald varspace
varused version wcols weekday wrows wsid wsname wstype year yearday
""".split())

# Print directives and printer names that are not entries in sysvars.md.
EXTRA_SYSVARS = set("""
header ordr cust slip dwon dwoff redon redoff
""".split())

# Functions (functions.md) and their fixed argument counts where the syntax line
# states them. Used by L035.
KNOWN_FUNCTIONS = set("""
abs arraysize asc bit chr env feof ftell gethex getmaxdiscount instr key
keynumber keytype len makekeys mid tointeger trim varsize one_time_auto_discounts
clearchkid clearchkinfo clearreararea displayreararea displaytouchscreen
""".split())
FUNCTION_ARITY = {
    'abs': 1, 'arraysize': 1, 'asc': 1, 'bit': 2, 'chr': 1, 'feof': 1, 'ftell': 1,
    'gethex': 1, 'instr': 3, 'keynumber': 1, 'keytype': 1, 'len': 1,
    'makekeys': 1, 'mid': 3, 'tointeger': 1, 'trim': 1, 'varsize': 1,
}

# Commands that wait for the operator (L016) and ones that need a Window (L017).
USER_INPUT_COMMANDS = {
    'input', 'inputkey', 'listinput', 'displayinput', 'displaymsinput', 'windowedit',
    'windowinput', 'windoweditwithsave', 'windowinputwithsave', 'waitforclear',
    'waitforconfirm', 'waitforenter', 'getenterorclear',
}
NEEDS_WINDOW = {
    'display', 'displayinverse', 'displayinput', 'displaymsinput', 'listdisplay',
    'listinput', 'windowedit', 'windowinput', 'windoweditwithsave', 'windowinputwithsave',
}
# Commands allowed outside an Event or Sub (errors.md "Command outside procedure").
TOP_LEVEL_COMMANDS = {
    'var', 'continueoncancel', 'exitoncancel', 'prorate', 'retainglobalvar',
    'discardglobalvar', 'setsignonleft', 'setsignonright', 'usecompatformat',
    'useislformat', 'usestdtimeouts', 'useisltimeouts', 'include',
}
# Commands that take no arguments (errors.md "Expected end of line").
NO_ARGUMENT_COMMANDS = {
    'break', 'endevent', 'endif', 'endwhile', 'endsub', 'endfor', 'forever', 'endprint',
    'endprintff', 'endprintnoff', 'clearislts', 'displayislts',
}
PROMPT_COMMANDS = {'prompt', 'input', 'getenterorclear'}

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
                if t in ('event', 'sub') and t != tok:
                    add(ln, 'error', 'L014',
                        f'{tok} declared inside {t} (opened on line {opened.number}); '
                        'events and subs cannot be nested')
                else:
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
                add(ln, 'error', 'L025', 'malformed sub declaration')
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
            else:
                add(ln, 'error', 'L025', 'malformed call statement')
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

    _lint_semantics(lines, add)

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


# ---------------------------------------------------------------- semantic rules (L010-L037)

IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
SPEC_RE = re.compile(r'^(?:(?P<key>key)|(?P<t>[NnAa$])(?P<sz>\d+|\(.*\)))$', re.I)
SPEC_SPACE_RE = re.compile(r'^[NnAa$]\s+(\d|\()', re.I)
ASSIGN_FULL_RE = re.compile(r'^(?P<name>@?[A-Za-z_]\w*)\s*(?P<idx>\[.*?\])?\s*=(?!=)\s*(?P<rhs>.*)$', re.S)
INT_LIT = re.compile(r'^-?\s*\d+$')
DEC_LIT = re.compile(r'^-?\s*(\d+)\.(\d+)$')
STR_LIT = re.compile(r'^"([^"]*)"$')
SYSVAR_RE = re.compile(r'@\s?([A-Za-z_]\w*)')
FOR_RE = re.compile(r'^for\s+(?P<v>.+?)\s*=\s*(?P<a>.+?)\s+to\s+(?P<b>.+?)(?:\s+step\s+(?P<s>.+))?$',
                    re.I | re.S)
INDEX_LIT_RE = re.compile(r'(?<![\w@])([A-Za-z_]\w*)\s*\[\s*(-?\d+)\s*\]')
FUNC_CALL_RE = re.compile(r'(?<![\w@.])([A-Za-z_]\w*)\s*\(')
FORMAT_RE = re.compile(r'^(?:format|formatq)\s+(?P<rest>.*)$', re.I | re.S)
TRAILING_OP_RE = re.compile(r'([,+\-*/%<>=]|\b(?:and|or|not))\s*$', re.I)
DIVIDE_ZERO_RE = re.compile(r'/\s*0+(?![\d.\w])')
MAX_LEN_NAME = 255
MAX_VAR_SIZE = 32768
PROMPT_LIMIT = 38


@dataclass
class Stmt:
    ln: Line
    idx: int
    text: str       # whole statement, continuations joined, strings intact
    code: str       # same with the contents of strings blanked
    tok: str


@dataclass
class Var:
    kind: str                   # n | $ | a | key | ''
    size: int | None            # declared size when it is a plain number
    array: int | None           # array size when it is a plain number
    is_array: bool
    line: int


def logical_code(lines: list[Line], start: int) -> str:
    parts = []
    i = start
    while i < len(lines):
        ln = lines[i]
        piece = ln.code.rstrip()
        if ln.continues and piece.endswith('\\'):
            piece = piece[:-1]
        parts.append(piece.strip())
        if not ln.continues:
            break
        i += 1
    return ' '.join(parts)


def call_args(text: str, name: str) -> list[list[str]]:
    """Argument lists of every ``name(...)`` call in text (strings respected)."""
    found = []
    for m in re.finditer(r'(?<![\w@.])' + re.escape(name) + r'\s*\(', text, re.I):
        depth, i, in_str = 1, m.end(), False
        start = i
        while i < len(text) and depth:
            ch = text[i]
            if in_str:
                in_str = ch != '"'
            elif ch == '"':
                in_str = True
            elif ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1
            i += 1
        if depth == 0:
            inner = text[start:i - 1]
            found.append(split_args(inner) if inner.strip() else [])
    return found


def parse_spec(spec: str) -> tuple[str, int | None] | str:
    """(kind, size) for a valid variable specifier, or an error message."""
    spec = spec.strip()
    m = SPEC_RE.match(spec)
    if not m:
        if SPEC_SPACE_RE.match(spec):
            return f'no whitespace is allowed inside the specifier "{spec}"'
        if re.match(r'^key\s*\S', spec, re.I):
            return 'a key variable takes no size'
        return f'"{spec}" is not a valid type (use N<digits>, $<digits>, A<chars> or key)'
    if m.group('key'):
        return ('key', None)
    kind = m.group('t').lower()
    sz = m.group('sz')
    if sz.startswith('('):
        return (kind, None)
    size = int(sz)
    if size == 0:
        return 'the size of a variable must be at least 1'
    if size > MAX_VAR_SIZE:
        return f'size {size} exceeds the maximum of {MAX_VAR_SIZE}'
    return (kind, size)


def _int_or_none(text: str) -> int | None:
    t = text.strip().replace(' ', '')
    return int(t) if re.fullmatch(r'-?\d+', t) else None


def _lint_semantics(lines: list[Line], add) -> None:
    stmts: list[Stmt] = []
    for idx, ln in enumerate(lines):
        if ln.blank or ln.comment_only or ln.continuation:
            continue
        stmts.append(Stmt(ln, idx, logical_text(lines, idx), logical_code(lines, idx), ln.token))

    # -- physical-line rules
    for ln in lines:
        if ln.blank or ln.comment_only:
            continue
        if ln.continues and ln.comment:
            add(ln, 'error', 'L013', 'a line continuation (\\) may not be followed by a comment')
        if ln.code_raw.rstrip().endswith('\\') and ln.code_raw.count('"') % 2:
            add(ln, 'error', 'L013', 'a string cannot be split across a line continuation (\\)')
        if not ln.continuation and not ln.token and ln.code.strip():
            add(ln, 'error', 'L033', f'invalid first character "{ln.code.strip()[0]}" '
                '(a statement starts with a command, variable name or @sysvar)')

    glob: dict[str, Var] = {}
    local: dict[str, Var] = {}
    proc: str | None = None            # 'event' | 'sub'
    proc_name = ''
    proc_arg = ''
    seen_proc = False
    # names declared inside any event: a sub runs under its caller, so it may use them
    caller_vars: dict[str, Var] = {}
    in_event = False
    for s in stmts:
        if s.tok == 'event':
            in_event = True
        elif s.tok in ('endevent', 'sub'):
            in_event = False
        elif s.tok == 'var' and in_event:
            for part in split_args(s.text[len('var'):]):
                nm = re.match(r'^[A-Za-z_]\w*', part.strip())
                if nm:
                    caller_vars[nm.group(0).lower()] = Var('', None, None, False, 0)
    # per-procedure state
    st: dict = {}

    def reset_state() -> None:
        st.clear()
        st.update(window=None, window_dims=None, window_pending=0, called=False, tx_seen=False,
                  prints=0, cleared_ts=False, ts_key=False, ref_info=0, loops=0)

    reset_state()

    def lookup(name: str) -> Var | None:
        n = name.lower()
        v = local.get(n) or glob.get(n)
        if v is None and proc == 'sub':
            v = caller_vars.get(n)
        return v

    def declare(name: str, var: Var, ln: Line) -> None:
        n = name.lower()
        scope = local if proc else glob
        if n in scope:
            add(ln, 'error', 'L029', f'variable {name} is already declared in this scope '
                f'(line {scope[n].line})')
        elif proc and n in glob:
            add(ln, 'warning', 'L029', f'local variable {name} hides the global declared '
                f'on line {glob[n].line}')
        scope[n] = var

    for pos, s in enumerate(stmts):
        ln, tok, code, text = s.ln, s.tok, s.code, s.text
        low = text.lower()
        nxt = stmts[pos + 1] if pos + 1 < len(stmts) else None

        # ---- procedure bookkeeping
        if tok == 'event':
            m = EVENT_RE.match(text)
            proc, seen_proc = 'event', True
            proc_name = m.group(1).lower() if m else ''
            proc_arg = (m.group(2) or '').strip() if m else ''
            local.clear()
            reset_state()
            if proc_name == 'rxmsg' and proc_arg and proc_arg != '*' \
                    and not re.fullmatch(r'[A-Za-z_]\w*', proc_arg):
                add(ln, 'error', 'L026', f'event id "{proc_arg}" must start with a letter and use '
                    'only letters, digits and underscores')
            continue
        if tok == 'sub':
            proc, seen_proc = 'sub', True
            local.clear()
            reset_state()
            m = SUB_RE.match(text)
            if m:
                proc_name = m.group(1)
                _check_name(m.group(1), ln, add, 'sub')
                for part in (split_args(m.group(2)) if m.group(2) else []):
                    _lint_sub_param(part, ln, add, local)
            continue
        if tok in ('endevent', 'endsub'):
            if proc == 'event':
                if st['window_pending'] and not st['called']:
                    add(ln, 'warning', 'L017', 'DisplayInput without a following WindowEdit or '
                        'WindowInput in this event')
            proc = None
            local.clear()
            continue

        # ---- statements valid anywhere
        if tok == 'var':
            _lint_var(s, ln, add, declare, st)
            continue

        if proc is None and tok and tok not in TOP_LEVEL_COMMANDS and tok not in ('event', 'sub'):
            m = ASSIGN_FULL_RE.match(text)
            if not (m and m.group('name').startswith('@')) and tok not in BLOCK_CLOSE:
                add(ln, 'error', 'L030', f'"{tok}" is not allowed outside an event or sub '
                    '(only var, Use…, Retain/DiscardGlobalVar, Prorate, SetSignOn… and '
                    '@system variable settings are)')

        _lint_statement(s, ln, add, lookup)

        if tok in ('call',):
            st['called'] = True

        # ---- flow tracking inside procedures
        if tok in LOOPS:
            st['loops'] += 1
        elif tok in ('endfor', 'endwhile'):
            st['loops'] = max(0, st['loops'] - 1)

        if tok == 'return' and proc == 'event':
            add(ln, 'error', 'L015', 'return is not allowed in an event procedure')

        if proc == 'event' and proc_name in ('init', 'exit') and tok in USER_INPUT_COMMANDS:
            add(ln, 'warning', 'L016', f'{tok} waits for the operator, but no user input is '
                f'allowed in Event {proc_name.capitalize()}')

        if tok == 'window':
            args = split_args(text[len(tok):])
            rows = _int_or_none(args[0]) if args else None
            cols = _int_or_none(args[1]) if len(args) > 1 else None
            if rows is not None and not 1 <= rows <= 12:
                add(ln, 'error', 'L017', f'window rows must be 1 to 12, not {rows}')
            if cols is not None and not 1 <= cols <= 78:
                add(ln, 'error', 'L017', f'window columns must be 1 to 78, not {cols}')
            st['window'] = True
            st['window_dims'] = (rows, cols)
            st['window_pending'] = 0
        elif tok == 'windowclose':
            st['window'] = None
            st['window_dims'] = None
        elif tok in ('windowedit', 'windowinput', 'windoweditwithsave', 'windowinputwithsave'):
            st['window_pending'] = 0
        if tok in NEEDS_WINDOW and proc == 'event' and not st['window'] and not st['called']:
            add(ln, 'warning', 'L017', f'{tok} before any Window command in this event')
        if tok in ('display', 'displayinverse') and st['window_dims']:
            args = split_args(text[len(tok):])
            rows, cols = st['window_dims']
            r = _int_or_none(args[0]) if args else None
            c = _int_or_none(args[1]) if len(args) > 1 else None
            if r is not None and rows is not None and r > rows:
                add(ln, 'error', 'L017', f'row {r} is outside the {rows}-row window')
            if c is not None and cols is not None and c > cols:
                add(ln, 'error', 'L017', f'column {c} is outside the {cols}-column window')
        if tok in ('displayinput', 'displaymsinput'):
            st['window_pending'] += 1
            if st['window_pending'] > 64:
                add(ln, 'warning', 'L017', 'more than 64 DisplayInput entries in one window')

        # printing
        if tok in ('startprint', 'startprintwithstatus'):
            if st['prints'] > 0:
                add(ln, 'error', 'L019', 'StartPrint while a print session is already active '
                    '(only one session at a time; EndPrint first)')
            st['prints'] += 1
            args = split_args(text[len(tok):])
            first = args[0].strip() if args else ''
            if INT_LIT.match(first):
                value = int(first.replace(' ', ''))
                if value < 0:
                    add(ln, 'error', 'L019', f'printer object number {value} is invalid')
                elif value == 0:
                    add(ln, 'warning', 'L019', 'printer object number 0 never prints anywhere')
        elif tok in ('endprint', 'endprintff', 'endprintnoff'):
            st['prints'] = max(0, st['prints'] - 1)
        elif tok in ('printline', 'linefeed', 'listprint') and proc == 'event' and st['prints'] == 0:
            add(ln, 'warning', 'L018', f'{tok} outside StartPrint ... EndPrint')

        # messaging
        if tok == 'txmsg':
            st['tx_seen'] = True
            j = pos + 1
            while j < len(stmts) and stmts[j].tok in ('else', 'elseif', 'endif', 'txmsg'):
                j += 1                   # both branches of an if may send, then share one wait
            after = stmts[j] if j < len(stmts) else None
            if after is None or after.tok not in ('waitforrxmsg', 'getrxmsg'):
                add(ln, 'warning', 'L020', 'txmsg should be followed by WaitForRxMsg or GetRxMsg')
        elif tok == 'getrxmsg' and not st['tx_seen']:
            add(ln, 'warning', 'L020', 'getrxmsg without a preceding txmsg in this procedure')

        if tok == 'saverefinfo':
            if proc == 'event' and proc_name not in ('tmed', 'rxmsg'):
                add(ln, 'warning', 'L021', 'SaveRefInfo only works in Event Tmed')
            if not st['loops']:
                st['ref_info'] += 1
                if st['ref_info'] == 9:
                    add(ln, 'warning', 'L021', 'more than 8 SaveRefInfo lines in one event '
                        '(the maximum is 8)')

        if tok == 'clearislts':
            st['cleared_ts'] = True
        elif tok in ('setisltskey', 'setisltskeyx'):
            st['cleared_ts'] = False
        elif tok == 'displayislts' and st['cleared_ts']:
            add(ln, 'warning', 'L037', 'DisplayIslTs straight after ClearIslTs: no touchscreen '
                'keys are defined')

        if tok == 'for':
            _lint_for(text, ln, add, lookup)

        # assignments: undeclared variable, literal overflow, read-only system variables
        m = ASSIGN_FULL_RE.match(text) if tok and tok not in KNOWN_COMMANDS else None
        if m:
            name = m.group('name')
            if name.startswith('@'):
                base = name[1:].lower()
                if base in READONLY_SYSVARS:
                    add(ln, 'error', 'L022', f'@{name[1:]} is read-only')
                if base == 'warnings_are_fatal' and seen_proc:
                    add(ln, 'warning', 'L022', '@Warnings_Are_Fatal must be set at the top of the '
                        'script, before any event or sub')
            else:
                var = lookup(name)
                if var is None:
                    add(ln, 'warning', 'L028', f'variable {name} is used but never declared')
                elif not m.group('idx'):
                    _lint_overflow(var, name, m.group('rhs').strip(), ln, add)
        _ = low


def _check_name(name: str, ln: Line, add, what: str = 'variable') -> bool:
    if name.startswith('@'):
        add(ln, 'error', 'L010', f'{name}: system variables cannot be declared')
        return False
    if not IDENT_RE.match(name):
        add(ln, 'error', 'L010', f'{what} name "{name}" must start with a letter or _ and use only '
            'letters, digits and _')
        return False
    if len(name) > MAX_LEN_NAME:
        add(ln, 'error', 'L010', f'{what} name is {len(name)} characters (maximum {MAX_LEN_NAME})')
    if name.lower() in KNOWN_COMMANDS:
        add(ln, 'error', 'L010', f'"{name}" is a reserved word and cannot be a {what} name')
    return True


def _lint_var(s: Stmt, ln: Line, add, declare, st: dict) -> None:
    body = s.text[len(s.tok):].strip()
    if not body:
        add(ln, 'error', 'L011', 'var needs a name and a type, e.g. var count : N3')
        return
    for part in split_args(body):
        m = re.match(r'^(?P<name>[^\s:\[=]*)\s*(?P<arr>\[[^\]]*\])?\s*(?::\s*(?P<spec>[^=]*?))?\s*'
                     r'(?:=\s*(?P<init>.+))?$', part.strip(), re.S)
        if not m:
            add(ln, 'error', 'L011', f'cannot read the declaration "{part.strip()}"')
            continue
        name = m.group('name')
        if not name:
            add(ln, 'error', 'L010', 'variable declaration has no name')
            continue
        ok = _check_name(name, ln, add)
        arr = m.group('arr')
        array_size = None
        if arr is not None:
            array_size = _int_or_none(arr[1:-1])
            if array_size is not None and not 1 <= array_size <= MAX_VAR_SIZE:
                add(ln, 'error', 'L011', f'array size {array_size} must be between 1 and {MAX_VAR_SIZE}')
        if m.group('spec') is None:
            add(ln, 'error', 'L011', f'{name} has no type: write {name} : N<digits>, $<digits>, '
                'A<chars> or key')
            var = Var('', None, array_size, arr is not None, ln.number)
        else:
            parsed = parse_spec(m.group('spec'))
            if isinstance(parsed, str):
                add(ln, 'error', 'L011', f'{name}: {parsed}')
                var = Var('', None, array_size, arr is not None, ln.number)
            else:
                var = Var(parsed[0], parsed[1], array_size, arr is not None, ln.number)
        if ok:
            declare(name, var, ln)
        if m.group('init') and arr is None:
            _lint_overflow(var, name, m.group('init').strip(), ln, add)


def _lint_overflow(var: Var, name: str, rhs: str, ln: Line, add) -> None:
    if var.size is None or var.is_array:
        return
    if var.kind == 'n' and INT_LIT.match(rhs):
        digits = len(rhs.replace('-', '').replace(' ', ''))
        if digits > var.size:
            add(ln, 'error', 'L031', f'{rhs} has {digits} digits but {name} holds only {var.size}')
    elif var.kind == '$':
        m = DEC_LIT.match(rhs)
        if m and len(m.group(1)) + len(m.group(2)) > var.size:
            add(ln, 'error', 'L031', f'{rhs} has more than {var.size} digits, too many for {name}')
    elif var.kind == 'a':
        m = STR_LIT.match(rhs)
        if m and len(m.group(1)) > var.size:
            add(ln, 'error', 'L031', f'string of {len(m.group(1))} characters does not fit {name} '
                f'(A{var.size})')


def _lint_sub_param(part: str, ln: Line, add, local: dict) -> None:
    part = part.strip()
    words = part.split(None, 1)
    mode = words[0].lower() if words else ''
    if mode not in ('var', 'ref'):
        add(ln, 'error', 'L024', f'sub parameter "{part}" must start with var or ref')
        return
    rest = words[1].strip() if len(words) > 1 else ''
    m = re.match(r'^([A-Za-z_]\w*)\s*(\[[^\]]*\]?)?\s*(?::\s*(.*))?$', rest)
    if not m:
        add(ln, 'error', 'L024', f'cannot read sub parameter "{part}"')
        return
    name, brackets, spec = m.group(1), m.group(2), m.group(3)
    if brackets is not None:
        if mode == 'var':
            add(ln, 'error', 'L024', f'{name}: arrays cannot be passed by value; use ref {name}[]')
        elif not re.fullmatch(r'\[\s*\]', brackets):
            add(ln, 'error', 'L024', f'{name}: an array reference is written {name}[] '
                f'(found "{brackets}")')
    var = Var('', None, None, brackets is not None, ln.number)
    if spec:
        parsed = parse_spec(spec)
        if isinstance(parsed, str):
            add(ln, 'error', 'L011', f'{name}: {parsed}')
        else:
            var = Var(parsed[0], parsed[1], None, brackets is not None, ln.number)
    elif mode == 'var':
        add(ln, 'error', 'L024', f'by-value parameter {name} needs a type, e.g. var {name} : N5')
    local[name.lower()] = var


def _lint_for(text: str, ln: Line, add, lookup) -> None:
    m = FOR_RE.match(text.strip())
    if not m:
        add(ln, 'error', 'L023', 'for needs the form: for counter = start to end [step n]')
        return
    counter = m.group('v').strip()
    if not IDENT_RE.match(counter):
        add(ln, 'error', 'L023', f'the for counter must be a variable, not "{counter}"')
    else:
        var = lookup(counter)
        if var is None:
            add(ln, 'warning', 'L028', f'for counter {counter} is never declared')
        elif var.kind in ('$', 'a', 'key'):
            add(ln, 'error', 'L023', f'the for counter {counter} must be an integer (N) variable')
    step = m.group('s')
    if step and _int_or_none(step) == 0:
        add(ln, 'error', 'L023', 'step 0 never ends')


def _lint_statement(s: Stmt, ln: Line, add, lookup) -> None:
    """Checks on the text of any statement, inside or outside a procedure."""
    code, text, tok = s.code, s.text, s.tok

    # L012 whitespace inside a language element
    for pat, what in ((r'@\s+[A-Za-z_]', 'between @ and the system variable name'),
                      (r'<\s+[>=]', 'inside <> or <='), (r'>\s+=', 'inside >='),
                      (r'/\s+/', 'inside the // comment marker')):
        if re.search(pat, code):
            add(ln, 'error', 'L012', f'whitespace {what}')

    # L033 statement shape
    if TRAILING_OP_RE.search(code.rstrip()) and tok not in ('else',):
        add(ln, 'error', 'L033', 'statement ends with a comma or operator; an operand is missing')
    if tok in NO_ARGUMENT_COMMANDS and code[len(tok):].strip():
        add(ln, 'error', 'L033', f'{tok} takes no arguments; unexpected text after it')
    if tok in ('format', 'formatq'):
        m = FORMAT_RE.match(text)
        rest = m.group('rest') if m else ''
        if re.match(r'^as\b', rest, re.I):
            add(ln, 'error', 'L033', f'{tok} needs a string variable before "as"')
        elif not re.search(r'\bas\b', rest, re.I):
            add(ln, 'error', 'L033', f'{tok} needs "as" before the expressions')

    # L034 operators
    if DIVIDE_ZERO_RE.search(code):
        add(ln, 'error', 'L034', 'division by zero')
    for m in re.finditer(r'"[^"]*"', text):
        before = text[:m.start()].rstrip()[-1:]
        after = text[m.end():].lstrip()[:1]
        if (before and before in '-*/%') or (after and after in '-*/%'):
            add(ln, 'error', 'L034', 'only relational operators work on strings')
            break
    for m in re.finditer(r'([A-Za-z_]\w*)\s*%\s*([A-Za-z_]\w*)', code):
        if any((lookup(n) or Var('', None, None, False, 0)).kind == '$' for n in m.groups()):
            add(ln, 'warning', 'L034', '% is not valid on decimal ($) values')
            break

    # L035 functions
    if tok not in ('var', 'sub', 'event', 'dllcall', 'dllcall_cdecl'):
        scan_code = re.sub(r'\{[^}]*\}', '', code[len(tok):])
        if tok == 'call':
            scan_code = re.sub(r'^\s*\w+', '', scan_code)
        for m in FUNC_CALL_RE.finditer(scan_code):
            name = m.group(1).lower()
            if name in KNOWN_FUNCTIONS or name in KNOWN_COMMANDS or name in ('and', 'or', 'not') \
                    or name in ('then', 'to', 'step', 'as') or len(name) == 1:
                continue
            add(ln, 'warning', 'L035', f'unknown function "{m.group(1)}"')
    for name, want in FUNCTION_ARITY.items():
        for args in call_args(text, name):
            if len(args) != want:
                add(ln, 'error', 'L035', f'{name} takes {want} argument(s), {len(args)} given')
    for args in call_args(text, 'mid'):
        for label, pos in (('start', 1), ('length', 2)):
            if len(args) > pos:
                v = _int_or_none(args[pos])
                if v is not None and v < 0:
                    add(ln, 'error', 'L035', f'Mid {label} {v} is invalid')

    # L036 input target
    if tok in ('input', 'inputkey'):
        args = split_args(text[len(tok):])
        if args and re.match(r'^[\d"+\-]', args[0].strip()):
            add(ln, 'error', 'L036', f'{tok} needs a variable first, not "{args[0].strip()}"')

    # L027 prompt length
    if tok in PROMPT_COMMANDS:
        total = sum(len(m.group(1)) for a in split_args(text[len(tok):])
                    for m in [STR_LIT.match(a.strip())] if m)
        if total > PROMPT_LIMIT:
            add(ln, 'warning', 'L027', f'prompt text is {total} characters; only {PROMPT_LIMIT} fit')

    # L022 system variables
    for m in SYSVAR_RE.finditer(code):
        base = m.group(1).lower()
        if base not in KNOWN_SYSVARS and base.rstrip('0123456789') not in KNOWN_SYSVARS \
                and base not in EXTRA_SYSVARS:
            add(ln, 'warning', 'L022', f'unknown system variable @{m.group(1)}')
        elif base.rstrip('0123456789') == 'si' or base == 'si':
            tail = code[m.end():m.end() + 1]
            digits = re.match(r'si(\d+)$', base)
            if digits:
                _check_si(int(digits.group(1)), ln, add)
            elif tail == '[':
                idx = INT_LIT.match(code[m.end() + 1:].split(']', 1)[0].strip())
                if idx:
                    _check_si(int(idx.group(0).replace(' ', '')), ln, add)
            elif tok != 'call':
                add(ln, 'warning', 'L022', '@SI needs an index (@SI[n] or @SIn) unless passed whole to a sub')

    # L032 list arrays and literal indexes
    for m in INDEX_LIT_RE.finditer(code):
        var = lookup(m.group(1))
        if var and var.is_array and var.array is not None:
            n = int(m.group(2))
            if not 1 <= n <= var.array:
                add(ln, 'error', 'L032', f'index {n} is outside {m.group(1)}[1..{var.array}]')
    if tok in ('txmsg', 'rxmsg', 'getrxmsg'):
        args = split_args(text[len(tok):])
        for i, a in enumerate(args):
            lm = re.fullmatch(r'([A-Za-z_]\w*)\s*\[\s*\]', a.strip())
            if not lm:
                continue
            if i == 0:
                add(ln, 'error', 'L032', f'{a.strip()} needs a list size before it')
                continue
            count, var = _int_or_none(args[i - 1]), lookup(lm.group(1))
            if count is not None and var and var.array is not None and count > var.array:
                add(ln, 'error', 'L032', f'list size {count} is above {lm.group(1)}[{var.array}]')

    # L031 format into a variable with only literal text
    if tok in ('format', 'formatq'):
        m = re.match(r'^(?:format|formatq)\s+([A-Za-z_]\w*)\s*(?:,[^,]*?)?\s+as\s+(.*)$', text, re.I | re.S)
        if m:
            var = lookup(m.group(1))
            args = split_args(m.group(2))
            lits = [STR_LIT.match(a.strip()) for a in args]
            if var and var.kind == 'a' and var.size and args and all(lits):
                total = sum(len(x.group(1)) for x in lits)
                if total > var.size:
                    add(ln, 'error', 'L031', f'format text is {total} characters but '
                        f'{m.group(1)} holds {var.size}')


def _check_si(n: int, ln: Line, add) -> None:
    if not 1 <= n <= 16:
        add(ln, 'error', 'L022', f'@SI index {n} is outside 1 to 16')
    elif n > 8:
        add(ln, 'warning', 'L022', f'@SI index {n}: the Guide documents 1 to 8, errors.md 1 to 16')


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
