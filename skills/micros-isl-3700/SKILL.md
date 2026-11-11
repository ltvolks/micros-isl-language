---
name: micros-isl-3700
description: Write, review and debug MICROS ISL (SIM scripting) for RES 3700. Use for .isl files, SIM events, TxMsg/RxMsg interfaces, ISL errors.
---

# MICROS ISL (RES 3700)

Target is 3700. Treat 9700 docs as optional: a 9700 function may not exist on 3700. Say so when unsure and flag it for testing.

## Reference
Searchable markdown lives in `isl-reference/` (see `INDEX.md`). Look up before writing; do not rely on memory.

- Command: `grep -n -i -A40 '^## <Name>$' isl-reference/reference/commands.md`
- Event: `.../events.md`; system variable (`@Name`): `.../sysvars.md`; function: `.../functions.md`
- Specifiers: `.../specifiers.md`; key names: `.../keys.md`; error text: `.../errors.md`
- Concepts: `.../guide.md` (2004 guide; the CHM-derived files win on conflict)

If the reference folder is missing, ask for it. Do not guess command syntax.

## Language essentials
- Event-driven: `Event Inq : n`, `Event Tmed : n` (also `*`), `Event RxMsg : id` (also `*`), plus named events (Init, Trans_Cncl, Svc, Tndr_Void, ...). Only Inq/Tmed take numbers. There is no plain `Event Void`. Verify names in events.md.
- `*` events must be last in the file.
- Comments `//`; `\` continues a line.
- Types: `A`/`N`/`$`/`key`; sizes may be expressions; arrays `name[n]`.
- Globals are discarded after each event unless `RetainGlobalVar`. Docs conflict, so test.
- Subs: `sub name(var p : A20, ref r, ref arr[])`. `var` by value, `ref` by reference, arrays only `ref`. Argument count/type mismatch errors. Subs see the caller's variables and globals. First duplicate sub name wins. Nesting limit 32.
- Messaging: `TxMsg` then `WaitForRxMsg` (implicit return, handled by `Event RxMsg : <first field>`) or `GetRxMsg` (inline; reply id in `@RxMsg`; then one `RxMsg`). `RxMsg` targets must be declared. `@Strict_Args` enforces exact field counts. `UseISLTimeOuts` plus `Event RxMsg : _Timeout` handles timeouts.
- Detail arrays are bounded by `@Numdtlt`; type letters in `@Dtl_Type`: I, M, D, S, T, R, C. `@SI` and `@Txbl` have 8 elements.

## Style guide
Follow these when writing or editing ISL. `tools/isl.py` enforces them.
- Indent 2 spaces, no tabs, no trailing whitespace. `event`/`sub`/`if`/`for`/`forever`/`while`/`startprint` bodies indent one level; `else`/`elseif` align with their `if`. A `\` continuation line keeps its offset from the first line.
- Every `event inq : n` has a trailing `// description`; the Sublime symbol list shows it, so inquires are found by name, not number.

      event inq : 1  // Foo the Bar, defiantly
        ...
      endevent

- Document every event, inquire and `sub` with a docstring banner on the line directly above it:

      // *********************************************************************
      // Name
      //   What it does
      //   Arguments / Usage as needed
      // *********************************************************************

- A `*` event (`Inq : *`, `Tmed : *`, `RxMsg : *`) comes after the specific events of its type.
- Max two consecutive blank lines. Keep keyword case as written; do not reformat string or comment text.

Tools live in `tools/` at the root of the repo this skill ships in, i.e. `../../tools/` relative to this file (plugin install or clone), or `Packages/micros-isl-language/tools/` when installed through Package Control. Stdlib-only Python 3.
- `isl.py fmt --write FILE.isl` formats; `--check` exits 1 if a change is needed; `-` reads stdin.
- `isl.py lint FILE.isl` reports `file:line:col: severity LNNN message`; `--fix` formats first. Rules: L001 unknown event or command, L002 unbalanced blocks or `break` outside a loop, L003 `*` event not last, L004 inq without description, L005 missing docstring, L006 duplicate sub or `waitforrxmsg` without `event rxmsg`, L007 reply wait with no timeout handling, L008 whitespace/indent, L009 `call` arity or ref/array mismatch. L001 and L009 "unknown" findings are warnings; check them against the reference.

## Review checklist
1. Every event name and command exists in the reference.
2. Argument counts and types match syntax pages.
3. Every `RxMsg` target is declared; field counts match `@Strict_Args`.
4. `*` events are last.
5. Array indexes bounded (`@Numdtlt`, declared sizes).
6. Variables used across events are retained or re-derived.
7. Sub signatures match call sites (var/ref, arrays).
8. Timeouts handled for every TxMsg wait.
9. Window/ListInput results checked for cancel (`ExitOnCancel`/`ContinueOnCancel` semantics).
10. Format/specifier strings valid per specifiers.md.
11. Anything 9700-only is flagged.
12. `isl.py lint` is clean (or each remaining finding is explained); `isl.py fmt --check` passes.

## Debugging
1. Get the exact error text; grep errors.md.
2. Identify the event and line; reproduce with minimal script.
3. Use `ErrorMessage`/`InfoMessage` tracing; remove after.
4. State what is verified from docs versus what needs testing on the system.

## Output conventions
- Give scripts for Linux/macOS unless Windows is stated.
- Repeatable procedures as markdown steps.
- Cite the reference entry (file + heading) for each non-obvious claim.
