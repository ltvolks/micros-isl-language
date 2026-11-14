# ISL reference: events

Source: RES 3700 SIM Online Help (CHM). Each entry starts with `## ` and the page name; grep `^## ` for an index.


---

## Event Begin_Check

<!-- src: Command_Event Begin_Check.htm -->

Event Begin_Check

### Syntax
```text
Event Begin_Check
```

**Event Begin_Check Example**

```isl
Event Begin_Check
  errormessage "Check Begun Check Number is ", @Cknum
EndEvent
```

---

## Event ClockIn

<!-- src: Command_Event ClockIn.htm -->

Event ClockIn

### Syntax
```text
Event ClockIn
```

**Event ClockIn Example**
```isl
Event ClockIn
  var text : a20 = "Clocked In"
  var title : a20 = "ClockIn Status"
  InfoMessage title, text
EndEvent
```

---

## Event ClockOut

<!-- src: Command_Event ClockOut.htm -->

Event ClockOut

### Syntax
```text
Event ClockOut
```

**Event ClockOut Example**
```isl
Event ClockIn
  var text : a20 = "Clocked Out"
  var title : a20 = "ClockOut Status"
  InfoMessage title, text
EndEvent
```

---

## Event Dsc

<!-- src: Command_Event Dsc.htm -->

Event Dsc

This event is called after a discount is added to the guest check. The event is executed for each configured SIM interface.

### Syntax
```text
Event dsc
```

**Event Dsc Example**
```isl
event dsc
  errorMessage "Discount added to the check."
endevent
```

---

## Event Dsc_Error_Correct_Items

<!-- src: Command_Event Dsc_Error_Correct_Items.htm -->

Event Dsc_Error_Correct_Items

This event is called after a discount is voided from the guest check an error correction (e.g., last item void). The event is executed for each configured SIM interface.

### Syntax
```text
Event dsc_error_correct_items
```

**Event Dsc_Error_Correct_Items Example**
```isl
event dsc_error_correct_items
  errorMessage "Discount was error corrected."
endevent
```

---

## Event Dsc_Void

<!-- src: Command_Event Dsc_Void.htm -->

Event Dsc_Void

This event is called after a discount is voided from the guest check via either direct void or touch void. The event is executed for each configured SIM interface.

### Syntax
```text
Event dsc_void
```

**Event Dsc_Void Example**
```isl
event dsc_void
  errorMessage "Discount was voided from the check."
endevent
```

---

## Event Dtl_Changed

<!-- src: Command_Event Dtl_Changed.htm -->

Event Dtl_Changed

This event is fired after the all totals have been updated to reflect changes made in the check detail during a POS operation (e.g., using auto-combo recognition, modifying condiments, voiding items, etc.).
The event will only fire once per POS operation.

### Syntax
```text
Event Dtl_Changed
```

**Event Dtl_Changed Example**
```isl
event Dtl_Changed
  var msg : A50
  format msg as "Number of detail items is now : ", @numdtlt
  infomessage msg
endevent
```

---

## Event Exit

<!-- src: Command_Event Exit.htm -->

Event Exit

### Syntax
```text
Event Exit
```
- This event executes when POS operations is exiting. It is executed for each active interface. If the interface script does not have an exit event defined, no error will be generated.
- This event should be used when a script needs to perform some cleanup processing upon exit.
- No user input is allowed in this event.

**Event Exit Example**
This is an example of where Event Exit would be used.

```isl
event exit
  call clean_up
endevent
```

---

## Event Final_Tender

<!-- src: Command_Event Final_Tender.htm -->

Event Final_Tender

### Syntax
```text
Event Final_Tender
```

- This event is called after the last tender has occurred, but just before the check is closed. This event is a separate event from the Event Tmed event. An Event Tmed event is used to post the tender, while the Event Final_Tender is used when the check has been completely tendered. For example, you could use the Event Final_Tender to implement the following features with the ISL:
- creating a specialized printout of a guest check for which neither the Event Inq or Tmed can be called when all the check detail is in the check
- sending log information to a PMS containing all of the check information
- If the Event Final_Tender is not present in the script, no error will occur.
- Unlike the Event Tmed, when using the Event Final_Tender command, a tender does not need to be linked to a PMS.
- When the Event Final_Tender is executed, ISL will execute the event for each script linked to a PMS Computer.
- There is no event_ID field for the Event Final_Tender.

**Event Final_Tender Example**
This event is used to send a message to the PMS indicating which table has just paid its check.

