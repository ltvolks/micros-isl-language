# ISL reference: functions

Source: RES 3700 SIM Online Help (CHM). Each entry starts with `## ` and the page name; grep `^## ` for an index.


---

## Abs

<!-- src: Function_abs.htm -->

Abs

### Description
This function returns the absolute value of the integer or decimal value.

### Syntax
Abs (integer or decimal)

### Argument/Description
**integer**  - an integer expression to be converted
**decimal**  - a decimal expression to be converted

**Abs Example**
event inq : 1
var int : N5 = -145
var mon : $8 = -12.35
waitforclear abs(int) //will display `145'
waitforclear abs(mon) //will display `12.35'
waitforclear abs("-34") //will display error
endevent

---

## ArraySize

<!-- src: Function_ArraySize.htm -->

ArraySize

### Description
This function returns the size (number of elements) of the array passed in.

### Syntax
ArraySize (array_name)

### Argument/Description
**array_name**  - the name of the array

**ArraySize Usage**
The array name must be placed between the parentheses without brackets. For example, the following references are illegal:
arraysize (list [ ])
arraysize (list [2])

The following entry is correct:
arraysize(list)

**ArraySize Example**
The following subroutine returns the declared size (number of elements) of an array.

sub array_size
var array_test[100] : a50
waitforclear "Size of array_test is ", arraysize(array_test)

//Would prompt "Size of array_test is 100"
endsub

---

## Asc

<!-- src: Function_Asc.htm -->

Asc

### Description
This function returns the ASCII integer value of the first character of the string passed in.

### Syntax
Asc (string_expression)

### Argument/Description
**string_expression**  - a place holder for text characters such as a user_variable (string)

**Asc Usage**
The process of returning a value with the Asc function works opposite of the Chr function.

**Asc Example**
The following subroutine displays the ASCII value of the first character of a string:

sub asc_value
var asc_val : n3
asc_val = asc("MICROS")
waitforclear "The ascii value of M = ", asc_val
//Would prompt "The ascii value of M = 77"
endevent

See also:

Chr Function

---

## Bit

<!-- src: Function_Bit.htm -->

Bit

### Description
This function will return the value (0 or 1) of a bit in a hexadecimal string.

### Syntax
Bit (hex_string, bit_position)

### Argument/Description
**hex_string**  - a place holder for the hexadecimal string that will be examined
**bit_position**  - the index of the bit whose value is desired

**Bit Usage**
The Bit function will generate an error if the string passed in contains non-hex characters. For example, the following statement will generate an error since the = character is not a hex digit:
i = gethex( "12AB=" )
Valid hex digits are 0-9, A-F, and a-f.
The bit_positions are numbered consecutively from 1. In the example below, a four-digit hexadecimal number would have bits numbered from 1 to 16. The digit values are determined by the standard hexadecimal assignment of bit values, i.e., within each digit, bit 1 = 8, bit 2 = 4, bit 3 = 2, bit 4 = 1.

Digit Position |  1 |  2 |  3 |  4 |

bit_position |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 |  10 |  11 |  12 |  13 |  14 |  15 |  16 |

digit value |  1 |  2 |  F |  E |

bit value |  0 |  0 |  0 |  1 |  0 |  0 |  1 |  0 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  0 |

**Bit Example**
In the below example, the following command would result in i being set to 1.

i = bit("12FE", 7) //i will be set to 1

Thus in all hex_strings, bit_position 1 corresponds to the highest bit value in the first of the string.

---

## Chr

<!-- src: Function_Chr.htm -->

Chr

### Description
This function returns a one-character string that is the ascii character representation of the integer passed in.

### Syntax
Chr (integer)

### Argument/Description
integer - an integer in the range from 32 to 255

**Chr Usage**
This function returns the ascii value of the specified integer.

**Chr Example**
The following subroutine constructs the name of a POS company using ASCII values:

sub make_name
var ascii_array[6] : n3
var pos_king : a6
var arr_cnt : n3
ascii_array[1] = 77
ascii_array[2] = 73
ascii_array[3] = 67
ascii_array[4] = 82
ascii_array[5] = 79
ascii_array[6] = 83
for arr_cnt = 1 to 6 //Count through the array
format pos_king as pos_king, chr(ascii_array[arr_cnt])
endfor
waitforclear "The POS king is ", pos_king
endsub

See also:

Display

---

## ClearChkID

<!-- src: Function_ClearChkID.htm -->

ClearChkID
### Function
This command will clear the guest check ID and set it to null in the database.

