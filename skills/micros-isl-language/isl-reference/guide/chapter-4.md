# Chapter 4: Using Variables

This chapter contains a description of the data types and operators supported by the ISL, and an introduction to user variables.

## Variables and ISL

As in other programming languages, the ISL supports the use of variables for holding information, such as integers or character strings, that may change from from one ISL event to another.

Typically, variable results are stored in expressions like the following example:

```isl
variable_name = expression
```

An expression is a combination of variables and operators. Expressions may also include constants and functions.

For example, in the expression below, the size of a window is computed from the number of elements in a list:

```isl
window_length = ListSize + 2
```

The user variable window_length has a unique name defined by you, the user. The expression on the right contains a user variable called ListSize, which is added to the integer 2. The result of the expression on the right will be the value assigned to the user variable window_length: the ListSize plus 2.

In this chapter, we describe how to use the language elements that allow you to hold variable information and evaluate expressions of variables.

- This chapter contains the following:
- A listing of the different kinds of data types supported by ISL
- A discussion of the mathematical operators you can use to evaluate expressions containing variables
- A discussion of the type of user variables supported by the ISL

## Data Types

The ISL supports several kinds of data types, including numeric, decimal, alphanumeric, and key data types, to specify different kinds of variables and constants.

When a variable is declared using the Var1 command, its data type and size must also be declared. The type and size are referred to as the variable_specifier and type_specifier, respectively.

The table below lists the different kinds of data types and provides the abbreviations you must use when declaring them.

```text
Data Type       Abbreviation                   Description                        Example
Numeric                 Nx         These variables are used for numeric       var rowcnt : n3
                                   information and may comprise x digits
                                   (integers, not decimal), e.g., N4
                                   supports -9999 to 9999.
Decimal                 $x         These variables are used for decimal       var new_ttl :
                                   amounts. Operator entries will             $12
                                   assume a decimal place according to
                                   the currency's default setting, as
                                   specified in the System|Restaurant
                                   form for the base currency and the
                                   Sales|Currency form for foreign
                                   currencies; i.e., entering 1234 in the
                                   US will result in an amount of 12.34.
                                   They may comprise x digits, e.g., $4
                                   in the US will support -99.99 to 99.99.
Alphanumeric            Ax         These variables may include any non-       var name : a20
                                   control character, including
                                   punctuation marks. They may
                                   comprise x characters.
Key                     key        This system variable is used for key       var keypressed : key
                                   press variables.
```

The examples below declare a 32-character alphanumeric variable and a four-digit room number variable, respectively.

```isl
event inq : 1
   var message_text : A32
   var room_num : N4
endevent
```

## Relational and Logical Operators

### Unary Operators

The mathematical operators described in this section are supported by the ISL. Before using these operators in a script, review each description carefully, as well as the “Operator Rules” on page 4-8.

For an explanation of the operand types (Nx, $x, Ax, and Key), please see “Data Types” on page 4-3.

#### There are two unary operators

```text
Operator         Description                           Example
             Negation operator (a    -3
             minus sign). This is
-            used to negate an       -count
             expression.
                                     -( (     count + 5     )   *   -index       )
              Will negate the         The NOT operator will negate the result of the
              result of the           expression. For example, the following
              expression. The         expression is always TRUE:
              NOT operator can
              be applied to           ( 3 < 4 )
NOT           expressions in the
              same way as the         The NOT operator will negate the sense of the
              unary minus             above expression; thus the following
              operator.               expression is always FALSE:

                                      NOT ( 3 < 4 )
```



Given that ISL expressions are true if they evaluate to a non-zero value, and false if they are zero, the NOT operator will change non-zero values to 0 and 0 values to non- zero. The expression NOT 3 is valid and will evaluate to a 0.

The NOT operator is generally used in If, ElseIf, and While statements to control program flow.

The following example is a subroutine of a loop that executes until the variable done becomes true.

```isl
sub get_id( ref id )
  var done : N3 = 0
  while NOT done
    input id, "Enter id"
    if id > 0 AND id < MAX_ID
      done = 1
    else
      errormessage "Not Valid"
    endif
  endwhile
endsub

```

### Binary Operators

The following table lists the available binary and logical operators in order of precedence (highest to lowest); AND and OR, the logical operators, have a lower precedence than all the binary operators;


