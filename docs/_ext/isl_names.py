"""Name handling shared by the isl Sphinx domain and the tests.

The reference titles entries like ``If...Else[If]...EndIf`` or ``Use[Compat/ISL]Format``;
``aliases()`` expands those into the words that appear in scripts so that code and prose can
link to the right entry.
"""

import itertools
import re

# objtype -> (label prefix, directive name, role name, human label, page)
TYPES = {
    'command': ('cmd', 'command', 'cmd', 'Command', 'commands'),
    'event': ('evt', 'event', 'event', 'Event', 'events'),
    'function': ('fn', 'function', 'fn', 'Function', 'functions'),
    'sysvar': ('sysvar', 'sysvar', 'sysvar', 'System variable', 'sysvars'),
    'specifier': ('spec', 'specifier', 'spec', 'Specifier', 'specifiers'),
    'error': ('err', 'error', 'err', 'Error message', 'errors'),
    'key': ('key', 'key', 'key', 'Key names', 'keys'),
}
PAGE_TYPE = {v[4]: k for k, v in TYPES.items()}
PAGE_TITLES = {'commands': 'Commands', 'events': 'Events', 'functions': 'Functions',
               'sysvars': 'System variables', 'specifiers': 'Specifiers', 'errors': 'Error messages',
               'keys': 'Key names and codes'}
PAGE_INTROS = {
    'commands': 'Language commands: syntax, arguments, usage and examples.',
    'events': 'Events a script can handle, with syntax and examples.',
    'functions': 'Built-in functions.',
    'sysvars': 'System variables (``@Name``) that scripts can read or set.',
    'specifiers': 'Input and output format specifiers.',
    'errors': 'Run-time error messages and what causes them.',
    'keys': 'Key names, key types and key codes.',
}
PRIORITY = ['command', 'function', 'event', 'sysvar', 'specifier', 'error', 'key']

# Ordinary English words: never linked in running prose, only inside code/literals.
COMMON_WORDS = {
    'display', 'format', 'input', 'window', 'system', 'split', 'prompt', 'return', 'break', 'call',
    'event', 'sub', 'key', 'mid', 'len', 'trim', 'var', 'if', 'else', 'for', 'while', 'to', 'as',
    'debug', 'beep', 'bit', 'env', 'abs', 'chr', 'asc', 'instr', 'touchscreen', 'rxmsg', 'txmsg',
    'ref', 'and', 'or', 'not', 'exit', 'init', 'svc', 'dsc', 'tndr', 'line', 'script', 'date', 'day',
    'hour', 'minute', 'month', 'second', 'year', 'weekday', 'version', 'trace', 'printing', 'center',
    'seat', 'gst', 'tax', 'version', 'platform', 'cashier', 'employee', 'ckid', 'chk', 'rcpt', 'jnl',
    'trailer', 'prefix', 'validate', 'warnings', 'ordr', 'rvc', 'si', 'txbl', 'mlvl', 'slvl', 'plvl',
}


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def _expand_brackets(word):
    """``Use[Compat/ISL]Format`` -> UseFormat, UseCompatFormat, UseISLFormat."""
    parts = re.split(r'(\[[^\]]*\])', word)
    options = []
    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            options.append([''] + part[1:-1].split('/'))
        else:
            options.append([part])
    return {''.join(combo) for combo in itertools.product(*options)}


def aliases(objtype, title):
    """Every spelling (without the canonical title) that should resolve to this entry."""
    names = set()
    t = title.strip()
    if objtype == 'event':
        rest = re.sub(r'^event\s+', '', t, flags=re.I)
        if rest != t:
            names.add(rest)
            if '/' in rest:
                names.update(rest.split('/'))
                head, _, tail = rest.partition('/')
                names.add(head)
                names.add(head.rsplit('_', 1)[0] + '_' + tail)
    if objtype == 'sysvar':
        bare = re.sub(r'^@\s*', '', t)
        names.update({bare, '@' + bare})
        if ' and ' in bare:
            for piece in bare.split(' and '):
                if ' ' not in piece.strip():
                    names.update({piece.strip(), '@' + piece.strip()})
    if objtype == 'function':
        bare = re.sub(r'\s+Functions?$', '', t)
        if bare != t:
            names.add(bare)
    if ':' in t:
        names.add(t.split(':', 1)[1].strip())
    for piece in re.split(r'\.\.\.\s*', t):
        piece = piece.strip()
        if not piece:
            continue
        for expanded in _expand_brackets(piece):
            if expanded:
                names.add(expanded)
    names.discard(t)
    return {n for n in names if n and ' ' not in n.strip() or n == t}


def is_prose_linkable(name):
    """True if the name may be linked in running prose (CamelCase / underscore, not an English word)."""
    if name.lower() in COMMON_WORDS or ' ' in name:
        return False
    return bool(re.search(r'[a-z][A-Z]|_', name)) or name.startswith('@')