```isl
event final_tender
  txmsg "CHECK_PAID", @cknum, @tblnum
  // Here we do a 'getrxmsg' to receive the message to fulfill the
  // requirements of the protocol, but do not process any data
  // associated with the message.
  getrxmsg
endevent
```

---

## Event Idle_No_Trans

<!-- src: Command_Event Idle_No_Trans.htm -->

Event Idle_No_Trans

### Syntax
```text
Event Idle_No_Trans
```

- This event is used to run SIM scripts in the background, when POS operations are idle and no one is signed in. If an employee should sign in, POS operations will not call the Idle_No_Trans event until they sign out again.
- The frequency at which the SIM script is called is determined by the @Idle_Seconds variable.


**Event Idle_No_Trans Example**
The following scripts will initialize the @Idle_Seconds system variable, and then the Idle_No_Trans event be called 10 times before it stops the procedure.

```isl
var count : N5
event init
  //Set to call Idle_No_Trans every 5 seconds
  @Idle_Seconds = 5
  count = 0
endevent

event Idle_No_Trans
  count = count + 1
  waitforclear "Idle_No_Trans: count", count
  //If we’ve done this 10 times, stop the idle call.
  if count > 10
    @idle_seconds = 0
  endif
endevent
```

---

## Event Init

<!-- src: Command_Event Init.htm -->

Event Init

### Syntax
```text
Event Init
```

- This event executes when POS operations is started. This event should be used to perform any initialization required by the script.
- No user input is allowed in this event.


**Event Init Example**
The following scripts will initialize the @Idle_Seconds system variable, and then the Idle_No_Trans event be called 10 times before it stops the procedure.

```isl
var count : N5
event init
  //Set to call Idle_No_Trans every 5 seconds
  @Idle_Seconds = 5
  count = 0
endevent

event Idle_No_Trans
  count = count + 1
  wait forclear "Idle_No_Trans: count ", count
  //If we’ve done this 10 times, stop the idle call.
  if count > 10
    @idle_seconds = 0
  endif
endevent
```

---

## Event Inq

<!-- src: Command_Event Inq.htm -->

Event Inq

### Syntax
```text
Event Inq : number
```

### Argument/Description
**number** - corresponds to a pre-defined SIM Inquiry key programmed in the 3700 database, or * to execute the Event whenever it is encountered

**Caution**
If the *event command is placed before a specific event, OPS will not read any text entered after the *. Therefore, any code written after the * will be ignored and your program will not work as expected. When using the *event command, make sure to place it at the end of the ISL file.
- The Event Inq command is executed when a SIM Inquiry key is used at a UWS.
- The valid entry for number is 1 through 1023.

**Event Inq Example**
This is an example of a standard Inquiry event:

```isl
event inq : 1
  var menu_choice : n3
  window 3, 23
  .
  .
  .
endevent
```

---

## Event Pickup_Check

<!-- src: Command_Event Pickup_Check.htm -->

Event Pickup_Check

### Syntax
```text
Event Pickup_Check
```

**Event Pickup_Check Example**

```isl
Event Pickup_Check
  errormessage "Check Picked up", "Num detail = ", @Numdtlt
EndEvent
```

---

## Event Pretender

<!-- src: Command_Event Pretender.htm -->

Event Pretender

**Function:**

This event is called before a tender payment is added to the guest check. The event is executed for each configured SIM interface.

### Syntax
```text
Event Pretender
```

**Event Pretender Example**
```isl
Event Pretender
  InfoMessage "Pretender Event"
EndEvent
```

---

## Event Print_Header/Trailer

<!-- src: Command_Event Print_Header_Trailer.htm -->

Event Print_Header/Trailer

Note: The StartPrint command should not be used in a @trailer/@header event.

### Syntax
```text
Event Print_Header: alpha/numeric
Event Print_Trailer: alpha/numeric
```

### Argument/Description
**alpha/numeric**  - corresponds to an alpha/numeric entry in the Sales|Descriptor form in the 3700 POS Configurator. The 3700 database entry must be in the form @@<event_id>.
- The maximum number of SIM events available is the same as the number of descriptor lines available in the header and trailer fields. If there are six header lines available, then six SIM events can be used.
- The two variables that support this event are @Header and @Trailer. They are used to print descriptors.
- Control characters and SIM event(s) are programmed in the Sales|Descriptor form. The combination of the control characters (@@) and the SIM event (event_id) will call a SIM script.
- The event argument should consist of only letters, numbers, and an underscore (no spaces or punctuation). Also, the first character must be a letter.
- The @Header and @Trailer arrays are unique to each event. This means that each event can begin writing to the array starting at index 1, rather than at the next available index.
- All transaction system variables are valid in these events. User input is allowed, as are file operations and display manipulation.
- The events are called when POS Operations is formatting the print data, and not printing it. Therefore, StartPrint and other SIM commands can be used to generate printouts while the formatting process takes place.
- If the event is not found in the SIM script, then no error is given. The @@ line is ignored.

