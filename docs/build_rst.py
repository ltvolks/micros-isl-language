#!/usr/bin/env python3
"""Generate Sphinx reStructuredText from the markdown ISL reference.

    docs/build_rst.py [--out docs/_generated]

Reads  skills/micros-isl-language/isl-reference/reference/*.md
Writes <out>/reference/<category>.rst, <out>/guide/*.rst and the index fragments.
The markdown is the only source; nothing in <out> is edited by hand.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / 'skills' / 'micros-isl-language' / 'isl-reference' / 'reference'
sys.path.insert(0, str(HERE / '_ext'))
import isl_names  # noqa: E402
sys.path.insert(0, str(HERE.parent / 'tools'))
import isl  # noqa: E402

CODE_WORDS = set(isl.KNOWN_COMMANDS) | set(isl.BLOCK_OPEN) | set(isl.BLOCK_MIDDLE) | set(isl.BLOCK_CLOSE)
from isl_names import TYPES, slug  # noqa: E402

CATEGORIES = [
    # file, page title, objtype, intro
    ('commands', 'Commands', 'command', 'Language commands: syntax, arguments, usage and examples.'),
    ('events', 'Events', 'event', 'Events a script can handle, with syntax and examples.'),
    ('functions', 'Functions', 'function', 'Built-in functions.'),
    ('sysvars', 'System variables', 'sysvar', 'System variables (``@Name``) that scripts can read or set.'),
    ('specifiers', 'Specifiers', 'specifier', 'Input and output format specifiers.'),
    ('errors', 'Error messages', 'error', 'Run-time error messages and what causes them.'),
    ('keys', 'Key names and codes', 'key', 'Key names, key types and key codes.'),
]


# ------------------------------------------------------------------ inline text

BOLD = re.compile(r'\*\*(?=\S)(.+?)(?<=\S)\*\*')
CODE = re.compile(r'`([^`\n]+)`')


def esc(text: str) -> str:
    text = text.replace('\\', '\\\\')
    text = re.sub(r'([*`|])', r'\\\1', text)
    text = re.sub(r'_(?=[\s\[(,.;:\\]|$)', r'\\_', text)   # trailing underscore reads as a link
    text = re.sub(r'(?<![\w])_(?=\w)', r'\\_', text)   # leading underscore (e.g. _Timeout)
    text = re.sub(r'<(?=\w+>)', r'\\<', text)
    return text


def inline(text: str) -> str:
    """Markdown-ish text -> RST inline markup (bold and code spans survive; the rest is escaped)."""
    out: list[str] = []
    pos = 0
    pieces = sorted([(m.start(), m.end(), 'b', m) for m in BOLD.finditer(text)] +
                    [(m.start(), m.end(), 'c', m) for m in CODE.finditer(text)])
    last_end = 0
    for start, end, kind, m in pieces:
        if start < last_end:
            continue
        out.append(esc(text[pos:start]))
        if kind == 'b':
            out.append('**' + esc(m.group(1)) + '**')
        else:
            out.append('``' + m.group(1) + '``')
        pos = last_end = end
    out.append(esc(text[pos:]))
    s = ''.join(out)
    s = re.sub(r'^(\d+)([.)])(\s)', r'\1\\\2\3', s)      # "1. " would start a list
    s = re.sub(r'^([-+>])(\s)', r'\\\1\2', s)
    s = re.sub(r'^(\.\.)', r'\\\1', s)
    if s.endswith('::'):
        s = s[:-2] + '\\:\\:'
    return s


def title_text(text: str) -> str:
    return inline(re.sub(r'\*\*(.+?)\*\*', r'\1', text.strip()))


def role_text(text: str) -> str:
    return text.replace('<', '\\<').replace('>', '\\>')


# ------------------------------------------------------------------ parsing

class Entry:
    def __init__(self, title: str, lines: list[str]):
        self.title = title.strip()
        self.lines = lines
        self.type = ''
        self.label = ''


def split_entries(md: str) -> list[Entry]:
    entries: list[Entry] = []
    cur: Entry | None = None
    in_fence = False
    for line in md.split('\n'):
        if line.startswith('```'):
            in_fence = not in_fence
        if not in_fence and line.startswith('## '):
            cur = Entry(line[3:], [])
            entries.append(cur)
        elif cur is not None:
            cur.lines.append(line)
    for e in entries:
        while e.lines and (not e.lines[-1].strip() or e.lines[-1].strip() == '---'):
            e.lines.pop()
        # drop the source comment and the echoed page title
        body = e.lines
        i = 0
        while i < len(body) and not body[i].strip():
            i += 1
        if i < len(body) and body[i].startswith('<!--'):
            i += 1
            while i < len(body) and not body[i].strip():
                i += 1
            norm = lambda s: re.sub(r'[\s*]+', '', s).lower()  # noqa: E731
            if i < len(body) and norm(body[i]) == norm(e.title):
                i += 1
            e.lines = body[i:]
    return entries


class Index:
    """All entries of all categories, with alias lookup (used for See also links)."""

    def __init__(self):
        self.entries: list[Entry] = []
        self.by_key: dict[str, list[Entry]] = {}

    def add(self, entry: Entry):
        self.entries.append(entry)
        for name in {entry.title, *isl_names.aliases(entry.type, entry.title)}:
            self.by_key.setdefault(name.lower().lstrip('@ '), []).append(entry)

    def find(self, name: str, prefer: str | None = None) -> Entry | None:
        hits = self.by_key.get(name.strip().lower().lstrip('@ '), [])
        if not hits:
            return None
        exact = [h for h in hits if h.title.lower() == name.strip().lower()]
        pool = exact or hits
        order = ([prefer] if prefer else []) + isl_names.PRIORITY
        for objtype in order:
            for h in pool:
                if h.type == objtype:
                    return h
        return pool[0]


def role(entry: Entry, text: str | None = None) -> str:
    rname = TYPES[entry.type][2]
    shown = text if text is not None else entry.title
    if shown == entry.title:
        return f':isl:{rname}:`{role_text(entry.title)}`'
    return f':isl:{rname}:`{role_text(shown)} <{role_text(entry.title)}>`'


# ------------------------------------------------------------------ block conversion

def indent(lines: list[str], n: int = 3) -> list[str]:
    pad = ' ' * n
    return [pad + ln if ln.strip() else '' for ln in lines]


def is_row(line: str) -> bool:
    s = line.strip()
    return bool(s) and (' |  ' in s or s.startswith('|  ') or s.endswith(' |')) and s.count('|') >= 1


def cells(line: str) -> list[str]:
    parts = [c.strip() for c in line.strip().split('|')]
    if parts and parts[-1] == '':
        parts.pop()
    if parts and parts[0] == '' and line.strip().startswith('|'):
        parts.pop(0)
    return parts


def render_table(rows: list[str]) -> list[str] | None:
    parsed = [cells(r) for r in rows]
    width = len(parsed[0])
    if len(parsed) < 2 or width < 2 or any(len(p) != width for p in parsed):
        return None
    header = parsed.count(parsed[0]) > 1 or all(BOLD.fullmatch(c) for c in parsed[0] if c)
    body = [p for i, p in enumerate(parsed) if i == 0 or p != parsed[0]]
    out = ['.. list-table::']
    if header:
        out.append('   :header-rows: 1')
    out.append('')
    for r in body:
        for j, c in enumerate(r):
            out.append(('   * - ' if j == 0 else '     - ') + inline(c))
    return out


def convert_body(lines: list[str], index: Index | None, own_type: str, guide: bool = False,
                 see_also=None, current_heading: str = '', page_headings: set[str] | None = None) -> list[str]:
    out: list[str] = []
    i, n = 0, len(lines)

    def blank():
        if out and out[-1] != '':
            out.append('')

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if line.startswith('```'):
            lang = line[3:].strip() or 'text'
            j = i + 1
            code = []
            while j < n and not lines[j].startswith('```'):
                code.append(lines[j])
                j += 1
            while code and not code[-1].strip():
                code.pop()
            blank()
            if guide and line.strip() == '```':
                out += bare_block(code, current_heading, page_headings)
                i = j + 1
                continue
            if lang == 'mermaid':
                out += ['.. mermaid::', ''] + indent(code) + ['']
                i = j + 1
                continue
            out.append(f'.. code-block:: {lang}')
            out.append('')
            out += indent(code)
            out.append('')
            i = j + 1
            continue
        if re.match(r'#{3,6} ', line):
            blank()
            out.append(f'.. rubric:: {title_text(line.lstrip("#"))}')
            out.append('')
            i += 1
            continue
        if re.fullmatch(r'\*\*See also:?\*\*:?', s) or re.match(r'See also:', s):
            j = i + 1
            items: list[str] = []
            if re.match(r'See also:\s*\S', s):
                items += [x.strip() for x in re.split(r'[;]', s.split(':', 1)[1]) if x.strip()]
            while j < n and not (lines[j].startswith(('```', '#', '**')) or lines[j].strip() == '---'):
                if lines[j].strip():
                    items += [x.strip() for x in lines[j].split(';') if x.strip()]
                j += 1
            blank()
            out.append('.. rubric:: See also')
            out.append('')
            for item in items:
                item = item.rstrip('.')
                target = see_also(item) if see_also else None
                hit = None if target else (index.find(item) if index else None)
                out.append('* ' + (target if target else (role(hit, item) if hit else inline(item))))
            out.append('')
            i = j
            continue
        if is_row(line):
            rows, j = [], i
            while j < n:
                if is_row(lines[j]):
                    rows.append(lines[j])
                    j += 1
                elif not lines[j].strip() and j + 1 < n and is_row(lines[j + 1]):
                    j += 1
                else:
                    break
            table = render_table(rows)
            blank()
            if table:
                out += table
            else:
                out.append('.. code-block:: text')
                out.append('')
                out += indent([r.rstrip() for r in rows])
            out.append('')
            i = j
            continue
        if re.match(r'[-*] ', line):
            blank()
            while i < n and re.match(r'[-*] ', lines[i]):
                out.append('* ' + inline(lines[i][2:]))
                i += 1
                while i < n and lines[i].strip() and not re.match(r'([-*] |```|#|\*\*)', lines[i]) \
                        and not is_row(lines[i]):
                    out.append('  ' + inline(lines[i].strip()))
                    i += 1
            out.append('')
            continue
        # one source line = one paragraph
        blank()
        out.append(inline(s))
        out.append('')
        i += 1
    while out and out[-1] == '':
        out.pop()
    return out


# ------------------------------------------------------------------ guide

FOOTER = re.compile(r'^[A-Z]?-?\d+\s{3,}\S')
GAPS = re.compile(r'\S\s{3,}\S')


def bare_block(code: list[str], heading: str, headings: set[str] | None = None) -> list[str]:
    """A bare ``` block in the guide is PDF layout: tables, callouts, wrapped prose, page furniture."""
    real = [c.strip() for c in code if c.strip()]
    if not real:
        return []
    if len(real) == 1 and (FOOTER.match(real[0]) or re.fullmatch(r'[A-Z]-\d+\s+.*', real[0])):
        return []                                           # running page footer
    if real[0].startswith('In This Chapter'):
        return []                                           # CHM-style page list
    if re.match(r'Note\s{2,}', real[0]):
        text = ' '.join(re.sub(r'^Note\s+', '', ' '.join(real)).split())
        return ['.. note::', '', '   ' + inline(text), '']
    known = {heading.strip().lower()} | (headings or set())
    if real[0].lower() in known:
        real = real[1:]                                      # the PDF repeats the heading in the box
        if not real:
            return []
    gaps = sum(1 for r in real if GAPS.search(r))
    avg = sum(len(r) for r in real) / len(real)
    if gaps <= max(1, len(real) // 6) and avg > 45:
        lines = real
        paras, cur = [], []
        for r in lines:
            cur.append(r)
            if r.endswith(('.', ':')):
                paras.append(' '.join(cur))
                cur = []
        if cur:
            paras.append(' '.join(cur))
        out: list[str] = []
        for para in paras:
            out += [inline(para), '']
        return out
    first = re.match(r'[A-Za-z_]\w*', real[0])
    if first and first.group(0).lower() in CODE_WORDS and gaps == 0 and not GAPS.search(real[0]):
        return ['.. code-block:: isl', ''] + indent([c.rstrip() for c in code]) + ['']   # unvalidated fragment
    return ['.. code-block:: text', ''] + indent([c.rstrip() for c in code]) + ['']


GUIDE_CHAPTERS = [
    # slug, title, regex matching the H2 heading that starts it, inferred?
    ('preface', 'Preface', r'Preface$'),
    ('chapter-1', 'Chapter 1: Understanding SIM and ISL', r'Chapter 1\b'),
    ('chapter-2', 'Chapter 2: Getting Started', r'Chapter 2\b'),
    ('chapter-3', 'Chapter 3: Writing Scripts', r'Getting Started with Script Writing$'),
    ('chapter-4', 'Chapter 4: Using Variables', r'Chapter 4\b'),
    ('chapter-5', 'Chapter 5: ISL Printing', r'Getting Started with ISL Printing$'),
    ('chapter-6', 'Chapter 6: ISL System Variables', r'Chapter 6\b'),
    ('chapter-7', 'Chapter 7: Format Specifiers', r'Chapter 7\b'),
    ('appendix-a', 'Appendix A: Windows DLL Access', r'APPENDIX A\b'),
    ('appendix-b', 'Appendix B: Database Access', r'APPENDIX B\b'),
    ('glossary', 'Glossary', None),
]
ADORN = {2: '-', 3: '~', 4: '^', 5: '"', 6: "'"}


def split_guide(md: str) -> dict[str, list[str]]:
    lines = md.split('\n')
    # fences hide headings
    in_fence, marks = False, []
    for n, ln in enumerate(lines):
        if ln.startswith('```'):
            in_fence = not in_fence
        elif not in_fence and ln.startswith('## '):
            for slug_, _t, pattern in GUIDE_CHAPTERS:
                if pattern and re.match(pattern, ln[3:].strip()):
                    marks.append((n, slug_))
    gloss = next(n for n, ln in enumerate(lines) if ln.startswith('#### Argument'))
    marks.append((gloss, 'glossary'))
    marks.sort()
    pages: dict[str, list[str]] = {}
    for (start, slug_), nxt in zip(marks, marks[1:] + [(len(lines), None)]):
        body = lines[start:nxt[0]]
        if slug_ != 'glossary' and nxt[1] == 'glossary':
            body = lines[start:nxt[0]]
        pages[slug_] = body
    # glossary start belongs to the page after Appendix B: trim the B-6 page header
    pages['appendix-b'] = [ln for ln in pages['appendix-b'] if not re.match(r'#+ B-\d+\s', ln)]
    return pages


