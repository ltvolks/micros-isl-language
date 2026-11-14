"""Sphinx domain ``isl``: commands, events, functions, system variables, ...

* ``.. isl:command:: Break`` (etc.) registers an entry; the generator emits one per section.
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
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_refnode

sys.path.insert(0, str(Path(__file__).resolve().parent))
import isl_names  # noqa: E402
from isl_names import PRIORITY, TYPES  # noqa: E402


class IslMarker(SphinxDirective):
    """Registers the entry for the enclosing section (renders nothing)."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {'anchor': directives.unchanged_required}

    def run(self):
        objtype = self.name.split(':')[-1]
        name = self.arguments[0].strip()
        anchor = self.options['anchor']
        domain = self.env.get_domain('isl')
        domain.note_object(objtype, name, anchor, self.env.docname)
        label = TYPES[objtype][3]
        index_node = addnodes.index(entries=[('single', f'{name} ({label.lower()})', anchor, '', None)])
        return [index_node]


class IslDomain(Domain):
    name = 'isl'
    label = 'ISL'
    object_types = {t: ObjType(v[3], v[2]) for t, v in TYPES.items()}
    directives = {v[1]: IslMarker for v in TYPES.values()}
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


# ---------------------------------------------------------------- auto-linking

CAMEL = re.compile(r'(?<![\w@])(@\s?[A-Za-z_]\w*|[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+|'
                   r'[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)(?![\w])')
SKIP_PARENTS = (nodes.reference, nodes.literal_block, nodes.title, nodes.raw, addnodes.desc_signature,
                nodes.strong, nodes.rubric, nodes.term)
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


def setup(app):
    app.add_domain(IslDomain)
    app.connect('doctree-resolved', autolink)
    return {'parallel_read_safe': False, 'version': '1.0'}