**Event Print_Header/Trailer Example**

The following SIM script will be called by the restaurant check header and, according to the time of day (from 4:00 p.m.- 6:00 p.m.), will print the additional header information on the check:

```isl
event print_header: Hap_Hr
  if @hour >= 16 AND @hour <18
    format @header[1]= " HAPPY HOUR"
    format @header[2]=" ALL DRINKS $1.00"
  endif
endevent
```

The header definition in the Sales|Descriptors form might look like this:

```isl
line [0] = "Mike Rose Restaurant & Grill"
line [1] = "ANYWHERE, MD 20705"
line [2] = ""@@Hap_Hr"
line [3] = " "
line [4] = " "
line [5] = " "
line [6] = " "
```

When the guest check prints, it will look like this:

---

## Event RxMsg

<!-- src: Command_Event RxMsg.htm -->

Event RxMsg

### Syntax
```text
Event RxMsg : event_ID
```

### Argument/Description
**event_ID** - the first field in the response message that identifies the event that is expecting that response or a *
- The first field in a response message is always the event_ID and should not be used in any successive RxMsg variable. The event_ID must begin with a letter A - Z, a - z, or the underline character (_), and can be up to 255 characters.
- When a message has been received from the PMS, the ISL will search the script for an RxMsg Event whose Event type matches the first field in the application_data segment of the message. If ISL encounters a message of the form: Event RxMsg : * it will automatically run that Event without regard to the PMS message's first field value. This feature is useful for debugging ISL scripts when the message from the PMS may not be correct.

**Caution**

If the *event command is placed before a specific event, OPS will not read any text entered after the *. Therefore, any code written after the * will be ignored and your program will not work as expected. When using the *event command, make sure to place it at the end of the ISL file.
- The Event RxMsg command is executed when SIM has been instructed to wait for a response and a response is received from the interfaced system. This event requires that both the TxMsg and WaitForRxMsg commands be used in another event, in the script file, for the RxMsg command to work.
- If the UseISLTimeOuts command is used and the PMS does not respond to an ISL message within the timeout period, the ISL will search the script for an RxMsg event with an event_ID of _Timeout (Event RxMsg : _Timeout). If _Timeout is found, ISL will bypass the standard 3700 error messaging and process a user-defined ISL instruction in its place.
- The interface application data message fields are always separated by an ASCII field separator character (1CH).

**Event RxMsg Example**

This is an example of a standard response message event:

```isl
event inq : 1
  var room_num : a4
  input room_num, "Enter Room Number"
  txmsg "charge_inq",@CKEMP,@CKNUM,@TNDTTL,room_num
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

**Event RxMsg Example 2**

This is an example of an event that is run when the response message is not received within the ISL timeout period:

```isl
useisltimeouts
event tmed : 10
  var room : N5
  input room, "Enter room number"
  txmsg "CHARGE", room, @tndttl
  waitforrxmsg
endevent

event rxmsg : charge_response
  waitforclear "Posting successful"
endevent

event rxmsg : _timeout
  window 4, 30
  display 2, @center, "PMS is down."
  waitforconfirm
endevent
```

---

## Event SignIn

<!-- src: Command_Event SignIn.htm -->

Event SignIn

### Syntax
```text
Event SignIn
```

**Event SignIn Example**
```isl
Event SignIn
  var text : a20 = "Signed In"
  var title : a20 = "SignIn Status"
  InfoMessage title, text
EndEvent
```

---

## Event SignOut

<!-- src: Command_Event SignOut.htm -->

Event SignOut

### Syntax
```text
Event SignOut
```

**Event SignOut Example**
```isl
Event SignOut
  var text : a20 = "Signed Out"
  var title : a20 = "SignOut Status"
  I nfoMessage title, text
EndEvent
```

---

## Event Srvc_Total

<!-- src: Command_Event Srvc_Total.htm -->

Event Srvc_Total

### Syntax
```text
Event Srvc_Total: event_ID
```

### Argument/Description
**event_ID** - corresponds to a specific Service Total object number programmed in the 3700 database, or * to execute the Event whenever it is encountered
- This event executes when a check is service totalled.
- If the Event Srvc_Total is not present in the script, no error will occur.
- When the Event Srvc_Total is executed, ISL will execute the event for each script linked to a PMS Computer.

**Event Srvc_Total Example**
This is an example of the Event Srvc_Total.

```isl
event srvc_total:*
  var i : n5
  for i = 1 to @numdtlt
    if @dtl_type[i] = "M" AND @dtl_objnum[1] > 1000
      call perform_mi_process( i )
    endif
  endfor
