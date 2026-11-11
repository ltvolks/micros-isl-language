# Micros ISL

Sublime Text support for MICROS RES 3700 ISL (SIM scripts): syntax highlighting,
snippets, a symbol list, auto-indent rules, a lint build system and a formatter.

## Installing

**Sublime Text (Package Control)**: run *Package Control: Add Repository* with this
repository's git URL, then *Package Control: Install Package* and pick the package
(`ISL-language-sublime`). Tag releases as `v1.0.0` etc. so Package Control
installs versions. Files ending in `.isl` open with the ISL syntax and 2-space
indentation. The formatter and linter (one tool, `isl.py`) are bundled in `tools/` (system
`python3`, standard library only); no further setup.

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

## Development

`ISL.JSON-tmLanguage`, `ISL.tmLanguage` and `Symbol List.tmPreferences` are
generated from the linter's vocabulary; do not edit them by hand:

```bash
python3 tools/gen_isl_grammar.py
```

Tests: `python3 -m pytest tests`.

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
