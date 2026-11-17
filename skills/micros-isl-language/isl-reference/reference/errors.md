# ISL reference: errors

Source: RES 3700 SIM Online Help (CHM). Each entry starts with `## ` and the page name; grep `^## ` for an index.


---

## Array Index Out of Range

<!-- src: Error_Messages_array_index_out_of_range.htm -->

Array Index Out of Range

This message occurs if an index number used to access a list_array is invalid.
```isl
var array[10] : N5
array[12] = 1 //Valid range is 1-10
array[-2] = 4 //No negative numbers
```

---

## Bad sys var index

<!-- src: Error_Messages_Bad sys var index.htm -->

Bad sys var index

This message occurs if a system_variable size was out of range.
```isl
txmsg "MSG", @SI34 //Valid @SI range is 1-16
```

---

## Break with too many endfor

<!-- src: Error_Messages_Break_with_too_many_endfor.htm -->

Break with too many endfor

This message occurs if too many EndFor commands occurred within a script without a corresponding For command .
```isl
for i = 1 to 10
a[i] = 0
endfor
endfor //No corresponding for command
```

---

## Break without endfor

<!-- src: Error_Messages_Break_without_endfor.htm -->

Break without endfor

This message occurs if a Break command is issued within a For loop, but there is no EndFor command to complete the loop.

---

## Call has no arguments

<!-- src: Error_Messages_Call_has_no_arguments.htm -->

Call has no arguments

This message occurs if the subroutine called by the Call command has arguments, but no arguments were specified in the Call command.
```isl
event inq:1
  call mysub //Mysub has no arguments
endevent

sub mysub( var i:N5 )
  .
  .
  .
endsub
```

---

## Can not evaluate

<!-- src: Error_Messages_Can_not_evaluate.htm -->

Can not evaluate

This message occurs if invalid text was encountered when trying to read an expression.
```isl
display 3, *, "Test"
```

---

## Command outside procedure

<!-- src: Error_Messages_Command_outside_procedure.htm -->

Command outside procedure

This message occurs if certain commands are issued outside an Event procedure.
```isl
window 10,20 //This must be within the event procedure.
event inq:1
  .
  .
  .
endevent
```

The following commands are allowed outside an Event procedure:

ContinueOnCancel
ExitOnCancel
Prorate
Retain GlobalVar

Discard GlobalVar
SetSignOn(Left/Right)
Use(Compat/ISL) Format
Use(ISL/STD)TimeOuts
Var

---

## Decimal overflow

<!-- src: Error_Messages_Decimal_overflow.htm -->

Decimal overflow

This message occurs if an attempt to assign a value to a real exceeded the real's storage size.
```isl
var n : $3
n = 123.45 //n only holds 3 digits
```

---

## Display column or row out of ran

<!-- src: Error_Messages_Display_column_or_row_out_of_range.htm -->

Display column or row out of range

This message occurs if the row and/or column declared with the Display command is outside the range declared by the Window command .
```isl
window 10, 20
display 11, 1, "Line" //Row range is 1-10
display 1, 40, "Line" //Column range is 1-20
```

---

## Divide by zero

Divide by zero
This message occurs if an attempt was made to divide a numeric value by 0.
```isl
i = a / 0
```

---

## Duplicate variable def

<!-- src: Error_Messages_Duplicate_variable_def.htm -->

Duplicate variable def

This message occurs if an attempt is made to declare the same variable either within or outside an Event procedure.
```isl
event inq : 1
  var i : N5 //First declaration OK.
  var i : A20 //Redeclaration error.
  .
  .
  .
endevent
```

---

## Encountered non-hex data

<!-- src: Error_Messages_Encountered_non-hex_data.htm -->

Encountered non-hex data

This message occurs if Hexadecimal data was expected and the string contained non-hex data.
```isl
i = gethex( "145B*" ) //* is not a hex character
```

---

## Endsub nesting mismatch

<!-- src: Error_Messages_Endsub_nesting_mismatch.htm -->

Endsub nesting mismatch

This message occurs if an Endsub occurred within an Event command without its corresponding Sub command .
```isl
event inq : 1
.
.
.
endsub
endevent
```