### Syntax
CLEARCHKID

---

## ClearChkInfo

<!-- src: Function_ClearChkInfo.htm -->

ClearChkInfo

### Function
This command clears any check information detail lines that have not been written to the database.

### Syntax
ClearChkInfo

**ClearChkInfo Usage**
Check information detail is a type of check detail that can be stored in the database via the SaveChkInfo command. Typically, check information detail lines are used to store customer information such as name and address, so that it can print on a guest check or a remote order device.
This command is executed upon exiting the script.

POS Setup
Refer to the detailed description of SaveChkInfo for a discussion of check information detail and the 3700 database programming required to enable the Guest Check Information Detail Lines feature.

**ClearChkInfo Example**
The subroutine below requires that the operator input a string five times, then prompts the operator to confirm saving the information. If the operator responds by pressing the [Clear] key, the check information detail is discarded; otherwise, the information is saved.

sub get_info
var string : A20
var answer : N5
var i : N5
for i = 1 to 5
input string, "Enter string ", i
savechkinfo string
endfor
getenterorclear answer, "Save information?"
if answer = 0
clearchkinfo
endif
endsub

See also:

EditDetail

SaveChkInfo

---

## ClearRearArea

<!-- src: Function_ClearRearArea.htm -->

ClearRearArea
### Usage
Command to clear the rear display and reset the @sustaincustomtext SIM variable.

**ClearRearArea Example:**
event SignIn
event inq = 1
DisplayRearArea = “Hello”
WaitForClear “Press clear to clear display”
ClearRearArea
endevent

---

## DisplayRearArea

<!-- src: Function_DisplayRearArea.htm -->

DisplayRearArea

### Usage
Command to display up to 40 characters in the rear display until the end of the event unless the @sustaincustomtext SIM variable is used.

**DisplayRearArea Example**
event SignIn
var msg: a80 = “ “
@sustaincustomtext = 1
format msg as @tremp, “signed in”
DisplayRearArea msg
endevent

---

## DisplayTouchscreen

<!-- src: Function_DisplayTouchscreen.htm -->

DisplayTouchscreen

### Function
This function will display the touchscreen specifed in the argument field. The argument must be a valid touchscreen object number.

**Type/Size**
Takes One Argument

### Syntax
displayTouchscreen <N>
N = the number of touchscreens to be displayed.

**DisplayTouchscreen Example**
event inq : 1
var tsObjectNum : n7 = 301
DisplayTouchScreen tsObjectNum
endevent

---

## Env

<!-- src: Function_Env.htm -->

Env
Not used.

---

## Feof

<!-- src: Function_Feof.htm -->

Feof

### Description
This function tests whether the file pointer is at the end of the file.

### Syntax
Feof (file_number)

### Argument/Description
**file_number**  - an integer variable which was assigned in the FOpen statement when the file was opened

**Feof Usage**
A 1 is returned if there is no more data left to read, and a 0 is returned if there is more data left to be read.

**Feof Example**
The following example shows how to use the Feof function as the condition of a While command:
while not feof( fn )
call process_data( fn )
.
endwhile

See also:

FClose

FOpen

While...EndWhile

---

## FTell

<!-- src: Function_FTell.htm -->

FTell

### Description
This function returns the file position in a file.

### Syntax
FTell (file_number)

### Argument/Description
**file_number**  - an integer variable which was assigned in the FOpen statement when the file was opened

**FTell Example**
The following example will read a certain field position:

sub find_emp
while not feof( fn )
current_position = ftell( fn ) //Remember this position.
fread fn, emp_number, * //Read first field.
if emp_number = target_emp_number //If match, reposition back
fseek fn, current_position // to original position and
return // let calling function
endif // reread data.
endwhile
endsub

See also:

FClose

FOpen

FRead

FSeek

While...EndWhile

---

## GetHex

<!-- src: Function_GetHex.htm -->

GetHex

### Description
This function will convert a Hex string to a decimal integer.

### Syntax
GetHex (hex_string)

### Argument/Description
**hex_string**  - the string to be converted

**GetHex Usage**
The GetHex function will generate an error if the string passed in contains non-hex characters. The following statement will generate an error since the = character is not a hex digit, for example:
i = gethex( "12AB=" )
A string should be made up of any combination of the following characters 0-9, a - f, or A - F.

**GetHex Example**
The following subroutine converts a hex string to its decimal equivalent:
sub hex_2_dec
var hex_str : a4 = "FFFF"
waitforclear "The decimal equiv of 'FFFF' is ", gethex(hex_str)
endsub

