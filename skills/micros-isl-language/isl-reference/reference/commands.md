# ISL reference: commands

Source: RES 3700 SIM Online Help (CHM). Each entry starts with `## ` and the page name; grep `^## ` for an index.


---

## Break

<!-- src: Command_Break.htm -->

Break

### Function
Break is used to exit a ForEver loop or to exit a For loop before the end expression is reached.

### Syntax
```text
Break
```

**Break Usage**
- The break command will only break out of the For or Forever loop it is currently in. If the loops are nested, then multiple breaks are required:

```isl
forever
  forever
    break //break out of inner loop
  endfor
  break //break out of outer loop
endfor
```
- If the ability to break out of a nested For is required, then use a subroutine and Return out of the loop instead:

```isl
sub break_out
  forever
    for i = 1 to 10
      for num = i to count
        if...
          return
        endif
      endfor
    endfor
  endfor
endsub
```

**Break Example**

The following script provides an example of how to break out of a Forever loop:

```isl
event inq : 1
  var user_input : N6
  forever
    input user_input, "Enter a number and press [ENTER]"
    if user_input > 0 AND user_input <99999
      break
    else
      errormessage "Value outside valid range"
    endif
  endfor
  errormessage "Well done"
endevent
```

**See also:**

For...EndFor
ForEver...EndFor

---

## Call

<!-- src: Command_Call.htm -->

Call

### Function
This command is used to call a subroutine defined by the Sub command.

### Syntax
```text
(entered as a single line)
Call name [(parameter[parameter]…)]
```

### Argument/Description
**name**  - the name of the subroutine defined by the Sub command

**parameter**  - a variable or expression passed from the associated Call command; it may be one of the following:
- variable by reference
- array by reference
- expression by value, i.e. local_variable_name : [A, $, N ] Size, or Key

**Call Usage**
- The subroutine has access to all the local variables within the Event that called the subroutine, and all global variables in the script file, so these variables may be used to pass parameters. In addition, local variables may be declared in the subroutine.
- When a Call is made, ISL will start searching for the subroutine from the top of the program. Therefore, if there are two subroutines with the same name, only the first one will ever be called.
- Up to 32 calls can be nested within a subroutine. If there are more, an error will occur.

```isl
sub mysub
  call mysub //this will occur 32 times
endsub
```

**Call Example**

The following script will call a subroutine to build a window:

```isl
event inq : 1
  var win_string : a40 = "This window was built in a subroutine!"
  call msg_window
  waitforclear
endevent

sub msg_window
  window 1, len(win_string) + 2
  display 1, 2, win_string
endsub
```

See also:

Sub...EndSub

---

## ClearArray

<!-- src: Command_Cleararray.htm -->

ClearArray

### Function
This command sets all elements of the specified array equal to zero if the array is numeric, or null if alphanumeric. By default, arrays are initialized in this way when declared.

### Syntax
```text
ClearArray array_variable
```

### Argument/Description
array_variable - the name of the array to clear, based on the name of a user_variable

**ClearArray Example**

The following script allows the user to send a message of up to 10 lines to the kitchen printer. Before actually sending to the printer, it allows the user the opportunity to edit their work. If the user presses clear when prompted, the array_variable is cleared and the user can retype a message.

```isl
event inq : 1
  var kitchen_msg[10] : a20
  var sender_name : a20
  var rowcnt : n3
  var term_key : key
  var data_entered : a20
  forever
    call get_message
    window 1, 66
    display 1, 2, "PAGE UP=edit, CLEAR=retype, ENTER=send, CANCEL=quit"
    inputkey term_key, data_entered, ""
    if term_key = @Key_Enter
      break
    elseif term_key = @Key_Clear
      cleararray kitchen_msg
    elseif term_key = @Key_Cancel
      exitcontinue
    endif
  endfor
  call print_message
endevent
sub get_message
  window 12, 22
  displayinput 1, 2, sender_name, "Enter your name"
  for rowcnt = 1 to 10
    displayinput rowcnt + 1, 2, kitchen_msg[rowcnt], "Enter kitchen message"
  endfor
  windoweditwithsave
endsub
sub print_message
  startprint @ordr1
    printline "============================"
    printline "Message from ", sender_name
    printline "============================"
    for rowcnt = 1 to 10
      if len(kitchen_msg[rowcnt]) > ""
        printline kitchen_msg[rowcnt]
      endif
    endfor
    printline "======= END MESSAGE ========"
  endprint
endsub
```

See also:

EditDetail

SaveChkInfo

---

## ClearChkID

<!-- src: Command_ClearChkID.htm -->

ClearChkID

### Function
This command will clear the guest check ID and set it to null in the database.

### Syntax
```text
CLEARCHKID
```

---

## ClearChkInfo

<!-- src: Command_ClearChkInfo.htm -->

ClearChkInfo

### Function
This command clears any check information detail lines that have not been written to the database.

### Syntax
```text
ClearChkInfo
```

**ClearChkInfo Usage**
- Check information detail is a type of check detail that can be stored in the database via the SaveChkInfo command. Typically, check information detail lines are used to store customer information such as name and address, so that it can print on a guest check or a remote order device.
- This command is executed upon exiting the script.

**POS Setup**
Refer to the detailed description of SaveChkInfo for a discussion of check information detail and the 3700 database programming required to enable the Guest Check Information Detail Lines feature.

**ClearChkInfo Example**

The subroutine below requires that the operator input a string five times, then prompts the operator to confirm saving the information. If the operator responds by pressing the [Clear] key, the check information detail is discarded; otherwise, the information is saved.

```isl
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
```

See also:

EditDetail

SaveChkInfo

---

## ClearIslTs

<!-- src: Command_ClearIslTs.htm -->

ClearIslTs

### Function
This command clears any touchscreen keys that have been defined using the SetIslTsKey command.

### Syntax
```text
ClearIslTs
```

**ClearIslTs Usage**
- All previously defined keys are cleared each time a script executes.
- After a touchscreen has been displayed, its keys remain defined, thus, we recommend that you use the ClearIslTs command to clear previously defined touchscreen keys when building two or more touchscreens in the same event.

**ClearIslTs Example**

The following example is a subroutine (create_ts) that clears previously defined touchscreen keys before calling another subroutine (set_keys), one that will build a new touchscreen.

```isl
sub create_ts
  clearislts //Clear out any previously
  // defined touchscreen keys
  call set_keys //Build the keys needed
  .
  .
  .
endsub
```

See also:

DisplayIsTs
SetIsTsKey
SetIsTsKeyx

---

## ClearKybdMacro

<!-- src: Command_ClearKybdMacro.htm -->

ClearKybdMacro

### Function
This command will clear out any macro keys that have been defined by the LoadKybdMacro or LoadDbKybdMacro commands since the script started.

### Syntax
```text
ClearKybdMacro
```

**ClearKybdMacro Usage**

All macro keys are cleared out when the script is started.

**ClearKybdMacro Example**

This command may be used if the LoadKybdMacro command were issued, but the response from the PMS system or the third party system timed out; the ClearKybdMacro would be used to clear the macro in preparation for a rebroadcast or transaction cancel.

```isl
event inq:1
  loadkybdmacro…
  .
  .
  .
  txmsg "inq_1_request"
  wait for rxmsg
endevent

event rxmsg: _timeout
  errormessage "Inquiry Timeout"
  clearkybdmacro
endevent
```

See also:

LoadDbKybdMacro

LoadKybdMacro

---

## ClearRearArea

<!-- src: Command_ClearRearArea.htm -->

ClearRearArea

**ClearRearArea Usage**
Command to clear the rear display and reset the @sustaincustomtext SIM variable.

**ClearRearArea** Sample

```isl
event SignIn
event inq = 1
DisplayRearArea = "Hello"
WaitForClear "Press clear to clear display"
ClearRearArea
endevent
```

---

## Command Category Communications

<!-- src: Command_Category_Communications.htm -->

GetRxMsg
RxMsg
TxMsg
Use[Compat/ISL]Format
Use[ISL/STD]TimeOuts
WaitForRxMsg

---

## Command Category File I/O

<!-- src: Command_Category_File_I_O.htm -->

FClose
FOpen
FRead
FReadBfr
FReadLn
FSeek
FWrite
FWriteBfr
FWriteLn

---

## Command Category Flow control

<!-- src: Command_Category_Flow_control.htm -->

Break
Call
ContinueOnCancel
Event...EndEvent
ExitCancel
ExitContinue
ExitOnCancel
ExitWithError
For...EndFor
ForEver...EndFor
If...Else[If]...EndIf
```isl
MSleep
Return
Sub... EndSub
WaitForClear
WaitForConfirm
WaitForEnter
While...EndWhile
```

---

## Command Category Input / Output

<!-- src: Command_Category_Input_Output.htm -->

Beep
ClearIslTs
Display
DisplayInput
DisplayInverse
DisplayIslTs
DisplayMSInput
EditDetail
ErrorBeep
ErrorMessage
GetEnterOrClear
InfoMessage
Input
InputKey
ListDisplay
ListInput
Prompt
RegIdleEvent
SetIslTsKeyx
Touchscreen
VoidDetail
Window
WindowClear
WindowClose
Window[Edit/Input][WithSave]
WindowScrollDown
WindowScrollUp

---

## Command Category Miscellaneous

<!-- src: Command_Category_Miscellaneous.htm -->

DLLCall
DLLCall_CDECL
DLLFree
DLLLoad
Item Discount
LoadDbKybdMacro
LoadKybdMacro
LoadMAGInfo
SaveChkInfo
SaveRefInfo

---

## Command Category Printing

<!-- src: Command_Category_Printing.htm -->

LineFeed
ListPrint
PrintLine
StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Command Category Variables

<!-- src: Command_Category_Variables.htm -->

ClearArray
```isl
DiscardGlobalVar
Event Pretender
Format
FormatBuffer
FormatQ
LowerCase
MakeAscii
Mid
ProRate
RetainGlobalVar
SetSignOn[Left/Right]
SetString
Split
SplitQ

System
UpperCase
UseFilteredDetail
UseUnFilteredDetail
Var
```

---

## Command: Beep

<!-- src: Command_Beep.htm -->

Beep

### Function
This command can be used to sound the beeper at a UWS. It should be used for operator confirmation or notification. Note that a separate ErrorBeep command is provided to notify the operator of errors.

### Syntax
```text
Beep
```

**Beep Usage**

The Disable Error Beep option in the User Workstation form is ignored when this command is used.

See also: ErrorBeep

---

## Commands by Category

<!-- src: Command_by_Category.htm -->

Commands by Category       <body> <p>This page uses frames, but your browser doesn't support them.</p> </body>

---

## ContinueOnCancel

<!-- src: Command_ContinueOnCancel.htm -->

ContinueOnCancel

### Function
This command will continue processing the script even if the [Cancel] or [Clear] key is pressed after an Input command is issued.

### Syntax
```text
ContinueOnCancel
```

**ContinueOnCancel Usage**
- In normal operations, when ISL is waiting for user data after an Input command is issued (i.e., Input, WindowInput, WindowEdit,...) and the user presses the [Cancel] key or the [Clear] key at the input prompt, the script will terminate. It may be necessary for the script to continue even if the user has cancelled the entry. If the ContinueOnCancel command is executed, then the Input commands will not terminate the script if the [Cancel] key or the [Clear] key is pressed. Instead, they will return to the line after the Input command. The @Inputstatus system variable will be set to 0 if the user cancelled the input, or 1 if valid data was entered.
- If the ContinueOnCancel is used, the script should check all Input commands to determine if the user cancelled the input or not.

See also:

ExitCancel

ExitOnCancel

Input

Window[Edit/Input][WithSave]

---

## Debug

<!-- src: Command_Debug.htm -->

Debug

(not used)

---

## DiscardGlobalVar

<!-- src: Command_DiscardGlobalVar.htm -->

DiscardGlobalVar

### Function
These commands instruct the ISL to discard all global variable values in between transactions.

### Syntax
```text
DiscardGlobalVar
```

**DiscardGlobalVar Usage**
This command is global, which means it remains in affect until the alternative command is used or until the script file has been changed (i.e., until a new script is downloaded to the UWS).
The default action is to discard the global variable values after each event.

---

## Display

<!-- src: Command_Display.htm -->

Display

### Function
This command can be used to display a message in a window.

### Syntax
```text
(entered as a single line)
Display row, column, expression[{output_specifier}]
[, expression[{output_specifier}]...]
```

### Argument/Description
**row**  - the integer expression specifying the screen row within the defined window where the message will be displayed
**column**  - the integer expression specifying the screen column within the defined window where the message will be displayed
**[expression]**  - an expression to be displayed; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**Display Usage**
- Since this command provides information about where to locate the text or fields within the window, a Window command must be executed prior to this command.
- The Display row and column must fall within the boundaries of the defined window.
- An error will occur if the data to be displayed extends past the end of the window:

```isl
window 10, 10, "10 columns"

display 1, 1, "this line is greater than 10 columns" //ERROR!
```
- The Display command can be used to display line drawing graphics characters. These characters will allow you to build other windows within ISL-defined windows (e.g., Window command).

**Display Example**

The following script will display a guest room number and name in a window:

```isl
event rxmsg : room_info
  var room_num : a5
  var guest_name : a20
  xmsg room_num, guest_name
  window 1, 40
  display 1, 2, "The guest in room ", room_num, " is ", guest_name
  waitforclear
endevent
```

See Also:

```isl
Chr Function

Window
```

---

## Display_Rear_Area

<!-- src: Command_Display_Rear_Area.htm -->

Display_Rear_Area

### Function
Command to display up to 40 characters in the rear display until the end of the event unless the @sustaincustomtext SIM variable is used.

### Syntax
```text
DisplayRearArea
```

**Display_Rear_Area Example**
```isl
event SignIn
  var msg: a80 = “ “
  @sustaincustomtext = 1
  format msg as @tremp, “signed in”
  DisplayRearArea msg
endevent
```

---

## DisplayInput

<!-- src: Command_DisplayInput.htm -->

DisplayInput

### Function
This command defines an input field within a window. Thus, a Window command must be executed prior to this command. In addition, a WindowEdit or WindowInput must follow it, or the grouping of DisplayInput commands to which it belongs.

### Syntax
```text
(entered as a single line)
DisplayInput row, column, input_variable[{input/output_specifier}], prompt_expression[, prompt_expression,...]
```

### Argument/Description
**row**  - the integer expression specifying the screen row within the defined window where the input_variable will be displayed
**column**  - the integer expression specifying the screen column within the defined window where the input_variable will be displayed
**input_variable**  - an array_variable or user_variable that allows user input
**{input/output_specifier}**  - one or more of the input/output specifiers that determine the format of all input and output fields
**prompt_expression**  - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation

**DisplayInput Usage**
- The DisplayInput row and column must fall within the boundaries of the defined window.
- The prompt_expression is required.
- DisplayInput can be used with the WindowEdit\Input commands to build a screen of input fields in order to accept input from the user. Navigating among the input fields is achieved with the movement keys: up arrow, down arrow, home, and end. You can also navigate with [Enter], which moves the focus to the next field, and [Clear], which moves the focus to the previous field.
- When a WindowEdit or WindowInput command is executed, each field displayed using the DisplayInput command will be edited in turn.
- The DisplayInput, DisplayMSInput, Input, and InputKey commands are the only commands that act on both the Input and Output Specifiers.
- The maximum number of window input entries allowed is 64.
- If the input_variable to be displayed extends past the end of the window, then an error will occur on the WindowEdit or WindowInput command, and not the DisplayInput command.

**DisplayInput Example**

The following script will allow input of customer information in a window:
```isl
event inq : 1
  var rowcnt: n3
  var field_name[5] : a15
  var customer_info[5] : a20
  field_name[1] = "Customer name:"
  field_name[2] = "Company:"
  field_name[3] = "Address:"
  field_name[4] = "City:"
  field_name[5] = "Phone:"

  window 5, 36
  for rowcnt = 1 to 5
    display rowcnt, 2,
    field_name[rowcnt]
    displayinput rowcnt, 16, customer_info[rowcnt],\
    "Enter ", field_name[rowcnt]
  endfor
  windowedit
endevent
```

See also:

Window

Window[Edit/Input][WithSave]

---

## DisplayInverse

<!-- src: Command_DisplayInverse.htm -->

DisplayInverse

### Function
This command can be used to display a message in a window in inverse video. Since this command provides information about where to locate the text or fields within the window, a Window command must be executed prior to this command.

### Syntax
```text
(entered as a single line)
DisplayInverse row, column, expression[{output_specifier}] [, expression[{output_specifier}]...]
```

### Argument/Description
**row**  - the integer expression specifying the screen row within the defined window where the input_variable will be displayed
**column**  - the integer expression specifying the screen column within the defined window where the input_variable will be displayed
**expression**  - an expression to be displayed; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**DisplayInverse Usage**
- The DisplayInverse row and column must fall within the boundaries of the defined window.
- An error will occur if the data to be displayed extends past the end of the window:

```isl
window 10, 10, "10 columns"

displayinverse 1, 1, "this line is greater than 10 columns" //ERROR!
```

**DisplayInverse Example**

The following script will display a guest room number and name in a window:
```isl
event rxmsg : room_info
  var room_num : a5
  var guest_name : a20
  rxmsg room_num, guest_name
  window 1, 50
  displayinverse 1, 2, "The guest in room ", room_num, " is ", guest_name
  waitforclear
endevent
```

See also:

Display

Window

---

## DisplayIslTs

<!-- src: Command_DisplayIsITs.htm -->

DisplayIslTs

### Function
This command displays a touchscreen defined by the SetIslTsKey command.

### Syntax
```text
DisplayIslTs
```

**DisplayIslTs Usage**

After a touchscreen has been displayed, its keys remain defined until cleared by the ClearIslTs command or until the script terminates.

**DisplayIslTs Example**

The subroutine below first clears any previously defined touchscreen keys and displays two touchscreen keys, [YES] and [NO], using the DisplayIslTs command. This subroutine displays these keys as the operator is issued a prompt by the system and captures the operator's input.

```isl
sub get_yes_or_no( ref answer, var prompt_s:A38 )
  var keypress : key
  var data : A20
  clearislts
  setisltskey 2, 2, 4, 4, 1, @Key_Enter, "YES"
  setisltskey 2, 6, 4, 4, 1, @Key_Clear, "NO"
  displayislts
  inputkey keypress, data, prompt_s
  if keypress = @Key_Enter
    answer = 1
  else
    answer = 0
  endif
endsub
```

See also:

CleatIsITs

SetIsTSKey

SetIsTSKeyx

---

## DisplayMSInput

<!-- src: Command_DisplayMSInput.htm -->