def build_guide_page(slug_: str, title: str, lines: list[str], index: Index) -> tuple[str, list[str]]:
    glossary = slug_ == 'glossary'
    out = [f'.. _guide-{slug_}:', '', title, '=' * len(title), '']
    if lines and lines[0].startswith('## '):
        lines = lines[1:]                                    # chapter marker heading
    seg: list[str] = []
    heading = ''
    labels: list[str] = []
    term_labels = {}

    def flush():
        nonlocal seg
        out.extend(convert_body(seg, index, '', guide=True, current_heading=heading,
                                page_headings=page_headings,
                                see_also=(lambda t: glossary_ref(t, term_labels)) if glossary else None))
        out.append('')
        seg = []

    in_fence = False
    stack: list[int] = []
    page_headings = {m.group(1).strip().lower() for ln in lines for m in [re.match(r'#{2,6} (.+)', ln)] if m}
    if glossary:
        for ln in lines:
            m = re.match(r'#{2,6} (.+)', ln)
            if m:
                term_labels[m.group(1).strip().lower()] = f'glossary-{slug(m.group(1))}'
    for ln in lines:
        if ln.startswith('```'):
            in_fence = not in_fence
        m = None if in_fence else re.match(r'(#{2,6}) (.+)', ln)
        if m:
            flush()
            src_level = 2 if glossary else len(m.group(1))
            while stack and stack[-1] >= src_level:
                stack.pop()
            stack.append(src_level)
            level = len(stack) + 1                           # no skipped heading levels
            heading = m.group(2).strip()
            t = title_text(heading)
            if glossary:
                out += [f'.. _glossary-{slug(heading)}:', '']
            out += [t, ADORN[level] * max(len(t), 3), '']
            labels.append(heading)
            continue
        seg.append(ln)
    flush()
    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n'
    return text, labels