| Operation             | Operator | Allowable Operand<br/>Types: Nx, $x, and Ax |
| ---- | ---- | ---- |
| multiplication        |  *       |     Nx, $x      |
| division              |   /      |     Nx, $x      |
| modulus               |  %       |     Nx, $x      |
| plus                  |  +       |     Nx, $x      |
| minus                 |   -      |     Nx, $x      |
| bit-wise and          |  &       |       Nx        |
| bit-wise or           |  \|      |       Nx        |
| equality              |  =       | Nx, $x Ax, Key  |
| greater than or equal |  \>=      | Nx, $x, Ax, Key |
| greater than          |  \>       | Nx, $x, Ax, Key |
| less than or equal    |  <=      | Nx, $x, Ax, Key |
| inequality            |  <>      | Nx, $x, Ax, Key |
| less than             |  <       | Nx, $x, Ax, Key |
| logical and           | AND      |       Nx        |
| logical or            | OR       |       Nx        |


### Operator Rules

#### Relational Operators

All relational operators produce a non-zero value if they are true, and 0 if they are false. For example:

```isl
result = 1 < 2//true, result will be non-zero

result = 100 < 4//false, result will zero
```

#### Logical (Boolean) Operators
The logical (Boolean) AND and OR operators treat their operand as either true (non- zero) or false (zero) values. For example: Fix These

```isl
result = 5 AND 6 //true, since 5 and 6 are both non- zero

result = 5 AND 0//false, since 0 is false

result = 0 OR 0//false, since neither one is true

result = 0 OR 5//true, at least one value is non-zero
```

#### Precedence
ISL expression operands are evaluated from left to right until the end of the expression is reached. For example, note the following expression:

`1 + 5 + 2`

This evaluates to 8.

When expressions mix operators (i.e., `+` and `*`), then ISL will use the precedence table to determine which subexpression within the expression will evaluate first. In the following example, the * operator has higher precedence than the + operator, therefore, the last two operands will be combined first, even though they are not the first in the expression:

`1 + 5 * 2`

The result is 11 (1 + 10), rather than 12 (6 * 2). The precedence rules are used for all operators. Note the following example:

`a < 1 OR b > 3`

Since the < operator has greater precedence than the OR operator, `a < 1` and `b > 3` are evaluated first, and both results are combined with the OR operator.

#### Overriding and Clarifying Precedence
You can use parentheses to override the default precedence rules. Parentheses are used for two reasons:
- To override the default expression evaluation
- To clarify the expression

Subexpressions enclosed in parentheses always override the operator evaluation. For example, note the following expression:

`(1 + 5) * 2`

The `1 + 5` is evaluated first since it is within parentheses, even though the multiplier `*` has higher precedence.

The following expression

`a < 1 OR b < 3`

can be rewritten as:

`(a < 1) OR (b < 3)`

It is good practice to always place parentheses around subexpressions, to reduce programming errors and to make scripts easier to understand and maintain.

For example, the following expression

`offset + width * 2 <= w_width / stlen + 1`

is equivalent to:

`(offset + (width * 2) ) <= ( ( w_width / stlen) + 1)`

The second expression is clearer.

## User Variables

### Declaring User Variables

User variables are defined by you, the interface designer, and may be used to get operator input, such as customer name and address information, a room number, etc.

They can also reference an entry in a message received over a SIM Interface.

Use the Var command to declare user variables. These variables are given a value by an operator, or by the interface, in a response message. Example:

```isl
event inq : 5
var rowcnt : n3 . . .
```

#### Guidelines
- The variable name must begin with a letter A-Z, a-z, or the underline character (_).
- The first character cannot be a number. It may subsequently include any character in the range A-Z, a-z, 0-9, or the underscore _ character.
- String variables will initially equal a null string " ".
- Numeric variables will initially equal a 0.

### Local and Global Variables

Variables can be declared either globally or locally.

#### Global Variables
If a variable is declared outside of an Event procedure, it is considered global. The variable is called global because it can be referenced by any event or subroutine in the script. As a result, the ISL must maintain the contents of the variable the duration of a script. The variable is then reset at the start of a new transaction (i.e., when tendering a check). Also, since the variable will be used by other events and subroutines in the script, you only need to declare a global variable once, at the top of the script, before any events or subroutines. Please refer to the Retain/Discard Global Variable command in SIM Online help.