---

## Evaluation nesting

<!-- src: Error_Messages_Evaluation_nesting.htm -->

Evaluation nesting

This message occurs if an overly complex expression was specified on the command line.
```isl
i = (((((((((((((((((( a + 5 ))))))))))))))))))
```

---

## Event inside procedure

Event inside procedure
This message occurs if an Event command was encountered within a subroutine.
```isl
sub check_message
event inq : 1 //Event within subroutine
.
.
.
endsub
```

---

## Event type must be word

Event type must be word
This message occurs if an invalid Event type was specified in the Event line. There are four types of Events: Inquire, Tmed, RxMsg, and Final_Tender.
```isl
event 123 : 377 //No such event type as 123
```

---

## Exceeded max array or variable size

Exceeded max array or variable size
This message occurs if the array_size or variable_size exceeded the system maximum size of 32768 bytes.
```isl
var array[100000] : N5
```

---

## expected ..., encountered...

<!-- src: Error_Messages_expected___encountered.htm -->

expected ..., encountered...

This message occurs when ISL receives unexpected text as part of the command syntax.
```isl
format date @DAY, "-" , month_arr[@MONTH], "-", @YEAR //"As" is missing after the format command
```

---

## Expected array in call

<!-- src: Error_Messages_Expected_array_in_call.htm -->

Expected array in call

This message occurs if the Sub command had an array argument, but the Call command tried to pass a normal variable.
```isl
event inq:1
var i:N5
call mysub( i ) //Has a normal variable
endevent

sub mysub( ref arr[] ) //Has an array
```

---

## Expected decimal

<!-- src: Error_Messages_Expected_decimal.htm -->

Expected decimal

There are places in ISL where the script writer must specify a decimal number (and not an integer or a string). Using any expression other than a decimal expression results in this error.
For example: the function tointeger() expects a decimal number as its argument.
i:N5
```isl
i = tointeger( 12.34 ) //OK
i = tointeger( 1234 ) //Not ok. 1234 is not decimal.
i = tointeger( "12.34" ) //Not ok. "12.34" is not decimal.
```

---

## Expected end of line

<!-- src: Error_Messages_Expected_end_of_line.htm -->

Expected end of line

This message occurs if extraneous data was found at the end of a command line.
```isl
startprint 12 i // Data after 12 is an error
```

---

## Expected format token

<!-- src: Error_Messages_Expected_format_token.htm -->

Expected format token

This message occurs if a variable was specified with the Display command that did not have a comma after it.
```isl
display 1, 2, i 123
```

---

## Expected operand

<!-- src: Error_Messages_Expected_operand.htm -->

Expected operand

This message occurs if an invalid expression was encountered.
```isl
var i : n5
i = 5 + //Invalid expression
```

---

## Expected string

<!-- src: Error_Messages_Expected_string.htm -->

Expected string

This message occurs if a command or function expected a string as one of its arguments, and a non-string expression was encountered.
```isl
var i : n5
setstring i, "a" //n : 5 is a non-string expression
```

---

## Format needs string

<!-- src: Error_Messages_Format_needs_string.htm -->

Format needs string

This message occurs if the Format command requires a string_variable as its first argument.
```isl
var line : A15
format as "This is a line" //Missing the variable after format command
```

---

## Format too long

<!-- src: Error_Messages_Format_too_long.htm -->

Format too long

This message occurs if the allocated size of the variable to be formatted is smaller than the total length of the expressions to be included.
```isl
var line : A10
format line as "This line is greater than 10 characters"
```

---

## Integer overflow

<!-- src: Error_Messages_Integer_overflow.htm -->

Integer overflow

This message occurs if an attempt to assign a value to an integer exceeded the integer's storage size.
```isl
var n : N3
n = 12345 // n only holds 3 digits.
```

---

## Invalid decimal operation

<!-- src: Error_Messages_Invalid_decimal_operation.htm -->

Invalid decimal operation

This message occurs if the operation is not allowed on real numbers. Real numbers are amounts, currencies, and decimals.
```isl
var a : $5, b : $5, c : $5
a = b % c
```

---