def glossary_ref(text: str, term_labels: dict[str, str]) -> str | None:
    key = text.strip().rstrip('.').lower()
    if key in term_labels:
        return f':ref:`{role_text(text.strip().rstrip("."))} <{term_labels[key]}>`'
    return None


def build_guide(md: str, out: Path, index: Index) -> int:
    (out / 'guide').mkdir(parents=True, exist_ok=True)
    pages = split_guide(md)
    toc = ['Guide', '=====', '',
           'The SIM Companion Guide for the 3700 (RES) system: concepts, message formats, writing and testing',
           'scripts, variables, printing, system variables, specifiers, and the DLL and database appendices.',
           '', '.. toctree::', '   :maxdepth: 2', '']
    for slug_, title, _pattern in GUIDE_CHAPTERS:
        text, _labels = build_guide_page(slug_, title, pages[slug_], index)
        (out / 'guide' / f'{slug_}.rst').write_text(text, encoding='utf-8')
        toc.append(f'   {slug_}')
    (out / 'guide' / 'index.rst').write_text('\n'.join(toc) + '\n', encoding='utf-8')
    return len(GUIDE_CHAPTERS)


# ------------------------------------------------------------------ pages

def underline(text: str, ch: str) -> str:
    return ch * max(len(text), 3)


def build_category(fname: str, page_title: str, objtype: str, intro: str, entries: list[Entry],
                   index: Index) -> str:
    prefix = TYPES[objtype][0]
    directive = TYPES[objtype][1]
    out = [f'.. _isl-{fname}:', '', page_title, underline(page_title, '='), '', intro, '',
           '.. rubric:: Contents', '', '.. hlist::', '   :columns: 3', '']
    for e in entries:
        out.append(f'   * :ref:`{role_text(title_text(e.title))} <{e.label}>`')
    out.append('')
    for e in entries:
        t = title_text(e.title)
        out += [f'.. _{e.label}:', '', t, underline(t, '-'), '',
                f'.. isl:{directive}:: {e.title}', f'   :anchor: {e.label}', '']
        body = convert_body(e.lines, index, objtype)
        out += body
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


