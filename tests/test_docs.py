"""Tests for the docs tooling (docs/_ext/* and the Sphinx build). Needs only the stdlib + pygments."""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'docs'))
sys.path.insert(0, str(ROOT / 'docs' / '_ext'))
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


@pytest.fixture(scope='module')
def built(tmp_path_factory):
    """Build the whole site once (MyST reads reference/*.md and guide/*.md as they are)."""
    pytest.importorskip('sphinx')
    pytest.importorskip('myst_parser')
    pytest.importorskip('furo')
    from io import StringIO

    from sphinx.application import Sphinx
    out = tmp_path_factory.mktemp('site')
    warnings = StringIO()
    app = Sphinx(str(ROOT / 'docs'), str(ROOT / 'docs'), str(out / 'html'), str(out / 'doctrees'), 'html',
                 status=None, warning=warnings, freshenv=True, warningiserror=True)
    app.build()
    return app, out / 'html'


def test_every_reference_entry_has_stable_label(built):
    app, _ = built
    labels = app.env.get_domain('std').labels
    assert labels['cmd-break'][0] == 'reference/commands'
    assert 'evt-event-inq' in labels
    assert 'isl-commands' in labels
    objects = app.env.get_domain('isl').data['objects']
    assert objects[('command', 'Break')] == ('reference/commands', 'cmd-break')


def test_entry_counts(built):
    app, _ = built
    counts = {}
    for objtype, _name in app.env.get_domain('isl').data['objects']:
        counts[objtype] = counts.get(objtype, 0) + 1
    assert counts == {'command': 101, 'event': 31, 'function': 28, 'sysvar': 221, 'specifier': 19,
                      'error': 96, 'key': 13}


def test_markdown_tables_render_with_headers(built):
    _, html = built
    keys = (html / 'reference' / 'keys.html').read_text()
    assert keys.count('<table') == 13 and keys.count('<thead>') == 13
    assert '| ----' not in keys and '| ---' not in keys
    sysvars = (html / 'reference' / 'sysvars.html').read_text()
    assert 'DTL_PREV_RND' in sysvars and sysvars.count('<thead>') >= 14


def test_see_also_links(built):
    _, html = built
    functions = (html / 'reference' / 'functions.html').read_text()
    assert '>See also<' in functions
    assert 'title="Chr"' in functions       # the See also list links to the entry


def test_guide_chapters_labels_and_notes(built):
    app, html = built
    names = sorted(p.stem for p in (html / 'guide').glob('*.html'))
    assert names == ['appendix-a', 'appendix-b', 'chapter-1', 'chapter-2', 'chapter-3', 'chapter-4',
                     'chapter-5', 'chapter-6', 'chapter-7', 'glossary', 'preface']
    labels = app.env.get_domain('std').labels
    assert labels['guide-chapter-3'][0] == 'guide/chapter-3'
    assert 'glossary-argument' in labels
    assert '<blockquote' in (html / 'guide' / 'chapter-2.html').read_text()      # "> **Note:**"
    assert 'class="mermaid"' in (html / 'guide' / 'chapter-1.html').read_text()


def test_lexer_covers_vocabulary():
    from isl_lexer import ISLLexer
    from pygments.token import Keyword
    kinds = {v: k for k, v in ISLLexer().get_tokens('event inq : 1 usefiltereddetail waitforrxmsg')}
    assert kinds['usefiltereddetail'] is Keyword
    assert kinds['waitforrxmsg'] is Keyword


def test_general_index_lists_every_entry(built):
    _, out = built
    html = (out / 'genindex.html').read_text(encoding='utf-8')
    assert '<a href="reference/commands.html#cmd-break">Break (command)' in html
    assert html.count('href="reference/') >= 500


def test_commands_by_category_index(built):
    _, out = built
    html = (out / 'reference' / 'commands.html').read_text(encoding='utf-8')
    block = html[html.index('isl-categories'):html.index('id="beep"')]
    for category in ('Communications', 'File I/O', 'Flow control', 'Input / Output', 'Miscellaneous',
                     'Printing', 'Variables'):
        assert f'>{category}<' in block.replace('&amp;', '&') or category in block
    assert 'href="#cmd-txmsg"' in block
    assert block.count('class="reference internal"') == 94          # every listed name is linked


def test_lint_rule_pages_are_in_the_site(built):
    _, out = built
    index = (out / 'lint_rules' / 'index.html').read_text(encoding='utf-8')
    assert 'L001.html' in index and 'L037.html' in index
    page = (out / 'lint_rules' / 'L011.html').read_text(encoding='utf-8')
    assert '../guide/chapter-4.html#data-types' in page          # source link into the Guide
    assert 'isl-autolink' in page                                # example code links to the reference