## Invalid first token

<!-- src: Error_Messages_Invalid_first_token.htm -->

Invalid first token

This message occurs if the start of a line contained invalid text.
```isl
display 2, 3, "Line"
```
`*waitclear //*` is invalid

---

## Invalid input fmt spec

<!-- src: Error_Messages_Invalid_input_fmt_spec.htm -->

Invalid input fmt spec

This message occurs if the input format specification contained invalid data.
```isl
input name{;}
```

---

## Invalid list size

<!-- src: Error_Messages_Invalid_list_size.htm -->

Invalid list size

This message occurs if a command which required a list value encountered a list value of 0 or below.

---

## Invalid output format

<!-- src: Error_Messages_Invalid_output_format.htm -->

Invalid output format

This message occurs if the output format specification contained invalid data.
```isl
txmsg name{;}
```

---

## Invalid pms send

<!-- src: Error_Messages_Invalid_pms_send.htm -->

Invalid pms send

This message occurs if the system was unable to send the PMS message.

---

## Length invalid

<!-- src: Error_Messages_Length_invalid.htm -->

Length invalid

This message occurs if the third argument in the Mid command and/or function was less than 0.

---

## List value too big

<!-- src: Error_Messages_List_value_too_big.htm -->

List value too big

This message occurs if the list value in the command exceeded the array which it referenced.
```isl
var list[10] : A20
txmsg 21, list[] // Valid range is 1-10
```

---

## Loop variable constant

<!-- src: Error_Messages_Loop_variable_constant.htm -->

Loop variable constant

This message occurs if the For loop variable was not a variable.
```isl
for 10 = 1 to 20
```

---

## Loop variable not int

<!-- src: Error_Messages_Loop_variable_not_int.htm -->

Loop variable not int

This message occurs if the For loop variable was not an integer.
```isl
var i : $10
for i = 1 to 10
```

---

## Max lines executed

<!-- src: Error_Messages_Max_lines_executed.htm -->

Max lines executed

This message occurs if the system_variable @Max_Lines_To_Execute was set to a non-zero value and @Max_Lines_To_Execute command lines were executed.

---

## Max macro keys

<!-- src: Error_Messages_Max_macro_keys.htm -->

Max macro keys

This message occurs if the maximum number of defined macro keys was encountered.
```isl
for i = 1 to 1000
  loadkybdmacro 1 = i
endfor
```

---

## Max ref info

<!-- src: Error_Messages_Max_ref_info.htm -->

Max ref info

This message occurs if the maximum number of reference lines were issued by the SaveRefInfo command . The maximum number of lines is 8.

---

## Max window input entries

<!-- src: Error_Messages_Max_window_input_entries.htm -->

Max window input entries

This message occurs if too many DisplayInput entries were specified. The maximum number of DisplayInput entries is .

---

## Memory allocation

<!-- src: Error_Messages_Memory_allocation.htm -->

Memory allocation

This message occurs if an internal memory error has occurred.

---

## Must have list var

<!-- src: Error_Messages_Must_have_list_var.htm -->

Must have list var

This message occurs if ISL encountered a list specification without a list value.
```isl
txmsg list[]
```

---

## Name is a reserved word

<!-- src: Error_Messages_Name_is_a_reserved_word.htm -->

Name is a reserved word

This message occurs if an attempt was made to declare a variable with the same name as a reserved word.
```isl
var display : n4
```

---

## New tndttl exceeds original

<!-- src: Error_Messages_New_tndttl_exceeds_original.htm -->

New tndttl exceeds original

This message occurs if an attempt was made to increase the system_variable @Tndttl value, but the value can only be decreased.

---

## No arrays in sub var

<!-- src: Error_Messages_No_arrays_in_sub_var.htm -->

No arrays in sub var

This message occurs if a Sub command tried to declare an array_variable in the argument list.
```isl
sub mysub( var i[ 10 ] : N5 )
```

---

## No isl file

<!-- src: Error_Messages_No_isl_file.htm -->

No isl file

This message occurs if the script was not found or did not exist.

---

## No match for endfor

<!-- src: Error_Messages_No_match_for_endfor.htm -->