#### Local Variables
Conversely, a variable is considered local when it is declared inside an event procedure. Local variables are only maintained while the event procedure is being executed; executing the EndEvent command, or any other command that stops the script, purges the local variable from the event procedure. Thus, you must declare local variables within event procedures.

**Local Variables Used by Subroutines**
Local variables declared by a parent event procedure are visible within a child subroutine. This functionality is possible because a local variable is accessible to the event in which it is included, and to any child subroutine called by the parent event. Moreover, the contents of a local variable, declared in the parent event, can be changed by the operation of a subroutine called by the same parent event. Consequently, the new contents of the local variable are retained when the subroutine is complete.

### Array Variables

Arrays of variables can also be declared by including an array size with the declaration. The syntax for an array variable is:

```isl
var variable_name[array_size]:variable_specifier
```

The example below declares an array of strings named message_text, containing eight elements, each 32 characters in length.

```isl
var message_text[8]:A32
```

> **Note:** The use of brackets in the example above does not denote an optional entry, but is actually part of the system.

For more information on the Var command, please see the SIM Online Help.

### Variable Size Variables

It is possible to declare a variable with a size that is defined by an expression, rather than a hard-coded number. If the SIM encounters an open parenthesis immediately following the type of the variable, it will assume that an expression follows, defining the variable’s size. For example, the following commands have the same effect:

```isl
var window_width : N30

var window_width : N(15 + 15)
```

This feature is useful for declaring variables whose size is not known until run-time. Example:

```isl
var : a(str_len)
```

### Using List Arrays and Records

The application data message contains the information that the SIM sends to and receives from a PMS. The message consists of a set of ASCII fields, separated by the ASCII field separator (1CH).

In many cases, the number of variables to be sent by the SIM or the PMS is not known until run-time. For example, a script may query the PMS for a list of guests whose last name starts with “SMITH”. The PMS may respond with two names, or with ten names, depending on who is in the hotel at the time.

In order to send and receive variable amounts of data, ISL uses two methods: list arrays and records.

#### List Arrays
The SIM provides more than one method for sending and receiving variable amounts of data within one message. The simplest method is to send a list. A list consists of a list_size and the array_variable that contains the list. The list_size is any user-defined integer variable. The array_variable is any user-defined array (see Array Variables).

**Specifying a List Array**
A list is specified for an RxMsg or TxMsg command by using empty array brackets ( [] ) after the array name.

Example: `Rxmsg list_size, list[]`

When specifying a list array, follow these guidelines:
- The variables used for the list size and the list are user-defined.
- The list size variable should always precede the list array variable.
- Array system variables (e.g., `@DTL_OBJNUM`) cannot be used as list arrays.
- The values in the list[ ] should be formatted into as many lines as are specified in list_size. In the example below, list_size is 5, thus five values from the list[ ] will be formatted if these ISL statements are executed.

```isl
var list_size : N5
var list[ 10 ] : A20
txmsg list_size, list[]
```

- Using the same example, if we let the [fs] symbol stand for the field separator and the message from PMS is: `5[fs]L1[fs]L2[fs]L3[fs]L4[fs]L5` then:

```isl
listsize = 5
list[ 1 ] = "L1"
list[ 2 ] = "L2"
list[ 3 ] = "L3"
list[ 4 ] = "L4"
list[ 5 ] = "L5"
```

- The PMS should read the first value in the message and receive that many elements from the rest of the message. The RxMsg command reads the data from the message in a similar manner. For example:

```isl
var listsize : N5
var list[ 10 ] : A20

rxmsg listsize, list[]
```

If message from PMS is: `2[fs]L1[fs]L2`,then:

```isl
listsize = 2
list[1] = "L1"
list[2] = "L2"
```

If message from PMS is: `4[fs]L1[fs]L2[fs]L3[fs]L4`, then:

```isl
listsize = 4
list[1] = "L1"
list[2] = "L2"
list[3] = "L3"
list[4] = "L4"
```

In another example, the script collects a guest name from the operator, transmits the guest name to the PMS, receives a list of names from the PMS, and displays the list in a window:

```isl
event inq : 1
  var name : A20
  input name, "Enter guest name"
  txmsg "GST_INQ", guest
  waitforrxmsg
endevent

event rxmsg : GST_RSP
  var guest_count : N5   //declare list size var guest_name[10] : A20   //declare list //receive up to 10 names rxmsg guest_count, guest_name[]

  //open up window
  window guest_count, 25, "Guest List" listdisplay 1, 1, guest_name //display names
  waitforclear
endevent
```

