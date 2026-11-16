# Chapter 7: Format Specifiers

This chapter contains a discussion of format specifiers used in command syntax.

## Format Specifiers

The Interface Script Language (ISL) provides commands to display information, get
operator entries, display touchscreens, execute keyboard macros, as well as transmit
and receive messages over the interface. A detailed description of each ISL command
is provided in the SIM Online Help.

Format specifiers can be part of the syntax of certain commands. Format specifiers allow you to change the format of both input and output data. Review “Using Format Specifiers” on page 7-3 to learn the ways in which this language element can be used in command syntax.

## Using Format Specifiers

### What is a Format Specifier?

In general, the default behavior for entering data and displaying data in ISL is
sufficient for most needs. However, it is necessary sometimes to change the default
behavior to suit the application at hand. For example, you might want to allow
magnetic card data entry, to pad displayed data with 0s instead of spaces, or to center
data within a display area.

A variety of ISL commands allow you to accomplish this type of formatting, using a language element called a format specifier. You’ll know if the command takes a format specifier as an argument by looking at the syntax for the command in the ISL Command Reference.

A format specifier is text enclosed in braces and appears directly after the variable or constant whose input/output behavior is affected. When defined, a format specifier changes the way that the variable or constant is input or output. For example, the following command will display the contents of the user variable guest_name in the prompt area. The format specifier appears directly after the guest_name variable.

```isl
PROMPT guest_name{ 20" }
```

### Types of Format Specifiers

There are two types of specifiers: **Input** and **Output**.

Input specifiers are placed after input variables in commands that get data from a user: `Display`, `DisplayMSInput`, `Input`, and `InputKey`.
Output specifiers are placed after variables and expressions that are being converted to ASCII for outputting data to the screen, printer, or a message to a PMS.


**Specifier Attributes**

The general layout of a format specifier is:

- { [input_specifier] [output_specifer] }
- The input_specifier and output_specifier consists of individual specifiers, which are usually one character.
- Spaces and tabs may be used in a format specifier for clarity. The following two format specifiers are equivalent: {-=08} { - = 0 8 }

Input and output specifiers can appear within one format specifier. However, not all of the individual specifiers may have meaning. For example, it is possible to put input specifiers after a variable that is going to be displayed, but since data is not being entered into the variable, the input specifiers are meaningless and will be ignored.

#### Input Specifiers

The input specifiers only have meaning for commands that receive input from the user. They will be ignored if they appear in commands that only output data (for example, the Display command).

All input specifiers must be placed before any output specifiers. If they are present, they must also be placed in the order listed in the following table:

| Input Specifier | Description |
| ---- | ---- |
|      -          | Data being typed in by the operator should not be echoed back to the display |
|     Mn          | Specify the track number (n) and what data to read from the magnetic card. For use with the Input, InputKey, DisplayInput, and DisplayMSInput commands only. The M character is not case sensitive. |

**- Input Specifier**

The - specifier is used to hide data being entered by the operator. For example,
authorization codes or passwords should not be echoed to the display as the operator
types them in. The following command prompts the operator for an authorization
code, but echoes it back to the display as it is being typed:

```isl
input auth_code, “Enter authorization code”
```

It can be rewritten so that no data is echoed:

```isl
input auth_code{-}, “Enter authorization code”
```

If the - specifier is used in commands that require both operator input and the data to be displayed, then not only will the data not be echoed, it will also not be displayed in the window after it is entered. Instead, the field will contain asterisks where data is expected.

**M Input Specifier**
The M specifier is used when magnetic card data may be entered in lieu of the operator typing the data in. The M specifier defines whether the data is on a mag card, and which track and field the data should be read from. For example, it is possible to use the M specifier to get an authorization code from track 2, field 1, starting offset 3, and copy in 10 characters.

There are two M formats:
- Format 1 Syntax: `Mn,*`
- Format 2 Syntax: `Mn, field, start, count | *`

These fields are defined as follows

| Field | Description |
| --- | --- |
| Mn: | the track number (M2); this can be followed by a star (\*) to specify all fields on the track, or use the following fields to read specific information: |
| field: | the field position within the specified track; this is a positive integer |
| start: | starting offset (character) within the field; for example, if you want to take the last four characters of the “Blaine Richard” string, you would start the offset at 11 |
| count: | number of characters to be read from the start (first character) to the end of the field (place an asterisk \* to include all characters) |

**Format One**
In format 1, the data from the entire track (2) will be placed into the variable when the mag card is swiped. The following command allows the user to enter a code or swipe a magnetic card: Input auth_code{ M2,* }, “Enter authorization code”