DisplayMSInput

### Function
This command defines an input field within a window; therefore, a Window command must be executed prior to this command, and a WindowEdit or WindowInput must follow it. This command defines an input field within a window that may be entered through the keyboard or touchscreen, or by swiping a magnetic card through the magnetic card reader on the UWS.

### Syntax
```text
(entered as a single line)
DisplayMSInput row, column, input_variable [{input/output_specifier}], prompt_expression[, row, column, input_variable[input/output_specifier], prompt_expression,...]
```

### Argument/Description
**row**  - the integer expression specifying the screen row within the defined window where the input_variable will be displayed
**column**  - the integer expression specifying the screen column within the defined window where the input_variable will be displayed
**input_variable**  - an array_variable or user_variable that allows user input**{input/output_specifier}**  - one or more of the input/output_specifiers that determine the format of all input and output fields
**prompt_expression**  - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function. equation

**DisplayMSInput Usage**
- This command allows the designer to specify the fields that the operator can enter manually, fields that may be entered from a magnetic card swipe, or fields that may be entered in both fashions. In addition, the location and length of the data to be used on the magnetic card stripe may also be defined.
- After the WindowInput command is executed, the system variable @MAGSTATUS will be set to Y if the magnetic card was swiped during the WindowInput. It will be set to N if a magnetic card was not swiped. To use @MAGSTATUS in this way, use only one DisplayMSInput command with each WindowInput entry (otherwise, @MAGSTATUS will be undefined). If more than one DisplayMSInput command is needed, use the Len function to check if the input string is set to zero.
- The prompt_expression is required.
- DisplayMSInput can be used with the WindowEdit\Input commands to build a screen of input fields in order to accept input from the user. Navigating among the input fields is achieved with the movement keys: up arrow, down arrow, home, and end. You can also navigate with [Enter], which moves the focus to the next field, and [Clear], which moves the focus to the previous field.
- The DisplayInput, DisplayMSInput, Input, and InputKey commands are the only commands which act on both the Input and Output Specifiers
- The maximum window input entries allowed is 64.
- If the input_variable to be displayed extends past the end of the window, then an error will occur on the WindowInput command, and not the DisplayInput command.
- In the case where row and column is 0, the input field (e.g., account_num) is considered hidden and will not be displayed; additionally, it can only be satisfied with a magnetic card, which means no keyboard input is allowed.

```isl
displaymsinput 0, 0, account_num{m2, 1, 1, *},\
```

"Enter Account Number",...
There can be more than one hidden field in a DisplayMSInput

command. In most cases, the input specification for this field
will contain magnetic stripe information.
- The prompt_expression for all hidden field(s) will be ignored.

**DisplayMSInput Example**

The following script will read the information from Track 2 of a credit card:

```isl
event inq : 1
  var account_num : a19
  var expiration_date : n4
  var track2_data : a79
  window 3, 78
  displaymsinput 1, 2, account_num{m2, 1, 1, *}, "Enter Account Number",\
  2, 2, expiration_date{m2, 2, 1, 4}, "Enter Expiration"
  windowinput
  waitforclear
endevent
```

See also:

```isl
Len Function

Window

Window[Edit/Input][WithSave]
```

---

## DLLCall

<!-- src: Command_DLLCall.htm -->

DLLCall

### Function
This command is used to call a function contained in the DLL.

Note: Please refer to the 3700 System Interface Module Manual for more information on 3700 DLL Support.

### Syntax
```text
(entered as a single line)
DLLCall handle, function_name ( [parm1 [parm2 [parm3...] ] ] )
```

### Argument/Description
**handle**  - N9 variable that is returned from the DLLLoad command
**name** - string expression used to identify the function
**parm#**  - optional parameters

**DLLCall Usage**

This command performs two functions:
- The first is to get the address of the function using the Windows GetProcAddress() function. If this function fails, then an ISL error will be generated.
- The second is to call the DLL function.
- It is not possible for a DLL to check the validity of the parameters, it is up to the SIM script writer to insure that the proper number and type are used.
- It is not possible for the DLL to return a value. More specifically, if one is returned, it is ignored.
- Passing information back to the SIM script should be done using reference parameters.

Note: Please see the 3700 System Interface Module (SIM) Manual for more information on 3700 DLL Support.

---

## DLLCall_CDECL

<!-- src: Command_DLLCall_CDECL.htm -->

DLLCall_CDECL
### Function
This command is used to call a function contained in the DLL using CEDC conventions.

Note: Please refer to the 3700 System Interface Module Manual for more information on 3700 DLL Support.

See also:

DLLCall

---

## DLLFree

<!-- src: Command_DLLFree.htm -->

DLLFree

### Function
This command is used to free a loaded DLL.

Note: Please refer to the 3700 System Interface Module Manual for more information on 3700 DLL Support.

### Syntax
```text
DLLFree handle
```

### Argument/Description
**handle**  - N9 variable that is returned after the DLL is loaded

**DLLFree Usage**

This command is automatically called when OPS exits, or the SIM script is reread. It can be called to free up resources loaded by the DLL.

---

## DLLLoad

<!-- src: Command_DLLLoad.htm -->

DLLLoad

### Function
This command loads an external DLL. It needs to be called only once during the lifetime of the SIM script.

Note: Please refer to the 3700 System Interface Module (SIM) Companion Guide for more information on 3700 DLL Support.

### Syntax
```text
DLLLoad handle, name
```

### Argument/Description
**handle**  - N9 variable that is returned after the DLL is called
**name**  - string expression used to identify the DLL

**DLLLoad Usage**
- This command is a wrapper around the Windows LoadLibrary() function. All rules that apply to path settings, apply here.
- When using SIM on a CE platform, be sure to include the full path to the DLL in the script. Do not place the DLL in the Windows folder as this folder is not saved to disk during reboot.
- If the DLL is already loaded, then Windows will prevent it from being loaded again.
- If the command fails, then dll_handle will be 0. If not, then dll_handle is the handle used for any further accesses for the other DLL functions.
- The ‘name’ parameter is used to identify the DLL, and the resulting handle is stored in the ‘handle’ variable. An example of this would be:

```isl
var dll_handle:N9
DLLLoad dll_handle, "myops.dll"
```

---

## EditDetail

<!-- src: Command_EditDetail.htm -->

EditDetail

**This feature not implemented as of version 2.5**

### Function
This command, when passed an array of menu item object numbers and an array of corresponding menu item price levels, displays those menu items in a pop-up window over the transaction summary window. The user can then choose from the displayed menu items by moving a highlight among them and pressing [Enter] when the highlight is on the desired menu item.

### Syntax
```text
(entered as a single line)
EditDetail num_detail, object_number_list[], price_level_list[]
```

### Argument/Description
**num_detail** - integer expression evaluating to the number of elements in the array's object_number_list[] and price_level_list[]
**object_number_list[]**  - an array of N9 integers corresponding to the object numbers of the detail to be edited
**price_level_list[]**  - an array of N1 integers corresponding to the price levels of the detail to be edited

```isl
EditDetail Usage
```

The Edit Detail Feature
EditDetail is the ISL command that must be executed in order to enable the Edit Previous Order feature. This feature uses SIM to recall a customer's last guest check from a third-party database. Once recalled, some or all of the detail items from that previous guest check can then be posted to the current guest check.

The obvious benefit of such a feature is that it is a time-saving and more efficient procedure for performing POS transactions in environments where speed of service is critical, particularly in a delivery service environment. For instance, in the case of a pizza delivery system, a customer may always order the same size pizza, with the same toppings. Instead of re-entering the same information, the operator can query the third-party database for the customer's previous guest check and use this existing order information.
- In order to retrieve previous order menu item detail, the EditDetail command must be executed by the ISL to call the Edit Detail procedure. The design of the script should be such that the operator is prompted to enter customer information and query the third-party system for the previous order history associated with the customer. For instance, in the implementation of a delivery system.
- A SIM Inquiry key must be pressed by an operator after beginning a guest check, for example.
- The procedure may begin by requiring an operator to collect the name or telephone number of the customer who calls in an order.
- After which, the third-party system would be queried by the 3700 System for this customer information, including any previous order history belonging to the customer.
- And finally, the delivery system would send the results of its query to the 3700 System, which would include the name, address, and directions, to the customer's residence or workplace, as well as the customer's previous order history.
- Once the previous order information is retrieved by the EditDetail call, all control of the information, functions keys, etc., return to the 3700 System and are not determined by the ISL.

Operational Procedures

Previous Guest Check Detail
Previous order information is menu item detail stored by a third-party system that can be sent to the 3700 System for editing. For example, in the case of a delivery system interfaced with the 3700 System, a customer's complete order history may be stored in the delivery system's database. This information can then be retrieved using the EditDetail command and placed in the transaction detail of an open guest check.

Displaying Previous Order History

A customer calls Personal Pizza and says, "This is Joe Decker. Give me my usual order, please."
The employee replies, "Good evening, Mr. Decker," and presses the [Delivery] key on the UWS. In this system’s database, the [Delivery] key is actually one of the SIM keys. The [Delivery] key generates a SIM script. This SIM script is programmed to display an entry box that prompts for the customer’s name. The operator enters Decker, and the script executes a search in the third-party database.

Result:
If the query is successful, The search finds a matching record, and the script prompts for confirmation.

All previous order history information is displayed. The first menu item will be highlighted in inverse video.

Selecting Previous Order Menu Items
The employee can perform any of the following actions:
- Press [Enter] to post a highlighted menu item to the new check.
- Press the [Up] or [Down] arrow keys to move through the detail of the previous check.
- Press [Edit Detail, Transfer All] to post the entire contents of the previous check to the new check.
- Press [Clear] to reject all menu items on the previous check, and display an order screen.
- To display the previous order history again, you must initiate the EditDetail procedure again. That is, the operator would need to execute an ISL event that retrieves the previous order history information.

The customer says, "Give me everything I ordered last time, except for the mineral water."
The employee can highlight each menu item from the previous check except for the mineral water, and post each one individually.
Instead, the employee presses [Edit Detail, Transfer All] to post all menu items to the new check. She highlights the mineral water on the new check, and presses [Void] to remove it.
The employee then presses [Clear] to exit this screen, and return to the UWS main menu screen.

**EditDetail Example**

Use the script below to demonstrate the EditDetail command without interfacing with a third-party system. Begin a check, enter menu items, then execute this ISL event. All menu item detail will appear in the previous order window.

```isl
event inq : 7
  var cnt : n3
  var mi_mlvl [ @numdtlt ] : n1
  var mi_slvl [ @numdtlt ] : n1
  var mi_lvl[ @numdtlt ] : n3
  var mi_obj[ @numdtlt ] : n5
  var mi_cnt : n3 = 0
  touchscreen 3
  if @cknum = 0
    exitwitherror "Begin a check and try again"
  endif
  for cnt = 1 to @numdtlt
    if @dtl_type[ cnt ] = "M"
      mi_cnt = mi_cnt + 1
      mi_lvl[ mi_cnt] = @dtl_plvl[ cnt ]
      mi_obj[ mi_cnt ] = @dtl_objnum[ cnt ]
    endif
  endfor
  editdetail mi_cnt, mi_obj, mi_lvl
endevent
```

---

## ErrorBeep

<!-- src: Command_ErrorBeep.htm -->

ErrorBeep

### Function
This command can be used to sound the error beeper at the UWS.

### Syntax
```text
ErrorBeep
```

**ErrorBeep Usage**

The error beep must be enabled in the User Workstation form.

See also:

Beep

---

## ErrorMessage

<!-- src: Command_ErrorMessage.htm -->

ErrorMessage

### Function
This command can be used to display an error message at the UWS when an incorrect entry is made by the operator.

### Syntax
```text
(entered as a single line)
ErrorMessage expression[{output_specifier}][, expression
[{output_specifier}]...]
```

### Argument/Description
**expression** - an expression to be displayed; it may be one of the following: user_variable system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**ErrorMessage Usage** The ErrorMessage command expects one error line of up to 38 characters to be displayed. However, the UWS displays two lines. The error line to be displayed is broken up between the two logical lines. If the line is too long to be displayed, an error occurs.

**ErrorMessage Example**

The following script will display a message indicating that an entry is invalid:

```isl
event inq : 1
var menu_choice : n3
window 3, 23
display 1, 2, "[1] Edit member info"
display 2, 2, "[2] Add new member"
display 3, 2, "[3] Exit"
forever
input menu_choice, "Choose a number and press [ENTER]."
if menu_choice < 1 OR menu_choice > 3
errormessage "Choice [" , menu_choice, "]is outside the valid",\
" range"
else
break
endif
endfor
endevent
Event...EndEvent
```

---

## Event...EndEvent

<!-- src: Command_Event...EndEvent.htm -->

Event...EndEvent

___________________________________________________________________________________

Event Begin_Check |  Event Idle_No_Trans |  Event Svc |

Event ClockIn |  Event Init |  Event Svc_Error_Correct_Items |

Event ClockOut |  Event Inq |  Event Svc_Void |

Event Dsc |  Event Pickup_Check |  Event Tmed |

Event Dsc_Error_Correct_Items |  Event Print_Header/Trailer |  Event Tndr |

Event Dsc_Void |  Event Rxmsg |  Event Tndr_Error_Correct Items |

Event Dtl_Changed |  Event SignIn |  Event Tndr_Void |

Event Exit |  Event SignOut |  Event Trans_Cncl |

Event Final_Tender |  Event Srvc_Total |    |

___________________________________________________________________________________

### Function
The Event command indicates the start of a procedure associated with an operator inquiry, payment, or an interface response message. The EndEvent indicates the end of the event procedure. There are several different Events available for 3700 SIM. They are listed above.
- If the * specifier is present in an Event line, in the Event ID field, then the Event will be executed if the Event types match, regardless of the Event ID. The * event is used only if there is not a matching event that explicitly defines Event ID. The * specifier affects the following events: Inq, Tmed, Srvc_Total, and RxMsg. For example, the following Event will catch all RxMsg Events:

```isl
event rxmsg : *
endevent
```

**Caution**

If the *event command is placed before a specific event, OPS will not read any text entered after the *. Therefore, any code written after the * will be ignored and your program will not work as expected. When using the *event command, make sure to place it at the end of the ISL file.
- It is possible to write an Event Inq or Event Tmed as an expression. For example:

```isl
event inq : 5
```
can be defined as:
```isl
event inq : ( 2 + 3 )
```
- Variables may also be used, but must be defined as global variables. For example:

```isl
var guest_inq_number : N5 = 5
event inq : guest_inq_number
```
- The EndEvent command cannot be used within a subroutine.

---

## ExitCancel

<!-- src: Command_ExitCancel.htm -->

ExitCancel

### Function
This command should be used to exit the current script and cancel the current POS tendering operation.

### Syntax
```text
ExitCancel
```

**ExitCancel Usage**

This command might be useful if charge posting was denied.

**ExitCancel Example**

The following example will either allow a check to be tendered to a room charge or prevent the room charge from being posted:

```isl
event tmed : 9
  var room : a6
  var guest_name : a20
  window 4, 22, "Room Charge"
  displayinput 2, 2, room, "Enter room number"
  displayinput 3, 2, guest_name, "Enter guest name"
  windowinput
  txmsg "room_charge", room, guest_name
  waitforrxmsg
endevent

event rxmsg : post_response
  var status : a10
  var room : a6
  var guest_name : a40
  rxmsg status, room, guest_name
  if status = "accept"
    exitcontinue
  elseif status = "deny"
    errormessage "Room charge denied"
    exitcancel
  else
    call get_more_info( room, guest_name )
  endif
endevent
```

---

## ExitContinue

<!-- src: Command_ExitContinue.htm -->

ExitContinue

### Function
This command should be used to end the current script and continue processing the POS tendering operation.

### Syntax
```text
ExitContinue
```

**ExitContinue Usage**
- This might be useful if tendering should continue after a guest charge is approved.
- Do not confuse the ExitContinue command with the EndEvent command. EndEvent acts as both an Event procedure delimiter and an implicit ExitContinue. Do not use the EndEvent command instead of the ExitContinue command.

**ExitContinue Example**

The following example will either allow a check to be tendered to a room charge or prevent the room charge from being posted:

```isl
event tmed : 9
  var room : a6
  var guest_name : a20
  window 4, 22, "Room Charge"
  displayinput 2, 2, room, "Enter room number"
  displayinput 3, 2, guest_name, "Enter guest name"
  windowinput
  txmsg "room_charge", room, guest_name
  waitforrxmsg
endevent

event rxmsg : post_response
  var status : a10
  var room : a6
  var guest_name : a40
  rxmsg status, room, guest_name
  if status = "accept"
    exitcontinue
  elseif status = "deny"
    errormessage "Room charge denied"
    exitcancel
  else
    call get_more_info( room, guest_name )
  endif
endevent
```

See also:

ContinueOnCancel

ExitCancel

ExitOnCancel

---

## ExitOnCancel

<!-- src: Command_ExitOnCancel.htm -->

ExitOnCancel

### Function
This command will exit the script when the [Cancel] key or the [Clear] key is pressed after an Input command has been issued.

### Syntax
```text
ExitOnCancel
```

See also:

ContinueOnCancel

ExitCancel

ExitContinue

---

## ExitWithError

<!-- src: Command_ExitWithError.htm -->

ExitWithError

### Function
This command is used to display an error message and cancel the current POS tendering operation.

### Syntax
```text
(entered as a single line)
ExitWithError error_message[{output_specifier}] [, error_message [{output_specifier}]...]
```

### Argument/Description
**error_message** - an expression displayed in the error banner, usually to instruct the user of a problem; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**ExitWithError Usage**
The error_message is required.

**ExitWithError Example**

The following script illustrates how this command will display an error if a charge is denied:

```isl
event rxmsg : charge_declined
  var room_num : a4
  rxmsg room_num
  exitwitherror "Charge for room ", room_num," declined"
endevent
```

---

## FClose

<!-- src: Command_FClose.htm -->

FClose

### Function
This command closes a file that was previously opened by the FOpen command.

### Syntax
```text
FClose file_number
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened

**FClose Usage**
- The file_number specified must be a valid file number. That is, it must correspond to a file already opened. Otherwise, an error message will be generated.
- All files are automatically closed at the end of a script.

**FClose Example**
The following example would open a file, read from it, and then close it:

```isl
event inq: 1
  var fn : n5
  fopen fn, "\3700\etc\emplist.dat", read
  .
  .
  .
  fclose fn