- Lists can be intermingled with other non-list variables, as well as other lists. In the following example, one single variable and two lists, each with its size variable, are received from the PMS:

```isl
rxmsg status, guest_count, guest_name[],\
      action_count, action_list[]
```

For each list, only one array may be assigned. It is possible, for example, for the PMS to send not only the guest name, but also the room number. One way to handle this would be to receive two lists within one message:

```isl
event rxmsg : GST_RSP
  var guest_count : N5
  var guest_name[10] : A20
  var guest_room[10] : N5
  rxmsg guest_count, guest_name[], guest_count,\
        guest_room[]
  .
  .
endevent
```

**Implicit List_Sizes**

There are occasions where the script writer may desire to use lists, but does not want to actually specify the list_size, since the list_size is not specified in the data. For example, assume that a PMS message contains 20 fields. In order for the ISL to read the message, a separate variable must be specified in the Rxmsg command for each field.

```isl
var n[20] : n5

rxmsg n[1], n[2], n[3], n[4], n[5], n[6], n[7],\ n[8],\n[9], n[10], n[11], n[12], n[13], n[14], n[15],\ n[16], n[17], n[18], n[19], n[20]
```

The ISL provides a method for specifying list_sizes implicitly for those cases when the data does not contain a list_size. An implicit list_size is identified by a pound symbol (#) placed before the list_size. Alternatively, the example above could be written as:

```isl
var n[20]
rxmsg #20, n[]
```

Only integer expressions may be placed in the implicit list_size field. Integer variables may also be used.

```isl
var size : n2 = 20
var n[size] : n5
rxmsg #size, n[]
```

Implicit list_sizes may be used anywhere standard list_sizes may be used.

#### Records

ISL also provides a more powerful, yet more complicated, syntax for specifying variable amounts of data called records. In this format, the variables following the list size are considered to be in groups of records. The syntax for receiving this type of information is:

```isl
listsize, list1[] : list2[] : list3[] ...
```

The colon separates fields within a record and must be used when specifying records.

For example, if the PMS received an inquire on SMITH, then it may want to group the data as follows:

`3[fs]Smith[fs]1423[fs]Smithers[fs]1827[fs]Smithson[fs]1887`

Note that each record consists of a name followed by a room number.

To receive the message above, use the following statement:

```isl
rxmsg count, name[] : room[]
```

In this case, the variables would be set as follows:

```isl
count = 3
name[1] = "Smith"
name[2] = "Smithers"
name[3] = "Smithson"
room[1] = 1423
room[2] = 1827
room[3] = 1887
```

The same format would be used for transmitting data.

A list specification is a special case of a record format, where each record consists of one element.

### Promotion

ISL allows the programmer to freely combine and assign variables of the different types. For example, it is possible to add a string and an integer, and assign it to a decimal value.

```isl
var amt : $10 amt = 12 + "25" + 100.45
```

Whenever two variables and/or constants are operated upon with an operator, and they are not the same types, one will be “promoted” (have its type changed) before the operation takes place.

Strings promote to integers and integers promote to decimal values. A final promotion occurs when the expression is assigned to a variable. Therefore, the expression is promoted (or demoted) to the variable type.

For example, if the following variables are declared

```isl
var string : A20
var integer : N10
var decimal : $10
```

Then the following statements are assigned within an Event procedure, the statements would be equivalent to:

| Assignment | Equivalent To |
| --- | --- |
| string = "12" + 35 | string = "47" |
| string = "14.15" + 2 | string = "16" |
| string = "14.15" + 2.00 | string = "16.15" |
| integer = "14" + 12.5 | integer = 26 |
| integer = "14.5" + 12.5 | integer = 27 expression was real, and then demoted to integer |
| decimal = 12.23 + 1 | decimal = 13.23 |
| decimal = "12.23" + 1 | decimal = 13.00 "12.23" + 1 yields an integer 13, which is then assigned to decimal |

Strings are converted to integers by using the first digits in the string field. “12.35” converts to an integer 12, since “.” does not belong in an integer. “12NUM” also converts to 12. Therefore, it is legal to write:

```isl
integer = "ABC123"// integer = 0
```

Only relational operators are allowed between strings; see “Relational and Logical Operators” on page 4-5.

Correct:

```isl
integer = "12" > "35"
```

Incorrect:

```isl
integer = "12" + "35
```
