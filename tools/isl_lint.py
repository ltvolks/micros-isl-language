#!/usr/bin/env python3
"""Linter for MICROS RES 3700 ISL scripts.

    isl_lint.py FILE...             file:line:col: severity LNNN message
    isl_lint.py --fix FILE...       format in place (isl_fmt), then report what remains
    isl_lint.py --format json FILE...
    isl_lint.py --strict FILE...    fail on warnings too

Standard library only. Rules L001-L009; see skills/micros-isl-3700/SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from isl_fmt import (  # noqa: E402
    ASSIGN_RE, BANNER_RE, BLOCK_CLOSE, BLOCK_MIDDLE, BLOCK_OPEN, DEFAULT_INDENT, EVENT_RE,
    KNOWN_COMMANDS, KNOWN_EVENTS, LOOPS, NUMERIC_EVENTS, SUB_RE, Line, _read, format_source, scan,
)

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



def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog='isl_lint', description='Lint ISL scripts')
    p.add_argument('files', nargs='+', help='ISL files, or - for stdin')
    p.add_argument('--indent', type=int, default=DEFAULT_INDENT, help='spaces per level (default 2)')
    p.add_argument('--fix', action='store_true', help='re-format files first')
    p.add_argument('--format', choices=['text', 'json'], default='text')
    p.add_argument('--strict', action='store_true', help='fail on warnings too')
    args = p.parse_args(argv)
    all_diags: list[Diag] = []
    for path in args.files:
        src = _read(path)
        if args.fix and path != '-':
            out = format_source(src, args.indent)
            if out != src:
                Path(path).write_text(out, encoding='utf-8')
                src = out
        all_diags += lint_source(src, path, args.indent)
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


if __name__ == '__main__':
    raise SystemExit(main())
