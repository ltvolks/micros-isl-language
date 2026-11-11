"""Tests for tools/isl_fmt.py and tools/isl_lint.py."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import isl_fmt  # noqa: E402
import isl_lint  # noqa: E402

ISL_FILES = sorted((ROOT / 'tests' / 'fixtures').glob('*.isl'))

BANNER = '// ' + '*' * 40


def codes(src):
    return [d.code for d in isl_lint.lint_source(src)]


def tokens(text):
    return [line.strip() for line in text.split('\n') if line.strip()]


def test_indents_blocks_two_spaces():
    src = 'event inq : 1 // x\nif a\nb = 1\nelseif c\nd = 2\nelse\ne = 3\nendif\nendevent\n'
    assert isl_fmt.format_source(src) == (
        'event inq : 1 // x\n  if a\n    b = 1\n  elseif c\n    d = 2\n  else\n    e = 3\n  endif\nendevent\n'
    )


def test_indent_option_and_tabs_replaced():
    src = 'sub s\n\tfor i = 1 to 2\n\t\tx = i\n\tendfor\nendsub\n'
    out = isl_fmt.format_source(src, indent=4)
    assert out == 'sub s\n    for i = 1 to 2\n        x = i\n    endfor\nendsub\n'


def test_forever_closed_by_endfor_and_startprint():
    src = 'sub s\nforever\nbreak\nendfor\nstartprint\nprintline "a"\nendprint\nendsub\n'
    out = isl_fmt.format_source(src)
    assert '  forever\n    break\n  endfor\n  startprint\n    printline "a"\n  endprint\n' in out
    assert codes(src).count('L002') == 0


def test_comments_and_strings_untouched():
    src = 'event init\nerrormessage "if endif // not a comment"  // if\nendevent\n'
    out = isl_fmt.format_source(src)
    assert '  errormessage "if endif // not a comment"  // if\n' in out


def test_continuation_keeps_relative_indent():
    src = 'event init\nerrormessage "a", \\\n      "b"\nendevent\n'
    out = isl_fmt.format_source(src)
    # level 1 (2 spaces) + the original 6-space offset from the first line
    assert out == 'event init\n  errormessage "a", \\\n' + ' ' * 8 + '"b"\nendevent\n'


def test_blank_lines_collapsed_and_trailing_space_stripped():
    out = isl_fmt.format_source('\n\na = 1   \n\n\n\n\nb = 2\n')
    assert out == 'a = 1\n\n\nb = 2\n'


@pytest.mark.parametrize('path', ISL_FILES, ids=lambda p: p.name)
def test_format_idempotent_and_token_preserving(path):
    src = path.read_text(encoding='utf-8', errors='replace')
    once = isl_fmt.format_source(src)
    assert isl_fmt.format_source(once) == once
    assert tokens(once) == tokens(src)


# -- lint rules ------------------------------------------------------------


def test_clean_script_has_no_errors():
    src = f'{BANNER}\n// Foo\n{BANNER}\nevent inq : 1  // Foo the Bar\n  var a : N1\nendevent\n'
    assert not [d for d in isl_lint.lint_source(src) if d.severity == 'error']
    assert codes(src) == []


def test_L001_unknown_event_and_command():
    assert 'L001' in codes('event void\nendevent\n')
    assert 'L001' in codes('event inq : 1 // x\nfrobnicate 1\nendevent\n')


def test_L002_unbalanced_blocks():
    assert 'L002' in codes('event init\nif a\nendevent\n')
    assert 'L002' in codes('endif\n')
    assert 'L002' in codes('event init\nbreak\nendevent\n')


def test_L003_wildcard_event_must_be_last():
    src = 'event tmed : *\nendevent\nevent tmed : 1\nendevent\n'
    assert 'L003' in codes(src)
    assert 'L003' not in codes('event tmed : 1\nendevent\nevent tmed : *\nendevent\n')


def test_L004_inq_needs_description():
    assert 'L004' in codes('event inq : 1\nendevent\n')
    assert 'L004' in codes('event inq : 1 //\nendevent\n')
    assert 'L004' not in codes('event inq : 1 // Do it\nendevent\n')


def test_L005_docstring_required():
    assert 'L005' in codes('sub s\nendsub\n')
    assert 'L005' not in codes(f'{BANNER}\nsub s\nendsub\n')


def test_L006_duplicate_sub():
    assert 'L006' in codes('sub s\nendsub\nsub s\nendsub\n')


def test_L007_wait_without_timeout_handling():
    src = 'event inq : 1 // x\ntxmsg "a"\nwaitforrxmsg\nendevent\nevent rxmsg : a\nendevent\n'
    assert 'L007' in codes(src)
    assert 'L007' not in codes('useisltimeouts\n' + src)


def test_L008_whitespace():
    assert 'L008' in codes('event init\nx = 1\nendevent\n')
    assert 'L008' in codes('x = 1   \n')


def test_L009_call_arity_and_ref():
    base = 'sub s(var a : N1, ref b)\nendsub\n'
    assert 'L009' in codes(base + 'call s(1)\n')
    assert 'L009' in codes(base + 'call s(1, 2)\n')  # ref given a literal
    assert 'L009' not in codes(base + 'call s(1, x)\n')


def test_fix_via_cli(tmp_path):
    f = tmp_path / 'a.isl'
    f.write_text('event init\nx = 1\nendevent\n')
    assert isl_lint.main(['--fix', str(f)]) == 0
    assert f.read_text() == 'event init\n  x = 1\nendevent\n'
    assert isl_fmt.main(['--check', str(f)]) == 0


def test_format_range_only_touches_selected_lines():
    src = 'event init\nif a\nx=1\nendif\ny=2\nendevent\n'
    out = isl_fmt.format_range(src, 3, 3)
    # selected line gets its context indent (inside event + if = 4 spaces); others untouched
    assert out.split('\n')[2] == '    x=1'
    assert out.split('\n')[4] == 'y=2'


def test_format_range_full_equals_format_source():
    src = 'event init\nif a\nx=1\nendif\nendevent\n'
    assert isl_fmt.format_range(src, 1, 5) == isl_fmt.format_source(src)


def test_lint_lines_filter(tmp_path, capsys):
    f = tmp_path / 'a.isl'
    f.write_text('event init\nx = 1\nendevent\n')
    isl_lint.main(['--lines', '1-1', str(f)])
    assert 'a.isl:2' not in capsys.readouterr().out
    isl_lint.main(['--lines', '2-2', str(f)])
    assert 'a.isl:2' in capsys.readouterr().out