def build_index(by_cat: dict[str, list[Entry]]) -> str:
    out = ['Index', '=====', '', '.. toctree::', '   :hidden:', '']
    out += [f'   reference/{f}' for f, *_ in CATEGORIES]
    out.append('')
    for fname, title, objtype, _intro in CATEGORIES:
        entries = by_cat[fname]
        out += [title, underline(title, '-'), '',
                f'{len(entries)} entries; see :doc:`{title} <reference/{fname}>`.', '',
                '.. hlist::', '   :columns: 3', '']
        for e in entries:
            out.append(f'   * {role(e)}')
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', default=str(HERE / '_generated'))
    args = ap.parse_args(argv)
    out = Path(args.out)
    (out / 'reference').mkdir(parents=True, exist_ok=True)

    by_cat: dict[str, list[Entry]] = {}
    index = Index()
    for fname, _title, objtype, _intro in CATEGORIES:
        entries = split_entries((REFERENCE / f'{fname}.md').read_text(encoding='utf-8'))
        seen: dict[str, int] = {}
        for e in entries:
            e.type = objtype
            base = f'{TYPES[objtype][0]}-{slug(e.title)}'
            seen[base] = seen.get(base, 0) + 1
            e.label = base if seen[base] == 1 else f'{base}-{seen[base]}'
            index.add(e)
        by_cat[fname] = entries

    for fname, title, objtype, intro in CATEGORIES:
        text = build_category(fname, title, objtype, intro, by_cat[fname], index)
        (out / 'reference' / f'{fname}.rst').write_text(text, encoding='utf-8')
    (out / 'reference_index.rst').write_text(build_index(by_cat), encoding='utf-8')
    chapters = build_guide((REFERENCE / 'guide.md').read_text(encoding='utf-8'), out, index)
    total = sum(len(v) for v in by_cat.values())
    print(f'wrote {total} entries in {len(CATEGORIES)} pages and {chapters} guide pages to {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
