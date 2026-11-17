# ISL lint rules

Every finding of `isl.py lint` carries a rule code. Each code has a page that says what is checked, why (with a link to the passage of the Guide or Reference it comes from), and a failing and a passing example. Errors are things ISL itself rejects; warnings are style rules or heuristics that can have exceptions.

| Code | Rule | Severity |
| --- | --- | --- |
| [L001](L001.md) | Unknown event, command or malformed event line | error / warning |
| [L002](L002.md) | Unbalanced blocks | error |
| [L003](L003.md) | Wildcard event before specific events | error |
| [L004](L004.md) | Inquire without a description | warning |
| [L005](L005.md) | Missing docstring banner | warning |
| [L006](L006.md) | Duplicate sub, or WaitForRxMsg without handlers | warning / error |
| [L007](L007.md) | Waiting for a reply without timeout handling | warning |
| [L008](L008.md) | Whitespace and indentation | warning |
| [L009](L009.md) | Call arguments do not match the sub | error / warning |
| [L010](L010.md) | Invalid or reserved name | error |
| [L011](L011.md) | Malformed variable declaration | error |
| [L012](L012.md) | Whitespace inside a language element | error |
| [L013](L013.md) | Misused line continuation | error |
| [L014](L014.md) | Sub inside an event, or event inside a sub | error |
| [L015](L015.md) | Return in an event | error |
| [L016](L016.md) | User input in Event Init or Event Exit | warning |
| [L017](L017.md) | Window protocol | error / warning |
| [L018](L018.md) | Printing outside StartPrint | warning |
| [L019](L019.md) | Print session errors | error / warning |
| [L020](L020.md) | TxMsg without a reply wait | warning |
| [L021](L021.md) | SaveRefInfo outside Event Tmed | warning |
| [L022](L022.md) | System variable misuse | error / warning |
| [L023](L023.md) | For loop errors | error |
| [L024](L024.md) | Sub parameter list errors | error |
| [L025](L025.md) | Malformed sub or call line | error |
| [L026](L026.md) | Invalid event id | error |
| [L027](L027.md) | Prompt text too long | warning |
| [L028](L028.md) | Variable used but never declared | warning |
| [L029](L029.md) | Duplicate variable declaration | error / warning |
| [L030](L030.md) | Command outside a procedure | error |
| [L031](L031.md) | Literal too large for its variable | error |
| [L032](L032.md) | List and array index errors | error |
| [L033](L033.md) | Statement shape | error |
| [L034](L034.md) | Operator errors | error / warning |
| [L035](L035.md) | Function errors | error / warning |
| [L036](L036.md) | Input needs a variable | error |
| [L037](L037.md) | Touchscreen displayed with no keys | warning |