endevent
```

See also:

FOpen

---

## FOpen

<!-- src: Command_FOpen.htm -->

FOpen

### Function
This command opens a file for reading or writing.

### Syntax
```text
(entered as a single line)
FOpen file_number, file_name, [Append] [And] [Read] [And]
[Write]
```

### Argument/Description
**file_number** - an integer variable which will be assigned a file number to identify the file
**file_name**  - a string which identifies the file to be opened
Append - a mode separator that appends to an open file
And - required by syntax if more then one mode separator is issued
Read - a mode separator that reads from an open file
Write - a mode separator that writes to an open file

**FOpen Usage**
- The variable file_number will be assigned a value of 0 if the operation was unsuccessful. This could occur if the file was opened for reading and did not exist, or the permissions of the file were not set correctly.
- The System Variable @File_Errnum will contain the operating system error code corresponding to the error which occurred when FOpen was executed.

**FOpen Example 1**
The following statements would open a file and read it:
```isl
var fn : N5
//open a file for reading
fopen fn, "\3700\data\emplist.dat", read
```

**FOpen Example 2**
The following statement would open a file and append to it:
```isl
var fn : N5 //open a file for appending.
fopen fn, "\3700\etc\transact.log", append
```

**FOpen Example 3**
The following statement would open a file and write to it:
```isl
var fn : N5 //create a file for writing
fopen fn, "\3700\etc\ws.log", write
```

**FOpen Example 4**
The following statement would open a file then read and write to it:
```isl
var fn : N5 //open a file for reading and writing
fopen fn, "\3700\data\emplist.dat", read and write
endevent
```

**FOpen Example 5**
The following script will open a file. If the open was unsuccessful, an error message will display the cause of the error.
```isl
event inq : 1
  var fn : N5
  fopen fn, "myfile.dat", read
  if fn = 0
    errormessage @File_errstr
    exitcontinue
  endif
endevent
```

See also:

FClose

---

## For...EndFor

<!-- src: Command_For...EndFor.htm -->

For...EndFor

### Function
These commands are used to implement an iterative loop. The EndFor command should always be used to terminate the loop.

### Syntax
```text
For counter = start_expression To end_expression [Step increment]
..
..
..
EndFor
```

### Argument/Description
**counter** - a variable that is incremented by the For command
**start_expression**  - the first variable in the counter; separated from counter by = sign; it can be one of the following: user_variable, system_variable (N or $ format), constant, function ...=...To ...[Step...] required by syntax
**end_expression**  - the last variable in the counter; separated from the start expression by the reserved word To; it can be one of the following: user_variable, system_variable (N or $format), constant, function
**increment** - used with the reserved word Step to increase or decrease the value of the counter; use a negative value to decrease the counter

**For...EndFor Usage**
- Normally, the variable in the For loop will be incremented by one. If required, the Step feature may be used to override this so that the variable may be incremented or decremented by any integer value.
- For loops work similar to C and Basic; the For loop counter will always increment to the end_expression + 1. A For loop will execute when the following conditions are met:

```isl
If Step > 0 and counter <= end_expression
If Step < 0 and counter >= end_expression
Sample For commands:
for i = 1 to 10 // execute 10 times
for i = 1 to 10 step 5 // execute 2 times (i=1,6)
for i = 1 to 10 step -5 // will not execute
for i = 10 to 1 // will not execute
for i = 10 to 1 step -1 // execute 10 times
for i = 10 to 1 step -5 // execute 2 times (i=10,5)
```

**ForEver...EndFor Example**

The following script will wait for a magnetic card swipe:
```isl
event inq : 1
  var mag_card_track2_data : a79
  window 1, 28
  // build the window
  forever // loop until the user swipes a
    // card or presses clear
    displaymsinput 1, 0, mag_card_track2_data{m2, 1, 4, *}, " "
    display 1, 2, "Please swipe your ID card."
    windowinput
    if @MAGSTATUS = "Y" // we got a swipe
      windowclose // close the window
      break // and exit the loop
    endif
    errormessage "Swipe card or press clear twice"
  endfor
endevent
```

See also:

Break

ForEver...EndFor

---

## ForEver...EndFor

<!-- src: Command_ForEver...EndFor.htm -->

ForEver...EndFor

### Function
The ForEver command provides continuous looping capabilities in a script. The ForEver command is generally used when the conditions for terminating the loop are too complex for a For command, or may not be known ahead of time. This loop may be broken by executing a Break command or by exiting the script (e.g., ExitCancel or ExitContinue).

### Syntax
```text
ForEver
.
.
.
EndFor
```

**ForEver...EndFor Example**

The following script will wait for a magnetic card swipe:
```isl
event inq : 1
  var mag_card_track2_data : a79
  window 1, 28
  // build the window
  forever // loop until the user swipes a
    // card or presses clear
    displaymsinput 1, 0, mag_card_track2_data{m2, 1, 4, *}, " "
    display 1, 2, "Please swipe your ID card."
    windowinput
    if @MAGSTATUS = "Y" // we got a swipe
      windowclose // close the window
      break // and exit the loop
    endif
    errormessage "Swipe card or press clear twice"
  endfor
endevent
```

See also:

```isl
Break

ExitCancel

ExitContinue

Return
```

---

## Format

<!-- src: Command_Format.htm -->

Format

### Function
This command is used to concatenate expressions into a string variable.

### Syntax
```text
(entered as a single line)
Format string_variable [, field_sep_char] As
expression[{output_specifier}]
[, expression[{output_specifier}],…]
```

### Argument/Description
**string_variable** - a place holder for text characters such as a user_variable (string)
**field_sep_char**  - the character used to separate fields; use the Chr function to define the character required
**as**  - required by syntax
**expression** - an expression to be concatenated; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**Format Usage**
If the field separator character is specified, then the first character in the string is used to separate variables within the string.

```isl
format string as 1, 2, 3 // will create '123'
format string, "," as 1, 2, 3 // will create '1,2,3'
```

**Format Example**

The following script will construct a string_variable containing
the current date in the form dd-mm-yy:

```isl
event inq : 1
  var date : a9
  call get_date_string
  window 3, len(date)+2
  display 2,2,date
  waiforclear
endevent

sub get_date_string
  var month_arr[12] : a3
  //Listing of all the months
  month_arr[1] = "JAN"
  month_arr[2] = "FEB"
  month_arr[3] = "MAR"
  month_arr[4] = "APR"
  month_arr[5] = "MAY"
  month_arr[6] = "JUN"
  month_arr[7] = "JUL"
  month_arr[8] = "AUG"
  month_arr[9] = "SEP"
  month_arr[10] = "OCT"
  month_arr[11] = "NOV"
  month_arr[12] = "DEC"
  format date as @DAY, "-", month_arr[@MONTH], "-", @YEAR
  // i.e., 10-NOV-93
endsub
```

See also:

FormatQ

Split

---

## FormatBuffer

<!-- src: Command_FormatBuffer.htm -->

FormatBuffer

### Function
This command will format a string containing non-printable characters into a string that is printable.

### Syntax
```text
(entered as a single line)
FormatBuffer source_string, destination_string
```

### Argument/Description
**source_string** - a string_variable containing non-printable characters
**destination_string**  - a place holder for the string_variable containing the printable characters

**FormatBuffer Usage**
- All printable characters will display as-is. All non-printable characters will be formatted as a two-digit hexadecimal number surrounded by angle brackets.
- This function is generally used to look at data from the PMS.

**FormatBuffer Example**
The following script will convert a string containing a non-printable character into a string that can be displayed:

```isl
event inq : 1
  var source_s : A30, dest_s : A30
  format source_s as "before: ", chr( 27 )
  waitforclear source_s //displays 'before: '
  format source_s as "after: ", chr( 27 )
  formatbuffer source_s, dest_s
  waitforclear dest_s //displays 'after: <1B>'
endevent
```

See also:

Format

FormatQ

---

## FormatQ

<!-- src: Command_FormatQ.htm -->

FormatQ

### Function
This command is used to concatenate variables into a string. String variables are automatically surrounded by quotes. This feature can be used to create comma-separated lines in ASCII files.

### Syntax
```text
(entered as a single line)
FormatQ string_variable [, field_sep_char] As
expression[{output_specifier}]
[, expression[{output_specifier}],…]
```

### Argument/Description
**string_variable** - a place holder for text characters such as a user_variable (string)
**field_sep_char**  - the character used to separate fields; use the Chr function to define the character required
**as**  - required by syntax
**expression** - an expression to be concatenated; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**FormatQ Usage**
- If the field separator character is specified, then the first character in the string is used to separate variables within the string.
- The FormatQ command operates in the same way as the Format command, except that all strings are automatically quoted. This command is generally used to format lines to a file.

See also:

Format

Split

---

## FRead

<!-- src: Command_FRead.htm -->

FRead

### Function
This command reads formatted data from a file.

### Syntax
```text
(entered as a single line)
FRead file_number, user_variable or list_spec[, user_variable or list_spec...]
```

### Argument/Description
**file_number** - identifies the file to be read; an integer variable which was assigned in the FOpen statement when the file was opened
**user_variable**  - a user_variable which will be assigned the data from the file
list_spec is defined as:
- number_records - a user_variable (integer) containing the number of records to be built from this string
- field_array [: field_array] - an array_variable that will hold one field per record; you can split a field into more than one array by separating the array_variables using a colon (:)

**FRead Usage**
- The file must be opened in Read mode in order to execute this command.
- If the System Variable @Strict_Args is set to 1, then ISL will ensure that the variable count in the FRead command line matches the number of fields in the file record. If an incorrect number of fields is specified in the statement or the file is corrupted, then an error message will be generated.
- It is possible to skip over fields in a line by not specifying the variables. For example the third field in the line below would be ignored:

```isl
fread file_number, variable1, variable2, , variable4
```
- If a script needs to read only the first few fields in a file, but wishes to ignore the rest of the fields, then it should specify a * in the statement to indicate that no more variables should be assigned to that line. For example, if each line in a file has 20 fields, but only the first three need to be read, the following line will only read the first three. All fields are assigned in the order they occur. The * must be the last element on the FRead line.

```isl
fread file_number, variable1, variable2, variable3, *
```
- This command will assign data to the variables a line at a time. If the line in the file has 10 variables and only 7 variables are specified, then the last 3 are thrown away. They are not read on the next FRead.
- The field delimiter is specified by the @file_separator variable.

**FRead Example**

If a file contains this line:
145,"Interlandi","Dan"
An ISL script uses the following lines to read the file:

```isl
event inq : 1
  var num:N5, last_name:A20, first_name:A20
  var file_number : n9
  fopen file_number, "example.dat", READ
  fread file_number, num, last_name, first_name
  fclose file_number
  window 3,50
  display 1,1,num //num will be 145
  display 2,1,last_name //last_name will be "Interlandi"
  display 3,1,first_name //first_name will be "Dan"
  waitforclear
endevent
```

See also:

FClose

File_Seperator

FOpen

FReadBfr

FReadLn

---

## FReadBfr

<!-- src: Command_FReadBfr.htm -->

FReadBfr

### Function
This command reads a block of data from a file.

### Syntax
```text
(entered as a single line)
FReadBfr file_number, data, count_to_read, count_read
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened
**count_to_read**  - how much data to read (bytes)
**count_read**  - how much data was actually read (bytes)
**data**  - identifies the file data string_variable the data block will read into

**FReadBfr Usage**
- The file must be opened in read mode in order to execute this command.
- This command will read data across lines.

**FReadBfr Example**

The following script will attempt to read 100 characters:

```isl
event inq : 1
  var fn : n5
  var data:A100, linesread:N5
  fopen fn, "\3700\etc\script.isl" READ
  freadbfr fn, data, 100, linesread
  if linesread <> 100
    errormessage "Tried to read 100 and read ", linesread
    exitcancel
  endif
endevent
```

See also:

FClose

FOpen

FRead

FReadln

---

## FReadLn

<!-- src: Command_FReadLn.htm -->

FReadLn

### Function
This command reads a line of data from a file.

### Syntax
```text
FReadLn file_number, line
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened
**line**  - identifies the file line string variable that the line will read into

**FReadLn Usage**
- The file must be opened in Read mode in order to execute this command.
- This command may be useful if the file being read does not store its data in comma-separated format.

**FReadLn Example**

The following script will display the message of the day:

```isl
event inq : 1
  var filename : a80 = "message.txt"
  var fn : n9
  var msg[10] : a79
  var i : n2 = 1
  fopen fn,filename, READ
  if fn = 0 or @FILE_ERRNO <> 0
    errormessage @FILE_ERRSTR
    exitcancel
  endif
  while not Feof(fn) and I <= 10
    freadln fn,msg[i]
    i = i + 1
  endwhile
  fclose fn
  window 10,78,"Message of the Day"
  for i = i + 1
    display i,@center,msg[i]
  endfor
  waitforclear
endevent
```

See also:

FClose

FOpen

FRead

FReadBfr

---

## FSeek

<!-- src: Command_FSeek.htm -->

FSeek

### Function
This command goes to a specified position in the file.

### Syntax
```text
FSeek file_number, seek_position
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened
**seek_position** - where to position the file pointer (specify the offset of the byte you want to position to)

**FSeek Usage**
- Whenever a file is opened, the file pointer is positioned at the start of the file. When data (a line or number of characters) is read or written, the file pointer is positioned at the end of the data that was read or written. The FSeek command allows the user to position the file pointer to an arbitrary point in the file so that the next read or write statement will act on the data or position following the new location of the file pointer.
- If a seek position of -1 is specified, the file pointer will be positioned to the end of the file.

**FSeek Example**

The following example gets a number from the user, then uses FRead to read the first field from each line, testing it against the number the user entered. Once the number is found using FSeek, the file pointer is positioned at the beginning of the line where the number was found. The entire line is read and the first 77 characters displayed for the user.
```isl
event inq : 1
  var fn : n3
  var fname : a30 = "\3700\sql\sql.out"
  var line : a200
  var objnum : n6
  fopen fn, fname, read //Open the file
  forever
    input objnum, "Enter number to search for" //Get number to search
    // for from user
    fseek fn, 1 // move file pointer
    // to beginning of file
    call find_obj( fn, objnum ) //Call the subroutine
    if objnum = 0 // if 0, no match was
      // found, break out
      break
    endif
    freadln fn, line //Read the line where
    // match found
    window 1, 78 //Open window
    display 1, 2, mid( line, 1, 77 ) //Display the line
    waitforclear
    windowclose //Close the window
  endfor
endevent

sub find_obj( ref fn, ref objnum )
  var current_position : n6
  var found_num : n6
  prompt "Searching, please wait..."
  while not feof( fn ) //Loop until end of
    //file encountered
    current_position = ftell( fn ) ` //Get the current file
    // pointer position
    fread fn, found_num, * //Fread the first field
    // only from the file
    if found_num = objnum //If it matches
      //what user entered
      fseek fn, current_position //Fseek to the beginning
      // of the line
      return //Exit the subroutine
    endif
  endwhile
  errormessage "Can't find that number" //If end of file is

  // encountered then
  objnum = 0 // we didn't find a
  // match, tell user, set
endsub // objnum = 0, and return
```

See also:

FClose

FOpen

---

## FWrite

<!-- src: Command_FWrite.htm -->

FWrite

### Function
This command writes formatted data to a file.

### Syntax
```text
(entered as a single line)
FWrite file_number, variable1 [, variable2][, variable3... ]
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened to identify the file
**variable n**  - variables which will be written to the file, where n is the number of variables to write

**FWrite Usage**
- The file must be opened in Write mode in order to execute this command.
- All strings on the FWrite line will be enclosed in quotes.
- This function will write one line of data to the file. The line will be terminated with the standard new line character.
- The fields will be delimited with the @file_separator character.

**FWrite Example**

The following statements will write a single line of data to 3 different
lines:

```isl
fwrite fn, 1, 500, "line 1"
fwrite fn, 2, 501, "line 2"
fwrite fn, 3, 502, "line 3"
```

The above statements will produce the lines below in the data file:

1,500,"line 1"
2,501,"line 2"
3,502,"line 3"

See also:

FClose

FOpen

FWriteBfr

FWriteLn

---

## FWriteBfr

<!-- src: Command_FWriteBfr.htm -->

FWriteBfr

### Function
This command writes formatted data to a file.

### Syntax
```text
(entered as a single line)
FWriteBfr file_number, data, count_to_write, count_written
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened
**count_to_write**  - how much data to write
**count_written**  - how much data was actually written
**data**  - identifies the file data string variable to write

**FWriteBfr Usage**
- The file must be opened in Write mode in order to execute this command.
- This command will write data across lines.

**FWriteBfr Example**

This example reads from a file one character at a time, capitalizes the character as long as it is not in a quoted string, and, if the character was changed, writes the new character back to the position in the file where its lowercase counterpart was found.

```isl
event inq : 1
  var fn : n3 = 1
  var fname : a40 = "\3700\etc\temp1.dat"
  var ritecnt : n5 = 1
  var rotecnt : n5
  var char : a20
  var fpos : n6
  var aschar : n3
  var inquotes : n3
  var changed : n3
  fopen fn, fname, read and write //Open the file for
  // read and write
  if fn = 0 // If fn = 0, file
    // couldn't be opened
    call ferr(fname)
  endif
  while not feof( fn ) //Loop until the end

    // of file is encountered

    fpos = ftell( fn ) //Store the current
    // file pointer position
    freadbfr fn, char, 1, rotecnt //Read 1 character
    aschar = asc( char ) //Get the ascii number
    // for the character
    if aschar = 34 // if the character
      // is a quotation mark
      if inquotes = 1 // and if it is a
        // closing quote
        inquotes = 0 //Set inquotes flag to 0
      else // But if it's an opening quote
        inquotes = 1 //Set inquotes flag to 1
      endif
    endif
    if not inquotes //If this character
      // is not in quotes
      call capitalize( char, changed ) //Pass it to the subroutine
    endif
    if changed = 1 //If the character was changed
      fseek fn, fpos //Fseek back to position
      // where we found the character
      fwritebfr fn, char, ritecnt, rotecnt // and write the character
      // to the file
      changed = 0 //Reset the changed flag
    endif
  endwhile
  fclose fn
endevent

sub ferr( ref fname)
  exitwitherror "Can't open file ", fname
endsub

sub capitalize( ref achar, ref changed ) //We could also use the
  // UpperCase command
  var aschar : n3 = asc( achar ) // but we'll take the
  // slow difficult route for fun
  if aschar > 96 and aschar < 123 //If the character
    // is a lower case alpha
    aschar = aschar - 32 // get its upper case equivalent
    achar = chr( aschar )
    changed = 1 // and set the changed flag
  endif
