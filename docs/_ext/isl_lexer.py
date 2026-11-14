"""Pygments lexer for MICROS RES 3700 SIM ISL, registered as ``isl``.

Keywords come from tools/isl.py so the docs, the linter and the Sublime grammar agree.

    .. code-block:: isl

        event inq : 1
          var total : N6 = 0
        endevent
"""

import re
import sys
from pathlib import Path

from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import isl  # noqa: E402

FUNCTIONS = ('abs', 'arraysize', 'asc', 'bit', 'chr', 'env', 'feof', 'ftell', 'gethex', 'getmaxdiscount',
             'instr', 'key', 'keynumber', 'keytype', 'len', 'makekeys', 'mid', 'one_time_auto_discounts',
             'tointeger', 'trim', 'varsize')
EXTRA_KEYWORDS = ('and', 'or', 'not', 'to', 'as', 'ref', 'endforever', 'read', 'write', 'append')
KEYWORDS = tuple(sorted(
    (set(isl.KNOWN_COMMANDS) | set(isl.BLOCK_OPEN) | set(isl.BLOCK_MIDDLE) | set(isl.BLOCK_CLOSE)
     | set(EXTRA_KEYWORDS)) - set(FUNCTIONS), key=lambda w: (-len(w), w)))


class ISLLexer(RegexLexer):
    name = 'ISL'
    aliases = ['isl']
    filenames = ['*.isl']
    flags = re.IGNORECASE | re.MULTILINE

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'\\\n', Text),                                   # line continuation
            (r'//.*$', Comment.Single),
            (r'"[^"\n]*"', String.Double),
            (r'[“”][^“”\n]*[“”]', String.Double),   # curly quotes in old text
            (r'@\s?[A-Za-z_][A-Za-z0-9_]*', Name.Builtin),       # @SysVar
            (r'\$\d+|\b[AN]\d+\b', Keyword.Type),               # $8, A20, N5
            (r'\b\d+(\.\d+)?\b', Number),
            (words(KEYWORDS, prefix=r'\b', suffix=r'\b'), Keyword),
            (words(FUNCTIONS, prefix=r'\b', suffix=r'\b(?=\s*\()'), Name.Function),
            (r'\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()', Name.Function),
            (r'\b[A-Za-z_][A-Za-z0-9_]*\b', Name),
            (r'<>|<=|>=|[-+*/=<>^]', Operator),
            (r'[{}()\[\],:;.#]', Punctuation),
            (r'.', Text),
        ],
    }


def setup(app):
    app.add_lexer('isl', ISLLexer)
    return {'parallel_read_safe': True, 'version': '1.1'}
