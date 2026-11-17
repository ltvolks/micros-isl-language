"""One violating and one clean snippet for every rule from L010 on, and the rule pages.

The pages in ``tools/lint_rules`` are checked against the linter (``test_rule_pages_*``): every
code the linter can emit has a page, the index lists each page in order, and the Bad/Good
examples on a page behave as the page says.
"""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import isl  # noqa: E402

RULES = ROOT / 'tools' / 'lint_rules'


def codes(src):
    return {d.code for d in isl.lint_source(src)}


def ev(body, head='event inq : 1 // test'):
    return f'{head}\n{body}\nendevent\n'


CASES = {
    'L010': [
        ev('var 1abc : n3'), ev('var display : n4'), ev('var @chk : n3'),
        ('good', ev('var abc_1 : n3\nabc_1 = 1')),
    ],
    'L011': [
        ev('var x'), ev('var x : q3'), ev('var x : n 5'), ev('var k : key5'), ev('var x : n0'),
        ev('var big[100000] : n5'),
        ('good', ev('var x : N3\nvar k : key\nvar s : a(10)\nvar t[10] : a20')),
    ],
    'L012': [
        ev('display 1, 1, @ CKNUM'), ev('if 1 < > 2\nendif'),
        ('good', ev('display 1, 1, @CKNUM\nif 1 <> 2\nendif')),
    ],
    'L013': [
        'event init\n  txmsg "a", \\ // note\n    "b"\nendevent\n',
        'event init\n  errormessage "Pick 1\\\n   or 2"\nendevent\n',
        ('good', 'event init\n  txmsg "a", \\\n    "b" // note\nendevent\n'),
    ],
    'L014': [
        'event init\nsub s\nendsub\nendevent\n', 'sub s\nevent init\nendevent\nendsub\n',
        ('good', 'event init\nendevent\nsub s\nendsub\n'),
    ],
    'L015': [ev('return'), ('good', 'sub s\n  return\nendsub\n')],
    'L016': [
        ev('input x, "Enter"', 'event init'), ev('waitforclear', 'event exit'),
        ('good', ev('input x, "Enter"')), ('good', ev('display 1, 1, "x"', 'event init')),
    ],
    'L017': [
        ev('display 1, 1, "x"'), ev('window 13, 20'), ev('window 4, 100'),
        ev('window 10, 20\ndisplay 11, 1, "x"'), ev('window 4, 20\ndisplayinput 1, 1, v, "p"'),
        ('good', ev('window 10, 20\ndisplay 10, 20, "x"\ndisplayinput 1, 1, v, "p"\nwindowinput')),
        ('good', ev('call helper\ndisplay 1, 1, "x"')),
    ],
    'L018': [ev('printline "x"'), ('good', ev('startprint @chk\nprintline "x"\nendprint'))],
    'L019': [
        ev('startprint @chk\nstartprint @rcpt\nendprint\nendprint'), ev('startprint 0\nendprint'),
        ev('startprint -1\nendprint'),
        ('good', ev('startprint @chk\nendprint\nstartprint @rcpt\nendprint')),
    ],
    'L020': [
        ev('txmsg "a"'), ev('getrxmsg'),
        ('good', ev('txmsg "a"\nwaitforrxmsg')),
        ('good', ev('if 1\ntxmsg "a"\nelse\ntxmsg "b"\nendif\ngetrxmsg')),
    ],
    'L021': [ev('saverefinfo "x"'), ('good', ev('saverefinfo "x"', 'event tmed : 1 // t'))],
    'L022': [
        ev('display 1, 1, @RVVC'), ev('@cknum = 1'), ev('display 1, 1, @SI[17]'),
        'event init\nendevent\n@warnings_are_fatal = 1\n',
        ('good', ev('display 1, 1, @SI[3]\n@strict_args = 1')),
        ('good', '@warnings_are_fatal = 1\nevent init\nendevent\n'),
    ],
    'L023': [
        ev('for 10 = 1 to 20\nendfor'), ev('var i : n3\nfor i = 1\nendfor'),
        ev('var i : n3\nfor i = 1 to 3 step 0\nendfor'), ev('var i : $5\nfor i = 1 to 3\nendfor'),
        ('good', ev('var i : n3\nfor i = 1 to 9 step 2\nendfor')),
    ],
    'L024': [
        'sub s(var a[] : n3)\nendsub\n', 'sub s(ref a[)\nendsub\n', 'sub s(a : n3)\nendsub\n',
        ('good', 'sub s(ref a[], var n : n3)\nendsub\n'),
    ],
    'L025': ['sub s - 4\nendsub\n', ev('call s + 3'), ('good', 'sub s\nendsub\n' + ev('call s'))],
    'L026': [ev('', 'event rxmsg : 1bad'), ('good', ev('', 'event rxmsg : ok_id'))],
    'L027': [
        ev('prompt "this prompt text is much longer than thirty-eight characters"'),
        ('good', ev('prompt "short"')),
    ],
    'L028': [ev('x = 1'), ('good', ev('var x : n3\nx = 1'))],
    'L029': [ev('var x : n3\nvar x : a5'), 'var x : n3\n' + ev('var x : n3'),
             ('good', ev('var x : n3') + ev('var x : n3'))],
    'L030': ['window 10, 20\n', 'display 1, 1, "x"\n',
             ('good', 'var g : n3\nuseisltimeouts\n@strict_args = 1\n' + ev('window 4, 4'))],
    'L031': [
        ev('var n : N3\nn = 12345'), ev('var s : a3\ns = "message"'), ev('var d : $3\nd = 123.45'),
        ev('var line : a10\nformat line as "This line is greater than 10 characters"'),
        ('good', ev('var n : N3\nn = 123\nvar s : a9\ns = "message"')),
    ],
    'L032': [
        ev('var a[10] : n5\na[12] = 1'), ev('var a[10] : n5\na[0] = 1'), ev('txmsg list[]'),
        ev('var l[10] : a20\ntxmsg 21, l[]\nwaitforrxmsg'),
        ('good', ev('var a[10] : n5\na[10] = 1\nvar l[10] : a20\ntxmsg 10, l[]\nwaitforrxmsg')),
    ],
    'L033': [
        ev('display 2, 2,'), ev('var i : n3\ni = 5 +'), ev('if 1\nendif x'), ev('*waitclear'),
        ev('format as "x"'), ev('var s : a9\nformat s "x"'),
        ('good', ev('var s : a9\nformat s as "x"\nif 1\nendif')),
    ],
    'L034': [
        ev('var i : n3\ni = 5 / 0'), ev('var s : a9\ns = "123" - "abc"'),
        ev('var a : $5, c : $5\nc = a % c'),
        ('good', ev('var i : n3\ni = 5 / 2 + 10')),
    ],
    'L035': [
        ev('var x : n3\nx = frobnicate(1)'), ev('var s : a9\ns = mid("abc", -2, 3)'),
        ev('var s : a9\ns = mid("abc", 1)'),
        ('good', ev('var s : a9\ns = mid("abc", 1, 2)\ns = trim(s)')),
    ],
    'L036': [ev('input 123, "Enter value"'), ('good', ev('var v : n3\ninput v, "Enter value"'))],
    'L037': [ev('clearislts\ndisplayislts'),
             ('good', ev('clearislts\nsetisltskey 1, 1, 2, 1, 1, @key_clear, "CLEAR"\ndisplayislts'))],
}