endsub
```

See also:

FClose

FOpen

FWrite

FWriteLn

---

## FWriteLn

<!-- src: Command_FWriteLn.htm -->

FWriteLn

### Function
This command writes a line of data to a file.

### Syntax
```text
FWriteLn file_number, line
```

### Argument/Description
**file_number** - an integer variable which was assigned in the FOpen statement when the file was opened
**line**  - identifes the file line written to

**FWriteLn Usage**
- The file must be opened in Write mode in order to execute this command.
- No quotes will be removed from the string that is written.

See also:

FClose

FOpen

FWrite

FWriteBfr

---

## GetEnterOrClear

<!-- src: Command_GetEnterOrClear.htm -->

GetEnterOrClear

### Function
This command waits for the operator to press the [Enter] key or the [Clear] key and reports which key was pressed.

### Syntax
```text
(entered as a single line)
GetEnterOrClear input_variable, prompt_expression [{output_specifier}][, prompt_expression[{output_specifier}]...]]
```

### Argument/Description
**input_variable** - an user_variable that accepts user input
**prompt_expression**  - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - required by syntax expression one or more of the output_specifiers that determine the format of the output fields

**GetEnterOrClear Usage**
- A value of 0 or 1 is placed in the input_variable, depending upon which key is pressed; 0 is placed in the variable if the [Clear] key is used and 1 if the [Enter] key is used.
- The combined length of all prompt_expressions must not exceed 38 characters (including spaces); extra characters will be truncated.
- The prompt_expression is required.

**GetEnterOrClear Example**

The following script will wait for either the [Enter] key or the
[Clear] key:

```isl
event inq : 1
  var ent_or_clr : n1
  var ENTER : n1 = 1
  getenterorclear ent_or_clr, "Press ENTER to Inquire, CLEAR to end"
  if ent_or_clr = ENTER
    txmsg "inquiry_1"
    waitforrxmsg
  else
    exitcontinue
  endif
endevent
```

---

## GetRxMsg

<!-- src: Command_GetRxMsg.htm -->

GetRxMsg

### Function
This command is used to transmit a message over the interface and wait for a response. GetRxMsg differs from WaitForRxMsg as described below.
- When a response is received from the interfaced system, SIM continues executing the script with the line immediately following the GetRxMsg command, while WaitForRxMsg stops the script at this point. The script writer can then use the RxMsg command to get the fields for the response message.

### Syntax
```text
(entered as a single line)
GetRxMsg [prompt_expression[{output_specifier}]] [, prompt_expression[{output_specifier}]...]
```

### Argument/Description
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**GetRxMsg Usage**
- The default prompt, "Please Wait--Sending Message", will appear on the prompt line of the UWS. The default prompt may be overridden by providing a prompt_expression with the command.
- The GetRxMsg is not a stand-alone command; the TxMsg command must precede the GetRxMsg command.
- While WaitForRxMsg is an implicit return from an event, meaning that it stops the script to execute an event for the received message, GetRxMsg is not. Thus, by using GetRxMsg instead of WaitForRxMsg, you have the option to continue executing any instructions following the GetRxMsg command.

**GetRxMsg Example 1**

The following examples illustrate the difference between using GetRxMsg instead of WaitForRxMsg:

In the Event Inq below, WaitForRxMsg is used so the script stops after executing the command and executes an Event RxMsg (ver_rsp).

```isl
event inq : 1
  txmsg "ver_req" //Transmit string requesting
  // version of system software
  waitforrxmsg //Wait for response, stop script
  waitforclear //Not executed because
  // waitforrxmsg has
  // terminated event
endevent

//Ver_rsp is message id field returned, so script
// executes event with corresponding event_id
event rxmsg : ver_rsp
  rxmsg version_s //format message as variable
  waitforclear version_s //display it
endevent
```

**GetRxMsg Example 2**
Using the GetRxMsg, the same procedure could be executed as
follows, without stopping the script:

```isl
event inq : 1
  txmsg "ver_req" //Format message to transmit
  getrxmsg //Transmit message and wait
  // for response
  //Continue executing script by formatting received
  // message into variable
  rxmsg version_s //Format message as variable
  waitforclear version_s //Display it
endevent
```

In the example above, the RxMsg command is used to retrieve the data for the received message, as opposed to an Event RxMsg.
- Be aware that when using the RxMsg with the GetRxMsg command, the message id field (the first field within the ISL response message Application_Data segment) is not provided. However, when using the WaitForRxMsg, the message id field defines the name of the ISL event to execute when processing the response message. Thus, in order to mimic this behavior with the GetRxMsg, you must use the @RxMsg system variable to return the message id.
- In the example that follows, the @RxMsg system variable is used to return the message id because, when the GetRxMsg command is used alone, the script has no way of determining if the received message is the correct message. So the script tests the returned event id before actually formatting the data into a variable. If the event id returned is incorrect, an error is displayed and the script stops.

```isl
event inq : 1
  txmsg "ver_req" //Format message to transmit
  getrxmsg //Transmit message and wait
  // for response
  if @rxmsg = "ver_rsp"
    rxmsg version_s //Format message received
    waitforclear version_s//Display it
  elseif @rxmsg = "ver_err"
    errormessage "Version number invalid"
    exitcancel
  endif
endevent
```

See also:

```isl
Event RxMsg

RxMsg

TxMsg

WaitForClear

WaitForConfirm

WaitForEnter

WaitForRxMsg
```

---

## If...Else[If]...EndIf

<!-- src: Command_If...Else[If]...EndIf.htm -->

If...Else[If]...EndIf

### Function
These commands allow conditional execution. The If command may be used to compare one expression to another. The Else command is used to execute a group of commands when the If command's condition is not met. The ElseIf command can be used to execute commands when the If command's condition is not met and you want another condition tested.

### Syntax
```text
If expression [operator expression][And | Or expression operator expression...]
.
.
.
Else
```

or

```isl
ElseIf expression [operator expression][And | Or expression operator expression...]
```
.
.
.
EndIf]

### Argument/Description
**expression** - one of the following: user_variable, system_variable, constant, string, function, equation
**operator**  - can be one or more Relational Operators
**And | Or**  - relational Operators used to provide additional or alternative conditions

**If...Else(If)...EndIf Usage**
- Numeric, currency, alphanumeric, and key variables may be compared. For example, the following usages are valid:

```isl
if counter < 20

if name = "Richard"
if keyname > @Key_Clear
```
- The expression will always be evaluated as true or false; i.e., anything that evaluates to 0 is false and anything that evaluates to non-0 (including a negative) is true. If the operator and second expression are left off, the remaining expression will still be evaluated in this way.

```isl
if counter //This will be true as long

//as the counter is not 0
```
- It is not considered a fatal error if an Else command appears without an If command preceding it. An error will occur if a corresponding EndIf command is not found.
- The text "Then" is allowed after an If or ElseIf statement, but it is not required. Although this syntax is legal, it conveys no additional meaning to the If or ElseIf statement in which it used.

If i < 4 then //Correct

.
.
.
```isl
ElseIf i > 10 then //Correct
```
.
.
.

**If...Else(If)...EndIf Example**

The following script will wait for a number entry between 1 and 10:

```isl
event inq : 9
  var key_pressed : key //Hold the function key user presses
  var data : a10 //Hold the number user chooses
  forever
    inputkey key_pressed, data, "Number then Enter, Clear to Exit "
    if key_pressed = @Key_Clear
      exitcontinue
    elseif key_pressed = @Key_Cancel
      exitcontinue
    elseif key_pressed = @Key_Enter
      if data > 0 and data <= 10
        waitforclear "You chose" , data, ". Press clear. "
      else
        errormessage "Choose a number between 1" , \
        " and 10, then press enter"
      endif
    endif
  endfor
endevent
```

See also:

For...EndFor

ForEver...EndFor

While...EndWhile

---

## InfoMessage

<!-- src: Command_InfoMessage.htm -->

InfoMessage

### Function
This command may be used to display a message box at the user workstation and allows you to specify a title for the box.

### Syntax
```text
(entered as a single line)
InfoMessage title, expression
```

### Argument/Description
**title**  — the string to appear as the title of the message box.
**expression**  — an expression that represents the string to appear in the message box.

**InfoMessage_Example**

The following script describes a sample message box, with both title and text defined.

```isl
Event init
  @idle_seconds = 10
EndEvent

Event idle_no_trans
  Var text : a20 = "Hello World"
  Var title : a20 = "My Title"
  InfoMessage title, text
EndEvent
```

---

## Input

<!-- src: Command_Input.htm -->

Input

### Function
This command accepts an entry from the operator.

### Syntax
```text
(entered as a single line)
Input input_variable[{input/output_specifier}], prompt_expression [{input/output_specifier}][, prompt_expression,...]
```

### Argument/Description
**input_variable** - a user_variable that will store the user's input
**{input/output_specifier}**  - one or more of the input and output_specifiers that determine the format of all input and output fields
**prompt_expression**  - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation

**Input Usage**
- Prior to changing the input_variable, the user's entry will be validated against the field type and optional format definition.
- The combined length of all prompt_expressions must not exceed 38 characters (including spaces); extra characters will be truncated.
- The prompt_expression is required.
- Magnetic card entry input formats are allowed with the Input command.
- If the [Clear] key is pressed during execution of the Input command, the script will terminate unsuccessfully. This can have undesired side effects. If a script transacts a successful posting and then uses the Input command to get reference information on the posting from the user, the [Clear] key will perform an implicit ExitCancel, even though the posting was successful. Use the ContinueOnCancel command to avoid this side effect. The variable @inputstatus can be tested to determine if the user pressed [Clear].

**Input Example**

The following script accepts a patron number from the user, then transmits it to the PMS for further action:

```isl
event inq : 1
  var ptrn_no : a8
  input ptrn_no,"Enter Patron Number" //Get patron number
  txmsg "Inquire_1", ptrn_no //Send to PMS
  waitforrxmsg //Wait for reply
endevent
```

See also:

ContinueOnCancel

InputKey

---

## InputKey

<!-- src: Command_InputKey.htm -->

InputKey

### Function
This command accepts an alphanumeric entry from the operator, then stores the entry and the terminating key stroke in separate variables.

### Syntax
```text
(entered as a single line)
InputKey key_variable, input_variable, prompt_expression {input/output_specifier}[, prompt_expression[{input/output_specifier}]...]]
```

### Argument/Description
**key_variable** - a user_variable key type
**input_variable**  - a user_variable that will store the user's input
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{input/output_specifier}**  - one or more of the input and output_specifiers that determine the format of all input and output fields

**InputKey Usage**
- The key_variable will be set equal to the terminating key press. In this way, the script can compare the value held by key_variable to the @KEY... System Variables, to test for the terminating keystroke the user pressed.
- The prompt_expression is required.

**InputKey Example**

The following script waits for a number entry between 1 and 9 followed by the [Enter] key. If the [Clear] or [Cancel] key is pressed, it exits the script:

```isl
event inq : 9
  var key_pressed : key //Hold the function key user presses
  var data : a10 //Hold the number user chooses
  forever
    inputkey key_pressed, data, "Number then Enter, Clear to Exit "
    if key_pressed = @Key_Clear
      exitcontinue
    elseif key_pressed = @Key_Cancel
      exitcontinue
    elseif key_pressed = @Key_Enter
      if data > 0 AND data <= 10
        waitforclear "You chose ", data, ". Press clear. "
      else
        errormessage "Choose a number between 1 ", \
        "and 10, then press enter"
      endif
    endif
  endfor
endevent
```

See also:

Input

---

## Item Discount

<!-- src: Command_Item Discount.htm -->

Item Discount

### Function
This command is used to apply a list of discount amounts to the corresponding list of detail index values. The GetMaxDiscount function will be used to help the ISL developer determine how much can actually be discounted for each menu item.

When this command is passed, the discount object number, array size, detail index array, discount amount array, and optionally, a discount reference string, will apply the discount amounts to the applicable menu items using the discount object number.
```isl
For more information see GetMaxDiscount Function.
```

**Syntax:**
ItemDiscount

**Item Discount Example:**
ItemDiscount obj_num, array_size, detail_array[], detail_array[], amount_array[]
ItemDiscount obj_num, array_size, detail _array[], amount_array[], ref_num

---

## LineFeed

<!-- src: Command_LineFeed.htm -->

LineFeed

### Function
This command will line feed the selected printer. The number of line feeds is optional.

### Syntax
```text
LineFeed [number_of_line_feeds]
```

### Argument/Description
**number_of_line_feeds**  - an expression which defines the number of line feeds

**LineFeed Usage**
- Prior to the LineFeed command, the printer (Slip, Roll, etc.) must be activated within the script using the StartPrint command.
- Printing will not begin until the EndPrint command is executed.
- A line feed is automatically executed after the PrintLine command is issued.

**LineFeed Example**

```isl
event inq : 1
  var kitchen_msg[11] : a20
  var sender_name : a20
  var rowcnt : n3
  window 12, 22 //Display the window
  displayinput 1, 2, sender_name, "Enter your name"
  //Accept users name
  for rowcnt = 1 to 11 //Have user input the message
    displayinput rowcnt + 1, 2, kitchen_msg[rowcnt], "Enter kitchen message"
  endfor
  windowedit //Only save or cancel will end input
  startprint @ordr1 //Start the print job at
    // remote printer1
    printline "============================"
    printline "Message from ", sender_name
    printline "============================"
    for rowcnt = 1 to 11
      if len(kitchen_msg[rowcnt]) > ""
        printline kitchen_msg[rowcnt]
      endif
    endfor
    printline "======= END MESSAGE ========"
    linefeed 5
  endprint
endevent
```

See also:

PrintLine

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## ListDisplay

<!-- src: Command_ListDisplay.htm -->

ListDisplay

### Function
This command is used to display a list (array) variable within a window. This command is useful when displaying the contents of an array variable that contains data received from a PMS, such as a list of names.

### Syntax
```text
(entered as a single line)
ListDisplay row, column, list_size, array_variable
```

### Argument/Description
**row** - the integer expression specifying the screen row within the defined window where the first array_variable entry will be displayed
**column**  - the integer expression specifying the screen column within the defined window where first array_variable entry will be displayed
**list_size**  - the number of array_variable entries to display
**array_variable**  - the name of the user_variable that holds the matrix of values to be displayed

**ListDisplay Usage**
- The Window command must precede this command.
- It is acceptable to set list_size equal to 0, but if this is done, nothing will display. If the list_size is less than zero, an error will occur.
- Each entry will be placed on a separate line directly beneath the previous.

**ListDisplay Example**
The following script will display an employee list:
```isl
event rxmsg : emp_list
  var emp_list_size : n3
  var emp_list_array[12] : a40
  rxmsg emp_list_size, emp_list_array[ ]
  window 12, 42
  l istdisplay 1, 2, emp_list_size, emp_list_array
  waitforclear
endevent
```

See also:

Window

---

## ListInput

<!-- src: Command_ListInput.htm -->

ListInput

### Function
This command is used to display a list (array) variable within a window at the UWS, then waits for the operator to select an item from the list.

### Syntax
```text
(entered as a single line)
ListInput row, column, list_size, array_variable, input_variable, prompt_expression[{output_specifier}]
```

### Argument/Description
**row** - the integer expression specifying the screen row within the defined window where the first array_variable entry will be displayed
**column**  - the integer expression specifying the screen column within the defined window where the first array_variable entry will be displayed
**list_size**  - the number of array_variable entries to display
**array_variable**  - the name of the user_variable that holds the matrix of values to be displayed
**input_variable**  - a user_variable that accepts user input
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**ListInput Usage**
- The Window command must precede this command.
- Each list entry is displayed with a selection number starting at 1. The selection numbers 1 to 9 are preceded by a space. Selection numbers are followed by a period, then a space, then the list entry. For this reason, the window drawn must be at least four columns wider than the longest item in the list. Each list entry is placed on a separate line. The user's entry is placed in the input_variable and is validated against the number of items in the list.
- The prompt_expression is required.
- It is acceptable to set list_size equal to 0, but if this is done, nothing will display. If the list_size is less than zero, an error will occur.

**ListInput Example**
The following script receives and displays a list of guests from the PMS, allows the user to choose one from the list, and then transmits the user's choice to the PMS for further processing:

```isl
event rxmsg : room_inquire
  var rm_guest[14] : a20 //Guest names array
  var rm_num : a6 //Room number
  var list_size : n3 //Number of array items
  var user_choice : n3 //Guest number user chooses
  rxmsg rm_num, list_size, rm_guest[ ] // receive message from POS
  window list_size, 24, "Guests- Room #", rm_num
  listinput 1, 1, list_size, rm_guest, user_choice, "Choose a guest"
  txmsg "guest inquiry", rm_num, user_choice
  //Ask for info from PMS
  waitforrxmsg // on guest user chooses
endevent
```

See also:

Window

---

## ListPrint

<!-- src: Command_ListPrint.htm -->

ListPrint

### Function
This command will print a list on the selected printer.

### Syntax
```text
ListPrint list_size, array
```

### Argument/Description
**list_size** - the number of array_variable entries to be printed
**array_variable**  - the name of the user_variable that holds the matrix of values to be printed

**ListPrint Usage**
- The StartPrint and EndPrint commands are required when using the ListPrint command.
- It is acceptable to set list_size equal to 0, but if this is done, nothing will display. If the list_size is less than zero, an error will occur.

**ListPrint Example**
The following script receives a list of directions from the PMS that describes how to get from the property to another location and prints them at the UWS's check printer:

```isl
event rxmsg : directions
  var directions[50] : a35 //Our direction array
  var list_size : n3 //Number of array items
  rxmsg list_size, directions[ ] //Here's the message from PMS
  startprint @CHK //Print at the check printer
    listprint list_size, directions //Print the list
  endprint
endevent
```

See also:

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## LoadDbKybdMacro

<!-- src: Command_LoadDbKybdMacro.htm -->

LoadDbKybdMacro

### Function
This command loads a keyboard macro that is pre-defined in the 3700 Database. The macro will execute when transaction processing successfully resumes.
Another keyboard macro command is available, LoadKybdMacro, which uses a script-defined keyboard macro.

### Syntax
```text
LoadDbKybdMacro numeric_expression]
```

### Argument/Description
**numeric_expression**  - an expression that requires a number; it may be one of the following: user_variable, system_variable, constant, string, function, equation

**LoadDbKybdMacro Usage**
- The macro is referenced by its object number.
- Only integer variables can be used to run a pre-defined macro.
- If more than one LoadDbKybdMacro command is used in the same event, only the last command will be used when transaction processing resumes.

**LoadDbKybdMacro Example**
The following script will load a macro from the 3700 database that will add two menu items to a guest check currently open at the UWS:

```isl
event inq : 1
  loaddbkybdmacro 1