No match for endfor

This message occurs if no corresponding EndFor command exists for a For command .
```isl
event inq : 1
for row_cnt = 1 to number_occupants
display row_cnt, 2, occupant_list[row_cnt]
.
.
.
//Missing endfor command
endevent
```

---

## No match for endwhile

<!-- src: Error_Messages_No_match_for_endwhile.htm -->

No match for endwhile

This message occurs if no corresponding EndWhile command exists for a While command .
```isl
event inq:1
.
.
.
while i < 10

.
.
.
//No endwhile declared
endevent
```

---

## No match for event

<!-- src: Error_Messages_No_match_for_event.htm -->

No match for event

This message occurs if the SIM Inquiry and/or SIM Tender key had no corresponding Event Inq or Event_Tmed.
For example, if the SIM Inquiry Key (SIM Key 1 : Inq 1) is pressed, and Event Inq : 1 does not exist, this message will display.

---

## No number in sys var

<!-- src: Error_Messages_No_number_in_sys_var.htm -->

No number in sys var

This message occurs if a system_variable requires a number entry after it and no number was entered.
For example, system_variable @SI must have a number 1 - after it.

---

## No ops on strings

<!-- src: Error_Messages_No_ops_on_strings.htm -->

No ops on strings

This message occurs if the declared string operation is not allowed.
```isl
a = "123" - "abc"
```

---

## No pms message received

<!-- src: Error_Messages_No_pms_message_received.htm -->

No pms message received

This message occurs if no response was received from the PMS system after the RxMsg command was executed.

---

## No touchscreen keys defined

<!-- src: Error_Messages_No_touchscreen_keys_defined.htm -->

No touchscreen keys defined

If the script executes a ClearIslTs command to clear the ISL-defined touchscreen, then immediately tries to display the ISL-defined touchscreen using DisplayIslTs , the ISL cannot display the touchscreen because there are no keys to display.
```isl
event inq:1
  clearislts //Remove any defined keys.
  displayislts //No keys, error occurs here.
endevent
```

---

## Not a variable

<!-- src: Error_Messages_Not_a_variable.htm -->

Not a variable

This message occurs if a variable was expected but not encountered.
```isl
input 123, "Enter value" //123 not variable
```

---

## Not enough input data

<!-- src: Error_Messages_Not_enough_input_data.htm -->

Not enough input data

This message occurs if the @Strict_Args variable is set and there were too many variables specified in the command.
Assume the following data was received in a PMS message: Dan|Tooher. The message has two fields. The following example expects three fields and would generate the above error:
```isl
var fname : A20, lname : A20, status : N3
```
.
.
.
```isl
rxmsg fname, lname, status
```

---

## Not enough list data

<!-- src: Error_Messages_Not_enough_list_data.htm -->

Not enough list data

This message occurs if the @Strict_Args variable is set to a non-zero value, but the input data did not have enough values to assign the specified list. Assume the following data was received in a PMS message: 3|Smith|Jones. The 3 signifies that three fields follow, and only two fields are present. The following would generate the above error:
```isl
var size : N3
var list[10] : A20
```
.
.
.
```isl
rxmsg size, list[ ]
```

---

## Not enough variables

<!-- src: Error_Messages_Not_enough_variables.htm -->

Not enough variables

This message occurs if the @Strict_Args variable is set to a non-zero value, but there were not enough variables specified in the command.
Assume the following data was received in a PMS message: DanTooher. The message has two fields. The following example expects one field and would generate the above error:
```isl
var fname : A20, lname : A20, status : N3
```
.
.
.
```isl
rxmsg fname
```

---

## Numeric entry required

<!-- src: Error_Messages_Numeric_entry_required.htm -->

Numeric entry required

This message occurs if non-numeric data was entered for a numeric variable.

---

## Print already started

<!-- src: Error_Messages_Print_already_started.htm -->

Print already started

This message occurs if a StartPrint command was encountered while print was still active (i.e., prior to a corresponding EndPrint ).
```isl
startprint @RCPT
printline ...
startprint @CUST
.
.
.
endprint
```

---

## Print not started

