# Chapter 6: ISL System Variables

This chapter contains guidelines to follow when specifying system variables.

## System Variables

System variables return status information from the 3700 RES System or the PMS System, etc., as well as provide you with access to transaction totals and other transaction parameters.

- Using the system variables that the ISL supports, you can:
- Access the system transaction variables and totals information and
- Set certain operational parameters.

Specifying System Variables If this is the first time that you have used ISL system variables, review this section to determine the quidelines to follow when specifying system variables. A detailed description of each system variable in alphabetical order and in order by category of function is provided in SIM Online Help.

## Specifying System Variables

### Guidelines for Specifying System Variables

This section contains quidelines that you should follow when specifying system variables in ISL statements.

- Follow the guidelines below when specifying system variables:
- Since the names for system variables are reserved, do not declare other user variables using the same name.

The example below is incorrect because the local variable ccnumber has the same name as the system variable @CCNUMBER, which returns a credit card account number.

```isl
event : 1
var ccnumber : A16
// This problem can be corrected by replacing ccnumber with account_num, which is a user variable that represents the credit card account number, but is not a system variable.

event : 1
var account_num : A16 . . .
```

- Always precede each system variable with an At @ character. Example: @SI[1]
- Never put spaces between the At @ and the system variable name.

Correct: `@SI[ 1 ]`
Incorrect: `@ SI[ 1 ]`

## Using an Index to Specify System Variables

- Before using a system variable, review the detail description carefully for any special considerations.

-The majority of system variables must be used in conjunction with other commands, functions, or other system variables. For instance, the @DWON system variable can only be used with the Printline command.

-Some system variables are only valid within a certain event. For example, @CCNUMBER and @CCDATE will only return valid values if issued from within a tender/media event referencing a credit card tender type.

-You may or may not be required to place a system variable strategically within the script. For example, the @WARNINGS_ARE_FATAL system variable must be placed at the top of the script. But the @LINES_EXECUTED system variable can be placed anywhere in a script.

o Just as there are user variables that you can specify as arrays, there are array system variables. Array system variables require that you reference an array index. “Using an Index to Specify System Variables” on page 6-4 describes how to issue these types of system variables.

Specifying array system variables is the same as specifying user-declared array variables. Array references in ISL take the form:

`<array name> [ <expression> ]`

where `<array name>` can be either a user or system array variable, and `<expression>` (i.e., the index) can be a user variable (integer), another system variable, a constant, a function, or an equation.

```text
As long as the array index evaluates to an expression within the array limits for the
system variable, you can specify the index as a user variable, another system variable,
a constant, a function, or an equation. In the following examples, three different
references evaluate to 3:
    @si[ 3 ]                  // constant
    @si[ 6 - 3 ]              // equation
    @si[ ( index * 2 ) - 1 ]// equation using user
    variable,
                              // where index = 2
Array Subscripts
    The difference between system array variables and user-declared array variables, is
    that system array variables already have been declared and filled with the
    corresponding information. Consequently, there is no need to declare the subscripts of
    the array.
    For example, the user-declared array variable must be declared as follows:
        var myarray[5] : A20
                myarray[1] = “mytest”
                myarray[2] = “mytest”
                myarray[3] = “mytest”
                myarray[4] = “mystes”
                myarray[5] = “mytest”
```

But a system array variable can be specified as: @si[3]

For a system array variable, the variable data type and size, and subscript are assumed by the ISL to reference Sale Itemizer #3. If executed by a script, this system array variable would return the totals posted to this sales itemizer on the current guest check.

```text
Array Index Limits
    We include the array index limits for system variables with the detail description of
    each system array variable. These limits vary depending on the system variable.
    If you exceed the array index limit when referencing the system variable, an error will
    occur. For example, below are invalid limits for the @SI system array variable:
        @si[10]                     //incorrect
        @si[-10]                    //incorrect
```

The array index for @SI must evaluate to an index between 1 and 8.

All array indices start at 1, and not 0. For example, @si[0] will generate an error.

Embedded Index vs Array-Index System variables that require an index (e.g., DTL_*, @SI, etc.) can be referenced in two ways: by an embedded index or array-index. Both of these methods enable older versions of SIM scripts to maintain compatibility with the ISL. In early versions of the ISL, there was support only for the embedded index method.

If you are using the embedded index to maintain older SIM scripts, the desired index is placed immediately after the system variable.

Example: @SI2, @TAX1, @TXBL1, @DTL_STATUS9

Example: @SI[ 2 ], @TAX[ 1 ], @TXBL[ 1 ], @DTL_STATUS[ 9 ]

> **Note:** The embedded-index method remains in ISL to retain compatibility with older scripts and should not be used with new scripts.