---

## GetMaxDiscount

<!-- src: Function_GetMaxDiscount.htm -->

GetMaxDiscount

### Usage
This function will return the remaining amount of a menu item that can be discounted for a particular discount definition.
For example, use this function to apply a discount to the menu items that are the most heavily taxed.

**GetMaxDiscount Example**
GetMaxDiscount (detail_index, disc_obj_num)

---

## Instr

<!-- src: Function_Instr.htm -->

Instr

### Description
This function will return the index of the first occurrence of a character in a string.

### Syntax
Instr (index, string_expression, character)

### Argument/Description
**index**  - starting position of the search for the specified character string_expression - the string_expression to be searched; can be one of the following: user_variable, system_variable, constant, string, function, equation
**character**  - character to search for

**Instr Example**
The following statement will set i equal to 5, since "E" is the 5th character in the string:
i = instr( 2, "ABCDEFGHIJ", "E" ) //i will be set to 5

---

## KDS Functions

<!-- src: Function_KDS_Functions.htm -->

KDS Functions

### Description
This function is used for processing KDS-related functions.

### Syntax
Key_Type_Function(35)

**Variables**
Key_KDS_Done_Order(1)

---

## Key Function

<!-- src: Function_Key.htm -->

Key Function

### Description
This function will execute the key function code defined.

### Syntax
Key (key_pair)

### Argument/Description
key_pair - a link to a specific UWS key in the form of key_type or key_number

### Usage
The key_type determines the type of key (e.g., Function, Keypad); the key_number designates the specific Key Code.

Click here to view key names and key codes.

**Key Example**

The following script begins a check by number, then orders several menu items and prints the check:

event inq : 1
loadkybdmacro key (11,400), \ //Begin check
key (1, 552), key(1,554), key (1,555),\ //Order Menu Items
key (7, 101) //Service Total check
endevent

See also:

KeyNumber Function

KeyType Function

---

## KeyNumber Function

<!-- src: Function_KeyNumber.htm -->

KeyNumber Function

### Description
This function will return the key number (integer) portion of a key expression.

### Syntax
KeyNumber (key_expression)

### Argument/Description
**key_expression**  - an expression that can be one of the following: @KEY ...system_variable, user_variable (KeyType), Key function

**KeyNumber Example**

The following script reports the number and type of the [Enter] key:

event inq : 1
var key_var : a20 = "9,12"
window 3, 26
display 1, 2, "Enter key's key pair is", key_var
display 1, 2, "Enter key's key type is", keytype(key_var)
display 1, 2, "Enter key's key number is", keynumber(key_var) //keynumber = 12
waitforclear
endevent

See also:

Key Function

KeyType Function

---

## KeyType Function

<!-- src: Function_ KeyType.htm -->

KeyType Function

### Description
This function will return the key type (integer) portion of a key expression.

### Syntax
KeyType (key_expression)

### Argument/Description
**key_expression**  - an expression that can be one of the following: @KEY system_variable, user_variable (KeyType), Key function

**KeyType Example**

The following script reports the number and type of the [Enter] key:

event inq : 1
var key_var : a20 = "9,12"
window 3, 26
display 1, 2, "Enter key's key pair is", key_var
display 1, 2, "Enter key's key type is", keytype(key_var)//key_type = 9
display 1, 2, "Enter key's key number is", keynumber(key_var)
waitforclear
endevent

See also:

KDS Functions

Key Function

KeyNumber Function

---

## Len

<!-- src: Function_Len.htm -->

Len

### Description
This function is used to determine the length of a string or string variable.

### Syntax
Len (string_expression)

### Argument/Description
**string_expression**  - the string length to be returned

**Len Example**
The following script takes a list of names from the PMS and tests each name for its length. It then builds a window and displays the names. The longest string determines the width of the window.

event rxmsg : guest_list
var guest_list_size : n3
var guest_list[14] : a78
var arrcnt : n3
var longestr : n3
rxmsg guest_list_size, guest_list[] //Receive size and list from PMS
for arrcnt = 1 to guest_list_size //Count through the array to
if longestr < len(guest_list[arrcnt]) // find the longest member.
longestr = len(guest_list[arrcnt]) //If this member is longer than
endif // the longest so far, set
endfor // longestr equal to its length.
window guest_list_size, longestr + 2 //Build the window as high as
for arrcnt = 1 to guest_list_size // the number of guests in the
display arrcnt, 2, guest_list[arrcnt] // list and as wide as the
endfor // longest guest name + 2.
waitforclear //Display the names and wait
endevent // for user to press clear.