<!-- src: Error_Messages_Print_not_started.htm -->

Print not started

This message occurs if a PrintLine or EndPrint command was encountered without a corresponding StartPrint command .

---

## Reading ord dvc table

<!-- src: Error_Messages_Reading_ord_dvc_table.htm -->

Reading ord dvc table

This message occurs if an error occurred while reading the Order Device Table in the 3700 database.

---

## Reading tbl def

<!-- src: Error_Messages_Reading_tbl_def.htm -->

Reading tbl def

This message occurs if an error occurred while reading the Table Definition File in the 3700 database.

---

## Require array for list

<!-- src: Error_Messages_Require_array_for_list.htm -->

Require array for list

This message occurs if an array was expected but a non-array variable was encountered.
```isl
var i : N5
listdisplay 1, 2, 3, i //i is not an array
```

---

## Script memory allocation error

<!-- src: Error_Messages_Script_memory_allocation_error.htm -->

Script memory allocation error

This message occurs if an internal error is encountered.

---

## Start position invalid

<!-- src: Error_Messages_Start_position_invalid.htm -->

Start position invalid

This message occurs if the start_position parameter in the Mid command and/or function is invalid.
```isl
str = mid("abc", -2, 3) //-2 is invalid
```

---

## String overflow

<!-- src: Error_Messages_String_overflow.htm -->

String overflow

This message occurs if an attempt to assign a value to a string exceeded the string's storage size.
```isl
var n : A3
n = "message" //n only holds 3 characters
```

---

## Sub array ref invalid

<!-- src: Error_Messages_Sub_array_ref_invalid.htm -->

Sub array ref invalid

This message occurs if a Sub command had an invalid array declaration for an array_ variable.
```isl
sub mysub( ref array[ ) //Only one bracket Should be [ ]
```

---

## Sub has no arguments

<!-- src: Error_Messages_Sub_has_no_arguments.htm -->

Sub has no arguments

This message occurs if a Call command was made with arguments, and the subroutine called had no arguments.
```isl
event inq:1
  call mysub( 1, 2, 3 )
endevent

sub mysub //Mysub missing ( 1, 2, 3 )
  .
  .
  .
endsub
```

---

## Sub statement in procedure

<!-- src: Error_Messages_Sub_statement_in_procedure.htm -->

Sub statement in procedure

This message occurs if a Sub command was encountered while inside an Event.
```isl
event inq:1
  sub mysub
    .
    .
    .
  endsub
endevent
```

---

## Sys var not assignable

<!-- src: Error_Messages_Sys_var_not_assignable.htm -->

Sys var not assignable

This message occurs if an attempt was made to assign a value to a read-only system_variable.

---

## System variable declaration

<!-- src: Error_Messages_System_variable_declaration.htm -->

System variable declaration

This message occurs if an attempt was made to declare a system_variable (i.e., any variable name that begins with the @ character).
```isl
var @chk : N3
```

---

## Too few args in call

<!-- src: Error_Messages_Too_few_args_in_call.htm -->

Too few args in call

This message occurs if the Call command did not have enough arguments.
```isl
event inq:1
  call mysub( 1 )
endevent

sub mysub( var i:n5, var j:N5 )
  .
  .
  .
endsub
```

---

## Too few arguments

<!-- src: Error_Messages_Too_few_arguments.htm -->

Too few arguments

This message occurs if there were not enough arguments specified for a function.

---

## Too many args in call

<!-- src: Error_Messages_Too_many_args_in_call.htm -->

Too many args in call

This message occurs if the Call command had too many arguments.
```isl
event inq:1
  call mysub( 1, 2 )
endevent

sub mysub( var i:n5 )
  .
  .
  .
endsub
```

---

## Too many arguments

<!-- src: Error_Messages_Too_many_arguments.htm -->

Too many arguments

This message occurs if too many arguments were specified for a function.

---

## Too many nested calls

<!-- src: Error_Messages_Too_many_nested_calls.htm -->

Too many nested calls

This message occurs if too many subroutines were nested within each other.

---

## Too many touchscreens keys

<!-- src: Error_Messages_Too_many_touchscreens_keys.htm -->

