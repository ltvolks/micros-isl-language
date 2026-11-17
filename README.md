# Micros ISL

This repository contains tooling for developers working with the Micros Interactive Scripting Language (ISL) and System Interface Module (SIM).

- Sublime Text Package with support for MICROS RES 3700 ISL (SIM scripts): syntax highlighting, snippets, a symbol list, auto-indent rules, a lint build system and a formatter.
- Claude Code skill: Write, review and debug MICROS ISL (SIM scripting) for RES 3700. Use for .isl files, SIM events, TxMsg/RxMsg interfaces, ISL errors.
- ISL Reference hyperlinked and syntax-highlighted documentation buildable as Sphinx HTML site.
- Standalone Python script for ISL lint and formatting.


## Installing

**Sublime Text (Package Control)**: run *Package Control: Add Repository* with this
repository's git URL, then *Package Control: Install Package* and pick the package
(`micros-isl-language`).  Files ending in `.isl` open with the ISL syntax and 2-space
indentation. The formatter and linter (one tool, `isl.py`) are bundled in `tools/` (system
`python3`, standard library only); no further setup.

Without Package Control, symlink the package from a clone:

```bash
ln -s /path/to/clone/ ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/micros-isl-language
```

**Claude Code skill and reference**: this repository is also a Claude Code
plugin marketplace. The skill (`skills/micros-isl-3700`) and the ISL reference
markdown it uses (`skills/micros-isl-3700/isl-reference`) exist only here:

```
/plugin marketplace add <this repository>
/plugin install isl@isl-language
```

Without plugins, symlink the skill from a clone:

```bash
ln -s /path/to/clone/skills/micros-isl-3700 ~/.claude/skills/micros-isl-3700
```

**Python Package**: Install as a Python package to expose the isl utility for formatting and linting.

```sh
pipx install git+<repo-url>            # standalone command
pipx install git+<repo-url>@v1.0.0     # pinned to a tag

uv add --dev "isl-language @ git+<repo-url>@v1.0.0"
uv run isl lint isl/*.isl
```

**Documentation**

Sphinx docs can be built to provide a hyperlinked, syntax-highlighted site containing a narrative Guide and detailed ISL reference. The source documents are markdown in the `\skills\micros-isl-language\isl-reference` directory

The Guide is derived and reformatted from System Interface Module (SIM) Companion Guide, 3rd edition 2003. The reference is derived from RES 3700 SIM Online Help (CHM).

The lint rule pages in `tools/lint_rules` are included through the `docs/lint_rules` symlink.

The site is published to GitHub Pages by `.github/workflows/docs.yml` on every push to `main`. https://ltvolks.github.io/micros-isl-language

To build the docs:

```bash
pip install -r docs/requirements-docs.txt
make -C docs html          # open docs/_build/html/index.html
```

Other Sphinx projects can link to it with intersphinx: point a mapping at the built site (a path or
URL) and use either std labels, `` :ref:`TxMsg <isl:cmd-txmsg>` ``, or, with `docs/_ext` on `sys.path`
and the `isl_domain` extension enabled, `` :isl:cmd:`isl:TxMsg` ``, `` :isl:sysvar:`isl:Cknum` ``,
`` :isl:event:`isl:Inq` `` and `` :isl:fn:`isl:Mid` ``.

## Features

- **Symbol list** (`Cmd+R`): events, inquires and subs. Inquires with a
  trailing comment show as `Inq 1 - Foo the Bar`; others as `Tmed 300`,
  `RxMsg callback`, `Event Init` and `- subname`.
- **Snippets** (`inq`, `tmed`, `rxmsg`, `sub`, `doc`, `txmsg`, `getrxmsg`,
  `ifelse`, ...). `inq`, `tmed` and `sub` include the docstring banner.
- **Indentation rules** so Sublime auto-indents blocks the way the formatter does.
- **ISL: Format** (command palette): re-indents the file via `tools/isl.py fmt`.
  With a selection, only the selected lines are re-indented (using the context of
  the whole file). Set `"isl_format_on_save": true` in `ISL.sublime-settings` to
  run it on save.
- **Build (Cmd+B) / ISL: Lint**: runs `tools/isl.py lint`; errors are clickable.
  With a selection, only findings on the selected lines are shown. The "Lint and
  Fix" variant re-formats the whole file first.

## Command line

```bash
tools/isl.py fmt --check|--write FILE.isl    # formatter, "-" for stdin
tools/isl.py fmt --lines 10-25 FILE.isl      # only lines 10..25
tools/isl.py lint [--fix] [--format json] [--strict] [--lines A-B] FILE.isl
```

Set `isl_tools_path` / `isl_python` in `ISL.sublime-settings` to use another
copy of the tools or interpreter.

### Lint rules

Every finding carries a rule code (`L001` ... `L037`). [tools/lint_rules](tools/lint_rules/index.md) has one
page per rule: what it checks, why (linked to the Guide or Reference passage it comes from), and a failing and
a passing example. The pages are part of the Sphinx site and are not shipped in the Sublime package.


## Development

`ISL.JSON-tmLanguage`, `ISL.tmLanguage` and `Symbol List.tmPreferences` are
generated from the linter's vocabulary; do not edit them by hand:

```bash
python3 tools/gen_isl_grammar.py
```

Tests need pytest, and the docs tests also need the docs requirements.

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]' -r docs/requirements-docs.txt
.venv/bin/python -m pytest tests
```

To update the SublimeText package:

- Tag releases as `v1.0.0` etc. so Package Control installs versions.
- Add a release note in `messages/1.0.0.txt`
- Update `messages.json`

## Style Guide

Your code will be easier to read and easier to work with if you follow these
simple guidelines. `tools/isl.py` enforces them.

### Indentation

Two spaces, no tabs, no trailing whitespace. Bodies of `event`, `sub`, `if`,
`for`, `forever`, `while` and `startprint` indent one level; `else`/`elseif`
align with their `if`.

### Inquires

Inquires should contain a trailing comment with a description. This will display
in the symbol list, allowing you to jump quickly to named inquires without
committing the inquire numbers to memory.

```isl
event inq : 1  // Foo the Bar, defiantly
...
endevent
```

### Docstrings

Use a docstring format to document events, inquires, and subroutines. The banner
goes on the line directly above the declaration.

```isl
// *********************************************************************
// Docstring
// *********************************************************************
```

### Wildcard events

A `*` event (`Inq : *`, `Tmed : *`, `RxMsg : *`) comes after the specific events
of its type.
