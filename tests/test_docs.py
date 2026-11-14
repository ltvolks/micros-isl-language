"""Tests for the docs tooling (docs/build_rst.py, docs/_ext/*). Needs only the stdlib + pygments."""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'docs'))
sys.path.insert(0, str(ROOT / 'docs' / '_ext'))
import build_rst  # noqa: E402
import isl_names  # noqa: E402

pygments = pytest.importorskip('pygments')


def test_alias_expansion():
    assert {'If', 'Else', 'ElseIf', 'EndIf'} <= isl_names.aliases('command', 'If...Else[If]...EndIf')
    assert {'UseCompatFormat', 'UseISLFormat'} <= isl_names.aliases('command', 'Use[Compat/ISL]Format')
    assert {'StartPrint', 'StartPrintWithStatus', 'EndPrint', 'EndPrintFF', 'EndPrintNOFF'} <= \
        isl_names.aliases('command', 'StartPrint[WithStatus]...EndPrint[FF/NOFF]')
    assert 'Init' in isl_names.aliases('event', 'Event Init')
    assert {'Print_Header', 'Print_Trailer'} <= isl_names.aliases('event', 'Event Print_Header/Trailer')
    assert '@Cknum' in isl_names.aliases('sysvar', 'Cknum')


def test_prose_linkable():
    assert isl_names.is_prose_linkable('StartPrint')
    assert isl_names.is_prose_linkable('@Cknum')
    assert not isl_names.is_prose_linkable('Display')


def test_inline_escaping():
    assert build_rst.inline('see array_ for **x**') == 'see array\\_ for **x**'
    assert build_rst.inline('a * b | c') == 'a \\* b \\| c'
    assert build_rst.inline('1. not a list') == '1\\. not a list'


def test_every_reference_entry_has_stable_label(tmp_path):
    build_rst.main(['--out', str(tmp_path)])
    commands = (tmp_path / 'reference' / 'commands.rst').read_text()
    assert '.. _cmd-break:' in commands
    assert '.. isl:command:: Break' in commands
    events = (tmp_path / 'reference' / 'events.rst').read_text()
    assert '.. _evt-event-inq:' in events


def test_entry_counts(tmp_path):
    build_rst.main(['--out', str(tmp_path)])
    counts = {name: len(re.findall(r'^\.\. isl:\w+::', (tmp_path / 'reference' / f'{name}.rst').read_text(),
                                   re.M))
              for name, *_ in build_rst.CATEGORIES}
    assert counts == {'commands': 109, 'events': 27, 'functions': 28, 'sysvars': 222, 'specifiers': 19,
                      'errors': 92, 'keys': 13}


def test_guide_chapters(tmp_path):
    build_rst.main(['--out', str(tmp_path)])
    names = sorted(p.stem for p in (tmp_path / 'guide').glob('*.rst'))
    assert names == ['appendix-a', 'appendix-b', 'chapter-1', 'chapter-2', 'chapter-3', 'chapter-4',
                     'chapter-5', 'chapter-6', 'chapter-7', 'glossary', 'index', 'preface']


def test_lexer_covers_vocabulary():
    from isl_lexer import ISLLexer
    from pygments.token import Keyword
    kinds = {v: k for k, v in ISLLexer().get_tokens('event inq : 1 usefiltereddetail waitforrxmsg')}
    assert kinds['usefiltereddetail'] is Keyword
    assert kinds['waitforrxmsg'] is Keyword