Too many touchscreens keys

The ISL-defined touchscreen will hold a finite number of keys (i.e, ). If the user tries to define too many keys, this error will occur.
```isl
event inq:1
  var i:n5

  clearislts // Remove any defined keys.
  for i = 1 to 100 // Loop will generate an error.
    setisltskey 1, 1, 2, 1, 1, @key_clear, "CLEAR"
  endfor
  displayislts // No keys, error occurs here.
endevent
```

---

## Undefined call

<!-- src: Error_Messages_Undefined_call.htm -->

Undefined call

This message occurs if a Call was made to a subroutine that did not exist within the script.

---

## Undefined function

<!-- src: Error_Messages_Undefined_function.htm -->

Undefined function

This message occurs if an undefined function was called.

---

## Undisplayable variable

<!-- src: Error_Messages_Undisplayable_variable.htm -->

Undisplayable variable

This message occurs if the variable cannot be displayed.
```isl
display 2, 3, @TRDTL //@TRDTL can not be displayed
```

---

## Unexpected data after call

<!-- src: Error_Messages_Unexpected_data_after_call.htm -->

Unexpected data after call

This message occurs if the Call command is invalid.
```isl
call mysub + 3
```

---

## Unexpected data after sub

<!-- src: Error_Messages_Unexpected_data_after_sub.htm -->

Unexpected data after sub

This message occurs if the Sub command is invalid.
```isl
sub mysub - 4
```

---

## Unexpected data is sub

<!-- src: Error_Messages_Unexpected_data_is_sub.htm -->

Unexpected data is sub

This message occurs if the parameter list in the Sub command is invalid.
```isl
sub mysub( var fred:N5, i : N5 )
```

---

## Unexpected end of line

<!-- src: Error_Messages_Unexpected_end_of_line.htm -->

Unexpected end of line

This message occurs if not enough data was specified on the command line.
```isl
display 2, 2, //should be data after 2,
```

---

## Unexpected token type

<!-- src: Error_Messages_Unexpected_token_type.htm -->

Unexpected token type

This message occurs if invalid text is encountered when trying to read a command or function.

---

## Unknown command

<!-- src: Error_Messages_Unknown_command.htm -->

Unknown command

This message occurs if an unknown command is specified.
dsplay 2, 2, "Line" //display is misspelled

---

## Unknown system variable

<!-- src: Error_Messages_Unknown_system_variable.htm -->

Unknown system variable

This message occurs if an unknown system_variable is referenced.
```isl
display 2, 2, @RVVC
```

---

## Unmatched endevent

<!-- src: Error_Messages_Unmatched_endevent.htm -->

Unmatched endevent

This message occurs if an Endevent was encountered without a corresponding Event command .

---

## Unmatched endfor

<!-- src: Error_Messages_Unmatched endfor.htm -->

Unmatched endfor

This message occurs if a For/EndFor nesting error occurred.

---

## Unmatched if

<!-- src: Error_Messages_Unmatched_if.htm -->

Unmatched if

This message occurs if an If, ElseIf, Else, or EndIf nesting error occurred.

---

## Value not key definition

<!-- src: Error_Messages_Value_not_key_definition.htm -->

Value not key definition

This message occurs if an attempt to use a non-key variable in an expression which required a key_variable was encountered.
```isl
loadkybdmacro 12.47
```

---

## Variable undefined

<!-- src: Error_Messages_Variable_undefined.htm -->

Variable undefined

This message occurs if an undefined variable was referenced.

---

## Window columns out of range

<!-- src: Error_Messages_Window_columns_out_of_range.htm -->

Window columns out of range

This message occurs if an attempt was made to declare a Window that was too wide.
```isl
window 4, 1000
```

---

## Window has not been defined

<!-- src: Error_Messages_Window_has_not_been_defined.htm -->

Window has not been defined

This message occurs if an attempt to display text within a Window occurred without a Window first being declared.

---

## Window rows out of range

<!-- src: Error_Messages_Window_rows_out_of_range.htm -->

Window rows out of range

This message occurs if an attempt was made to declare a Window that was too tall.
```isl
window 1000, 10
```