endevent
```

---

## Event Svc

<!-- src: Command_Event Svc.htm -->

Event Svc

This event is called after a service charge is added to the guest check. The event is executed for each configured SIM interface.

### Syntax
```text
Event svc
```

**Event Svc Example**
```isl
event svc
  errorMessage "Service charge added to the check."
endevent
```

---

## Event Svc_Error_Correct_Items

<!-- src: Command_Event Svc_Error_Correct_Items.htm -->

Event Svc_Error_Correct_Items

This event is called after a service charge is voided from the guest check an error correction (e.g., last item void). The event is executed for each configured SIM interface.

### Syntax
```text
Event svc_error_correct_items
```

**Event Svc_Error_Correct_Items Example**
```isl
event svc_error_correct_items
  errorMessage "Service charge was error corrected."
endevent
```

---

## Event Svc_Void

<!-- src: Command_Event Svc_Void.htm -->

Event Svc_Void

This event is called after a service charge is voided from the guest check via either direct void or touch void. The event is executed for each configured SIM interface.

### Syntax
```text
Event svc_void
```

**Event Svc_Void Example**
```isl
event svc_void
  errorMessage "Service charge was voided from the check."
endevent
```

---

## Event Tmed

<!-- src: Command_Event Tmed.htm -->

Event Tmed

### Syntax
```text
Event Tmed : number
```

### Argument/Description
number - corresponds to a specific Tender object number programmed in the 3700 database, or * to execute the Event whenever it is encountered

**Caution**
If the *event command is placed before a specific event, OPS will not read any text entered after the *. Therefore, any code written after the * will be ignored and your program will not work as expected. When using the *event command, make sure to place it at the end of the ISL file.
- The Event Tmed command is executed when an ISL Tender key is used at the UWS. The Tender number must be an object number in the Sales|Tender/Media form. The PMS must be enabled, and the appropriate PMS options must be enabled in the Sales|Tender/Media form.
- The UWS must be within a transaction for this Event to work.

**Event Tmed Example**
This is an example of a standard Tender/Media event:

```isl
event tmed : 10
  var rowcnt : n3
  var deliv_desc[6] : a15
  deliv_desc[1] = "Name:"
  window 6, 43
  .
  .
  .
endevent
```

---

## Event Tndr

<!-- src: Command_Event Tndr.htm -->

Event Tndr

This event is called after a tender payment is added to the guest check. The event is executed for each configured SIM interface.

### Syntax
```text
Event tndr
```

**Event Tndr Example**
```isl
event tndr
  errorMessage "Tender added to the check."
endevent
```

---

## Event Tndr_Error_Correct_Items

<!-- src: Command_Event Tndr_Error_Correct_Items.htm -->

Event Tndr_Error_Correct_Items

This event is called after a tender payment is voided from the guest check an error correction (e.g., last item void). The event is executed for each configured SIM interface.

### Syntax
```text
Event tndr_error_correct_items
```

**Event Tndr_Error_Correct_Items Example**
```isl
event tndr_error_correct_items
  errorMessage "Tender was error corrected."
endevent
```

---

## Event Tndr_Void

<!-- src: Command_Event Tndr_Void.htm -->

Event Tndr_Void

This event is called after a tender payment is voided from the guest check via either direct void or touch void. The event is executed for each configured SIM interface.

### Syntax
```text
Event tndr_void
```

**Event Tndr_Void Example**
```isl
event tndr_void
  errorMessage "Tender (payment) was voided from the check."
endevent
```

---

## Event Trans_Cncl

<!-- src: Command_Event Trans_Cncl.htm -->

Event Trans_Cncl

### Syntax
```text
Event Trans_Cncl
- This event executes when the transaction cancel key is pressed.
- If Event Trans_Cncl is not present in the script, no error will occur.
- When the Event Trans_Cncl is executed, ISL will execute the event for each script linked to a PMS Computer.
- There is no event_ID field for the Event Trans_Cncl.
```

**Event Trans_Cncl Example**
This is an example of the Event Trans_Cncl.

```isl
event trans_cncl
  if @tremp >= 1000
    call special_trans_cancel( @tremp )
  endif
endevent
```
