"""Sphinx domain ``isl``: commands, events, functions, system variables, ...

* Every ``## Title`` section of ``reference/<page>.md`` (commands, events, ...) is registered as an
  entry by ``read_reference`` below; the markdown is read by MyST as it is.
* Roles ``:isl:cmd:``, ``:isl:event:``, ``:isl:fn:``, ``:isl:sysvar:``, ``:isl:spec:``,
  ``:isl:err:``, ``:isl:key:`` and the type-agnostic ``:isl:ref:`` link to entries.
* Entries are exported in objects.inv, so another project can use intersphinx. Without any extension
  that project can use the std labels (``:ref:`TxMsg <isl:cmd-txmsg>```); if it also loads this
  extension (put docs/_ext on sys.path, add 'isl_domain') it can write ``:isl:cmd:`isl:TxMsg```.
* A doctree transform links ``@SysVars``, inline literals and CamelCase names in prose, and the
  command, function and @sysvar names inside highlighted ``isl`` code blocks (HTML builders).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from docutils import nodes
from sphinx import addnodes
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

sys.path.insert(0, str(Path(__file__).resolve().parent))
import isl_names  # noqa: E402
from isl_names import PAGE_INTROS, PAGE_TITLES, PAGE_TYPE, PRIORITY, TYPES  # noqa: E402


class IslDomain(Domain):
    name = 'isl'
    label = 'ISL'
    object_types = {t: ObjType(v[3], v[2]) for t, v in TYPES.items()}
    roles = {**{v[2]: XRefRole() for v in TYPES.values()}, 'ref': XRefRole()}
    initial_data = {'objects': {}}      # (objtype, name) -> (docname, anchor)
    data_version = 1

    # -- registration / bookkeeping
    def note_object(self, objtype, name, anchor, docname):
        self.data['objects'][(objtype, name)] = (docname, anchor)

    def clear_doc(self, docname):
        for key in [k for k, v in self.data['objects'].items() if v[0] == docname]:
            del self.data['objects'][key]

    def merge_domaindata(self, docnames, otherdata):
        for key, val in otherdata['objects'].items():
            if val[0] in docnames:
                self.data['objects'][key] = val

    # -- lookup (case-insensitive over titles and aliases)
    def _table(self):
        table = getattr(self, '_lookup', None)
        if table is None or table[0] != len(self.data['objects']):
            lookup: dict[str, list[tuple]] = {}
            for (objtype, name), (docname, anchor) in self.data['objects'].items():
                for spelling in {name, *isl_names.aliases(objtype, name)}:
                    lookup.setdefault(spelling.lower().lstrip('@ '), []).append(
                        (spelling == name, objtype, name, docname, anchor))
            self._lookup = table = (len(self.data['objects']), lookup)
        return table[1]

    def find(self, text, objtype=None, types=None):
        hits = self._table().get(text.strip().lower().lstrip('@ '), [])
        if objtype:
            hits = [h for h in hits if h[1] == objtype]
        if types:
            hits = [h for h in hits if h[1] in types]
        if not hits:
            return None
        exact = [h for h in hits if h[0]]
        pool = exact or hits
        pool.sort(key=lambda h: PRIORITY.index(h[1]))
        return pool[0]

    # -- xrefs
    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        objtype = next((t for t, v in TYPES.items() if v[2] == typ), None)
        hit = self.find(target, objtype)
        if not hit:
            return None
        _, _, name, docname, anchor = hit
        return make_refnode(builder, fromdocname, docname, anchor, contnode, name)

    def resolve_any_xref(self, env, fromdocname, builder, target, node, contnode):
        hit = self.find(target)
        if not hit:
            return []
        _, objtype, name, docname, anchor = hit
        return [(f'isl:{TYPES[objtype][2]}', make_refnode(builder, fromdocname, docname, anchor, contnode, name))]

    def get_objects(self):
        for (objtype, name), (docname, anchor) in sorted(self.data['objects'].items()):
            yield name, name, objtype, docname, anchor, 1
            for alias in sorted(isl_names.aliases(objtype, name)):
                yield alias, alias, objtype, docname, anchor, 2

    def get_full_qualified_name(self, node):
        return node.get('reftarget')


# ---------------------------------------------------------------- reference pages (plain markdown)

def _norm(text):
    return re.sub(r'[\s*]+', '', text).lower()


def read_reference(app, doctree):
    """doctree-read: turn each ``##`` section of a reference page into an ``isl`` domain entry.

    Adds the stable label (``cmd-break``), the domain object, an index entry, and removes the page
    name that the source repeats under the heading.
    """
    docname = app.env.docname
    if docname.startswith('guide/'):
        return read_guide(app, doctree, docname)
    if not docname.startswith('reference/'):
        return
    page = docname.split('/', 1)[1]
    objtype = PAGE_TYPE.get(page)
    top = doctree.next_node(nodes.section)
    if not objtype or top is None:
        return
    prefix, human = TYPES[objtype][0], TYPES[objtype][3]
    domain, std = app.env.get_domain('isl'), app.env.get_domain('std')
    index = app.env.get_domain('index')

    top[0].children = [nodes.Text(PAGE_TITLES[page])]
    page_label = f'isl-{page}'
    top['ids'].insert(0, page_label)
    std.labels[page_label] = (docname, page_label, PAGE_TITLES[page])
    std.anonlabels[page_label] = (docname, page_label)

    # the source's own preamble ("Source: ... grep ^## ...") is for Claude; show a one-line intro instead
    top.children = [top[0], nodes.paragraph('', PAGE_INTROS[page].replace('``', ''))] + \
        [c for c in top.children[1:] if isinstance(c, nodes.section)]
    for c in top.children:
        c.parent = top

    seen = {}
    for sec in [c for c in top.children if isinstance(c, nodes.section)]:
        title = sec[0].astext().strip()
        if title == CATEGORY_INDEX:
            categorise(sec)
            continue
        base = f'{prefix}-{isl_names.slug(title)}'
        seen[base] = seen.get(base, 0) + 1
        label = base if seen[base] == 1 else f'{base}-{seen[base]}'
        sec['ids'].insert(0, label)
        std.labels[label] = (docname, label, title)
        std.anonlabels[label] = (docname, label)
        domain.note_object(objtype, title, label, docname)
        for child in list(sec.children[1:]):
            if isinstance(child, nodes.raw) and child.astext().lstrip().startswith('<!--'):
                sec.remove(child)               # "<!-- src: ... -->" provenance comment
                continue
            if isinstance(child, nodes.comment):
                continue
            if isinstance(child, nodes.paragraph) and _norm(child.astext()) == _norm(title):
                sec.remove(child)
            break
        entry = ('single', f'{title} ({human.lower()})', label, '', None)
        sec.insert(1, addnodes.index(entries=[entry]))
        # the index domain has already scanned this document by now, so register the entry directly
        index.entries.setdefault(docname, []).append(entry)


CATEGORY_INDEX = 'Commands by category'


def categorise(sec):
    """Turn the ``### Category`` + bullet lists of a "by category" section into links to the entries.

    The names stay plain markdown in the source; here each one becomes a cross-reference (resolved by
    the domain, so ``Event...EndEvent`` and friends match their titles) and the section is marked for
    the two-column layout in ``_static/isl.css``.
    """
    sec['classes'].append('isl-categories')
    for item in sec.findall(nodes.list_item):
        para = item[0]
        name = para.astext().strip()
        xref = addnodes.pending_xref('', nodes.Text(name), refdomain='isl', reftype='ref', reftarget=name,
                                     refexplicit=False, refwarn=True)
        para.children = [xref]
        xref.parent = para
        item['classes'].append('isl-category-item')


def read_guide(app, doctree, docname):
    """Stable labels for the guide: ``guide-<page>`` and, in the glossary, ``glossary-<term>``."""
    std = app.env.get_domain('std')
    top = doctree.next_node(nodes.section)
    if top is None:
        return
    page = docname.split('/', 1)[1]
    label = f'guide-{page}'
    top['ids'].insert(0, label)
    std.labels[label] = (docname, label, top[0].astext())
    std.anonlabels[label] = (docname, label)
    if page == 'glossary':
        for sec in [c for c in top.children if isinstance(c, nodes.section)]:
            title = sec[0].astext().strip()
            gl = f'glossary-{isl_names.slug(title)}'
            sec['ids'].insert(0, gl)
            std.labels[gl] = (docname, gl, title)
            std.anonlabels[gl] = (docname, gl)


SEE_ALSO = re.compile(r'^\s*See also:?\s*', re.I)


def _items(text):
    return [i.strip().rstrip('.').strip() for line in text.split('\n') for i in line.split(';') if i.strip()]


def see_also(app, doctree, docname, domain):
    """Turn ``See also:`` paragraphs (and the paragraphs of names that follow) into a linked list."""
    glossary = {v[2].lower(): (True, 'glossary', v[2], v[0], v[1]) for k, v in app.env.get_domain('std').labels.items()
                if k.startswith('glossary-')} if docname.startswith('guide/') else {}
    for para in list(doctree.findall(nodes.paragraph)):
        if para.parent is None or not SEE_ALSO.match(para.astext()):
            continue
        items = _items(SEE_ALSO.sub('', para.astext(), count=1))
        parent = para.parent
        pos = parent.index(para)
        consumed = [para]
        for sib in parent.children[pos + 1:]:
            if not isinstance(sib, nodes.paragraph) or (sib.children and isinstance(sib.children[0], nodes.strong)):
                break
            items += _items(sib.astext())
            consumed.append(sib)
        if not items:
            continue
        bullets = nodes.bullet_list(bullet='*')
        for item in items:
            hit = glossary.get(item.lower()) or domain.find(item) \
                or domain.find(re.sub(r'\s+(Function|Command|Event)$', '', item))
            content = _link(app, docname, hit, nodes.Text(item)) if hit else nodes.Text(item)
            bullets += nodes.list_item('', nodes.paragraph('', '', content))
        parent[pos:pos + len(consumed)] = [nodes.rubric('', 'See also'), bullets]


# ---------------------------------------------------------------- auto-linking

CAMEL = re.compile(r'(?<![\w@])(@\s?[A-Za-z_]\w*|[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+|'
                   r'[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)(?![\w])')
SKIP_PARENTS = (nodes.reference, nodes.literal_block, nodes.title, nodes.raw, addnodes.desc_signature,
                nodes.strong, nodes.rubric, nodes.term, nodes.comment)
TOKEN_SPAN = re.compile(r'<span class="(k|nf|n|nb)">(@?[A-Za-z_][\w]*|@ [A-Za-z_]\w*)</span>')


def _link(app, fromdocname, hit, content):
    _, _, name, docname, anchor = hit
    uri = app.builder.get_relative_uri(fromdocname, docname) + '#' + anchor
    ref = nodes.reference('', '', internal=True, refuri=uri, classes=['isl-autolink'])
    ref += content
    ref['title'] = name
    return ref


def autolink(app, doctree, docname):
    if app.builder.format != 'html':
        return
    domain = app.env.get_domain('isl')
    if not domain.data['objects']:
        return                      # a consuming project (intersphinx): nothing local to link to

    if docname.startswith(('reference/', 'guide/')):
        see_also(app, doctree, docname, domain)

    # 1. prose and literals
    for text_node in list(doctree.findall(nodes.Text)):
        parent = text_node.parent
        if parent is None or isinstance(parent, SKIP_PARENTS):
            continue
        if any(isinstance(p, SKIP_PARENTS) for p in _ancestors(parent)):
            continue
        s = text_node.astext()
        if isinstance(parent, nodes.literal):
            hit = domain.find(s)
            if hit and len(parent.parent.children) >= 1:
                parent.replace_self(_link(app, docname, hit, nodes.literal('', s)))
            continue
        pieces, pos = [], 0
        for m in CAMEL.finditer(s):
            word = m.group(1)
            if word.startswith('@'):
                hit = domain.find(word, types=('sysvar',))
            elif isl_names.is_prose_linkable(word) or word.lower() not in isl_names.COMMON_WORDS and word[0].isupper() \
                    and re.search(r'[a-z][A-Z]', word):
                hit = domain.find(word, types=('command', 'function', 'event', 'specifier'))
            else:
                hit = None
            if not hit:
                continue
            pieces.append(nodes.Text(s[pos:m.start()]))
            pieces.append(_link(app, docname, hit, nodes.Text(word)))
            pos = m.end()
        if pieces:
            pieces.append(nodes.Text(s[pos:]))
            parent.replace(text_node, pieces)

    # 2. highlighted code blocks
    for block in list(doctree.findall(nodes.literal_block)):
        if block.get('language') != 'isl':
            continue
        html = app.builder.highlighter.highlight_block(block.rawsource or block.astext(), 'isl')

        def repl(m):
            word = m.group(2).replace(' ', '')
            if m.group(1) == 'n' and not word.startswith('@'):
                return m.group(0)
            hit = domain.find(word, types=('sysvar',) if word.startswith('@') else ('command', 'function'))
            if not hit:
                return m.group(0)
            uri = app.builder.get_relative_uri(docname, hit[3]) + '#' + hit[4]
            return f'<a class="isl-autolink" href="{uri}" title="{hit[2]}">{m.group(0)}</a>'

        linked = TOKEN_SPAN.sub(repl, html)
        if 'class="highlight-' not in linked:
            linked = f'<div class="highlight-isl notranslate">{linked}</div>'
        block.replace_self(nodes.raw('', linked, format='html'))


def _ancestors(node):
    while node is not None:
        yield node
        node = node.parent


REFERENCE_PREFIX = '../../skills/micros-isl-language/isl-reference/'
REPO_FILE = 'https://github.com/ltvolks/micros-isl-language/blob/main/'


def rule_links(app, docname, source):
    """source-read: the lint rule pages are written for GitHub (``../../skills/…`` and ``L011.md``).

    ``docs/lint_rules``, ``docs/guide`` and ``docs/reference`` are symlinks, and MyST resolves
    document links through them to paths outside the source tree. Plain HTML links between the
    sibling pages avoid that; the heading anchors are the same GitHub-style slugs
    (``myst_heading_anchors``).
    """
    if docname.startswith('lint_rules/'):
        text = source[0].replace(f']({REFERENCE_PREFIX}', '](../')
        text = text.replace('](../../README.md', f']({REPO_FILE}README.md')
        source[0] = re.sub(r'\[((?:[^\[\]]|\[[^\]]*\])+)\]\(((?:\.\./(?:guide|reference)/)?[\w-]+)\.md(#[^)]*)?\)',
                           r'<a href="\2.html\3">\1</a>', text)


def setup(app):
    app.add_domain(IslDomain)
    app.connect('source-read', rule_links)
    app.connect('doctree-read', read_reference)
    app.connect('doctree-resolved', autolink)
    return {'parallel_read_safe': False, 'version': '1.0'}