If the mag card is swiped, then all the data from track 2 (M2) will be placed into the variable auth_code.

**Format Two**
Format 2 defines exactly where the data in the track occurs. If the authorization code appears in field 1 of track 2, and furthermore, starts at character 3 in the field and consists of 10 characters, then the command can be rewritten as: Input auth_code{ M2,1,3,10 }, “Enter authorization code”

If the operator swipes the card, the appropriate data will be extracted from the field and placed into auth_code.

> **Note:** You can substitute a * for count, to specify ALL data from the start offset in the field.

**Field Positions for Credit Cards**
The following is an illustration of the standard field positions for credit cards:

Track 2

| `Field #` | 1 | 2 |
| --- | --- | --- |
| Data | 16/19 Digit Account Number | YYMM |

The following Input command allows the operator to enter the credit card name or swipe the card and have the name transferred from track 2, field 1.

```isl
Input card_num{M2, 1, 1, *}, “Enter account number”
```

The following is an illustration of the standard field position for the MICROS Employee Card (Note: this card is Track 2 only):

| `Field #` | 1 |
| --- | --- |
| Data | 10 Digit Employee Number |


The following Input command will get the employee number from the operator or the mag card and will not echo the data as it is being entered: Input empl_num{ - M2,1,1,10 }, “Enter employee number”

For more information concerning the field numbers, please see the 3700 Hardware Installation Guide.


**Using Both Input Specifiers**

Both input specifiers may be used. This command uses both the - and the M specifiers:
```isl
Input auth_code{ - M2,1,3,10 }, “Enter authorization code”
```

#### Output Specifiers

Output specifiers are used after variables and expressions that are being converted to ASCII. The output specifiers are similar to the C language printf() specifiers. The following table lists some representative commands for each of these output types:


|            Commands                 | Output Type |
| ---- | ---- |
| Display, WaitForConfirm, and Window | Screen |
| PrintLine                           | Printing |
| TxMsg                               | PMS |

**Syntax**

The proper syntax for using the output_specifiers is as follows:

`[<|=|>|*] [+] [0] [size] [D|X|O|B] [^] ["] [:format_string]`

Output specifiers must also be placed in the order listed in the following table:

| Output Specifier | Description |
| ---- | ---- |
| < | Left justification; the size specifier may be used to specify the size of the field |
| = | Center justification; the size specifier may be used to specify the size  of the field |
| \>              | Right justification; the size specifier may be used to specify the size of the field |
| *              | Trim leading and trailing spaces; the size specifier may be used to specify the size of the field |
| +              | Place sign at start of field |
| 0              | Pad with zeroes (as opposed to spaces) |
| size           | Where size is the number of the characters in the required field. The size must be a positive integer or an expression that is a positive integer |
| D              | Decimal (Default); display numerics in decimal format |
| X              | Hexadecimal; display numerics in hexadecimal format |
| O              | Octal; display numerics in octal format |
| B              | Binary; display numerics in binary format |
| ^              | Place a space on each side of the data to be displayed |
| "              | Place double quotes around the data to be displayed |
| :format_string | Similar to the BASIC language PRINT USING command. All characters will be displayed except for the # character, which will be replaced by characters from the variable or expression preceding the format specifier.  |

### Examples of Specifiers

The following are examples of how Input and Output Specifiers may be used. For complete examples and explanations of the ISL commands, please see the ISL Command Reference in the SIM Online Help.

#### Input Specifier
The following lines would read data from a Credit Card:

```isl
displaymsinput 1, 2, account_num{m2, 1, 1, *, 019}, “Enter Account Number”,\
               2, 2, expiration_date{m2, 2, 1, *}, “Enter Expiration”
```


#### Output Specifiers

**Justification Specifiers**

The justification specifiers `<`, `=`, and `>` are only meaningful when the size of the expression being formatted is greater than the size of the variable itself.

All integers and decimal expressions are right justified, and all string expressions are left justified, by default. The following section gives examples and shows how these specifiers can be used to justify data:

| Expression | Output |
| --- | --- |
| `125 { 8 }` | 125 |
| `125 { <8 }` | 125 |
| `125 { =8 }` | 125 |
| `125 { >8 }` | 125 |
| `“abc” { 8 }` | abc |
| `“abc” { =8 }` | abc |

**\* Specifier**

The `*` specifier is used when the expression should be displayed with leading and trailing spaces removed.

| Expression | Output |
| --- | --- |
| `“125” {*}` | 125 |
| `“ 125 ” {*}` | 125 |
| `“ word 1 and word 2 ” {*}` | word 1 and word 2 |