endevent
```

See also:

LoadKybdMacro

---

## LoadKybdMacro

<!-- src: Command_LoadKybdMacro.htm -->

LoadKybdMacro

### Function
This command passes keystrokes to the UWS; these keystrokes will be executed when the script event terminates. Each macro key expression will access a specific key that is normally programmed in the Touchscreen Designer form in the 3700 database. There are a variety of ways to specify script-defined macros.
Note: This command may be used to call another SIM event.

### Syntax
```text
LoadKybdMacro key_expression[, key_expression,...]
```

### Argument/Description
**key_expression** - an expression that can be one of the following: Key function, Makekeys function, user_variable (type Key only) system_variable (@KEYS only)

**LoadKybdMacro Usage**
- For pre-defined database macros, see LoadDbKybdMacro .
- A script-defined macro is one that the script writer constructs using key function codes. These key function codes can be represented by any combination of the following methods:
- Key function - The Key function takes as its argument a hexadecimal string that defines the function key code. The ampersand preceding these characters specifies them as a hexadecimal string. For example:

```isl
loadkybdmacro key(1,65537), key(1,65538), key(1,65539), key(1,65549)
```
- Makekeys function - The Makekeys function takes as its argument a string, or some variable that holds a string, and expands the characters of the string out to a series of key function codes. So, another way to load 123 and the [Enter] key would be:

```isl
loadkybdmacro makekeys ("123"), key(1,65549)
```
OR
```isl
var key_string : a3 = "123"
loadkybdmacro makekeys (key_string), key(1,65549)
```
- @Key... System Variables - System Variables that begin with @Key... are special key type variables. These keys can be used to test for and represent movement keys and keys like [Enter] and [Clear]. The @KEY... System Variables can also be used in the loadKybdMacro command. To continue our example:

```isl
loadkybdmacro key(1,65537), key(1,65538), key(1,65539), @Key_Enter
```
- User-defined variables with the type Key - User-defined variables with the type Key can be assigned key function codes using the Key function or with @KEY... System Variables. Another way to load our keyboard macro:

```isl
var key_1 : Key //Declare variables as
//Key types
var key_2 : Key
var key_3 : Key
var Enter : Key
key_1 = key(1,65537) //Assign them with
//key()function
key_2 = key(1,65538)
key_3 = key(1,65539)
Enter = @Key_Enter // and system variable
loadkybdmacro key_1, key_2, key_3, Enter
```
- If more than one LoadKybdMacro command is used in the same event, they will be run in order of appearance when transaction processing resumes, as if they were one large macro.
- Macro keys will execute once a script is complete. When WaitForRxMsg is used, a macro will remain in effect across multiple events.
- Use this command with key type 24 to call another SIM event as shown in the following example:

loadkybdmacro key(24,16384*EVENT_NUM (inq: 1) + INTERFACE_SEQ) where the INTERFACE_SEQ is the number from the interface_def table in the Micros database.
- If the SIM event loads a keyboard macro that adds a menu item with reference entry to the check, then POS Operations will not go to the Next screen when the macro completes. The following scripts provide two examples of ways to add a display touchscreen command at the end of the event:

**Example 1**
```isl
VAR INQUIRE_OFFSET : N5 = 16384
VAR EMPTY_INQUIRE : N1 = 1
event inq : 1
  // empty event
endevent
event inq : 99
  if (trim(@USERENTRY) = "")
    // menu item (reference required)
    loadKybdMacro key (3, 1001)
    loadKybdMacro makekeys("Next screen")
    loadKybdMacro @KEY_ENTER
    loadKybdMacro key(24,INQUIRE_OFFSET*EMPTY_INQUIRE+@PMSNUMBER) // Call empty inquire event
  else
    / / menu item (no reference required)
    loadKybdMacro key(3, 1001)
  endif
endevent
```

**Example 2**
```isl
Event inq : 99
  if (trim(@USERENTRY) = "")
    // menu item (reference required)
    loadKybdMacro key (3, 211)
    loadKybdMacro makekeys("Next screen")
    loadKybdMacro @KEY_ENTER
    loadKybdMacro @KEY_ENTER
  else
    // menu item (no reference required)
    loadKybdMacro key(3, 1001)
  endif
endevent
```

**LoadKybdMacro Example 1**

In the following script, there will be three [Enter] keys that will be run once the script completes:
```isl
event inq:1
  loadkybdmacro @Key_Enter //first enter key
  txmsg "inq_1_request"
  waitforrxmsg
endevent

event rxmsg : inq_1_reply
  loadkybdmacro @Key_Enter //second enter key
  txmsg "inq_2_request"
  waitforrxmsg
endevent

event rxmsg : inq_2_reply
  loadkybdmacro @Key_Enter //third enter key
endevent
```

**LoadKybdMacro Example 2**
The following script receives an employee ID from the PMS and constructs a macro that clocks the employee in:

```isl
event rxmsg : emp_clock_in
  var micros_emp_id : a10
  var clock_in_key : key
  clock_in_key = key(1, 655368) //Assign key code for clock in
  // to a var
  //Receive the ID of the employee
  // to clock in
  // from PMS then load macro and
  // clock in employee
  rxmsg micros_emp_id
  loadkybdmacro clock_in_key, makekeys( micros_emp_id ),\
  @Key_Enter, @Key_Enter, @Key_Enter
endevent
```

See also:

```isl
Key Function

LoadDBKybdMacro

MakeKeys Function
```

---

## LoadMAGInfo

<!-- src: Command_LoadMAGInfo.htm -->

LoadMAGInfo

### Function
This command is used to load information via a SIM script into a OPS MAGInfo data area. When the MACRO system encounters a KEY_MAGCARD key, it triggers OPS to take the previously loaded MAGInfo and process it. The KEY_MAGCARD key (278528) is a KEY_TYPE_FUNCTION type (1).

### Syntax
```text
LoadMagInfo Track2_Expression
LoadMagInfo Track1_Expression, Track2_Expression
```

### Argument/Description
This will take either one or two parameters. If one parameter is supplied, the function will fill the TRACK2 data. If two parameters are supplied, then the function will fill both TRACK1 and TRACK2.

Both parameters are an expression that represents the string used as the mag card track. The SIM script that uses this function ensures that the format of the Track1 expression is in the form "%" + cc track1 data + "?" and that the Track2 expression is in the form ";" + cc track2 data + "?"

**LoadMAGInfo Example**

```isl
Event Inq : 1
  var CC_Track1 : a79
  var CC_Track2 : a79
  var fCC_Track1 : a79
  var fCC_Track2 : a79
  var CC_Auth_Key : key = key(1,458787)
  input CC_Track1 {m1, *}, CC_Track2 {m2, *}
  If (@MAGSTATUS = "Y")
    LoadKybdMacro MakeKeys("1.00"), CC_Auth_Key
    format fCC_Track1 as "%", CC_Track1, "?"
    // Notice format is "%" + Track 1 mag Info + "?"
    format fCC_Track2 as ";", CC_Track2, "?"
    // Notice format is ";" + Track 2 Mag Info + "?"
    LoadMagInfo fCC_Track1, fCC_Track2
    LoadKybdMacro key(1,278528)
  EndIf
EndEvent
```

---

## LowerCase

<!-- src: Command_LowerCase.htm -->

LowerCase

### Function
This command is used to convert a string variable to lower-case.

### Syntax
```text
LowerCase string_variable
```

### Argument/Description
**string_variable** - the string that will be changed; can be the following: user_variable (string)

See also:

UpperCase

---

## MakeAscii

<!-- src: Command_MakeAscii.htm -->

MakeAscii

### Function
This command will transfer the data from a source_string into a destination_string, stripping out any non-ASCII characters from the source_string.

### Syntax
```text
MakeAscii source_string, destination_string
```

### Argument/Description
**source_string** - a string_variable containing both ASCII and non-ASCII characters
**destination_string**  - a place holder for the string_variable containing only ASCII characters

**MakeAscii Example**

The following script will convert a string containing both ASCII and non-ASCII characters into a string that contains only ASCII characters:
```isl
event inq : 1
  var string1 : A20
  var string2 : A20
  format string1 as "ABC", chr(1), "DEF"
  makeascii string1, string2 //string2 will be "ABCDEF"
  waitforclear string2
endevent
```

---

## Mid

<!-- src: Command_Mid.htm -->

Mid

### Function
This command is used to set all or some part of one string variable equal to another string variable.

### Syntax
```text
Mid (string_variable, start, length) = replacement_string
```

### Argument/Description
**string_variable**  - the string that will be changed; can be any user_variable (string)
**start**  - the character position within the string_variable, where the replacement_string will begin to overwrite
**length** - the number of characters in the string_variable that will be changed using the replacement_string to the right of the equal sign = required by syntax
**replacement_string** - the string containing the characters used for the replacement can be any user_variable (string)

**Mid Usage**
- Do not confuse this command with the Mid function .
- The parentheses are required.
- The first character in the string is always 1. If the start or length is less the 0, then an error will occur.
- If the start is greater than the string_variable itself, no data will be assigned. If the length is greater than the room left to assign the string_variable, then the data will be truncated.

**Mid Example**

The following script will replace the first three letters of the
variable "string" with the string "NEW":

```isl
event inq : 1
  var string : a10 = "OLD STRING"
  waitforclear string //Prompt will show "OLD STRING"
  mid(string, 1, 3) = "NEW" //Change OLD to NEW
  waitforclear string //Prompt will show "NEW STRING"
endevent
```

---

## MSleep

<!-- src: Command_MSleep.htm -->

MSleep

### Description
This command will cause the execution of a SIM script to pause for approximately the number of milliseconds passed as the
parameter of the function.

### Syntax
```text
Msleep (n)
```

### Argument/Description
**n**  - milliseconds to pause

---

## PrintLine

<!-- src: Command_PrintLine.htm -->

PrintLine

### Function
This command prints a line on the selected printer defined in the StartPrint command. The print information can be provided as text or by referencing a variable field.

### Syntax
```text
(entered as a single line)
PrintLine expression[{output_specifier}] | directive[, expression[{output_specifier}] | directive...]
```

### Argument/Description
**expression**  - an expression that represents the string to be printed, it may be one of the following: user_variable, system_variable, constant, string, function, equation
**directive**  - specific instructions that affect the color, width, and justification of the printed characters
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**PrintLine Usage**
- This command will affect the printer selected using the StartPrint command. For a complete list of available printers, see the ISL Printer Table .
- Normally, the PrintLine command sends a carriage return/line feed to the printer after every line.
- The PrintLine command may be used to format characters to a certain position (i.e., left, right, or center justified, etc.).

**PrintLine Example 1**

```isl
startprint @CHK
  printline "This is on line 1, "
  printline "so is this."
  // line feed after printing
  printline "This is on the second line."
  // print on second line
endprint
```

The result would be the following output:
This is on the first line, so is this.
This is on the second line.

**PrintLine Example 2**
The following script constructs and prints a date string bordered by hash marks at the UWS's check printer:

```isl
sub print_date
  var date : a9
  var hash_mark : a16
  //Use format to build a date
  // string
  format date as @Day, "-", @Month, "-", @Year
  setstring hash_mark, "="
  startprint @Chk //Print what follows at this UWS
    // check printer
    printline hash_mark //Print the date string
    printline @Dwon, @Redon, date{=16} // double-wide, in red
    printline hash_mark // and centered between
    // hash marks
  endprint
endsub
```

See also:

```isl
Chr Function

StartPrint[WithStatus]...EndPrint[FF/NoFF]
```

---

## Prompt

<!-- src: Command_Prompt.htm -->

Prompt

### Function
This command is used to display an operator prompt on the prompt line at the UWS.

### Syntax
```text
(entered as a single line)
Prompt expression[{output_specifier}] [, expression [{output_specifier}]...]
```

### Argument/Description
**expression**  - an expression that represents the prompt for the user; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**Prompt Usage**
- The combined length of all expressions must not exceed 38 characters (including spaces); extra characters will be truncated.
- The Prompt command should only be used when a time-consuming piece of code is to be executed. This command will inform the user that the UWS is busy. All commands that require user input display their own prompts.

```isl
prompt "Posting unsuccessful"
// displayed but erased immediately
waitforclear
// "Press clear to continue" will display
```

**Prompt Example**

The following script receives a list of guests from the PMS, calls a subroutine that sorts the list, then calls another that displays the list:

```isl
event rxmsg : guest_list
  var num_guests : n3
  var guest_list[100] : a20
  rxmsg num_guests, guest_list[ ] //Get the guest array from PMS
  prompt "Sorting guest list - please wait..." //Tell the user
  call sort_list //Call routine that sorts the list
  call display_guests //Call routine that displays the list
endevent
```

---

## ProRate

<!-- src: Command_ProRate.htm -->

ProRate

### Function
This command is used to indicate to the system that prorated itemizers are to be used. Prorated itemizers are required for some Property Management Systems.

### Syntax
```text
ProRate
```

**ProRate Usage**
- If the ProRate command is encountered either inside or outside an Event procedure, all itemizers will be prorated for the duration of the ISL script. The following system variables are prorated:

@SI[]
@DSC
@SVC
@AUTOSVC
@TXBL[]
- Prorated itemizers are useful if the PMS is posting sales, discounts, tax, etc. during the charge posting operation. When prorated totals are used, the totals reflect the Current Payment's share of a guest check. If the Current Payment is voided, the totals will have the reversed polarity to reflect this. The only exception (i.e., the total that is not prorated) is a charged tip, which will always be completely attributed to its associated payment. This mode is supported by the 3700.

**ProRate Notes**
The following equations can be used by the PMS Computer to determine the Current Payment Total of the prorated transaction being posted:

Current Payment Total =

+ (+) Sales 1 Total
+ (+) Sales 2 Total
+ (+) Sales 3 Total
+ (+) Sales 4 Total
+ (+) Sales 5 Total
+ (+) Sales 6 Total
+ (+) Sales 7 Total
+ (+) Sales 8 Total
+ (-) Discount Total
+ (+) Service Charge Total (kybd)
+ (+) Service Charge Total (auto)
+ (+) Tax 1 Total (if non-VAT)
+ (+) Tax 2 Total (if non-VAT)
+ (+) Tax 3 Total (if non-VAT)
+ (+) Tax 4 Total (if non-VAT)
+ (+) Tax 5 Total (if non-VAT)
+ (+) Tax 6 Total (if non-VAT)

+ (+) Tax 7 Total (if non-VAT)
+ (+) Tax 8 Total (if non-VAT)

The Previous Payment Total is also provided.
- In some jurisdictions, the prorated calculations will result in inexact tax totals. This occurs because of rounding errors associated with proration and the methods required to compute tax. As an example, consider three guests paying a $10.00 check which includes $1.00 tax. The first two guests will be charged $0.33 tax and the third $0.34 tax (the rounding adjustment is included in the last total). These situations are unavoidable; if complete accuracy is required, a Split Check operation should be performed and the remaining checks (after the Split Check) should be individually posted to the PMS.
- In the formulas shown above, the first arithmetic operator indicates the operation that the PMS should perform on the total field. The second arithmetic operator (in parentheses) indicates the normal sign of the total field as presented in the message data block by the POS system.
- If Value Added Tax (VAT) is being used, the tax totals represent the total sales amounts (inclusive of VAT) for each of the VAT tax types and MUST NOT be included in the Transaction Total or Current Payment Total equations.
- In non-prorated mode, if the Current Payment Amount field in the message data block is less than the computed Transaction Total (above), then a partial amount has been tendered.
- If the U.S. inclusive tax method is used, the tax total associated with this rate will be zero.

---

## RegIdleEvent

<!-- src: Command_RegIdleEvent.htm -->

RegIdleEvent

### Function
This command is used to create idle events for SIM scripts to be run in the background when POS Operations is idle and no one is signed in. If an employee should sign in, POS Operations will call the Idle_No_Trans event until they sign out again.
Up to 128 idle events may be created with the RegIdleEvent command
The frequency at which the SIM script is called is determined by the @Idle_Seconds variable.

### Syntax
```text
RegIdleEvent expression, count
```

### Argument/Description
**expression**  — The name of the idle event.
**count**  — The amount of time (in seconds) for the event to be idle.

**RegIdleEvent Example**
```isl
event init
  @Idle_seconds = 10
  RegIdleEvent “MyEvent1Minute”, 60
  RegIdleEvent “MyEvent50Sec”, 50
endEvent

event MyEvent1Minute
  InfoMessage “One Minute Has Passed…”
endEvent

event MyEvent50Sec
  InfoMessage “Fifty Seconds Has Passed…”
endEvent
```

---

## RetainGlobalVar

<!-- src: Command_RetainGlobalVar.htm -->

RetainGlobalVar

### Function
These commands instruct the ISL to save all global variable values in between transactions.

### Syntax
```text
RetainGlobalVar
```

**RetainGlobalVar Usage**
This command is global, which means it remains in affect until the alternative command is used or until the script file has been changed (i.e., until a new script is downloaded to the UWS).
The default action is to discard the global variable values after each event.

**RetainGlobalVar Example**
The following example could be used to count the number of times Tender #1 has been used. This value will be retained and incremented until the script is changed.

```isl
retainglobalvar
var numtnd : n5 //Numtnd is retained until the script is downloaded to the UWS again.
event tmed : 1
  numtnd = numtnd + 1
  .
  .
  .
endevent
```

---

## Return

<!-- src: Command_Return.htm -->

Return

### Function
This command is used to return from a subroutine procedure prior to reaching the end of the routine (EndSub). It is provided as a means of breaking out of the subroutine under certain conditions.

### Syntax
```text
Return
```

**Return Usage**
The Return command is not allowed in an Event procedure.

**Return Example**

This script fills an array with a set of names, then prompts the user to enter an index of the array. If the data is displayable, it will be displayed. The Return command is used in the subroutine to return immediately if the list size passed in is invalid.

```isl
event inq : 1
  var names[20]:A20
  var i:N5
  var entry:N5
  for i = 1 to arraysize( names ) //Fill in 'names' with a set of
    // dummy names.
    format names[i] as "List name ", i
  endfor
  input entry, "Enter number of data to display"
  call display_entry( entry, 20, names[] )
endevent
```

This subroutine will display the data in names[ entry ] if it is valid.

```isl
sub display_entry( var entry:N5, var size:N5, ref names[] )
  var i:N5
  if size = 0 OR entry < 1 OR entry > size //Return immediately if no data
    // in array.
    return
  endif
  waitforclear names[ entry ]