---

## MakeKeys Function

<!-- src: Function_MakeKeys.htm -->

MakeKeys Function

### Description
This function turns characters into keystrokes. It is designed to be used with the LoadKybdMacro command.

### Syntax
MakeKeys (string_expression)

### Argument/Description
**string_expression**  - a string or user_variable (string) that will be treated as keystrokes by the system

**MakeKeys Example**
This function can only be used with the LoadKybdMacro command.

The following script receives authorization from the PMS, in the form of that employee's MICROS ID, then proceeds to clock the employee in:

event rxmsg : emp_clock_in
var micros_emp_id : a10
var clock_in_key : key
clock_in_key = key(11, 833) //Assign key pair for clock in var
rxmsg micros_emp_id //Receive the id of the employee to
// clock in from PMS then load the macro and clock the employee in.
loadkybdmacro clock_in_key, makekeys(micros_emp_id),\
@KEY_ENTER, @KEY_ENTER, @KEY_ENTER
endevent

See also:

LoadKybdMacro

---

## Mid Function

<!-- src: Function_Mid.htm -->

Mid Function

### Description
This function is used to extract text from a string. Note: This function is not to be confused with the Mid command.

### Syntax
Mid (string_expression, start, count)

### Argument/Description
**string_expression**  - a string or user_variable (string) start the starting offset (character) within the field
**count**  - the number of characters to be read

**Mid Function Usage**
This command is similar to the BASIC language "mid$" function.

**Mid Function Example**
The following subroutine searches a string for a specified character, starting at a specified place in the string, then returns the location of the character. The extracted text is compared to the desired characters. This example assumes that the calling routine declares the following four variables, and defines the first three:
//start : n3 position in string to start search, 1 if not defined
// string :a?? string to search
// search_char :a1 character to search for
// charpos :n3 the subroutine will set this variable equal to the
// location where the search_char is found in the
// string; it will be 0 if search_char is not found

sub instr
if start <= 0 //If user didn't define start set it = 1
start = 1
endif
for charpos = start to len(string)
if search_char = mid(string, charpos, 1) //If we find the search_char, return the charpos
return
endif
endfor
charpos = 0 //If not found, set charpos = 0
endsub

See also:

Mid Command

---

## One_Time_Auto_Discounts

<!-- src: Function_One_Time_Auto_Discounts.htm -->

One_Time_Auto_Discounts
### Usage
Indicates that the [Add Auto Discounts] key was used and automatic discounts were added to the check.

**One_Time_Auto_Discounts Example**
event SignIn
One_Time_Auto_Discounts
endevent

---

## Remove Auto Discounts

<!-- src: Function_Remove_Auto_Discounts.htm -->

Remove_Auto_Discounts
### Usage
Indicates that the [Remove Auto Discounts] key was pressed and that discounts were removed.

**Remove_Auto_Discounts Example**
event SignIn
Remvoe_Auto_Discounts
endevent

---

## ToInteger

<!-- src: Function_ToInteger.htm -->

ToInteger

### Description
This function returns an integer from a decimal value by removing the decimal point. This assumes that the new value will be interpreted correctly; i.e., the PMS will know where the decimal is placed.

### Syntax
ToInteger (decimal)

### Argument/Description
**decimal**  - a decimal expression to be converted

**ToInteger Usage**
The decimal point will be removed when returned.

**ToInteger Example**
event inq : 1
var n : N5
n = 12.45 //n will equal `12'
n = tointeger( 12.45 ) //n will equal `1245'
endevent

---

## Trim

<!-- src: Function_Trim.htm -->

Trim

### Description
This function is used to remove leading and trailing spaces from text or variable fields.

### Syntax
Trim (string_expression)

### Argument/Description
**string_expression**  - a string or user_variable (string)

**Trim Example**
The following subroutine trims leading and trailing spaces from a string:
sub trim_spaces
var string : a32 = " many spaces "
var trimmed_str : a11
trimmed_str = trim(string) //Result would be "many spaces"
endsub

---

## VarSize

<!-- src: Function_VarSize.htm -->

VarSize

### Description
This function returns the declared size of a variable.

### Syntax
VarSize (user_variable)

### Argument/Description
**user_variable**  - the name of the user_variable to be "sized"

VarSize Example
The following script displays the declared size of a very large string:

event inq : 12
var big_string : a200
waitforclear "BIG_STRING'S size is ", varsize(big_string)
//would prompt "BIG_STRING'S size is 200"
endevent