def cases():
    out = []
    for code, items in CASES.items():
        for i, item in enumerate(items):
            kind, src = item if isinstance(item, tuple) else ('bad', item)
            out.append(pytest.param(code, kind, src, id=f'{code}-{kind}-{i}'))
    return out


@pytest.mark.parametrize('code,kind,src', cases())
def test_rule_fires_on_bad_and_not_on_good(code, kind, src):
    found = codes(src)
    if kind == 'bad':
        assert code in found, f'{code} should fire on:\n{src}'
    else:
        assert code not in found, f'{code} should not fire on:\n{src}'


def test_every_new_rule_has_cases():
    assert set(CASES) == {f'L{n:03d}' for n in range(10, 38)}


def test_event_rxmsg_callback_may_save_ref_info():
    assert 'L021' not in codes(ev('saverefinfo "x"', 'event rxmsg : done'))


def test_sub_sees_variables_of_its_callers():
    src = ev('var shared : n3\ncall s') + 'sub s\n  shared = 1\nendsub\n'
    assert 'L028' not in codes(src)


# ---------------------------------------------------------------- rule pages

def page_codes():
    return sorted(p.stem for p in RULES.glob('L[0-9][0-9][0-9].md'))


def emitted_codes():
    src = (ROOT / 'tools' / 'isl.py').read_text(encoding='utf-8')
    return sorted(set(re.findall(r"""['"](L\d{3})['"]""", src)))


def test_rule_pages_exist_for_every_code():
    assert page_codes() == emitted_codes()


def test_rule_index_lists_every_page_in_order():
    text = (RULES / 'index.md').read_text(encoding='utf-8')
    listed = re.findall(r'^\|\s*\[(L\d{3})\]\((L\d{3})\.md\)', text, re.M)
    assert [a for a, _ in listed] == page_codes()
    assert all(a == b for a, b in listed)


def blocks(text):
    return re.findall(r'^```isl\n(.*?)^```', text, re.M | re.S)


@pytest.mark.parametrize('code', page_codes())
def test_rule_page_shape_and_examples(code):
    text = (RULES / f'{code}.md').read_text(encoding='utf-8')
    assert text.startswith(f'# {code}: ')
    assert re.search(r'^\|\s*Severity\s*\|', text, re.M)
    bad = re.search(r'^## Bad\n(.*?)(?=^## )', text, re.M | re.S)
    good = re.search(r'^## Good\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    assert bad and good, f'{code}.md needs "## Bad" and "## Good" sections'
    bad_blocks, good_blocks = blocks(bad.group(1)), blocks(good.group(1))
    assert bad_blocks and good_blocks
    for block in bad_blocks:
        assert code in codes(block), f'{code}.md: the Bad example does not raise {code}:\n{block}'
    for block in good_blocks:
        assert code not in codes(block), f'{code}.md: the Good example raises {code}:\n{block}'


def slug(heading):
    """GitHub-style heading anchor."""
    text = re.sub(r'`', '', heading.strip().lower())
    return re.sub(r'\s', '-', re.sub(r'[^\w\- ]', '', text))


def anchors(path):
    found = set()
    in_fence = False
    for line in path.read_text(encoding='utf-8').split('\n'):
        if line.startswith('```'):
            in_fence = not in_fence
        elif not in_fence and (m := re.match(r'#{1,6}\s+(.*)', line)):
            found.add(slug(m.group(1)))
    return found


@pytest.mark.parametrize('code', page_codes() + ['index'])
def test_rule_page_links_resolve(code):
    page = RULES / f'{code}.md'
    for target in re.findall(r'\]\(([^)]+)\)', page.read_text(encoding='utf-8')):
        if target.startswith('http'):
            continue
        path, _, frag = target.partition('#')
        dest = (page.parent / path).resolve()
        assert dest.exists(), f'{code}: {target} does not exist'
        if frag and dest.suffix == '.md':
            assert frag in anchors(dest), f'{code}: no heading "#{frag}" in {path}'