endsub
```

See also:

If...Else[If]...EndIf

Sub...EndSub

While...EndWhile

---

## RxMsg

<!-- src: Command_RxMsg.htm -->

RxMsg

### Function
This command defines the format of the data segment of an interface response message by specifying a variable name for each piece of data it receives. The RxMsg command will assign the values in the Applications Data Segment of the variables specified in the RxMsg statement.

### Syntax
```text
(entered as a single line)
RxMsg user_variable or list_spec[, user_variable or list_spec...]
```

### Argument/Description
**user_variable**  - a user_variable which will be assigned data
list_spec is defined as:
- **number_records** - a user integer variable containing the number of records to be built from this string
- **field_array[: field_array]**  - an array_variable that will hold one field per record; you can split a field into more than one array by separating the array_variables using a colon (:)

**RxMsg Usage**
- The Event RxMsg command is executed when a response is received from the interfaced system. The Event must contain an RxMsg command. The first field in a response message is always the Event ID and should not be declared using this command. The RxMsg command defines all the fields (and their order) following the Event ID field. The interface message fields are always separated by an ASCII field separator character (ASCII 1CH). The variable fields must be previously declared using the Var command.
- If the System Variable @Strict_Args is set to 1, then ISL will ensure that the variable count in the RxMsg command matches the number of fields in the file record. If an incorrect number of fields is specified in the statement or the file is corrupted, an error message will be generated.
- This Event requires that both the TxMsg and WaitForRxMsg commands be used in another event in the script for the RxMsg command to work. The exception, is when the GetRxMsg command, as opposed to WaitForRxMsg, is used to receive the returned message. In which case, the RxMsg command can be executed within the same script, outside of an Event RxMsg.
- If the RxMsg command specifies more variables than are present in the applications data segment, no error will occur. The extraneous variables on the command will retain their previous value. If the number of fields in the Applications Data Segment exceeds the number of variables in the RxMsg command, no error will occur. The command will execute successfully and the extraneous data in the message will be thrown away.
- It is not possible to execute an RxMsg if no message has been received. It is also not possible to execute multiple RxMsg commands within one RxMsg Event. Once the first RxMsg command executes, any subsequent RxMsg command will cause an error.
- This command is related to the Split command. While the Split command works with any string buffer and any field separator, the RxMsg command assumes the PMS message and the ASCII field separator character.

**RxMsg Example**

```isl
event inq : 1
  var room_num : a4
  input room_num, "Enter Room Number"
  txmsg @Ckemp,@Cknum,@Tndttl,room_num
  waitforrxmsg
endevent
event rxmsg : charge_declined
  var room_num : a4
  rxmsg room_num
  exitwitherror "Charge for room ", room_num," declined"
endevent
```

See also:

Event...EndEvent

GetRxMsg

Split

TxMsg

Use[ISL/STD]TimeOuts

Var

WaitForRxMsg

---

## SaveChkInfo

<!-- src: Command_SaveChkInfo.htm -->

SaveChkInfo

### Function
This command saves check information detail lines in the 3700 database.

### Syntax
```text
(entered as a single line)
SaveChkInfo expression[{output_specifier}][, expression [{output_specifier}]...]
```

### Argument/Description
**expression** - an expression that represents the information to be saved; it may be one of the following: user_variable system_variable, constant, string, function, equation**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**SaveChkInfo Usage**

Third-Party System
If the check information detail is captured by a third-party system, like a delivery system, accessing the information depends on the resources of that particular system. The SaveChkInfo command is issued once for each line of check information detail written to the check. The process goes like this:
- The first occurrence of SaveChkInfo in an event writes to the first check information detail line.
- Each subsequent call to SaveChkInfo writes to the next check information detail line.
- Check information detail is not actually written to the check detail until the script terminates.
- Check information detail can be overwritten by using SaveChkInfo in another event.

**Example of POS Application**

Guest Check Information Detail
Check information detail is a type of check detail that can be stored in the 3700 database, but unlike other types of check detail, it must be captured and saved using a facility designed with the ISL. In conjunction with SIM, this information is captured via operator input at a UWS or retrieved from a third-party source, such as a delivery system, and placed in the check detail of a guest check.

Purpose
Guest Check Information Detail works with the Edit Detail feature, which supports the retrieval and edit of previous order information from a third-party database. The previous order history is guest check detail stored in a third-party database from a customer's last guest check.

In addition to retrieving previous order information, customer information such as names and addresses or special handling instructions, can be added to the guest check by enabling the Guest Check Information Detail Lines feature. Using the SaveChkInfo command, the guest check information lines are saved in the 3700 database. This information can be printed on guest checks or to remote order devices and/or displayed in the transaction detail of the UWS screen.

Typically, check information detail lines are used to store customer information, such as names and addresses. A restaurant, for example, that uses a third-party delivery system could use this command to implement the operational procedure that follows:

1. A customer calls Personal Pizza and says, "This is Joe Decker. Give me my usual order, please."
2. The employee replies, "Good evening, Mr. Decker," and presses the [Delivery] key on the UWS. In this system’s database, the [Delivery] key is actually one of the SIM keys. The [Delivery] key generates a SIM script, which displays a series of touchscreens.
3. This SIM script is programmed to display an entry box that prompts for the customer’s name. The operator enters Decker, and the script executes a search in the third-party database.
4. The search finds a matching record, and the script prompts for confirmation.
5. The employee presses [Yes] to confirm that this is the correct customer. The SIM script then opens a guest check and prints guest check information lines for this customer.
6. The customer’s last order appears in the right side of the display, with the first menu item highlighted. The employee can perform any of the following actions:
- Press [Enter] to post a highlighted menu item to the new check.
- Press the [Up] or [Down] arrow keys to move through the detail of the previous check.
- Press [Edit Detail, Transfer All] to post the entire contents of the previous check to the new check.
- Press [Clear] to reject all menu items on the previous check, and display an order screen.
7. For the reference of the delivery driver, all of the customer information is printed before the guest check header.

Summary
In our example, the script writer had to design the SIM script to create a facility to collect the customer information: namely, an ISL-defined window and user prompting. Here, the SaveChkInfo command was used to actually save the customer name and address information, as well as the special instructions.

To display the customer information with other transaction detail and to print it on the guest check, specific 3700 programming was enabled to make these functions occur.

**How to Capture and Print Check Information Detail**
Introduction
Our example illustrates how check information detail is unique from other types of check detail, in that the mechanisms you put in place for collecting, saving, and printing this detail require a concerted effort between both SIM and the 3700 System. Both facilities must be used in the following ways to accomplish these tasks:
- A SIM script must be designed to collect and save the check information detail.
- Specific 3700 System programming must be enabled to print and display the check information detail to the specifications of the establishment.

Designing the SIM Script
SIM must be used to capture and save check information detail. That is, the script must be designed so that an operator can input check information detail and save it in the 3700 database.

When designing your script, keep the following rules in mind:
- Do not issue SaveChkInfo in a single event more times than the number of allocated check information detail lines; doing so will result in an error.
- Only 24 characters per check information detail line may be written with SaveChkInfo.

The following steps are the sequence of events that your script might execute in order to capture and save check information detail:
1. Begin a check.
2. Draw a window.
3. Prompt the operator to enter name and address information.
4. Issue the SaveChkInfo command to save the input data.

Programming the 3700 Database
Whether check information detail lines will print and where they will print on guest checks and remote output is determined by specific 3700 database programming, not the script. In order to print this detail and save it, check information detail lines must be allocated in the 3700 System and Programmed to print.

For example, you can program the 3700 System to print the check information detail captured before or after the guest check header, or after the guest check trailer. In our delivery system example, the restaurant programmed the check information detail lines to print before the guest check header.

All 3700 database programming required to enable the Check Information Detail Lines feature is discussed in the 3700 Feature Reference Manual. Refer to this manual for a detailed discussion of the programming involved.

**SaveChkInfo Example**

The ISL event below initiates a procedure for collecting and saving customer information for a fictional delivery system at a restaurant. The procedure will collect the customer’s last and first name, telephone number, street address, and up to four lines of directions.

```isl
event inq : 1
  var field_name[8] : a24
  var customer_info[8] : a24
  field_name[1] = "Last: "
  field_name[2] = "First: "
  field_name[3] = "Phone: "
  field_name[4] = "Addr: "
  field_name[5] = "D1: "
  field_name[6] = "D2: "
  field_name[7] = "D3: "
  field_name[8] = "D4: "
  var customer_info[8] : a24
  var rowcnt : n3
  window 8, 40
  touchscreen 13
  for rowcnt = 1 to 8
    display rowcnt, 2, field_name[rowcnt]
    displayinput rowcnt, 10, customer_info[rowcnt],\
    "Enter ", field_name[rowcnt]
  endfor
  windowedit
  for rowcnt = 1 to 8
    savechkinfo customer_info[rowcnt]
  endfor
  waitforclear
  windowclose
endevent
```

See also:

ClearChkInfo

EditDetail

---

## SaveRefInfo

<!-- src: Command_SaveRefInfo.htm -->

SaveRefInfo

### Function
This command is used to save the contents of an expression as part of tender reference information.

### Syntax
```text
(entered as a single line)
SaveRefInfo expression[{output_specifier}][, expression [{output_specifier}...]]
```

### Argument/Description
**expression** - an expression that represents the information to be saved; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**SaveRefInfo Usage**
The SaveRefInfo command will only work with the Event Tmed procedure.
Every time this command is used, a new reference line is created.
Up to eight references may be saved with each tender and each may be up to 19 characters long. Text or fields greater than 19 characters will be truncated.

**SaveRefInfo Example**
The following script allows a user to enter delivery information on a To Go check:

```isl
event tmed : 10
  var rowcnt : n3
  var deliv_desc[6] : a15
  var deliv_info[6] : a20
  var cnt : n3
  deliv_desc[1] = "Name:"
  deliv_desc[2] = "Company:"
  deliv_desc[3] = "Address 1:"
  deliv_desc[4] = "Address 2:"
  deliv_desc[5] = "City:"
  deliv_desc[6] = "Phone:"
  //Display a window with address prompts, and accept delivery info from user
  window 6, 43
  for rowcnt = 1 to 6
    display rowcnt, 2, deliv_desc[rowcnt]
    displayinput rowcnt, 13, deliv_info[rowcnt], "Enter ", deliv_desc[rowcnt]
  endfor
  windoweditwithsave
  //Input can only be terminated by cancel or save
  saverefinfo "DELIVER TO:" //Save this line to check detail
  for cnt = 1 to 6 //If user made an entry on a line, save the entry to check detail
    if len(deliv_info[cnt]) > 0 AND deliv_info[cnt] <> " "
      saverefinfo deliv_info[cnt]
    endif
  endfor
endevent
```

See also:
Event...EndEvent

---

## SetIslTsKey

<!-- src: Command_SetIslTsKey.htm -->

SetIslTsKey

### Function
This command defines a key to be displayed on a touchscreen, allowing you to define a key that normally would be programmed in the Touchscreen Designer form.

### Syntax
```text
(entered as a single line)
SetIslTsKey row, col, num_rows, num_cols, font, key_expression, expression
```

### Argument/Description
**row** - integer expression defining row coordinate of key (1-12)
**col**  - integer expression defining column coordinate of key (1-30)
**num_rows**  - integer expression defining the key height in rows (1-12)
**num_cols**  - integer expression defining the key width in columns (1-30)
**font**  - font size integer expression (1-3)
**key_expression**  - key value to be returned when this key is pressed; it may be one of the following: Key function, user_variable (type Key only) system_variable (@KEYS only)
**expression** - descriptor to appear on the key as it is displayed; it may be one of the following: user_variable, system_variable, constant, string, function, equation

**SetIslTsKey Usage**
- Up to 60 keys may be defined with the SetIslTsKey.
- Any previously defined touchscreen keys are automatically cleared each time a script executes. However, if two or more touchscreens are defined within an event, the ClearIslTs command must be used to clear the touchscreen keys.

**SetIslTsKey Example**
The subroutine below first clears any previously defined touchscreen keys and displays two touchscreen keys, [YES] and [NO], which are defined by the SetIslTsKey command. This subroutine displays these keys as the operator is issued a prompt by the system and captures the operator's input.

```isl
sub get_yes_or_no( ref answer, var prompt_s:A38 )
  var keypress : key
  var data : A20
  clearislts
  setisltskey 2, 2, 4, 4, 1, @Key_Enter, "YES"
  setisltskey 2, 6, 4, 4, 1, @Key_Clear, "NO"
  displayislts
  inputkey keypress, data, prompt_s
  if keypress = @Key_Enter
    answer = 1
  else
    answer = 0
  endif
endsub
```

See also:

ClearIsITs

DisplayIsITs

---

## SetIslTsKeyx

<!-- src: Command_SetIslTsKeyx.htm -->

SetIslTsKeyx

### Function
This command defines a key to be displayed on a touchscreen. Additionally, it defines the icon to be displayed on the touchscreen key as well as the color and placement.

### Syntax
```text
(entered as a single line)
SetIslTsKeyx row, col, num_rows, num_cols, font, key_expression, icon_id, icon_placement, color_combo, expression
```

### Argument/Description
**row** - integer expression defining row coordinate of key (1-6)
**col**  - integer expression defining column coordinate of key (1-10)
**num_rows**  - integer expression defining the key height in rows (1-6)
**num_cols**  - integer expression defining the key width in columns (1-10)
**font**  - font size integer expression (1-3)
**key_expression**  - key value to be returned when this key is pressed; it may be one of the following: Key function, user_variable (type Key only) system_variable (@KEYS only)
**icon_id** - id of icon to be displayed
**icon_placement**  - placement of icon ("L" left, "R", "T", "B", "C")
**color_combo**  - color combination (currently 1 - 42)
**expression**  - descriptor to appear on the key as it is displayed; it may be one of the following: user_variable, system_variable, constant, string, function, equation

**SetIslTsKeyx Example**
The following example defines the icon and icon color for the Enter key.
```isl
SetIslTskeyx 2, 2, 4, 4, 3, @Key_Enter, 10001, "Center", 10, "YES"
```

See also:

DisplayIsTs
SetIsTsKey
SetIsTsKey

---

## SetSignOn[Left/Right]

<!-- src: Command_SetSignOn[Left_Right].htm -->

SetSignOn[Left/Right]

### Function
These commands determine where ISL places the minus sign when formatting numbers.

### Syntax
```text
SetSignOnLeft
or
SetSignOnRight
```

**SetSignOn[Left/Right] Usage**
This is a global command.

By default, ISL puts the minus sign to the right of the number being displayed (for example, -45 will display as "45-"). If this is not acceptable, then executing the SetSignOnLeft command will cause ISL to format all numbers with the minus sign on the left.

SetSignOn[Left/Right] Example
```isl
event inq : 1
  waitforclear -123 //will display `123-' by default
  setsignonleft
  waitforclear -123 //will display `-123'
  setsignonright
  waitforclear -123 //will display `123-'
endevent
```

---

## SetString

<!-- src: Command_SetString.htm -->

SetString

### Function
This command will replace all characters in a string with a particular character.

### Syntax
```text
(entered as a single line)
SetString main_string, character_string[, count]
```

### Argument/Description
**main_string**  - the string in which characters will be replaced; it can be any string_variable
**character_string**  - a string whose first character will be used to replace characters in main_string; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**count**  - optional count of characters to set the main_string to. If not specified, the entire main_string will be replaced with the first character of the character_string

**SetString Example**
The following script constructs and prints a date string bordered by hash marks at the UWS's check printer:

```isl
sub print_date
  var date : a9
  var hash_mark : a24 //Use format to build a date string
  format date as @DAY, "-", @MONTH, "-", @YEAR
  setstring hash_mark, "="
  startprint @CHK //Print what follows at this UWS check printer
    printline hash_mark //Print the date string
    printline @DWON, @REDON, date{=16} // double-wide, in red
    printline hash_mark // and centered between hash marks
  endprint
endsub
```

---

## Split

<!-- src: Command_Split.htm -->

Split

### Function
This command is used to split a field-separated string into separate variables.

### Syntax
```text
(entered as a single line)
Split string_to_split, field_sep_char, user_variable or list_spec [, user_variable or list_spec...]
```

### Argument/Description
**string_to_split** - the field-separated string to split
**field_sep_char** - the character used to the separate fields in the string_to_split; use the Chr function to define the character required
**user_variable**  - a user_variable which will be assigned one of the individual fields from the string_to_split
list_spec is defined as:
- **number_records** : a user integer variable containing the number of records to be built from the string_to_split
- **field_array[: field_array]:** an array_variable that will hold one field per record; you can split a field into more than one array by separating the array_variables using a colon ( : )

**Split Usage**

If the system variable @Strict_Args is set to 1, ISL will ensure that the variable count in the Split command matches the number of fields in the file record. If an incorrect number of fields is specified in the statement or the file is corrupted, an error message will be generated.

**Split Example**

The following example will assume the PMS has sent the guest name and room number as one field. The name is separated by the room number with the [fs] character. Without the Split command, the script would have to search through the field one character at a time until the [fs] character was found. The Split command, however, will automatically split the data into fields:

```isl
event rxmsg : guest
  var name_and _room : a25
  var name : a20
  var room_number : n5
  //Get the data as one field, and
  //split it into 2 fields
  rxmsg name_and_room
  split name_and_room, chr(&1c), name, room_number
  //Display data in window
  window 5, 30, "Guest Inquiry"
  display 2, @CENTER, name
  display 4, @CENTER, room_number
  waitforclear
endevent
```

See also:

```isl
Chr Function

Format

SplitQ
```

---

## SplitQ

<!-- src: Command_SplitQ.htm -->

SplitQ

### Function
This command is used to split a field-separated string into separate variables and strips the quotes from the quoted string.

### Syntax
```text
(entered as a single line)
SplitQ string_to_split, field_sep_char, user_variable or list_spec [, user_variable or list_spec...]
```

### Argument/Description
**string_to_split** - the field-separated string to split
**field_sep_char**  - the character used to the separate fields in the string_to_split; use the Chr function to define the character required
**user_variable**  - a user_variable which will be assigned one of the individual fields from the string_to_split
**list_spec**  is defined as:
- **number_records** - a user integer variable containing the number of records to be built from the string_to_split
- **field_array[: field_array]:**  an array_variable that will hold one field per record; you can split a field into more than one array by separating the array_variables using a colon (:)

**SplitQ Usage**
- The SplitQ command operates in the same way as the Split command, except that it will strip quotes from quoted strings.
- If the system variable @Strict_Args is set to 1, ISL will ensure that the variable count in the SplitQ command matches the number of fields in the file record. If an incorrect number of fields is specified in the statement or the file is corrupted, an error message will be generated.

See also:

```isl
Chr Function

Format

