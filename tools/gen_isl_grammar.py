#!/usr/bin/env python3
"""Generate the Sublime Text ISL grammar and symbol-list preferences.

Keyword, command and event lists come from tools/isl_fmt.py so the editor and the
linter agree. Writes into the Sublime package directory (default below)::

    tools/gen_isl_grammar.py [PACKAGE_DIR]   (default: the repo root)

Files written: ISL.JSON-tmLanguage, ISL.tmLanguage, Symbol List.tmPreferences.
"""

import json
import plistlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import isl_fmt as islfmt  # noqa: E402

DEFAULT_PACKAGE = Path(__file__).resolve().parent.parent  # repo root = package root

# Built-in functions (isl-reference functions.md) that are not statement commands.
FUNCTIONS = set("""
abs arraysize asc bit chr env feof ftell gethex getmaxdiscount instr key
keynumber keytype len makekeys mid one_time_auto_discounts tointeger trim varsize
""".split())

CONTROL = {
    'if', 'else', 'elseif', 'endif', 'for', 'forever', 'endfor', 'while', 'endwhile',
    'endevent', 'endsub', 'break', 'call', 'return', 'to', 'continueoncancel',
    'exitcancel', 'exitcontinue', 'exitoncancel', 'exitwitherror', 'startprint',
    'startprintwithstatus', 'endprint', 'endprintff', 'endprintnoff',
}


def alt(words) -> str:
    return '|'.join(sorted(words, key=lambda w: (-len(w), w)))


def ci(word: str) -> str:
    """Case-insensitive regex for symbol transformations (no (?i) flag there)."""
    return ''.join(f'[{c.upper()}{c.lower()}]' if c.isalpha() else c for c in word)


def grammar() -> dict:
    commands = (islfmt.KNOWN_COMMANDS - CONTROL - {'event', 'sub', 'var'}) | FUNCTIONS
    return {
        'name': 'ISL',
        'scopeName': 'source.isl',
        'fileTypes': ['isl'],
        'uuid': '1B459BD3-7DE7-44BC-B50A-C433B9A5260E',
        'foldingStartMarker': r'(?ix) ^\s*( event\s+\w+ | sub\s+\w+ | if\b.* | for\b.* | forever\b | while\b.* | startprint\w* )',
        'foldingStopMarker': r'(?i)^\s*end(event|sub|if|for|while|print\w*)\b',
        'patterns': [
            {'name': 'comment.line.double-slash.isl',
             'begin': '//', 'end': r'$\n?',
             'beginCaptures': {'0': {'name': 'punctuation.definition.comment.isl'}}},
            {'name': 'string.quoted.double.isl', 'begin': '"', 'end': '"'},
            # Inq/Tmed: the trailing description stays inside the scope so the
            # symbol list can show it (see Symbol List.tmPreferences).
            {'name': 'entity.name.function.isl',
             'match': r'(?i)\bevent\s+(?:inq|tmed)\s*:\s*(?:\d+|\*)(?:[ \t]+//.*)?'},
            {'name': 'entity.name.function.isl',
             'match': r'(?i)\bevent\s+(?:rxmsg\s*:\s*[\w*]+|[A-Za-z_]\w*)'},
            {'name': 'entity.name.function.isl', 'match': r'(?i)\bsub\s+\w+'},
            {'name': 'keyword.control.isl',
             'match': rf'(?i)\b({alt(CONTROL)})\b'},
            {'name': 'keyword.operator.word.isl', 'match': r'(?i)\b(and|or|not)\b'},
            {'name': 'storage.type.isl', 'match': r'(?i)\b(var|ref)\b'},
            {'name': 'storage.modifier.isl', 'match': r'\$\d+|(?i)\b[AN]\d+\b'},
            {'name': 'variable.other.sysvar.isl', 'match': r'@\w+'},
            {'name': 'constant.numeric.isl', 'match': r'\b\d+(\.\d+)?\b'},
            {'name': 'support.function.isl',
             'match': rf'(?i)\b({alt(commands)})\b'},
            {'name': 'punctuation.separator.continuation.isl', 'match': r'\\\s*$'},
            {'name': 'keyword.operator.isl', 'match': r'<>|<=|>=|[-+*/%=<>]'},
        ],
    }


def symbol_prefs() -> bytes:
    event, inq, tmed, rxmsg, sub = (ci(w) for w in ('event', 'inq', 'tmed', 'rxmsg', 'sub'))
    rules = [
        rf's/^{event}\s+{inq}\s*:\s*(\S+)\s+\/\/\s*(.*)/Inq $1 - $2/',
        rf's/^{event}\s+{inq}\s*:\s*(\S+)/Inq $1/',
        rf's/^{event}\s+{tmed}\s*:\s*(\S+)\s+\/\/\s*(.*)/Tmed $1 - $2/',
        rf's/^{event}\s+{tmed}\s*:\s*(\S+)/Tmed $1/',
        rf's/^{event}\s+{rxmsg}\s*:\s*(\S+)/RxMsg $1/',
        rf's/^{event}\s+(\w+)/Event $1/',
        rf's/^{sub}\s+/- /',
    ]
    prefs = {
        'name': 'Symbol List',
        'scope': 'entity.name.function.isl',
        'settings': {'showInSymbolList': 1, 'symbolTransformation': '\n' + '\n'.join(rules) + '\n'},
        'uuid': 'F1F9695C-C99D-4EA8-96E9-6631CFB08FE0',
    }
    return plistlib.dumps(prefs)


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else DEFAULT_PACKAGE
    g = grammar()
    (out / 'ISL.JSON-tmLanguage').write_text(json.dumps(g, indent=4) + '\n', encoding='utf-8')
    (out / 'ISL.tmLanguage').write_bytes(plistlib.dumps(g))
    (out / 'Symbol List.tmPreferences').write_bytes(symbol_prefs())
    print(f'wrote grammar and symbol prefs to {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