**`+` Specifier**

The `+` specifier is used to override the default behavior of displaying negative numbers with the - sign to the right of the number by causing the - to appear on the left.

| Expression | Output |
| --- | --- |
| -891 | 891- |
| `-891 {+}` | -891 |

If the `SetSignOnLeft` command is executed, then the sign will always appear on the left side of the number. The + specification in this case will be superfluous.

**0 Specifier**

The 0 specifier is used to pad the data being displayed with ASCII 0s instead of spaces. The 0 specifier is only meaningful if the size specifier is also used:

| Expression | Output |
| --- | --- |
| `199 { 0 }` | 199 |
| `199 { 5 }` | 199 |
| `199 { 05 }` | 00199 |
| `199 { <05 }` | 19900 |

**size Specifier**

The size specifier defines the width of the expression being displayed. If no size specifier is present, then the width of the data formatted will be equal to the number of characters in the data.

If the size specifier is 8, then 8 characters will be displayed, irrespective of the width of the actual data being displayed. The output data will be padded with spaces (unless the 0 specifier is used) or truncated if the size specifier is less than the length of the data to be displayed.

There are two types of size specifiers: absolute and expression. All size specifiers must evaluate to positive integers. Negative numbers and/or decimal values are not allowed.

Absolute specifiers are an integer value, for example, 5. The size specified must not begin with a 0, since the 0 will be mistaken for the 0 specifier.

Expression sizes use standard ISL expressions to specify the size. However, the expression must be enclosed in parentheses, or an error will be displayed.

(In this example, the value of width is assumed to be 3.)

| Expression | Output |
| --- | --- |
| `“abcdefghij”` | abcdefghij |
| `“abcdefghij” { 8 }` | abcdefgh |
| `“abcdefghij { =8 }` | abcdefgh |
| `“abcdefghij { (width*2) }` | abcdef |
| `“abcdefghij” { width+2 }` | ERROR: not enclosed in ( ) |

**D,X,O, and B Specifiers**

The radix specifiers (D, X, O, and B) determine the numeric base of the integer expression being displayed. They have no meaning for decimal and string data. The default is base 10 (D).

| Expression | Output |
| --- | --- |
| 100 | 100 |
| `100 {H}` | 64 |
| `100 {B}` | 1100100 |
| `100 {08B}` | 01100100 |

**:format_string Specifier**

The format_string is the data that follows the colon : specifier. The format_string consists of ASCII characters and the # character. Format_strings are used when the data displayed should be interspersed with spaces and/or other characters to fit conventional display methods. For example, a 10-digit phone number should be displayed as: (nnn)nnn-nnnn

When the SIM encounters a format_string, all # characters will be replaced with data from the preceding expression. All other characters will be output as-is. Characters are replaced starting from the right side of the format string.

Output format specifiers may be used in a format specifier along with the format_string specifier. Any # characters in excess of the expression being formatted will be replaced with spaces, unless the 0 output specifier is used.

For example, to display a U.S phone number, assume that the variable phone_num contains the phone number and is equal to 3012108000. Also assume that room_num contains a room number and is equal to 17031.

| Expression | Output |
| --- | --- |
| `phone_num` | 3012108000 |
| `phone_num {:###-###-####}` | 301-210-8000 |
| `phone_num {:(###) ###-####}` | (301) 210-8000 |
| `room_num` | 17031 |
| `room_num {:##-###}` | 17-031 |
| `room_num {:Floor ## room ###}` | Floor 17 room 031 |

### Using Input and Output Specifiers Together

It may be necessary sometimes to display the # character and not have it replaced with a character from the output expression. In this case, precede the # character with a single quote.

| Expression | Output |
| --- | --- |
| `phone_num {:Phone ‘# ###-###-####}` | `Phone # 301-788-4531` |

It is possible to include format specifiers after each expression being formatted in one command. For example:

```isl
TXMSG room_number { 04 }, guest_name { <24 }, @cknum
```

Input and output specifiers may be used within the same syntax in the DisplayInput and DisplayMSInput commands only.

In the example below, if we wanted the credit card number to be displayed, we would add a 019 after the star on the account_num line. This would display a 19-digit number (padded with zeroes) at the UWS.

```isl
event inq : 1
  var account_num: a19
  var expiration_date: n4
  var track2_data: a79

  window 3, 78
  displaymsinput 1, 2, account_num{m2, 1, 1, *}, "Enter Account Number",\
                 2, 2, expiration_date{m2, 2, 1, 4}, "Enter Expiration"

  windowinput
  waitforclear
endevent
```