Split
```

---

## StartPrint[WithStatus]...EndPrint[FF/NOFF]

<!-- src: Command_StartPrint[WithStatus]...EndPrint[FF_NOFF].htm -->

StartPrint[WithStatus]...EndPrint[FF/NOFF]

### Function
These commands are used to start and end a print session on any MICROS printer. The StartPrint[WithStatus] command is used to select the printer and start the print session and the EndPrint command ends the print session (which may result in an unclamp of a slip printer). The Form Feed [FF] and No Form Feed [NOFF] may also be used with the EndPrint command, depending on the needs of the application and printer default.
Note: The StartPrint command should not be used in a @trailer/@header event.

### Syntax
```text
(entered as a single line)
StartPrint printer_name|expression [, backup_object number [, reference_line]
```

or

```isl
StartPrintWithStatus printer_name |expression [, reference_line]
  .
  .
  .
EndPrint [or EndPrintFF or EndPrintNOFF]]
```

### Argument/Description
**printer_name** - the object number of the printer
**expression**  - any variable that contains the object number of a printer in the system
**backup_object number**  - the object number for the backup printer that overrides the backup printer programmed in the database
**reference_line**  - the text string to be displayed in the printer error window if an error occurs during printing

**StartPrint[WithStatus]...EndPrint[FF/NOFF] Usage**
- The expression is defined using one of the ISL Printer system variables in the ISL Printer Table.

ISL Printer Table:

ISL Printer Name |  Printer Assignment |  Valid Printer Types |  Red |  FFDefault |  ExtendedPrint |

@RCPT |  Cust. Receipt |  Roll

Slip

|  Optional

No

|  Yes

Yes

|  Yes

No

|

@CHK |  Guest check |  Roll

Slip

|  Optional

No

|  Yes

Yes

|  Yes

No

|

@JNL |  Journal |  Roll |  Optional |  No |  Yes |

@ORDR#

(where # is 1-15 and refers to the appropriate order device)

|  Order (local/remote) |  Roll

Slip

|  Optional

No

|  Yes

Yes

|  Yes

No

|

@VALD |  Validation |  Roll

Slip

|  Optional

No

|  Yes

Yes

|  Yes

No

|

**Note: For all Printers, #Characters per line = 32 and #Character DW = 16**
- The physical printer is selected based on the UWS printer assignments in the 3700 database. For example, when @CHK is selected, the ISL will pass along the information to the Check Printer defined for the UWS, from which the Event was initiated.
- Although it is legal to specify a printer object number of 0, all print jobs printing to 0 will not print—anywhere.
- An invalid object number value (i.e.,-1) will generate an ISL error.
- In the case where a printer fails and a backup printer is programmed, the printing session will notify the operator at the UWS that the printing session has failed and the print session has been sent to the backup printer.
- Both supervised and unsupervised printing are supported by SIM. However, to start a supervised print job, the printer must be specified by the StartPrintWithStatus command.
- Printing will not begin until the EndPrint command is executed. Each printer will FormFeed or not, depending on its default characteristic; EndPrint will follow the printer's default. Use either EndPrintFF or EndPrintNOFF to force the opposite action.
- If single-wide printing is used, anything over 32 characters will be truncated. If the @DWON Print Directive is used, anything over 16 characters will be truncated.
- If the @REDON Print Directive is used with a printer, the correct type of ribbon is required (black/red) for output to print in red.
- Note that only one print session may be active at any one time from the same UWS.

**StartPrint[WithStatus]...EndPrint[FF/NOFF] Example**
The following script allows a user to enter a 10 line message and print it at the kitchen printer:

```isl
event inq : 1
  var kitchen_msg[10] : a20
  var sender_name : a20
  var rowcnt : n3
  var hash_mark : a24
  window 12, 22 //Display the window
  displayinput 1, 2, sender_name, "Enter your name"
  //Accept users name
  //Have user input the message
  for rowcnt = 1 to 10
    displayinput rowcnt + 1, 2, kitchen_msg[rowcnt], "Enter kitchen message"
  endfor
  windowedit //Only save or cancel will
  setstring hash_mark, "=" // end input
  startprint @ordr1 //Start the print job at
    / / remote printer1
    printline hash_mark
    printline "Message from ", sender_name
    printline hash_mark
    for rowcnt = 1 to 10
      if len(kitchen_msg[rowcnt]) > ""
        printline kitchen_msg[rowcnt]
      endif
    endfor
    printline "======= END MESSAGE ========"
  endprint
endevent
```

See also:

PrintLine

---

## Sub... EndSub

<!-- src: Command_Sub... EndSub.htm -->

Sub... EndSub

### Function
These commands are used to declare the start and end of a subroutine. A subroutine may be used by an Event or another subroutine by using the Call command.

### Syntax
```text
(entered as a single line)
Sub name [( Ref | Var parameter [, Ref | Var parameter]...)]
.
.
.
```

EndSub

### Argument/Description
**name** - the subroutine name
**Ref**  - ISL keyword
**Var**  - Var command
**parameter**  - a variable or expression passed from the associated Call command; it may be one of the following:
- variable by reference
- array by reference
- expression by value, i.e. local_variable_name : [A, $, N ] Size, or Key

**Sub... EndSub Usage**
- Each Sub command defines the number and type of parameters that can be passed in. If the Call command has the incorrect number of arguments or the incorrect type of arguments, an error will display.
- Sub commands are not allowed within an Event.
- Each subroutine has access to the calling Event's variables, all global variables, and may declare their own local variables.
- The name may be any length up to 255 characters and must begin with a letter A - Z, a - z, or the underscore character (_). It may include any character in the range A - Z, 0 - 9, and the underscore character.

**Using Subroutines**
ISL subroutines can be passed parameters in the same way as C, BASIC, or Pascal subroutines. Data can be passed in by two methods: value or reference.
By Value
- A parameter in a Sub command is considered to be by value if declared as a normal ISL variable.

Example
```isl
sub get_name( var target_name:A20, var target_id:N5 )
```

Both target_name and target_id are local variables which are assigned the value passed in with the Call command. A Call command to call this subroutine could be:
```isl
call get_name( "Smith", 145 )
```
- Any type of ISL expression can be passed in.
Example

```isl
call get_name( "Smith", 145 + offset )
call get_name( user_input, elist[ 25 ] )
```
- The expression type (string, numeric,...) can be different from the one declared in the Sub command.
Example
```isl
call get_name( "Smith", "45" )
```

The assignment of the expression to the subroutine parameter follows the same rules when setting a variable in a normal assignment expression.
- Arrays cannot be passed in by value.
- When a variable is passed in by value (using the Var command in the Sub statement), a copy is made of the variable and given the name specified in the Sub statement. Any change made to a variable passed by value in a subroutine does not affect the original value of the variable.

```isl
event inq : 1
  var i : n5 = 10 //Set i to 10
  call mysub ( i ) //Pass in i by value
  waitforclear "i = ", i //i is still equal
  // to 10
endevent

sub mysub ( var j : n5 )
  j = 20 //Change local copy,
  // not the original
endsub
```

By Reference
- There are two types of data that can be passed in by reference: variables and arrays. To pass either, the Ref variable is used in the Sub statement. No type information is specified for the referenced variable. For example, in the following line, status is passed by reference and prompt_string is passed by value:

```isl
sub mysub( ref status, var prompt_string:A20 )
```

The following example shows correct and incorrect ways to invoke mysub:
```isl
var result:N5
call mysub( result, "Enter data" ) // Correct
call mysub( result+1, "Enter data" )
// Incorrect: 'result+1' is not a variable.
call mysub( (result), "Enter data" )
// Incorrect: '(result)' is considered an
// expression
```
- To pass an array, empty brackets must be placed after the array name both in the Sub and the Call commands.

Example
```isl
sub mysub( ref data[], var prompt_string:A30 )
```

The following example passes an array to mysub:
```isl
var array[ 10 ]:A20
call mysub( array[], "Enter data" ) // Correct
call mysub( array, "Enter data" )
// Incorrect. Need [] after array
```
- When a variable is passed in by reference, any change in the subroutine to the variable affects the original value of the variable. The name after the Ref variable can be thought of as being another name for the variable passed in.

```isl
event inq : 1
  var i : n5 = 10 //Set i to 10
  call mysub ( i ) //Pass in i by
  // reference
  waitforclear "i = ", i //i is now equal to 20
endevent

sub mysub ( ref j )
  j = 20 //Change original value of i and j to 20
endsub
```

**Sub...EndSub Example**

The event below calls a subroutine, format_data, that formats the current date as follows: dd-mmm-yyyy.
```isl
event inq : 1
  var date : a11
  call format_date( date, @day, @month, @year)
  window 3,len(date)+2
  display 2,2,date
  waitforclear date
endevent

sub format_date( ref date, var day : n5, var month : n5, var year : n5 )
  var month_arr[12] : a3
  month_arr[1] = "JAN"
  month_arr[2] = "FEB"
  month_arr[3] = "MAR"
  month_arr[4] = "APR"
  month_arr[5] = "MAY"
  month_arr[6] = "JUN"
  month_arr[7] = "JUL"
  month_arr[8] = "AUG"
  month_arr[9] = "SEP"
  month_arr[10] = "OCT"
  month_arr[11] = "NOV"
  month_arr[12] = "DEC"
  format date as day, "-", month_arr[ month ], "-", year
endsub
```

See also:

Call

Var

---

## System

<!-- src: Command_System.htm -->

System

### Function
This command may be used to create a process on the local machine.

---

## Test_Dsvc

<!-- src: Command_Test_Dsvc.htm -->

Test_Dsvc

### Function
This command may be used to verify a discount or service charge. An amount or percentage can be passed with the function when checking a discount or service charge that is not a preset item.

### Syntax
```text
(entered as a single line)
Test_Dsvc Obj_Num
or
Test_Dsvc Obj_Num, Value
```

### Argument/Description
**Obj_Num**  — The object number of the discount or service charge.
**Value**  — Optional value that is the amount or percentage to be applied.

**Test_Dsvc Example**
```isl
Event inq:1
  Test_Dsvc 202, 5.00 // Open $ Discount
  InfoMessage "Open $ Discount, $5.00", @Test_Dsvc_Ttl
EndEvent
```

---

## Touchscreen

<!-- src: Command_Touchscreen.htm -->

Touchscreen

### Function
This command allows the system to display a pop-up touchscreen. This feature improves operator prompting, making the system easier to use.

### Syntax
```text
Touchscreen numeric_expression
```

### Argument/Description
**numeric_expression** - the object number of a pre-defined touchscreen, programmed in the 3700 database

**Touchscreen Usage**
- The command references a touchscreen in the Touchscreens form. This Touchscreen number must already be setup in the 3700 database.
- The Touchscreen will disappear when this interface session is complete. As an example, when prompting for the guest's room number, the Touchscreen could display a numeric keypad. Touchscreen 0 will cause the default touchscreen to be used.

---

## TxMsg

<!-- src: Command_TxMsg.htm -->

TxMsg

### Function
This command defines the applications data segment of a message that will be transmitted over the interface.

### Syntax
```text
(entered as a single line)
TxMsg expression[{output_specifier}][, expression[{output_specifier}] ...]
```

### Argument/Description
**expression** - an expression that will be transmitted over the interface; it may be one of the following: user_variable, system_variable, constant, string, function, equation, **{output_specifier}** , one or more of the output specifiers that determine the format of the output fields

**TxMsg Usage**
- The TxMsg command must be followed by the WaitForRxMsg or GetRxMsg command.
- If more than one field is required, multiple expressions must be separated by commas. These commas will be replaced in the message received by the interfaced system by field separator characters (ASCII 1CH).
- A statement may continue over multiple lines by including the line continuation character (\) at the end of each line. The line continuation character is very useful as TxMsg commands tend to be very lengthy.

**TxMsg Example**

A transmission message that includes the check employee number, the check number, tendered total, and a declared room number field could be defined as follows:

```isl
event inq : 1
  var room_num : a4
  input room_num, "Enter Room Number"
  txmsg "charge_inq",@Ckemp,@Cknum,@Tndttl,room_num
  //The first field (charge_inq) is an
  // example of an identifying string
  // that the PMS might use to process
  // message from the POS.
  waitforrxmsg
endevent

event rxmsg : charge_declined //This is one of the PMS response
  // possibilities
  var room_num : a4
  rxmsg room_num
  exitwitherror "Charge for room ", room_num," declined"
endevent
```

See also:

Event...EndEvent

GetRxMsg

RxMsg

WaitForRxMsg

---

## UpperCase

<!-- src: Command_UpperCase.htm -->

UpperCase

### Function
This command is used to convert a string variable to uppercase.

### Syntax
```text
UpperCase string_variable
```

### Argument/Description
**string_variable**  - the string that will be changed to an uppercase user_variable (string)

See also:

LowerCase

---

## Use[Compat/ISL]Format

<!-- src: Command_Use[Compat_ISL]Format.htm -->

Use[Compat/ISL]Format

### Function
These commands are used to instruct ISL to use the ISL message format or the 2700-compatible message format.

### Syntax
```text
UseCompatFormat
or
UseISLFormat
```

**Use[Compat/ISL]Format Usage**
- These commands are global.
- For more information, please see "Message Formats" in the 3700 System Interface Module (SIM) User’s Guide.

---

## Use[ISL/STD]TimeOuts

<!-- src: Command_Use[ISL_STD]TimeOuts.htm -->

Use[ISL/STD]TimeOuts

### Function
These commands instruct ISL how to process a PMS timeout. UseISLTimeOuts will search the script file for an RxMsg Event with an Event ID of _Timeout. UseSTDTimeOuts will use the standard 3700 error messaging for a PMS timeout.

### Syntax
```text
UseISLTimeOuts
or
UseSTDTimeOuts
```

**Use[ISL/STD]TimeOuts Usage**
- The Event ID _Timeout will by-pass the standard 3700 error messaging for a PMS timeout and process instructions from the ISL script file.
- For example, if the UseISLTimeOuts command is used and the PMS does not respond to an ISL message within the timeout period, the ISL script may then ask the user if the processing should be cancelled, or if a backup tender should be used.

**Use[ISL/STD]TimeOuts Example**

```isl
sub message
  UseIslTimeouts //To call timeout event var choice : n1
  forever
    window 3,30
    display 1,1,"Press 1 for Eat in"
    display 2,1,"Press 2 for Carry Out"
    display 3,1,"Press 0 to Exit"
    input choice,"Choice:"
    if choice = 1
      usecompatformat
      txmsg "eat in"
      waitforrxmsg
      exitcontinue
    elseif choice = 2
      useislformat
      txmsg "carry out
      waitforrxmsg
      exitcontinue
    elseif choice = 0
      exitcancel
    endif
  endfor
endsub //sub message

event rxmsg : _timeout
  errormessage "You need to re-transmit message"
  call message
endevent
```

See also:

Event...EndEvent

RxMsg

TxMsg

---

## UseFilteredDetail

<!-- src: Command_UseFilteredDetail.htm -->

UseFilteredDetail

### Function
This command is used to access guest check detail items that match the specified filter (if seat filtering is active).

### Syntax
```text
UseFilteredDetail
```

**UseFilteredDetail Usage**
- This is a global command. As a result, it is initialized at the beginning of the script and then maintained for the duration, or until a UseUnFilteredDetail command is encountered.
- Because Guest Check Information Detail Lines always default to seat 0, they ARE NOT accessible.
- The UseFilteredDetail command has no affect if seat filtering is inactive (@filter_active + "N"). In this case, all of the detail will be displayed.

```isl
UseFilteredDetail Example

event inq : 1
  var filter_flag: a1
  var filter_mask : a8
  var i : n4
  window 12,50
  filter_flag = @filter_active
  filter_mask = @filter_mask
  display 1,2,"filter var is - ", filter_flag
  display 2,2,"filter seat mask is - ", filter_mask
  waitforclear
  windowclear
  usefiltereddetail
  for i = 1 to @numdtlt
    display 11,5,i,"of",@numdtlt
    display 1,2,"detail main level - ",@dtl_mlvl[i]
    display 2,2,"detail name - ",@dtl_name[i]
    display 3,2,"detail object number - ",@dtl_objnum[1]
    display 4,2,"detail price level - ",@dtl_plvl[i]
    display 5,2,"detail quantity - ",@dtl_qty[i]
    display 6,2,"detail seat - ",@dtl_seat[i]
    waitforclear
  endfor
  windowclear
  useunfiltereddetail
  for i = 1 to @numdtlt
    display 11,5,i,"of",@numdtlt
    display 1,2,"detail main level - ",@dtl_mlvl[i]
    display 2,2,"detail name - ",@dtl_name[i]
    display 3,2,"detail object number - ",@dtl_objnum[1]
    display 4,2,"detail price level - ",@dtl_plvl[i]
    display 5,2,"detail quantity - ",@dtl_qty[i]
    display 6,2,"detail seat - ",@dtl_seat[i]
    waitforclear
  endfor
Endevent
```

See also:

Filter_active

Filter_mask

SaveChkInfo

UseUnFilteredDetail

---

## UseUnFilteredDetail

<!-- src: Command_UseUnFilteredDetail.htm -->

UseUnFilteredDetail

### Function
This command is used to access all of the guest check detail items.

### Syntax
```text
UseUnFilteredDetail
```

**UseUnFilteredDetail Usage**
- This is a global command. As a result, it is initialized at the beginning of the script and then maintained for the duration, or until a UseFilteredDetail command is encountered.
- This command can be used to toggle back and forth within a single event.

**UseUnFilteredDetail Example**

```isl
event inq : 1
  var filter_flag: a1
  var filter_mask : a8
  var i : n4
  window 12,50
  filter_flag = @filter_active
  filter_mask = @filter_mask
  display 1,2,"filter var is - ", filter_flag
  display 2,2,"filter seat mask is - ", filter_mask
  waitforclear
  windowclear
  usefiltereddetail
  for i = 1 to @numdtlt
    display 11,5,i,"of",@numdtlt
    display 1,2,"detail main level - ",@dtl_mlvl[i]
    display 2,2,"detail name - ",@dtl_name[i]
    display 3,2,"detail object number - ",@dtl_objnum[1]
    display 4,2,"detail price level - ",@dtl_plvl[i]
    display 5,2,"detail quantity - ",@dtl_qty[i]
    display 6,2,"detail seat - ",@dtl_seat[i]
    waitforclear
  endfor
  windowclear
  useunfiltereddetail
  for i = 1 to @numdtlt
    display 11,5,i,"of",@numdtlt
    display 1,2,"detail main level - ",@dtl_mlvl[i]
    display 2,2,"detail name - ",@dtl_name[i]
    display 3,2,"detail object number - ",@dtl_objnum[1]
    display 4,2,"detail price level - ",@dtl_plvl[i]
    display 5,2,"detail quantity - ",@dtl_qty[i]
    display 6,2,"detail seat - ",@dtl_seat[i]
    waitforclear
  endfor
