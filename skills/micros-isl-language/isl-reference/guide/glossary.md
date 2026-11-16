# Glossary

## Argument

An Argument is a generic term for an item, or group of items, that is used in the syntax of a command, that refers to the information that is required by the command. It may be an alphanumeric character, group of characters, or word(s) that receive the action of a command or function. For example, the Call command requires an argument (i.e., the variable name) in order to work.

See also: Array; Constant; Equation; Expression; Function; Input Expression; Prompt Expression; String Expression; Syntax; System Variable; and User Variable.

## Array

An Array is a set of values, based on the name of a User Variable. A User Variable Array (or Array Variable) identifies each value by the variable name and the index number, in brackets. For example, an Array called Rooms that has 20 values would be identified from Rooms [1] to Rooms [20].

See also: User Variable.

## Asynchronous Serial Interface

An Asynchronous Serial Interface is a full duplex interface supporting transmission speeds of 300 to 9600 baud.

## Concatenate

Concatenate means to join two or more text strings together to form a single contiguous string.

## Constant

A Constant is a value that does not change (the opposite of a variable). For example, the Window command can use a constant (i.e., window 5, 36).

See also: Expression; Variable.

## Encryption

The ISL Encryption Program is a utility that converts a script into an encrypted (hexadecimal) format. It is used as a security precaution for proprietary information.

## Equation

An Equation is a mathematical formula. The ISL may use the following operators within a formula: addition (+), subtraction (-), division (/), multiplications (*), greater than (>), or less than (<). Parentheses may be used to isolate parts of the equation, as necessary.

See also: Expression; Formula; Operator.

## Expression

An Expression is a place holder argument that can be one of the following:

User Variable System Variable Constant String Function Equation

See also: Argument; Hex Expression; Input Expression; Numeric Expression; String Expression.

## Format Specifiers

See: Operators.

## Formula

A Formula can be used to calculate numeric values, compare one value to another, and select an action based on a comparison, and join multiple string expressions into a single string. The ISL may use the following operators within a formula: addition (+), subtraction (-), division (/), multiplications (*), greater than (>), or less than (<). Parentheses may be used to isolate parts of the equation, as necessary.

See also: Equation; Operator.

## Function

A Function is a built-in ISL procedure used to evaluate fields, make calculations, or convert data.

See also: Expression.

## Global Commands

Global Commands are those commands that are allowed outside of an Event procedure. They are initialized at the beginning of each script and then maintained for the duration of that script. The following ISL commands are global:

ContinueOnCancel DiscardGlobalVar ExitOnCancel Prorate RetainGlobalVar SetSignOnLeft SetSignOnRight UseCompatFormat UseISLFormat UseISLTimeOuts UseSTDTimeOuts Var

See also: Local Commands.

## Global Variable

A Global Variable is declared outside an Event procedure, and usually initialized at the beginning of each script. The value of each global variable is maintained throughout all Events, unless the script is changed or the DiscardGlobalVar command is used.

See also: Local Commands.

## Hex Expression

A Hex Expression is a variable or function whose value must be a hexadecimal number. This variable is used with the GetHex and Bit functions.

See also: Expression.

## Input Expression

An Input Expression is an Array or User Variable that requires user input. The input expression is used by the DisplayInput, DisplayMS, Input, and InputKey commands.

See also: Array; Expression; User Variable.

## Interface Script Language (ISL)

See: SIM.

## Integer

An Integer is a positive or negative whole number or a zero, always without decimal places.

## ISL

See: SIM.

## Language Element

Language Elements are indivisible pieces of information which, if broken apart with whitespace, will generate an ISL error. The following items are considered language elements:

Command Names Function Names System Variables Relational and Boolean Operators Input and Output Specifiers Comment Symbols (//) Continuation Line Symbol (`\`) Commas Any Word and/or Symbol required by the Syntax

## Local Commands

Most ISL commands are considered Local Commands, in that they must be placed inside an Event procedure and only affect the processing within that Event.

See also: Global Commands.

## Local Variable

A Local Variable must always be declared inside an Event procedure, and will only be used by the Event and any subroutines called by that Event. Local variables are purged after each Event is complete, (when an EndEvent is executed).

See also: Global Variables.

## Nesting

Nesting is the act of using an If, For, Forever, or While command inside another. Since each of these commands is executed until its corresponding EndIf, EndFor, or EndWhile command is found, the entire If...EndIf, For...EndFor, ForEver...EndFor, or While...EndWhile nest must exist before the outer End... command. Nesting also refers to the ability to call a subroutine from within another subroutine.

## Null String

A Null String (" ") is a string expression that contains no characters. All string variables are initially set to null at the beginning of each Event procedure.

See also: Expression; Variable.

## Number of Records

Number of Records is used to send and receive variable amounts of data via a list or a list array.

## Numeric Expression

A Numeric Expression is a variable or function whose value must be a number. A
number expression is used when specifying a touchscreen number within the 3700
database.

See also: Expression.

## Offset

An Offset is a decimal integer that is used to calculate a position of a field within a string. For example, this may be used to extract certain field information from a credit card.

## Operator

1. An Operator is an employee who is privileged to place orders and/or control guest checks. Each operator maintains their own set of sales totals. Examples of operators include waiters or other order takers who record sales.

2. An Operator is a mathematical symbol that determines what action is taken on variables or constants in the equation.

See also: Equation; Formula.

## Prompt

A Prompt is a string expression which is displayed in the prompt line of the System Unit display. The prompt is used to instruct the user regarding a required action.

## Script

A Script contains a series of commands, functions, and arguments that perform a particular task at the UWS and/or the PMS.

## SIM

The 3700 System Interface Module (SIM) is a software module that allows the 3700 to interface with a variety of other data systems, including sophisticated Property Management Systems (PMS), automated delivery systems, and other electronic database systems.

SIM uses an Interface Script Language (ISL), which allows the interface designer to invoke touchscreens, direct operator prompting, define interface message formats and subsequent 3700 System processing, and execute keyboard macros on a UWS.

## String

A String is a series of connected characters (letters, numbers, symbols, spaces) stored and used as text. In ISL, a string is always in quotes.

See also: Subroutine; User Variable.

## String Expression

A String Expression is a variable or function whose value must be a string.

See also: Expression.

## Subexpression

A Subexpression is an expression within an expression. Subexpressions are used with binary operators. For example in the following expression: a + (b + c) + d, (b + c) is a subexpression.

See also: Expression; Operators.

## Subroutine

A Subroutine allows common code to be used by multiple events. Each subroutine has a unique name which is used to define it within the script, outside any Event procedure. Use the Call command to execute a subroutine.

## Syntax

A command or function Syntax is used to show the proper usage and rules that are required to execute it correctly within a script.

## System Interface Module

See: SIM.

## System Variable

A System Variable is a predefined name that identifies a value which contains information from the 3700 database.

See also: Argument; Expression.

## Token

A Token can be any individual language element inside a script.

See also: Language Element; Token Error.

## Token Error

A Token Error can occur any time an individual language element is usedincorrectly. For example, incorrect use of whitespace, missing commas, or erroneous data at the end of a command statement, etc.

See also: Language Element; Token.

## User Variable

A User Variable is a user-defined name which is assigned a value within a script. The value will remain the same until a newer value is assigned; if no newer value is assigned, the original value is maintained.

See also: Argument; Expression.

## Variable

A Variable is a container whose value changes (the opposite of a constant).

See also: Constant.