Endevent
```

See also:

Filter_active

Filter_mask

SaveChkInfo

UseFilteredDetail

---

## Var

<!-- src: Command_Var.htm -->

Var

### Function
This command is used to declare user variables. When it is used outside an Event or subroutine, the user variable will be accessible globally. When it is used inside an Event or subroutine, the variable is considered "local" and is only allowed to be used by that Event or any subroutine called by the Event.

### Syntax
```text
Var user_variable : variable_specifier
```

### Argument/Description
**user_variable** - a user-defined name for a variable. If an array_variable is being declared, the user_variable must be followed immediately by brackets containing the maximum number of items the array_variable may contain, e.g., name[100]
**variable_specifier**  - made up of a type and a size specifier. The type_specifier can be an N, $, or A key. The size specifier can be either a number (i.e., 12) or an integer expression enclosed in parentheses, i.e., (12 + 15). If the Key type_specifier is used, the size should not be included. The variable_specifier is concatenated together, and defines whether the variable is alphanumeric, numeric (integer), a decimal, or a key, and, if its one of the first three, how many characters/digits it contains

**Var Usage**
- The user_variable name can be up to 255 characters in length and must begin with a letter A - Z, a - z, or the underscore character (_). It may include any character in the range A - Z, 0 - 9, and the underscore character. Case is insignificant and the name must not contain spaces.
- It is possible to declare a variable with a size that is defined by an expression, rather than a hard-coded number. These are known as variable-size variables. If the ISL encounters a left parentheses immediately following the type of the variable, it will assume that an expression follows, which defines the variable's size. Variable-size variables can be declared as follows:

```isl
var i : n3 = 15
var window_width : n(i + 15)
```

If i = 15, then the line shown above would be the same as:

```isl
var window_width : N30
```
- If the size of the variable is not known when the variable is being defined, then the variable size may be placed within parentheses.

```isl
var string : A10
var string : A( 7 + 3 ) //Same as A10
var string : A( num_guests * 2 ) //Depends on value

// num_guests
```
- The type_specifier is different for each of the four types of user-defined variables. Note that no size is specified when declaring a key variable.

Field Type Type Specifier Example
Numeric n or N n3
Decimal $ $6
Alphanumeric a o A a25
Key key key
```isl
For more information about variable_specifiers, please see "Data Types".
```
The declaration of a four digit room number would be defined as:

```isl
var room_num:N4
```

An array with six elements may also be defined as:

```isl
var message_text[6]:A32
```

More than one variable can be declared on the same line, as long as they are separated by commas:

```isl
var room_num : a5, guest_count : n3
```

Variables can be declared and defined on the same line:

```isl
var city_name : a10 = "Charleston"
```
- Zero-length arrays and zero-size variables are allowed.
- All variables are cleared when a new Event is executed, unless the RetainGlobalVar command is used (which only affects global variables).

**Var Example**

```isl
var guest_name : A20
var guests[max_guests] : A(max_name_length)
```

See also:

Retain GlobalVar

Discard GlobalVar

---

## VoidDetail

<!-- src: Command_VoidDetail.htm -->

VoidDetail

### Function
This command is used to void an item from the check detail.

### Syntax
```text
VoidDetail(expression)
```

**Description/Argument**
Expression – Uses any valid expression that evaluates to a valid detail number in the range 1 to @NumDtlt.

Note
This function will “fail” silently. For example, if the expression is outside the range 1 to @NumDtlt, the function does not report an error. In addition, if the expression evaluates to a detail item that cannot be voided (i.e., part of a combo meal), the function will not void the item, and does not report an error.
The detail is voided as a “system” void. This method avoids prompting the user for authorization when it is otherwise required. This includes voiding of previous round items.

**VoidDetail Example**
The following example attempts to void all menu items in the previous and current rounds:

```isl
Var I : N9
For I = 1 to @NumDtlt
  If(@Dtl_Type[1] = “M”)
    voidDetail(i)
  endif
endFor
```

---

## WaitForClear

<!-- src: Command_WaitForClear.htm -->

WaitForClear

### Function
This command requires the operator to press the [Clear] key before proceeding. It is often used after the Display command.

### Syntax
```text
(entered as a single line)
WaitForClear [prompt_expression[{output_specifier}]] [,prompt_expression[{output_specifier}]...]
```

### Argument/Description
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**WaitForClear Usage**
- The default prompt, "Press Clear to continue", will appear on the prompt line of the UWS. This may be overridden by providing a prompt_expression with the command.
- The combined length of all prompt_expressions must not exceed 38 characters (including spaces); extra characters will be truncated.

**WaitForClear Example**

The following script would display some text, then require the operator to press the [Clear] key before continuing:

```isl
event inq : 1
  window 1, 14
  display 1, 2, "Goodbye " //"You say Goodbye"
  waitforclear
  display 1, 2, "Hello " // "and I say Hello"
  waitforclear
endevent
```

See also:

Display

GetRxMsg

WaitForConfirm

WaitForEnter

WaitForRxMsg

---

## WaitForConfirm

<!-- src: Command_WaitForConfirm.htm -->

WaitForConfirm

### Function
This command requires the operator to press the [Enter] key or the [Clear] key.

### Syntax
```text
(entered as a single line)
WaitForConfirm [prompt_expression[{output_specifier}]] [,prompt_expression[{output_specifier}]...]
```

### Argument/Description
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**WaitForConfirm Usage**
- If the operator presses the [Enter] key, the script will continue.
- If the operator presses the [Clear] key, the operation will be cancelled and the script will be exited. The default prompt, "Press [Enter] to continue", will appear on the prompt line of the UWS. This may be overridden by providing a prompt_expression with the command.
- The combined length of all prompt_expressions must not exceed 38 characters (including spaces); extra characters will be truncated.

**WaitForConfirm Example**

The following script is a transmission message that includes the check employee number, the check number, tendered total, and a declared room number field. After the room_num is displayed, the script will wait for the [Enter] key or the [Clear] key:

```isl
event inq : 1
  var room_num : a4
  input room_num, "Enter Room Number"
  waitforconfirm
  txmsg "charge_inq",@Ckemp,@Cknum,@Tndttl,room_num
  //The first field (charge_inq) is an
  // example of an identifying string
  // that the POS might use to process
  // message from the POS.
  waitforrxmsg
endevent

event rxmsg : charge_declined //This is one of the PMS response
  // possibilities
  var room_num : a4
  rxmsg room_num
  exitwitherror "Charge for room ", room_num," declined"
endevent
```

See also:

Display

GetRxMsg

WaitForClear

WaitForEnter

WaitForRxMsg

---

## WaitForEnter

<!-- src: Command_WaitForEnter.htm -->

WaitForEnter

### Function
This command requires the operator to press the [Enter] key before proceeding.

### Syntax
```text
(entered as a single line)
WaitForEnter [prompt_expression[{output_specifier}]] [,prompt_expression[{output_specifier}]...]
```

### Argument/Description
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**WaitForEnter Usage**
- The default prompt, "Press Enter to continue", will appear on the prompt line of the UWS. This may be overridden by providing a prompt_expression with the command.
- The combined length of all prompt_expressions must not exceed 38 characters (including spaces); extra characters will be truncated.

**WaitForEnter Example**

The following script would display the guest's name and require the operator to press the [Enter] key before continuing:

```isl
event rxmsg : guest
  var name : a20
  rxmsg name
  waitforenter "guest is ", name
endevent
```

See also:

Display

GetRxMsg

WaitForClear

WaitForConfirm

WaitForRxMsg

---

## WaitForRxMsg

<!-- src: Command_WaitForRxMsg.htm -->

WaitForRxMsg

### Function
This command is used after a message has been transmitted over the interface so that the system waits for a response.

### Syntax
```text
(entered as a single line)
WaitForRxMsg [prompt_expression[{output_specifier}]] [,prompt_expression[{output_specifier}]...]
```

### Argument/Description
**prompt_expression** - an expression displayed on the prompt line, usually to instruct the user what to enter; it may be one of the following: user_variable, system_variable, constant, string, function, equation
**{output_specifier}**  - one or more of the output_specifiers that determine the format of the output fields

**WaitForRxMsg Usage**
- The default prompt, "Please Wait--Sending Message", will appear on the prompt line of the UWS. The default may be overridden by providing a prompt_expression with the command.
- The WaitForRxMsg is not a stand-alone command; the TxMsg command must precede the WaitForRxMsg. The WaitForRxMsg command is an implicit return.
- When a TxMsg statement is followed by a WaitForRxMsg statement and a response message is received from the interfaced system, it will assume that there is a return event (Event RxMsg) that corresponds to the message from the interfaced system.

```isl
WaitForRxMsg Example
```

A transmission message that includes the declared room number field could be defined as follows:

```isl
event inq : 1
  var room : n5
  input room, "Room? "
  txmsg "room_inq", room
  waitforrxmsg //Script stops here
  waitforclear //Not executed because
  // waitforrxmsg has
  // terminated event
endevent
```

See also:

Event...EndEvent

GetRxMsg

RxMsg

TxMsg

WaitForClear

WaitForConfirm

WaitForEnter

---

## While

<!-- src: Command_While...EndWhile.htm -->

While...EndWhile

### Function
The While command is used to implement a loop structure. The EndWhile is used to end the loop.

### Syntax
```text
While expression
.
.
.
EndWhile
```

### Argument/Description
**expression** - the loop condition expression to be evaluated; it may be one of the following: user_variable, system_variable constant, string, function, equation

**While...EndWhile Usage**
- When ISL encounters a While statement, it will execute all statements within the While and its corresponding EndWhile command until the expression in the While command becomes FALSE. If the expression is not initially true, then the statements within the While block are not executed.

```isl
sub get_id(ref id )
  var done : N3
  done = 0
  while NOT done
    input id, "Enter id"
    if id > 0 AND id < MAX_ID
      done = 1
    endif
  endwhile
endsub
```
- The While command can be nested within other While commands.
- The expression in the While command is similar to the conditional expression within the If command.

**While...EndWhile Example**

```isl
event inq : 1
  while data_ok = 1
    max_data = 10
    while i < max_data
      call get_next_line
      i = i + 1
    endwhile
  endwhile
endevent
```

See also:

For...EndFor

ForEver...EndFor

If..Else[If]...EndIf

---

## Window

<!-- src: Command_Window.htm -->

Window

### Function
This command will draw a window on the operator display and is required in order to display information referenced by the various Display commands.

### Syntax
```text
(entered as a single line)
Window row, column[, expression[{output_specifier}]...]
```

### Argument/Description
**row** - the number of rows the window should contain; valid entries are 1 to 12
**column**  - the number of columns the window should contain; valid entries are 1 to 78
**expression**  - an expression that represents the title of the window, which will appear centered in the top line of the window itself (above the first row); it may be on of the following: user_variable, string, {output_specifiers}, one or more of the output_specifiers that, determine the format of the output fields

**Window Usage**
- The row and column values in the window are a function of how much you need to display. Refer to the Display commands to determine these requirements.
- The optional window title may be a text string or a combination of user_variables and string_variables.
- The maximum number of characters that will be displayed in the Window title is the number of columns minus 1; extra characters will be truncated.

**Window Example**

The following script will read the information from Track 2 of a
credit card and display it in a window:

```isl
event inq : 1
  var account_num : a19
  var expiration_date : n4
  var track2_data : a79
  window 2, 78
  displaymsinput 1, 2, account_num{m2, 1, 1, *}, "Enter Account Number",\
  2, 2, expiration_date{m2, 2, 1, 4}, "Enter Expiration"
  windowinput
  waitforclear
endevent
```

See also:

Display

DisplayInput

DisplayMSInput

WaitforClear

WaitforConfirm

WaitforEnter

WindowClear

WindowClose

---

## Window[Edit/Input][WithSave]

<!-- src: Command_Window[Edit_Input][WithSave].htm -->

Window[Edit/Input][WithSave]

### Function
One of these commands is required any time the DisplayInput and DisplayMSInput commands are used. The WindowEdit and WindowInput determine whether or not the contents of the variables are cleared before being displayed. The [WithSave] option, with either command, determines how the input session will be terminated.

**Syntax 1**
WindowEdit[WithSave]

**Syntax 2**
WindowInput[WithSave]

**Window[Edit/Input][WithSave] Usage**
- When one of the WindowEdit or WindowInput commands is found, SIM will look for the first and subsequent DisplayInput or DisplayMSInput, since the window was drawn and executes it. Therefore, the WindowEdit and WindowInput command must be preceded by both a Window command and at least one DisplayInput or DisplayMSInput command.
- The WindowEdit and WindowEditWithSave commands do not clear the variables. If the input_variables contain data, the contents will be displayed in the input window. These commands are useful when the operator must change only a few fields or characters of a record. The WindowInput and WindowInputWithSave commands clear the variables before they are displayed. All previous information in the fields is lost after the command is executed. These commands are useful for entering new information.
- WindowEdit\Input can be used with the Display[MS]Input commands to build a screen of input fields in order to accept input from the user. Navigating among the input fields is achieved with the movement keys: up arrow, down arrow, home, and end. You can also navigate with [Enter], which moves the focus to the next field, and [Clear], which moves the focus to the previous field.
- The WindowInput and WindowEdit commands complete the Input session when the cursor is on the last field and the user presses the [Enter] key or the [Down Arrow] key. The Input session is cancelled if the cursor is on the first field and the user presses the [Clear] key or the [Up Arrow] key or the last field and the user presses [Enter] or [Down Arrow].
- The WindowInputWithSave and WindowEditWithSave commands require the operator to either press the [Save] key to complete the Input session, or press the [Cancel] key to cancel it. If the cursor is on the last edit field and either the [Enter] key or the [Down Arrow] key is pressed, the cursor will roll to the first field. Likewise, if the cursor is on the first edit field and either the [Clear] key or the [Up Arrow] key is pressed, the cursor will roll to the last field.

**Window[Edit/Input][WithSave] Example 1**

The following script will read the information from Track 2 of a credit card:

```isl
event inq : 1
  var account_num : a19
  var expiration_date : n4
  var track2_data :a79
  window 2, 78
  displaymsinput 1, 2, account_num{m2, 1, 1, *}, "Enter Account Number",\
  2, 2, expiration_date{m2, 2, 1, 4}, "Enter Expiration"
  windowinput
  waitforclear
endevent
```

**Window[Edit/Input][WithSave] Example 2**
The following script will allow input of customer information in a window:

```isl
event inq : 1
  var name : a20
  var address1 : a20
  var address2 : a20
  var city : a20
  var state : a2
  var zip : a10
  var tel : a12
  window 7, 33
  display 1, 2, " Name:"
  display 2, 2, " Address1:"
  display 3, 2, " Address2:"
  display 4, 2, " City:"
  display 5, 2, " State:"
  display 6, 2, " Zip:"
  display 7, 2, "Telephone:"
  displayinput 1, 13, name, "Enter name"
  displayinput 2, 13, address1, "Enter address1"
  displayinput 3, 13, address2, "Enter address2"
  displayinput 4, 13, city, "Enter city"
  displayinput 5, 13, state, "Enter state"
  displayinput 6, 13, zip, "Enter zip"
  displayinput 7, 13, tel, "Enter telephone number"
  windoweditwithsave
  txmsg "new_member", name, address1, address2, city, state, zip, tel
  waitforrxmsg
endevent
```

See also:

DisplayInput

DisplayMSInput

Window

---

## WindowClear

<!-- src: Command_WindowClear.htm -->

WindowClear

### Function
This command clears the contents of a currently displayed window.

### Syntax
```text
WindowClear
```

**WindowClear Example**

The following script builds a window, displays some text, clears the text from the window (after the operator presses [Clear]), then displays some more text:

```isl
event inq : 1
  window 1, 14
  display 1, 2, "Hello" //"You say Hello"
  waitforclear
  windowclear
  display 1, 2, "Goodbye" // "and I say Goodbye"
  waitforclear
endevent
```

See also:

Window

---

## WindowClose

<!-- src: Command_WindowClose.htm -->

WindowClose

### Function
This command closes a currently displayed window.

### Syntax
```text
WindowClose
```

**WindowClose Usage**

Windows close automatically when a script is exited, or when a new window is built with the Window command. The WindowClose command allows the script writer to close a window before either of these events has occurred.

**WindowClose Example**

The following script builds a window, displays some text, then closes the window (after the operator presses [Clear]):

```isl
event inq : 1
  window 1, 14
  display 1, 2, "Hello" //"You say Hello"
  waitforclear
  windowclose
  display 1, 2, "Goodbye" // "and I say Goodbye"
  waitforclear
endevent
```

See also:

Window

---

## WindowScrollDown

<!-- src: Command_WindowScrollDown.htm -->

WindowScrollDown

### Function
This command is used to scroll all lines in the current window down one line.

### Syntax
```text
WindowScrollDown
```

**WindowScrollDown Usage**
- A Window command must be executed prior to this command.
- The first line in the window is cleared to all spaces.

See also:

WindowsScrollUp

---

## WindowScrollUp

<!-- src: Command_WindowScrollUp.htm -->

WindowScrollUp

### Function
This command is used to scroll all lines in the current window up one line.

### Syntax
```text
WindowScrollUp
```

**WindowScrollup Usage**
- A Window command must be executed prior to this command.
- The last line in the window is cleared to all spaces.

**WindowScrollUp Example**

This script opens a window and displays a list of names. When the [Enter] key is pressed, the window will scroll up, and the next name will be displayed at the bottom of the window. When all names have been displayed, the script will exit.

```isl
event inq:2
  var names[ 20 ] : A20
  var i:N5, next:N5, answer:N5
  var WINROWS:N3 = 10, WINCOLS:n3 = 20
  for i = 1 to arraysize( names ) //Fill in 'names' with a set
    // of dummy names to display.
    format names[i] as "List name ", i
  endfor
  window WINROWS, WINCOLS //Open window and display
  // first WINROWS entries in list.
  for i = 1 to WINROWS
    display i, 2, names[i]
  endfor
  next = WINROWS + 1 //Keep looping while ENTER is
  // pressed and data left to
  // display.
  forever
    // Get key from user. If CLEAR pressed, or no data left to display, quit.
    getenterorclear answer, "Press ENTER to scroll, CLEAR to quit"
    if answer = 0 OR next > arraysize( names )
      break
    endif
    windowscrollup //Scroll window up, display
    // next line at the bottom.
    display WINROWS, 2, names[ next ]
    next = next + 1
  endfor
endevent
```

See also:

WindowsScrollDown
