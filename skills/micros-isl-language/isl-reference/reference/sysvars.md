# ISL reference: sysvars

Source: RES 3700 SIM Online Help (CHM). Each entry starts with `## ` and the page name; grep `^## ` for an index.


---

## @ Bootserialnum

<!-- src: System_Variable_Bootserialnum.htm -->

@ Bootserialnum
Not used.

---

## @ Bootserialstr

<!-- src: System_Variable_Bootserialstr.htm -->

@ Bootserialstr
Not used.

---

## Alphascreen

<!-- src: System_Variable_Alphascreen.htm -->

Alphascreen

### Function
This system variable contains the number of the default alpha touchscreen defined for a Revenue Center.

**Type/Size**
N5

### Syntax
@Alphascreen

**Alphascreen Usage**
This system variable is Read-Only.

---

## Autosvc

<!-- src: System_Variable_Autosvc.htm -->

Autosvc

### Function
This system variable contains the auto service charge posted to the current guest check.

**Type/Size**
$10

### Syntax
@Autosvc

**Autosvc Usage**
This system variable is Read-Only.

---

## BackUpServerName

<!-- src: System_Variable_BackUpServerName.htm -->

BackUpServerName

### Function
This value is the LAN Node Address of the BSM server as entered in POS Configurator.

**Type/Size**
A15

### Syntax
@ BackUpServerName

**BackUpServerName Usage**
This system variable is Read-Only.

---

## Beverage_Reqd

<!-- src: System_Variable_Beverage_Reqd.htm -->

Beverage_Reqd

### Function
This variable determines whether or not POS Operations will prompt the user for beverages in accordance with the Beverage Control Feature. During "normal transaction processing", POS Operations checks the transaction state and tender media type definitions to determine if prompting is appropriate. Since it is not possible for POS Operations to be in this same state when calling the Beverage_reqd variable, the following logic is used internally to determine the value of the @beverage_reqd variable. This should help the SIM developer understand when POS Operations sets the variable to true.

Set @beverage_reqd = FALSE
If Beverage Control is on in the Revenue Center then
Get the Number of Beverages On the Check
If Beverages are Being Controlled by Cover Count then
If the Cover Count is greater than zero AND there
are no beverages, OR the cover count is greater than the
number of beverages then
Set @beverage_reqd = TRUE
EndIf
Else if there are no beverages on the check then
Set @beverage_reqd = TRUE
EndIf
EndIf

Note:
If you wish to execute your own beverage control without POS Operations prompting, leave the RVC Display Design | Beverage Name field blank. This will disable POS Operations from prompting the user but will not affect the value of this variable.

**Type/Size**
N1

### Syntax
@beverage_reqd

**Beverage_reqd example**
event inq : 1
Errormessage "Beverage Control state is ", @beverage_reqd
endevent

---

## Cashier

<!-- src: System_Variable_Cashier.htm -->

Cashier

### Function
This system variable returns the object number of active cashiers.

**Type/Size**
N9

### Syntax
@cashier

**Cashier Usage**
- This system variable is Read-Only.

---

## Cashier_Name

<!-- src: System_Variable_Cashier_Name.htm -->

Cashier_Name

### Function
This system variable returns the names of active cashiers.

**Type/Size**
A12

### Syntax
@cashier_name

**Cashier_Name Usage**
- This system variable is Read-Only.

---

## CCAuth_Count

<!-- src: System_Variable_CCAuth_Count.htm -->

CCAuth_Count

### Function
This system variable is used to return the number of untendered credit authorizations that are in the current seat filter.

**Type/Size**
N9

### Syntax
InfoMessage "CCAuth_Count",@CCAuth_Count

**CCAuth_Count Example**
//Cancel event if Credit Auths Exist
Event Inq : 1
if @CCAuth_Count > 0
errormessage "Not allow after credit card auth"
exitcancel
endif
//do something useful...
EndEvent

//"Credit Auths Exist, Abort Payment?"
Sub PrepareBybassCreditAuths
if @CCAuth_Count > 0
LoadKybdMacro @KEY_CLEAR
endif
EndEvent

---

## Ccdate

<!-- src: System_Variable_Ccdate.htm -->

Ccdate

### Function
This system variable contains the expiration date of a credit card that has been read from track data by a magnetic card reader, or has been manually entered.

**Type/Size**
A4

### Syntax
@Ccdate

**Ccdate Usage**
- This system variable is Read-Only.
- This system variable must be accessed within a tender/media event procedure that references a credit card tender type.

See also:

Ccnumber

---

## Ccnumber

<!-- src: System_Variable_Ccnumber.htm -->

Ccnumber

### Function
This system variable contains the account number of a credit card that has been read from track data by a magnetic card reader, or that has been manually entered.

**Type/Size**
A30

### Syntax
@Ccnumber

**Ccnumber Usage**
- This system variable is Read-Only.
- This system variable must be accessed within a tender/media event procedure that references a credit card tender type.

See also:

Ccdate

---

## Center

<!-- src: System_Variable_Center.htm -->

Center

### Function
This system variable contains the column number that is required to center text in an ISL-defined window.

**Type/Size**
N2

### Syntax
@Center

**Center Usage**
- This system variable is Read-Only.
- @Center evaluates to -1.
- This system variable can be used as the column argument when specifying the Display command.

**Center Example**
The following event procedure centers the text within an ISL-defined window:
event inq : 1
window 4, 40
display 1, @center, "In this window, all lines have "
display 2, @center, "been centered to give it "
display 3, @center, "that professional "
display 4, @center, "look."
waitforclear
endevent

See also:

Display

---

## Chgtip

<!-- src: System_Variable_Chgtip.htm -->

Chgtip

### Function
This system variable contains the charged tip for the associated tender in a Tmed event.

**Type/Size**
$12

### Syntax
@Chgtip

**Chgtip Usage**
- This system variable is Read-Only.
- Valid only in a Tmed event.
- In the 3700 System, the @Chgtip amount is included in the @Svc system variable.

---

## Chk

<!-- src: System_Variable_Chk.htm -->

Chk

### Function
This system variable contains the object number of the Guest Check Printer assigned to the UWS.

**Type/Size**
N7

### Syntax
@Chk

**Chk Usage**
- This system variable is Read-Only.
- This system variable can be used as an argument to the StartPrint[WithStatus] commands.

**Chk Example**
The event procedure below starts a print job at the Guest Check Printer.
event inq : 1
startprintwithstatus @chk
printline "this is a line"
endprint
if @printstatus = "Y"
waitforclear "Print successful"
else
waitforclear "Print failed"
endif
endevent

See also:

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Chk_Autofire_Time

<!-- src: System_Variable_Chk_Autofire_Time.htm -->

Chk_Autofire_Time

### Function
This system variable is used to return the next autofire activation time (if any) for the check. This can be the activation time for delayed or future orders or the next fire times for checks with timed fire items.

**Type/Size**
A17

### Syntax
@Chk_Autofire_Time

**Chk_Autofire_Time Usage**
- This system variable is Read-Only.

**Chk_Autofire_Time Example**
Event inq : 16
Window 8, 60
Var row: n2 = 1
Display row, 2, "AutofireTime = ",@chk_autofire_time
Waitforclear
endEvent

---

## Chk_Delayed_Order

<!-- src: System_Variable_Chk_Delayed_Order.htm -->

Chk_Delayed_Order

### Function
This system variable indicates whether the check is a delayed order. A delayed order is a check where sales post at the end of each service round, but items on the check do not print until the check’s delayed ordeer time.

**Type/Size**
N1

### Syntax
@Chk_Delayed_Order

**Chk_Delayed_Order Usage**
- This system variable is Read-Only.

**Chk_Delayed_Order Example**
Event inq : 16
Window 8, 60
Var row: n2 = 1
Row = row + 1
Display row 2, "Delayed order = 1", @chk_delayed_order
Waitforclear
endEvent

---

## Chk_Future_Order

<!-- src: System_Variable_Chk_Future_Order.htm -->

Chk_Future_Order

### Function
This system variable indicates whether the check is a future order. A future order is a check where do not post until the check’s future ordeer time.

**Type/Size**
N1

### Syntax
@Chk_Future_Order

**Chk_Future_Order Usage**
- This system variable is Read-Only.

**Chk_Future_Order Example**
Event inq : 16
Window 8, 60
Var row: n2 = 1
Row = row + 1
Display row 2, "Future order = 1", @chk_future_order
Waitforclear
endEvent

---

## Chk_Open_Time

<!-- src: System_Variable_Chk_Open_Time.htm -->

Chk_Open_Time

### Function
This system variable returns a string containing the date and time that the current guest check was opened.

**Type/Size**
A17

### Syntax
@Chk_Open_Time

**Chk_Open_Time Usage**
This system variable is Read-Only.

---

## Ckemp

<!-- src: System_Variable_Ckemp.htm -->

Ckemp

### Function
This system variable contains the number of the Check Employee..

**Type/Size**
N9

### Syntax
@Ckemp

**Ckemp Usage**
- This system variable is Read-Only.
- The employee who begins the guest check is the Check Employee. The employee who picks it up (or for whom it was begun) is the Transaction Employee. One employee may be both the Check Employee and the Transaction Employee.

**Ckemp Example**
The following example is a standard message exchange between a 3700 System and a PMS:
event inq : 1
var room_num : a4
input room_num, "Enter Room Number"
txmsg"charge_inq",@Ckemp,@Cknum,@Tndttl,room_num //The first field (charge_inq) is an example of an identifying string

//that the POS might use to process messsage from the POS.
waitforrxmsg
endevent

event rxmsg : charge_declined //This is one of the PMS response possibilities
var room_num : a4
rxmsg room_num
exitwitherror "Charge for room ", room_num," declined"
endevent

See also:

Tremp

---

## Ckemp_chkname

<!-- src: System_Variable_Ckemp_chkname.htm -->

Ckemp_chkname
### Function
This system variable contains the check employee’s check name.

**Type/Size**
A8

### Syntax
@CKEMP_CHKNAME

**Ckemp_chkname Usage**
- This system variable is Read-Only

---

## Ckemp_fname

<!-- src: System_Variable_Ckemp_fname.htm -->

Ckemp_fname
### Function
This system variable contains the check employee’s first name.

**Type/Size**
A8

### Syntax
@CKEMP_FNAME

**Ckemp_fname Usage**
- This system variable is Read-Only

---

## Ckemp_lname

<!-- src: System_Variable_Ckemp_lname.htm -->

Ckemp_lname
### Function
This system variable contains the check employee’s last name.

**Type/Size**
A16

### Syntax
@CKEMP_LNAME

**Ckemp_lname Usage**
- This system variable is Read-Only

---

## Ckemplopt

<!-- src: System_Variable_Ckemplopt.htm -->

Ckemplopt
### Function
This system variable is an array containing the setting of SIM employee privilege options 1-4, which are defined for the employee who started the check.

**Type/Size**
N1

### Syntax
@Ckemplopt[expression]

**Ckemplopt Usage**
- This system variable is Read-Only

Note
When the SIM script is executed, the variable should return a 1 (true) if the employee who started the check has the SIM privileges specified in the expression.
Using the Example script shown above, if a bartender with no SIM privileges picks up a check that was started by a server who had a SIM privilege of 2, then an info box with a value of "1" should display.

**Ckemplopt Example**
event MI
InfoMessage @Ckemplopt[2]
Endevent

---

## Ckid

<!-- src: System_Variable_Ckid.htm -->

Ckid
### Function
This system variable contains the current guest check ID. It can be used to access or assign a value to the current check ID.

**Type/Size**
A16

### Syntax
@Ckid

**Ckid Usage**
- If no guest check ID is assigned, null is returned.

---

## Cknum

<!-- src: System_Variable_Cknum.htm -->

Cknum
### Function
This system variable contains the number assigned to the current guest check.

**Type/Size**
N4

### Syntax
@Cknum

**Cknum Usage**
- This system variable is Read-Only.

**Cknum Example**
See @Ckemp example.

---

## CkSeqNum

<!-- src: System_Variable_CkSeqNum.htm -->

CkSeqNum
### Function
This system variable contains the sequence number assigned to the current guest check.

**Type/Size**
N4

### Syntax
@CkSeqNum

**CkSeqNum Usage**
- This variable is Read-Only.

---

## COM_Active

<!-- src: System_Variable_COM_Active.htm -->

COM_Active

### Function
Determines if Conversational Ordering Mode is active in the current Revenue Center.

**Syntax:**
@com_active

**COM_Active Example:**
Event Inq : 4
Errormessage "Conversational Ordering Mode status is ", @com_active
EndEvent

---

## Commands by Category

<!-- src: System_Variable_Reference_by_Category.htm -->

Commands by Category       <body> <p>This page uses frames, but your browser doesn't support them.</p> </body>

---

## CustomerInfo

<!-- src: System_Variable_CustomerInfo.htm -->

CustomerInfo

### Function
This system variable is used to set or retrieve the specified customer information.

**Type/Size**
N2

### Syntax
@CustomerInfo

**CustomerInfo Usage**
- This variable can be used for both read and write functions.
- The array limits for the expression are 0 to 32.

**CustomerInfo Example**

Event Inq: 1 // Display Customer Info
var i : N2
InfoMessage "CustomerSeq", @CustomerSeq[@Seat]
@CustomerInfo = @Seat
For i = 1 to 16 step 1
If @CustomerInfoLine[i] <> ""
InfoMessage "Customer Info", @CustomerInfoLine[i]
EndIf
EndFor
EndEvent

---

## CustomerInfoLine

<!-- src: System_Variable_CustomerInfoLine.htm -->

CustomerInfoLine

### Function
This system variable is used to retrieve the information from the specified GSS Guest Check/Delivery Info line number .

**Type/Size**
String, 80

### Syntax
@CustomerInfoLine[expression]

**CustomerInfoLine Usage**
- The array limits for the expression are 1 to 16.
- This variable relies on the @CustomerInfo system variable to specify the seats on which customer information is returned.
- This system variable is read-only.

**CustomerInfoLine Example**
Event Inq: 1 // Display Customer Info
var i : N2
InfoMessage "CustomerSeq", @CustomerSeq[@Seat]
@CustomerInfo = @Seat
For i = 1 to 16 step 1
If @CustomerInfoLine[i] <> ""
InfoMessage "Customer Info", @CustomerInfoLine[i]
EndIf
EndFor
EndEvent

---

## CustomerSeq

<!-- src: System_Variable_CustomerSeq.htm -->

CustomerSeq

### Function
This system variable is used set or get the customer sequence value for the supplied seat number index.

**Type/Size**
N9

### Syntax
@CustomerSeq[expression]

**CustomerSeq Usage**
- The array limits for the expression are 1 to 32.
- This system variable can be used for both read and write functions.

**CustomerSeq Example**

Event Inq : 1 // Add Customer
var cust : N9
input cust, "Customer Number to Add"
@CustomerSeq[@Seat] = cust
EndEvent

Event Inq : 2 // Remove Customer
@CustomerSeq[@Seat] = 0
EndEvent

---

## Data Entry

<!-- src: System_Variable_Data_Entry_Category.htm -->

Fieldstatus
Inputstatus
Magstatus
Userentry
Validate_Mag_Track

---

## Date and Time

<!-- src: System_Variable_Date_and_Time_Category.htm -->

Day
Hour
Minute
Month
Second
Weekday
Year
Yearday

---

## Day

<!-- src: System_Variable_Day.htm -->

Day

### Function
This system variable contains the current date.

**Type/Size**
N2

### Syntax
@Day

**Day Usage**
This system variable is Read-Only.

**Day Example**
The following script will construct a string_variable containing the current date in the form dd-mm-yy:
event inq : 1
var date : a9
call get_date_string
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
format date as @Day, "-", month_arr[@Month], "-", @Year // i.e., 10-NOV-93
endsub

See also:

Month

Year

---

## Dbmemlen

<!-- src: System_Variable_Dbmemlen.htm -->

Dbmemlen
Not used.

---

## Dbmemsize

<!-- src: System_Variable_Dbmemsize.htm -->

Dbmemsize
Not used.

---

## DepDscI

<!-- src: System_Variable_DepDscI.htm -->

DepDscI

### Function
This variable provides access to the current amount in a depleted discount itemizer. This value only exists when the Touch Item discount feature is enabled. Totals are NOT affected by the reset itemizer; that is, the reset option is not configurable when the Touch Item Discount feature is enabled.

**Type/Size**
$12

### Syntax
@DepDscI[Expression]

**DepDscI Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.
- This variable will return the depleted totals for the discount itemizer specified by the array index. For example, if the array index references @DepDscI[1], the depleted totals posted to Discount Itemizer #1 will be returned.

---

## Discount/Service Charge

<!-- src: System_Variable_Discount_Service_Charge_Category.htm -->

Autosvc
Chgtip
DepDscI
Dsc
DscI
DTL_is_auto_discount_
DTL_is_coupon
DTL_DSC_STTL
DscIttl
Numdsc
Numsvc
Svc
SvcI
SvcIttl
Test_Dsvc_Ttl

---

## Dsc

<!-- src: System_Variable_Dsc.htm -->

Dsc

### Function
This system variable contains the total amount of discounts applied to the current guest check. This total is the sum of all percentage and amount discounts on the guest check.

**Type/Size**
$12

### Syntax
@Dsc

---

## DscI

<!-- src: System_Variable_DscI.htm -->

DscI

### Function
This variable provides access to the current amount in the discount itemizer. Totals are affected by the reset itemizer.

**Type/Size**
$12

### Syntax
@DscI[Expression]

**DscI Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.
- This variable will return the totals posted to the discount itemizer specified by the array index. For example, if the array index references @DscI[1], any totals posted to Discount Itemizer #1 will be returned.

---

## DscIttl

<!-- src: System_Variable_DscIttl.htm -->

DscIttl

### Function
This variable provides access to the total amounts of each discount in the discount itemizer. Totals are affected by the reset itemizer.

**Type/Size**
$12

### Syntax
@DscIttl[Expression]

**DscIttl Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.
- This variable will return the totals posted to the discount itemizer specified by the array index. For example, if the array index references @DscIttl[1], any discount totals posted to Discount Itemizer #1 will be returned.

---

## Dtl_Autofire_Time

<!-- src: System_Variable_Dtl_Autofire_Time.htm -->

Dtl_Autofire_Time

### Function
This system variable indicates the time, if any, that the referenced item will automatically print in the kitchen.

**Type/Size**
A17

### Syntax
@Dtl_Autofire_Time[dtl_index]

**Dtl_Autofire_Time Usage**
- This system variable is Read-Only.

**Dtl_Autofire_Time Example**
Event inq : 16
Window 8, 60
Var row: n2 = 17
Row = row + 1
Display row, 2, @dtl_name[dtl_index], "Autofire Time = ", @dtl_autofire_time[dtl_index]
Waitforclear
endEvent

---

## Dtl_Charge_Tip_Amount

<!-- src: System_Variable_Dtl_Charge_Tip_Amount.htm -->

Dtl_Charge_Tip_Amount

### Function
This variable returns the amount of the charge tip, if the indexed detail item is a tender media type and has a charge tip associated with it. This variable returns a zero, if the item is not a tender media type or if the item is a tender type, but with no charge tip associated with it.

**Type/Size**
N1

### Syntax
@Dtl_Charge_Tip_Amount

**Dtl_Charge_Tip_Amount Usage**
This system variable is Read-Only.

**Dtl_Charge_Tip_Amount Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_has_charge_tip[counter] )
Errormessage "Detail ", counter," has a charge tip in the amount of ", @dtl_charge_tip_amount[counter]
endif
endfor
endevent

---

## Dtl_Charge_Tip_Name

<!-- src: System_Variable_Dtl_Charge_Tip_Name.htm -->

Dtl_Charge_Tip_Name

### Function
This variable returns the name of the charge tip, if the indexed detail item is a tender media type and has a charge tip associated with it. This variable returns an empty string, if the item is not a tender media type or if the item is a tender type, but with no charge tip associated with it.

**Type/Size**
N1

### Syntax
@Dtl_Charge_Tip_Name

**Dtl_Charge_Tip_Name Usage**
This system variable is Read-Only.

**Dtl_Charge_Tip_Name Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_has_charge_tip[counter] )
Errormessage "Detail ", counter," charge tip name is ", @dtl_charge_tip_name[counter]
endif
endfor
endevent

---

## Dtl_Dining_Course

<!-- src: System_Variable_Dtl_Dining_Course.htm -->

Dtl_Dining_Course

### Function
This variable indicates the dining course associated with the referenced menu items. It can also be varied to change the pre-assigned course numbers for printing purposes only.

**Type/Size**
N2

### Syntax
@Dtl_dining_course[dtl_index]

**Dtl_Dining_Course Usage**
This variable is read-only.

**Dtl_Dining_Course Example**

Event inq : 16
Window 8, 60
Var dtl_index: n2 = 17
Row = row + 2
Display row, 2, @dtl_name[dtl_index], "Dining Course = ", @dtl_dining_course[dlt_index], "Prep Time = ", @dtl_prep_time[dtl_index]
Waitforclear
endEvent

This modification allows users to change the pre-assigned course numbers for printing purposes only. This variable does not affect previous round items.

Example
event inq : 1
Infomessage @dtl_dining_course[2]
@dtl_dining_course[2] = 4
Infomessage @dtl_dining_course[2]
Endevent

---

## DTL_DSC_ITTL

<!-- src: System_Variable_DTL_DSC_ITTL.htm -->

DTL_DSC_ITTL

### Function
This variable determines which discounts are associated with the item discounts (e.g., Last Item Discount, Touch Item Discount).

**Type/Size**
$12

### Syntax
@Dtl_DSC_ITTL

**DTL_DSC_ITTL Usage**
This system variable is Read-Only.

---

## DTL_DSC_STTL

<!-- src: System_Variable_DTL_DSC_STTL.htm -->

DTL_DSC_STTL

### Function
The second variable identifies the Subtotal discounts and their associated totals. If more than one discount is being applied, only the first of these discounts will appear in the detail with the total discounted amount. The remaining discounts will report as zero amounts.

**Type/Size**
$12

### Syntax
@Dtl_DSC_STTL

**DTL_DSC_STTL Usage**
This system variable is Read-Only.

---

## Dtl_Famgrp

<!-- src: System_Variable_Dtl_Famgrp.htm -->

Dtl_Famgrp

### Function
This variable returns the menu item’s family group sequence number. This variable returns zero for all non-menu item detail.

**Type/Size**
N1

### Syntax
@Dtl_Famgrp

**Dtl_Famgrp Usage**
This system variable is Read-Only.

**Dtl_Famgrp Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ("M" = @dtl_type[counter] )
Errormessage "Detail ", counter," Family group sequence number is ", @dtl_famgrp[counter]
endif
endfor
endevent

---

## Dtl_Has_Charge_Tip

<!-- src: System_Variable_Dtl_Has_Charge_Tip.htm -->

Dtl_Has_Charge_Tip

### Function
This variable returns a numeric 1, if the indexed detail item is a tender media type, and has a charge tip associated with it. This variable returns a zero, if the item is not a tender media type, or if the item is a tender type but with no charge tip associated with it.

**Type/Size**
N1

### Syntax
@Dtl_Has_Charge_Tip

**Dtl_Has_Charge_Tip Usage**
This system variable is Read-Only.

**Dtl_Has_Charge_Tip Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_has_charge_tip[counter] )
Errormessage "Detail ", counter," has a charge tip"
endif
endfor
endevent

---

## Dtl_has_printed

<!-- src: System_Variable_Dtl_has_printed.htm -->

Dtl_has_printed

### Function
This system variable returns an array for the guest check detail that has printed through use of the "Touch and Fire" key in the current round. Zero is returned for items that were printed in the previous round.

**Type/Size**
N1

### Syntax
@dtl_has_printed

**Dtl_has_printed Usage**
This system variable is read only.

---

## Dtl_Id

<!-- src: System_Variable_Dtl_Id.htm -->

Dtl_Id

### Function
This variable returns the detail identification value associated with the transaction detail entry. MICROS recommends that you are specific as possible when validating menu items and parent items.

**Type/Size**
N1

### Syntax
@Dtl_Id

**Dtl_Id Usage**
This system variable is Read-Only.

---

## dtl_is_auto_discount

<!-- src: System_Variable_dtl_is_auto_discount.htm -->

dtl_is_auto_discount

### Function
This variable returns the detail identification value to determine if this discount was an automatic discount.

**Type/Size**
N1

### Syntax
@Dtl_is_auto_discount

**dtl_is_auto_discount Usage**
This system variable is Read-Only.

---

## Dtl_Is_Combo

<!-- src: System_Variable_Dtl_Is_Combo.htm -->

Dtl_Is_Combo

### Function
This variable determines if the detail specified in the array index is part of a combo meal.

**Type/Size**
N1

### Syntax
@Dtl_Is_Combo

**Dtl_Is_Combo Usage**
This system variable is Read-Only.

**Dtl_Is_Combo Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_is_combo[counter] )
Errormessage "Detail ", counter," is part of a combo meal"
endif
endfor
endevent

---

## Dtl_Is_Combo_Main

<!-- src: System_Variable_Dtl_Is_Combo_Main.htm -->

Dtl_Is_Combo_Main

### Function
This variable determines if the detail specified in the array index is a main item of a combo meal.

**Type/Size**
N1

### Syntax
@Dtl_Is_Combo_Main

**Dtl_Is_Combo_Main Usage**
This system variable is Read-Only.

**Dtl_Is_Combo_Main Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_is_combo_main[counter] )
Errormessage "Detail ", counter," is a main item of a combo meal"
endif
endfor
endevent

---

## Dtl_Is_Combo_Parent

<!-- src: System_Variable_Dtl_Is_Combo_Parent.htm -->

Dtl_Is_Combo_Parent

### Function
This variable determines if the detail specified in the array index is a parent item of a combo meal.

**Type/Size**
N1

### Syntax
@Dtl_Is_Combo_Parent

**Dtl_Is_Combo_Parent Usage**
This system variable is Read-Only.

**Dtl_Is_Combo_Parent Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_is_combo_parent[counter] )
Errormessage "Detail ", counter," is a parent of a combo meal"
endif
endfor
endevent

---

## Dtl_Is_Combo_Side

<!-- src: System_Variable_Dtl_Is_Combo_Side.htm -->

Dtl_Is_Combo_Side

### Function
This variable determines if the detail specified in the array index is a side item of a combo meal.

**Type/Size**
N1

### Syntax
@Dtl_Is_Combo_Side

**Dtl_Is_Combo_Side Usage**
This system variable is Read-Only.

**Dtl_Is_Combo_Side Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_is_combo_side[counter] )
Errormessage "Detail ", counter," is a side item of a combo meal"
endif
endfor
endevent

---

## Dtl_is_cond

<!-- src: System_Variable_Dtl_is_cond.htm -->

Dtl_is_cond

### Function
This system variable is an array that determines if a guest check menu item is a condiment.

**Type/Size**
N1

### Syntax
@Dtl_is_cond[expression]

**Dtl_is_cond Usage**
- This system variable is read only.
The array limits for the expression are 1 to @Numdtlt.

---

## dtl_is_coupon

<!-- src: System_Variable_dtl_is_coupon.htm -->

dtl_is_coupon

### Function
This variable returns the detail identification value to determine if this discount is a coupon for an automatic discount.

**Type/Size**
N1

### Syntax
@Dtl_is_auto_discount

**dtl_is_coupon Usage**
This system variable is Read-Only.

---

## Dtl_is_default_cond

<!-- src: System_Variable_Dtl_is_default_cond.htm -->

Dtl_is_default_cond

### Function
Determines if the condiment as it is ordered with its parent is a default condiment.

**Syntax:**
@dtl_is_default_cond

**Dtl_is_default_cond Example:**
Event Inq : 4
var i : n3
for i = 1 to @numdtlt
if @dtl_is_default_cond[i]
Errormessage "Default Condiment Found ", @dtl_name[i]
endif
Endfor
EndEvent

---

## Dtl_is_om

<!-- src: System_Variable_Dtl_is_om.htm -->

Dtl_is_om

### Function
This variable determines if the detail specified in the array index is an Ordering Module menu item.

**Type/Size**
N1

### Syntax
@dtl_is_om

**Dtl_is_om Usage**
This system variable is read only.

---

## Dtl_is_om_base

<!-- src: System_Variable_Dtl_is_om_base.htm -->

Dtl_is_om_base

### Function
This variable determines if the detail specified in the array index is an Ordering Module base menu item.

**Type/Size**
N1

### Syntax
@dtl_is_om_base

**Dtl_is_om_base Usage**
This system variable is read only.

---

## Dtl_is_om_container

<!-- src: System_Variable_Dtl_is_om_container.htm -->

Dtl_is_om_container

### Function
This variable determines if the detail specified in the array index is an Ordering Module menu item container

**Type/Size**
N1

### Syntax
@dtl_is_om_container

**Dtl_is_om_container Usage**
This system variable is read only.

---

## Dtl_is_om_section

<!-- src: System_Variable_Dtl_is_om_section.htm -->

Dtl_is_om_section

### Function
This variable determines if the detail specified in the array index is an Ordering Module menu item section.

**Type/Size**
N1

### Syntax
@dtl_is_om_section

**Dtl_is_om_section Usage**
This system variable is read only.

---

## Dtl_is_om_specialty

<!-- src: System_Variable_Dtl_is_om_specialty.htm -->

Dtl_is_om_specialty

### Function
This variable determines if the detail specified in the array index is an Ordering Module specialty menu item.

**Type/Size**
N1

### Syntax
@dtl_is_om_specialty

**Dtl_is_om_specialty Usage**
This system variable is read only.

---

## Dtl_is_om_topping

<!-- src: System_Variable_Dtl_is_om_topping.htm -->

Dtl_is_om_topping

### Function
This variable determines if the detail specified in the array index is an Ordering Module topping menu item.

**Type/Size**
N1

### Syntax
@dtl_is_om_topping

**Dtl_is_om_topping Usage**
This system variable is read only.

---

## Dtl_is_on_hold

<!-- src: System_Variable_Dtl_is_on_hold.htm -->

Dtl_is_on_hold

### Function
This system variable returns an array for the guest check detail that has been placed on hold with the Touch and Hold feature.

**Type/Size**
N1

### Syntax
@dtl_is_on_hold

**Dtl_is_on_hold Usage**
This system variable is read only.

---

## Dtl_is_void

<!-- src: System_Variable_Dtl_is_void.htm -->

Dtl_is_void

### Function
This system variable is an array that returns a 1 if the guest check item detail is a void and a 0 if it is not a void.
Note: Detail types of credit authorization and check info will always return a 0.

**Type/Size**
N1

### Syntax
@Dtl_is_void

**Dtl_is_void Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

---

## Dtl_Majgrp

<!-- src: System_Variable_Dtl_Majgrp.htm -->

Dtl_Majgrp

### Function
This variable returns the menu item’s major group sequence number. This variable returns zero for all non-menu item detail.

**Type/Size**
N1

### Syntax
@Dtl_Majgrp

**Dtl_Majgrp Usage**
This system variable is Read-Only.

**Dtl_Majgrp Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ("M" = @dtl_type[counter] )
Errormessage "Detail ", counter," Major group sequence number is ", @dtl_majgrp[counter]
endif
endfor
endevent

---

## Dtl_MajGrp_ObjNum and DTL_FamGrp_ObjNum

<!-- src: System_Variable_Dtl_MajGrp_ObjNum_and_DTL_FamGrp_ObjNum.htm -->

Dtl_MajGrp_ObjNum and DTL_FamGrp_ObjNum
### Function
These two variables will return a menu item's major group object number and family group object number respectfully. These variables will return zero for non -menu item detail. The variables work the same way as other check detail related SIM variables (i.e., an array specifier is required - @DTL_FAMGRP_OBJNUM[i] ).

**Type/Size**
N9

### Syntax
@DTL_FAMGRP_OBJNUM / @DTL_FamGrp_ObjNum

**Dtl_MajGrp_ObjNum and DTL_FamGrp_ObjNum Usage**
This system variable is Read-Only.

---

## Dtl_Mlvl

<!-- src: System_Variable_Dtl_Mlvl.htm -->

Dtl_Mlvl

### Function
This system variable is an array containing the Main Menu Level (1-4) of a detail item on the current service round.

**Type/Size**
N1

### Syntax
@Dtl_Mlvl[expression]

**Dtl_Mlv Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

**Dtl_Mlvl Example**
The script below will display existing guest check detail in the previous order window.
event inq : 7
var cnt : n3
var mi_mlvl [ @numdtlt ] : n1
var mi_slvl [ @numdtlt ] : n1
var mi_obj[ @numdtlt ] : n5
var mi_cnt : n3 = 0
touchscreen 3
if @cknum = 0
exitwitherror "Begin a check and try again"
endif
for cnt = 1 to @numdtlt
if @dtl_type[ cnt ] = "M"
mi_cnt = mi_cnt + 1
mi_obj[ mi_cnt ] = @dtl_objnum[ cnt ]
mi_mlvl[ mi_cnt ] = @dtl_mlvl[ cnt ]
mi_slvl[ mi_cnt ] = @dtl_slvl[ cnt ]
endif
endfor
endevent

{button ,Alink(Numdtlt, , , )} See Also

---

## Dtl_Name

<!-- src: System_Variable_Dtl_Name.htm -->

Dtl_Name

### Function
This system variable is an array containing the name of a detail item on the current guest check.

**Type/Size**
A24

### Syntax
@Dtl_Name[expression]

**Dtl_Name Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.
- The name 1 field is returned for menu items.

See also:

Numdtlt

---

## Dtl_name_two

<!-- src: System_Variable_Dtl_name_two.htm -->

Dtl_name_two

### Function
This system variable is used to return the Name 2 value from the menu item record.

**Type/Size**
A12

### Syntax
@Dtl_name_two

**Dtl_name_two Usage**
- This system variable is Read-Only.
- Only Name 2 menu item values will be returned. If detail item does not have a Name 2, it will return an empty string.

**Dtl_name_two example**
For cnt = 1 @numdtlt
If @dtl_type[cnt] = "M"
Format str as "Cnt=", "Type", @dtl_type[cnt], "Name=", @Dtl_name_two[cnt]
InfoMessage str
Endif
Endfor

---

## Dtl_Object

<!-- src: System_Variable_Dtl_Object.htm -->

Dtl_Object

### Function
This system variable is an array containing the object number of a detail item on the current guest check.

**Type/Size**
N7

### Syntax
@Dtl_Object[expression]

**Dtl_Object Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

**Dtl_Object Example**
See the example for @Dtl_Mlvl

See also:

Numdtlt

---

## Dtl_Objnum

<!-- src: System_Variable_Dtl_Objnum.htm -->

Dtl_Objnum

See Dtl_sequence

---

## Dtl_Ord_Dev_Output

<!-- src: System_Variable_Dtl_Ord_Dev_Output.htm -->

Dtl_Ord_Dev_Output

### Function
This variable returns a hexadecimal value representing the order device output for a menu item detail entry.
### Example
If a menu item prints to order device 1 and 2, then the return value will be "C000." If a menu item is programmed to print to all order devices then the return value will be "FFFC."
When the order device output is requested for a detail entry which is not a menu item, the return value is "0000." This variable works the same way as other check detail related SIM variables in that an array specifier is required to get the value for a specific detail entry (e.g., @Dtl_Ord_Dev_Output[i] ).

**Type/Size**
A4

### Syntax
@Dtl_Ord_Dev_Output

**Dtl_Ord_Dev_Output Usage**
This system variable is Read-Only.

---

## Dtl_Plvl

<!-- src: System_Variable_Dtl_Plvl.htm -->

Dtl_Plvl

### Function
This system variable is an array containing the price level 1 - 4 of a menu item on the current guest check.

**Type/Size**
N1

### Syntax
@Dtl_Plvl[expression]

**Dtl_Plvl Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

See also:

Numdtlt

---

## Dtl_prefix

<!-- src: System_Variable_Dtl_prefix.htm -->

Dtl_prefix

### Function
This variable will identify the prefix type of a prefix condiment by returning one of the following values:
0 = NOT A PREFIX
1 = DEFAULT_PREFIX
2 = NO_PREFIX
3 = PLAIN_PREFIX
4 = EVERYTHING_PREFIX
5 = ADD_PREFIX
6 = SUBSTITUTE_PREFIX

**Syntax:**
@dtl_prefix

**Dtl_prefix Example:**
Event Inq : 4
var prefix :n1
var prefix_type[6]: A32
prefix_type[1] = "DEFAULT_PREFIX"
prefix_type[2] = "NO_PREFIX"
prefix_type[3] = "PLAIN_PREFIX"
prefix_type[4] = "EVERYTHING_PREFIX"
prefix_type[5] = "ADD_PREFIX"
prefix_type[6] = "SUBSTITUTE_PREFIX"
var i : n3
for i = 1 to @numdtlt
prefix = @dtl_prefix[i]
if prefix
Errormessage "Prefix Found, type is ", prefix_type[prefix]
endif
Endfor
EndEvent

---

## Dtl_Prep_Time

<!-- src: System_Variable_Dtl_Prep_Time.htm -->

Dtl_Prep_Time

### Function
This variable indicates the kitchen preparation time associated with the referenced menu item.

**Type/Size**
N8

### Syntax
@Dtl_Prep_Time[dtl_index]

**Dtl_Prep_Time Usage**
- This system variable is Read-Only.

**Dtl_Prep_Time Example**
Event inq: 16
Window 8, 60
Var dtl_index: n2 = 17
Row = row + 2
Display row, 2, @dtl_name[dtl_index], "Dining Course = ", @dtl_dining_course[dtl_index], "Prep Time = ", @dtl_prep_time[dtl_index]
Waitforclear
EndEvent

---

## Dtl_PrtGstChk

<!-- src: System_Variable_Dtl_PrtGstChk.htm -->

Dtl_PrtGstChk

### Function
This variable returns a numeric 1 if the detail item specified in the index is programmed to print on the guest check.

**Type/Size**
N1

### Syntax
@Dtl_PrtGstChk

**Dtl_PrtGstChk Usage**
This system variable is Read-Only.

**Dtl_PrtGstChk Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_prtgstchk[counter] )
Errormessage "Detail ", counter," will print on the guest check."
endif
endfor
endevent

---

## Dtl_PrtRcpt

<!-- src: System_Variable_Dtl_PrtRcpt.htm -->

Dtl_PrtRcpt

### Function
This variable returns a numeric 1 if the detail item specified in the index is programmed to print on the receipt.

**Type/Size**
N1

### Syntax
@Dtl_PrtRcpt

**Dtl_PrtRcpt Usage**
This system variable is Read-Only.

**Dtl_PrtRcpt Example**
event inq : 1
var counter : N3 = 1
for counter = 1 to @NUMDTLT Step 1
if ( @dtl_prtrcpt[counter] )
Errormessage "Detail ", counter," will print on the receipt."
endif
endfor
endevent

---

## Dtl_Qty

<!-- src: System_Variable_Dtl_Qty.htm -->

Dtl_Qty

### Function
This system variable is an array containing the quantity of a detail item on the current guest check.

**Type/Size**
N5

### Syntax
@Dtl_Qty[expression]

**Dtl_Qty Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

See also:

Numdtlt

---

## Dtl_Seat

<!-- src: System_Variable_Dtl_Seat.htm -->

Dtl_Seat

### Function
This system variable is an array containing the seat number of the detail item.

**Type/Size**
N2

### Syntax
@Dtl_Seat[expression]

**Dtl_Seat Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

See also:

Numdtlt

---

## Dtl_Selected

<!-- src: System_Variable_Dtl_Selected.htm -->

Dtl_Selected

### Function
This variable returns a "1" is the detail entry is currently selected in the detail area of the touchscreen and a "0" if it is not selected. This variable works the same way as other check detail related SIM variables in that an array specifier is required to get the value for a specific detail entry.
Note: After OPS performs the action of a SIM Inquire keypress the detail entry items selected will remain selected.

**Type/Size**
N1

### Syntax
@DTL_SELECTED[i]

**Dtl_Selected Usage**
This system variable is Read-Only.
An index must be specified. (eg. @dtl_selected [3])

---

## Dtl_Sequence

<!-- src: System_Variable_Dtl_Sequence.htm -->

Dtl_Sequence

### Function
This system variable is an array containing the sequence number of a detail item on the current guest check.

**Type/Size**
N7

### Syntax
@Dtl_Sequence[expression]

**Dtl_Sequence Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

**Dtl_Sequence Example**
See the example for @Dtl_Mlvl

See also:

Numdtlt

---

## Dtl_Slvl

<!-- src: System_Variable_Dtl_Slvl.htm -->

Dtl_Slvl

### Function
This system variable is an array containing the Sub Menu Level (1-4) of a detail item on the current service round.

**Type/Size**
N1

### Syntax
@Dtl_Slvl[expression]

**Dtl_Slvl Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

**Dtl_Slvl Example**
See the example for @Dtl_Mlvl

See also:

Numdtlt

---

## Dtl_Status

<!-- src: System_Variable_Dtl_Status.htm -->

Dtl_Status

### Function
This system variable is an array containing the status of a detail item on the current guest check.

**Type/Size**
A8

### Syntax
@Dtl_Status[expression]

**Dtl Status Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

Dtl_status is a hexadecimal field. Using the items below** you must convert the hex number to the appropriate status bit. Note that there are some items using the same number. When this is the case, the dtl type is different so that you would never have the same status bit available at the same time.

**Dtl_Status Example**
If dtl_status returned A0100000 then the A in the 1st digit would mean DTL_PREV_RND is set and DTL_NLU_USED is set.

**1st digit**  |

#define DTL_PREV_RND  |  1 |

#define DTL_MASK  |  2 |

#define DTL_NLU_USED |  3 |

#define DTL_RETURN |  4 |

#define DTL_CHANGE  |  4 |

**2nd digit**  |

#define DTL_VOID |  5 |

#define DTL_REF_FOLLOWS |  6 |

#define DTL_CA_INIT_AUTH |  7 |  /* CA Only */ |

#define DTL_MODIFIED_BY_PLAIN |  7 |  /* MI Only RES 4.5: Plain support */ |

#define DTL_CA_AUTH_AND_PAYED |  8 |  /* CA Only */ |

#define DTL_MODIFIED_BY_ALL |  8 |  /* MI Only RES 4.5: All support */ |

**3rd digit**  |

#define DTL_SVC  |  9 |   /* DSVC ONLY */ |

#define DTL_EXMPT_SVC_TTL  |  9 |  /* SVC TTL ONLY */ |

#define DTL_SCNDRY_AUTH  |  9 |  /* CA AUTH ONLY */ |

#define DTL_MODIFIED_BY_NO |  9 |  /* MI ONLY */ |

#define DTL_PRV_RND_VOID  |  10 |    |

#define DTL_PREV_ROUND_CHANGE |  11 |    |

#define DTL_ERROR_CORRECT |  12 |    |

**4th digit**  |

#define DTL_PL_GST_CHK  |  13 |

#define DTL_ITEM_SHARED |  14 |

#define DTL_VOID_EDIT |  15 |

#define DTL_FIXED_PRICE_COURSE |  16 |

**5th digit**  |

#define DTL_LI_VOID_NOT_ALLOWED |  17 |

#define DTL_GROUP_START |  18 |

#define DTL_ITEM_FROM_LDS |  19 |

#define DTL_DEBIT_FLAG |  20 |  /* TENDERS W/ CA AUTH ONLY */ |

#define DTL_REQUIRED_CONDIMENT |  20 |  /* MI ONLY CRS 5-4-98 */ |

#define DTL_CA_AVAIL_BALANCE |  20 |  /* CA AUTH ONLY */ |

#define DTL_CASCADE_REMOVE |  20 |  /* DSC ONLY */ |

**6th digit**  |

#define DTL_CUR_CNV_ACTIVE |  21 |

#define DTL_CA_TAX1_EXMPT |  21 |

#define DTL_BVG_AFT_PROMPT  |  21 |  /* MI ONLY */ |

#define DTL_TAX_SHIFT  |  22 |  /* MI & REF ONLY */ |

#define DTL_CA_TAX2_EXMPT |  22 |

#define DTL_ON_HOLD |  23 |   /* MI, DSVC, TMED ONLY |

#define DTL_CA_TAX3_EXMPT |  23 |

#define DTL_CA_TAX4_EXMPT |  24 |

#define DTL_OVRDE_TAX_W_QTY_GROUP |  24 |  /*MI Only */ |

**7th digit**  |

#define DTL_CA_TAX5_EXMPT |  25 |

#define DTL_THAI_INVOICE  |  25 |  /* TMED ONLY */ |

#define DTL_CA_TAX6_EXMPT |  26 |

#define DTL_THAI_ACCOUNT  |  26 |  /* TMED ONLY */ |

#define DTL_CA_TAX7_EXMPT |  27 |

#define DTL_CA_TAX8_EXMPT  |  28 |

**8th digit**  |

#define DTL_OVERTENDER_CHG_TIP |  29 |

#define DTL_SKU_ENTRY |  30 |  /* MI DTL ONLY */ |

#define DTL_CC_VCHR_CANCELLED |  30 |  /* VOUCHER DTL ONLY */ |

#define DTL_AUTOMATIC_DISCOUNT |  30 |  /* DSC ONLY */ |

#define DTL_PRICE_OVERRIDE |  31 |

#define DTL_IS_DIRECT_VOID  |  32 |  /* BPD 2-10-98 */  |

**9th digit**  |

#define DTL_PRICE_FROM_NLU_FILE  |  33 |  /* CRS 2-2-99 V2.60 Retail Barcode Support */  |

#define DTL_PRICE_FROM_BARCODE  |  34 |  /* CRS 2-2-99 V2.60 Retail Barcode Support */ |

#define DTL_BARCODE_ENTRY |  35 |  /* CRS 2-5-99 V2.60 Retail Barcode Support */ |

#define DTL_PRINTED_ON_L_BY_L_RMT |  36 |  /* CPR 7-26-2000 V3.0 Combo Meals Support */ |

**10th digit**  |

#define DTL_NO_RPT_COUNT |  37 |  /* 3.2-SP7: Item has been split, report count must always be 0 */ |

#define DTL_DISCOUNT_COUPON |  38 |  /* DSC ONLY */ |

#define DTL_PRINTED_ON_L_BY_L_RCPT |  39 |

#define DTL_UNUSED_40 |  40 |  /* RES 4.0: Encryption support */ |

See also:
Numdtlt

---

## Dtl_Taxtype

<!-- src: System_Variable_Dtl_Taxtype.htm -->

Dtl_Taxtype

### Function
This system variable contains the tax types that were active when the corresponding menu item, service charge, or discount detail item was ordered.

**Type/Size**
A2

### Syntax
@Dtl_Taxtype[expression]

**Dtl_Taxtype Usage**
- This system variable is Read-Write.
- This system variable is represented as a two-digit hex field, ranging from 00 to FF. Each bit corresponds to the tax type. For example, 80 corresponds to tax type 1.

---

## Dtl_Ttl

<!-- src: System_Variable_Dtl_Ttl.htm -->

Dtl_Ttl

### Function
This system variable is an array containing the total of a detail item on the current guest check.

**Type/Size**
$12

### Syntax
@Dtl_Ttl[expression]

**Dtl_Ttl Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.

**Dtl_Ttl Example**
The example below is part of a script that checks a current guest check for a certain number of menu items. If four menu items are found, the script will call a subroutine that prints a coupon (call print_coupon) and a subroutine that determines how many items are on the check (call check_grill_list( objnum)); these subroutine scripts are not shown.
event tmed : *
var dtl_cnt : n3
var num_grill_items : n3 = 6
var grill_item[ num_grill_items ] : n5
var grill_hit : n3
var objnum : n5
grill_item[ 1 ] = 1501
grill_item[ 2 ] = 1510
grill_item[ 3 ] = 1520
grill_item[ 4 ] = 1530
grill_item[ 5 ] = 1540
grill_item[ 6 ] = 1550
// look through the check, have we ordered 4 grill items
for dtl_cnt = 1 to @numdtlt
if @dtl_type[ dtl_cnt ] = "M" AND @dtl_ttl[ dtl_cnt ] > 0
objnum = @dtl_objnum[ dtl_cnt ]
call check_grill_list( objnum)
endif
if grill_hit >= 4
call print_coupon
endif
endevent

See also:

Numdtlt

---

## Dtl_Type

<!-- src: System_Variable_Dtl_Type.htm -->

Dtl_Type

### Function
This system variable is an array containing the detail type of an item on the current guest check.

**Type/Size**
A1

### Syntax
@Dtl_Type[expression]

**Dtl_Type Usage**
- This system variable is Read-Only.
- The array limits for the expression are 1 to @Numdtlt.
- The detail type will be one of the following:

Type Description
I Check Information Detail
M Menu Item
D Discount
S Service Charge
T Tender/Media
R Reference Number
C CA Detail

**Dtl_Type Example**
See the example for @Dtl_Mlvl

See also:

Numdtlt

---

## Dtl_Typedef

<!-- src: System_Variable_Dtl_Typedef.htm -->

Dtl_Typedef

### Function
This system variable returns information on how a check detail item is configured. Detail information is provided for discounts (D), menu items (M), service charges (S), and tenders (T).

**Type/Size**
Variable size depends on the detail type.

**Detail**  |  **Type/Size**  |

Discount |  A4  |

Menu Item |  A10  |

Service Charge |  A4  |

Tender  |  A12 |

### Syntax
@Dtl_Typedef[expression]

### Argument/Description
- This system variable is read-only.
- The type definition is returned as a hex string. To get this information, the bit( ) function must be used. The detail tables describe the meaning of each bit returned.
- For menu items, this variable returns the type definition field from the revenue center (RVC) level menu item class file associated with that menu item.
- For discounts, service charges, and tender media detail items, this variable returns the type definition field from the system level files.

**Dtl Typedef Example**

The variable allows the Turkish Fiscal Printer to distinguish between condiments; weighted items; open priced items; and regular, preset items. For fiscal purposes, these items are handled differently. The variable provides a mechanism for determining what kind of menu item is on the check.
In the sample below, the event scans each item in the check detail and opens a window which displays each menu item found. If the menu item defines a preset and weight, then a "1" is shown next to the appropriate label; if not, a "0" is displayed.

event inq: 1
var i: N9
window 1, 60, "Detail information"
for i = 1 to @numdtlt
if (@Dtl_Type[i] = "M")
display 1, 1, @Dtl_Name[i],
"preset: ", bit(@Dtl_Typedef[i], 1),
"weighed: ", bit(@Dtl_Typedef[i], 28)
waitForClear
endif
endfor
windowClose
endevent // inq: 1

---

## Dwoff

<!-- src: System_Variable_Dwoff.htm -->

Dwoff

### Function
This system variable returns printed text to single-wide characters (default) if the @Dwon system variable was used to switch text to double-wide characters.

**Type/Size**
A1

### Syntax
@Dwoff

**Dwoff Usage**
- This system variable is Read-Only.
- @Dwon is also known as a print directive and can be an argument of the Printline command.
- All new lines of text print as single-wide characters.

**Dwoff Example**
The ISL statement below prints "Print line" in double-wide characters and red ink, then turns off these print directives.
startprint printer
printline "---------------------------"
printline @dwon, @redon, "chit"
printline "----------------------------"
@dwoff, @redoff
endprint

See also:

Dwon

PrintLine

---

## Dwon

<!-- src: System_Variable_Dwon.htm -->

Dwon

### Function
This system variable prints the expression that follows it in double-wide characters.

**Type/Size**
A1

### Syntax
@Dwon

**Dwon Usage**
- This system variable is Read-Only.
- @Dwon is also known as a print directive and can be an argument of the Printline command.
- Double- and single-wide characters may be mixed on the same line.

**Dwon Example**
The ISL statement below will print "Print line" in double-wide characters and red ink.
Printline @dwon, @redon, "Print line" //prints double-wide in red ink

See also:

Dwoff

PrintLine

---

## Emplopt

<!-- src: System_Variable_Emplopt.htm -->

Emplopt

### Function
This system variable is an array containing the setting of SIM employee privilege options 1- 4, which are defined for the employee who initiated the event.

**Type/Size**
N1

### Syntax
@Emplopt[expression]

**Emplopt Usage**
- This system variable is Read-Only.
- The array limits for the expression are from 1 to 4.
- The value returned by the system variable will be the setting of the privilege bit: "0" for OFF, or "1" for ON.
- These values correspond to the SIM Privilege options 1 - 4 in the Employee Class File.
- This system variable can be used to control access to specific events in scripts. For example, to prevent certain employees from initiating a particular event, set do not select one of the four available privilege bits. Within the event, include an ISL statement in which the setting of the corresponding privilege bit is checked. Thus, if the setting is not selected, for example, at this point in the script, issue an error message or direct the server to take some other action instead of performing the task.

---

## Employee

<!-- src: System_Variable_Employee_Category.htm -->

Cashier
Cashier Name
Ckemp
Ckemplopt
Emplopt
Trainingmode
Tremp

---

## Fieldstatus

<!-- src: System_Variable_Fieldstatus.htm -->

Fieldstatus

### Function
This system variable contains the Input Status Flag, which is set automatically by the ISL after the WindowEdit or WindowInput command is issued in an event procedure.

**Type/Size**
A1

### Syntax
@Fieldstatus

**Fieldstatus Usage**
- This system variable is Read-Only.
- The Input Status Flag will be either of the following settings:
Flag Description
Y indicates that all fields were entered by
the operator
N indicates that some, not all, of the fields were
entered by the operator
- This system variable will be set to "Y" if each DisplayInput variable has been entered using the WindowEdit or WindowInput command; otherwise the system variable will be set to "N".

**Fieldstatus Example**
In the example below, three variables have been defined for the DisplayInput command, and all have been set by the user; consequently, @Fieldstatus is set to "Y". If the user entered data for only two of the three fields, @Fieldstatus would be set to "N". Thus, accessing this system variable is most logical after issuing either the WindowEdit or WindowInput command.
event inq : 1
var data[3] : a20
window 3, 40
displayinput 1, 1, data[1], "Enter data 1"
displayinput 2, 1, data[2], "Enter data 2"
displayinput 3, 1, data[3], "Enter data 3"
windowinput
windowclear
if @fieldstatus = "Y"
display 2, @center, "All fields entered"
else
display 2, @center, "Some fields not entered"
endif
waitforclear
endevent

See also:

Window[Edit/Input][WithSave]

---

## File I/O

<!-- src: System_Variable_File I_O_Category.htm -->

File_Bfrsize
File_Errno
File_Errstr
File_Separator

---

## File_Bfrsize

<!-- src: System_Variable_File_Bfrsize.htm -->

File_Bfrsize

### Function
This system variable is a user-definable variable that the ISL sets when it expects to read lines greater than 2048 bytes in an open file.

**Type/Size**
N9

### Syntax
@File_Bfrsize

**File_Bfrsize Usage**
This user-definable variable has Read-Write attributes.

**File_Bfrsize Example**
If the script is reading lines from a file, which is 4K in length, for example, then the script should execute the following line:
@File_Bfrsize = 4096

---

## File_Errno

<!-- src: System_Variable_File_Errno.htm -->

File_Errno

### Function
This system variable is used where an error number value is saved after every file input/output operation initiated during an event procedure.

**Type/Size**
N6

### Syntax
@File_Errno

**File_Errno Usage**
This system variable has Read-Write attributes.
- The value will either be 0 or non-zero: 0 means no error occurred, and non-zero indicates an error has occurred.
- The @File_Errstr system variable contains the error message text corresponding to the Error Code. This system variable can be used to display that text if the error occurs.

See also:

File Errstr

---

## File_Errstr

<!-- src: System_Variable_File_Errstr.htm -->

File_Errstr

### Function
This system variable returns a string containing the error that occurred during a file input/output operation. The string corresponds to the error code saved in the @File_Errno system variable.

**Type/Size**
A80

### Syntax
@File_Errstr

**File_Errstr Usage**
- This system variable is Read-Only.
- This string can be used to display the actual error message text, based on the number value saved in the @File_Errno system variable. Displaying this error message can make it easier to troubleshoot problems with file I/O operations and to verify whether the script was successful in executing a file I/O operation. For example, assume an attempt is made to write to a file with the FWrite command and the error code 5 is saved in @File_Errno. If this file I/O operation is unsuccessful, specifying the @File_Errstr system variable will allow you to display the string "I/O error".

**File_Errstr Example**
The following script opens a file. If the operation is unsuccessful, an error message will display the cause of the error.
event inq : 1
var fn : N5
fopen fn, "myfile.dat", read
if fn = 0
errormessage @File_Errstr
exitcontinue
endif
endevent

See also:

File Errno

---

## File_Separator

<!-- src: System_Variable_File_Separator.htm -->

File_Separator

### Function
This system variable stores the user-defined field separator to be used in all file input/ouput operations.

**Type/Size**
A1

### Syntax
@File_Separator

**File_Separator Usage**
- This system variable has Read-Write attributes.
- In normal ISL File I/O operations, ISL assumes the comma (,) character is the field separator. But if a different field separator is needed, the script must change the @File_Separator system variable.
- If a string with more than one character is assigned to the variable, then only the first character will be used.
- When @File_Separator changes the field separator, all subsequent field operations will use the new field separator until the @File_Separator variable is changed.

---

## Filter_active

<!-- src: System_Variable_Filter_active.htm -->

Filter_active

### Function
This system variable is a Boolean variable that is equal to "Y" if seat filtering is active or "N" if seat filtering is inactive.

**Type/Size**
A2

### Syntax
@Filter_active

**Filter_active Usage**
This system variable is Read-Only.

See also:

Filter_mask

UseFilteredDetail

UseUnFilteredDetail

---

## Filter_mask

<!-- src: System_Variable_Filter_mask.htm -->

Filter_mask

### Function
This system variable is an eight character string that contains the seat filter mask.

**Type/Size**
A8

### Syntax
@Filter_mask

**Filter_mask Usage**
This system variable is Read-Only.

**Filter_mask Example**
The following is an example of a filter mask:

80000000 - seat 1 is active (@filter_active ="Y")
00000001 - seat 32 is active (@filter_active = "Y")
50A00000 - seats 2,4,9 and 11 are active (@filter_active = "Y")
00000000 - filter inactive, no seats

See also:

Filter_active

UseFilteredDetail

UseUnFilteredDetail

---

## Function Keys

<!-- src: System_Variable_Function_Keys_Category.htm -->

Key Cancel
Key Clear
Key Down Arrow
Key End
Key Enter
Key Exit
Key Home
Key Left Arrow
Key Page Down
Key Page Up
Key Right Arrow
Key Up Arrow

---

## Groupseqnum

<!-- src: System_Variable_Groupseqnum.htm -->

Groupseqnum
Not used.

---

## Grpnum

<!-- src: System_Variable_Grpnum.htm -->

Grpnum

### Function
This system variable contains the table ID group number assigned to the current guest check.

**Type/Size**
N2

### Syntax
@Grpnum

**Grpnum Usage**
- This system variable is Read-Only.
- If no table ID group number is assigned, then 0 is returned.

---

## Gst

<!-- src: System_Variable_Gst.htm -->

Gst

### Function
This system variable contains the number of guests assigned to the current guest check.

**Type/Size**
N5

### Syntax
@Gst

**Gst Usage**
- This system variable is Read-Only.
- If no guests are assigned, then 0 is returned.

See also:

Gstrmng

---

## Gstrmng

<!-- src: System_Variable_Gstrmng.htm -->

Gstrmng

### Function
This system variable contains the number of guests remaining on the current guest check after it has been prorated.

**Type/Size**
N9

### Syntax
@Gstrmng

**Gstrmng Usage**
- This system variable is Read-Only.
- This system variable must be used within an Event Tmed only.
- This system variable should be used in tandem with the @Gstthistender system variable and the Prorate command to determine the remaining guest count on a prorated guest check. In a PMS environment, the PMS may require that the guest count on a check be prorated. For example, if five guests are on a $100 check, and $60 ($20 * 3 = $60) is tendered, the PMS assumes that three of the guests have settled. A typical PMS posting scenario will include a step for prompting the operator to enter the number of guests for the current posting, to associate the guests with the tender.
- ISL provides the same capability. However, implementing this function via a SIM Interface requires 1) knowing the number of guests remaining on the check, and 2) informing the 3700 System of the number of guests to associate with a tender. Use @Gstrmng to get the number of guests remaining, then use this value as a condition for requiring an operator to enter the number of guests during a tendering transaction before posting to the PMS.
- When the Prorate command is active and a tender/media event occurs, @Gstrmng will contain the number of guests yet to post. When the first tender is posted, @Gstrmng will be equal to all of the guests on the check. When posting subsequent tenders, @Gstrmng will be the number of guests remaining. For example, if there are five guests on a check, @Gstrmng will be five. But if three are prorated with the first tender, @Gstrmng will be two upon the second round of proration.

**Gstrmng Example**
The following subroutine implements guest count proration:
sub prorate_guests
var num_guests : n5
prorate
// If there are still guests left on this check to be prorated, ask the user how many guests this check.
if @gstrmng > 0
forever
input number_guests, "Number of guests this tender?"
if number_guests > @gstrmng
errormessage "Max guests is ", @gstrmng
else
break
endif
endfor
// Prorate this many many guests for this tender. Next time around,this many guests will be subtracted from @gstrmng.
@gstthistender = num_guests
endif
endsub

See also:

Gst

Gstthistender

---

## Gstthistender

<!-- src: System_Variable_Gstthistender.htm -->

Gstthistender

### Function
This system variable contains the number of guests on the current guest check associated with a split tender when proration is active.

**Type/Size**
N9

### Syntax
@Gstthistender

**Gstthistender Usage**
- This system variable has Read-Write attributes.
- This system variable must be used within an Event Tmed only.
- Use this system variable in tandem with the @Gstrmng system variable and Prorate command to properly prorate guest count for a PMS via a SIM Interface. When set, @Gstthistender will define the number of guests that are prorated during a tendering transaction. For explanation, see the detail description of @Gstrmng.
- If the PMS requires prorated guest counts when posting tenders, the SIM script must set @Gstthistender.

**Gstthistender Example**
See example for @Gstrmng

See also:

Gst

Gstrmng

ProRate

---

## Guestseqnum

<!-- src: System_Variable_Guestseqnum.htm -->

Guestseqnum
Not used.

---

## Hotspots

<!-- src: System_Variable_Hotspots.htm -->

Hotspots
This is a hotspot popup window. Hotspot text also allows you to jump to other Help topics.

---

## Hour

<!-- src: System_Variable_Hour.htm -->

Hour

### Function
This system variable contains the current hour of the day.

**Type/Size**
N2

### Syntax
@Hour

**Hour Usage**
- This system variable is Read-Only.
- The value returned will be from 0 to 23.
- The hour will be in 24-Hour format. For example, 2 pm will be returned as "14".

---

## Idle_Seconds

<!-- src: System_Variable_Idle_Seconds.htm -->

Idle_Seconds

### Function
This system variable determines the frequency at which SIM scripts that may be running in the background are called.

**Type/Size**

### Syntax
@Idle_Seconds

**Idle_Seconds Usage**
- The SIM script should set this variable when the background operation is required.
- This system variable is set to the number of seconds that POS operations will wait, before it calls the Idle_No_Trans event again.

**Idle_Seconds Example**
The following scripts will initialize the @idle_seconds system variable, and then the Idle_No_Trans event will be called 10 times before it stops the procedure.

var count : N5
event init
//Set to call Idle_No_Trans every 5 seconds
@idle_seconds = 5
count = 0
endevent

event idle_no_trans
count = count + 1
waitforclear "Idle_No_Trans: count ‘, count
//If we’ve done this 10 times, stop the idle call.
if count > 10
@idle_seconds = 0
endif
endevent

---

## InBackupMode

<!-- src: System_Variable_InBackupMode.htm -->

InBackupMode

### Function
This variable returns a value of 1 if Ops is in backup server mode. Otherwise, zero is returned.

**Type/Size**
N1

### Syntax
@InBackupMode

**InBackupMode Usage**
This system variable is Read-Only.

---

## InEditClosedCheck

<!-- src: System_Variable_InEditClosedCheck.htm -->

InEditClosedCheck

### Function
This variable returns a numeric "1" if the current check status is in edit closed check.

**Type/Size**
N1

### Syntax
@InEditClosedCheck

**InEditClosedCheck Usage**
This system variable is Read-Only.
The Pickup_Check variable will fire when editing or reopening a closed check. The user may use the @InReopenClosedCheck and the @ineditclosedcheck variables to determine if the check is a reopened check, or an edited check.

**InEditClosedCheck Example**
event inq : 1
Errormessage "Edit Closed Check state is ", @InEditClosedCheck
endevent

---

## Inputstatus

<!-- src: System_Variable_Inputstatus.htm -->

Inputstatus

### Function
This system variable sets the User Input Status Flag if the ContinueOnCancel command is executed.

**Type/Size**
N1

### Syntax
@Inputstatus

**Inputstatus Usage**
- This system variable is Read-Only.
- The User Input Status Flag will be set to one of the following:
Flag Description
0 indicates that the user canceled any input by pressing [Cancel]
1 indicates that the user entered all valid data

See also:

ContinueOnCancel

---

## InReopenClosedCheck

<!-- src: System_Variable_InReopenClosedCheck.htm -->

InReopenClosedCheck

### Function
This variable returns a numeric 1, if the current check is in the re-open round.

**Type/Size**
N1

### Syntax
@InReopenClosedCheck

**InReopenClosedCheck Usage**
This system variable is Read-Only.
The Pickup_Check variable will fire when editing or reopening a closed check. The user may use the @InReopenClosedCheck and the @ineditclosedcheck variables to determine if the check is a reopened check, or an edited check.

**InReopenClosedCheck Example**
event inq : 1
Errormessage "Reopened Closed check state is ", @InReopenClosedCheck
endevent

---

## Instandalonemode

<!-- src: System_Variable_Instandalonemode.htm -->

Instandalonemode

### Function
This system variable indicates if POS Operations is in Stand Alone Mode. The variable is set to 1 if POS Operations is in Stand Alone Mode and 0 if it is not.

**Type/Size**
N1

### Syntax
@instandalonemode

**Instandalonemode Usage**
This system variable is Read-Only.

---

## Jnl

<!-- src: System_Variable_Jnl.htm -->

Jnl

### Function
This system variable contains the object number of the Journal Printer assigned to the UWS.

**Type/Size**
N7

### Syntax
@Jnl

**Jnl Usage**
- This system variable is Read-Only.
- This system variable can be used as an argument to the StartPrint[WithStatus] commands.

See also:

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Key_Cancel

<!-- src: System_Variable_Key_Cancel.htm -->

Key_Cancel

### Function
This system variable contains the [Cancel] key.

**Type/Size**
Key

### Syntax
@Key_Cancel

**Key_Cancel Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

**Key_Cancel Example** The script below tests that the [Cancel] key was pressed by using @Key_Cancel. The operator is prompted to enter a number between 1 and 9. However, if either the [Clear] or [Cancel] key is pressed instead, the script will terminate.
event inq : 4
var key_pressed : key // Hold the function key pressed
var data : a10 // Hold the number chosen
forever
inputkey key_pressed, data, "Type a Number then Enter, Clear to Exit"
if key_pressed = @Key_Clear
exitcontinue
elseif key_pressed = @Key_Cancel
exitcontinue
elseif key_pressed = @Key_Enter
if data > 0 and data <=10
waitforclear "You chose ", data, ". Press Clear."
else
errormessage "Choose a number between 1 and 10, then press Enter."
endif
endif
endfor
endevent

See also:

InputKey

---

## Key_Clear

<!-- src: System_Variable_Key_Clear.htm -->

Key_Clear

### Function
This system variable contains the [Clear] key.

**Type/Size**
Key

### Syntax
@Key_Clear

**Key_Clear Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

**Key_Clear Example**
See the example for @Key_Cancel

See also:

InputKey

LoadKybdMacro

---

## Key_Down_Arrow

<!-- src: System_Variable_Key_Down_Arrow.htm -->

Key_Down_Arrow

### Function
This system variable contains the [Down Arrow] key.

**Type/Size**
Key

### Syntax
@Key_Down_Arrow

**Key_Down_Arrow Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_End

<!-- src: System_Variable_Key_End.htm -->

Key_End

### Function
This system variable contains the [End] key.

**Type/Size**
Key

### Syntax
@Key_End

**Key_End Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Enter

<!-- src: System_Variable_Key_Enter.htm -->

Key_Enter

### Function
This system variable contains the [Enter] key.

**Type/Size**
Key

### Syntax
@Key_Enter

**Key_Enter Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

**Key_Enter Example**
See the example for @Key_Cancel

See also:

InputKey

LoadKybdMacro

---

## Key_Exit

<!-- src: System_Variable_Key_Exit.htm -->

Key_Exit

### Function
This system variable contains the [Exit] key.

**Type/Size**
Key

### Syntax
@Key_Exit

**Key_Exit Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Home

<!-- src: System_Variable_Key_Home.htm -->

Key_Home

### Function
This system variable contains the [Home] key.

**Type/Size**
Key

### Syntax
@Key_Home

**Key_Home Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Left_Arrow

<!-- src: System_Variable_Key_Left_Arrow.htm -->

Key_Left_Arrow

### Function
This system variable contains the [Left Arrow] key.

**Type/Size**
Key

### Syntax
@Key_Left_Arrow

**Key_Left_Arrow Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Page_Down

<!-- src: System_Variable_Key_Page_Down.htm -->

Key_Page_Down

### Function
This system variable contains the [Page Down] key.

**Type/Size**
Key

### Syntax
@Key_Page_Down

**Key_Page_Down Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Page_Up

<!-- src: System_Variable_Key_Page_Up.htm -->

Key_Page_Up

### Function
This system variable contains the [Page Up] key.

**Type/Size**
Key

### Syntax
@Key_Page_Up

**Key_Page_Up Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Right_Arrow

<!-- src: System_Variable_Key_Right_Arrow.htm -->

Key_Right_Arrow

### Function
This system variable contains the [Right Arrow] key.

**Type/Size**
Key

### Syntax
@Key_Right_Arrow

**Key_Right_Arrow Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Key_Up_Arrow

<!-- src: System_Variable_Key_Up_Arrow.htm -->

Key_Up_Arrow

### Function
This system variable contains the [Up Arrow] key.

**Type/Size**
Key

### Syntax
@Key_Up_Arrow

**Key_Up_Arrow Usage**
- This system variable is Read-Only.
- This system variable is designed for checking keystrokes from the InputKey command and setting keyboard macros with the LoadKyBdMacro command.

See also:

InputKey

LoadKybdMacro

---

## Lastauthemp

<!-- src: System_Variable_Lastauthemp.htm -->

Lastauthemp

### Function
This system variable contains the employee object number for the employee who last authorized a transaction. These values are cleared each time a new transaction begins in POS Operations.

**Type/Size**
N9

### Syntax
@LASTAUTHEMP

**Lastauthemp Usage**
- Use this system variable to keep track of the manager or privileged employee who last authorized a privileged operation.
- This system variable is Read-Only.

---

## Lastauthemp_fname

<!-- src: System_Variable_Lastauthemp_fname.htm -->

Lastauthemp_fname

### Function
This system variable contains the first name of the employee who performed the last transaction authorization. These values are cleared each time a new transaction begins in POS Operations.

**Type/Size**
A8

### Syntax
@LASTAUTHEMP_FNAME

**Lastauthemp_fname Usage**
- Use this system variable to track the manager or privileged employee who last authorized a privileged operation.
- This system variable is Read-Only.

---

## Lastauthemp_lname

<!-- src: System_Variable_Lastauthemp_lname.htm -->

Lastauthemp_lname

### Function
This system variable contains the last name of the employee who performed the last transaction authorization. These values are cleared each time a new transaction begins in POS Operations.

**Type/Size**
A16

### Syntax
@LASTAUTHEMP_LNAME

**Lastauthemp_lname Usage**
- Use this system variable to track the manager or privileged employee who last authorized a privileged operation.
- This system variable is Read-Only.

---

## Line

<!-- src: System_Variable_Line.htm -->

Line

### Function
This system variable contains the number of the current line in the script that is being executed.

**Type/Size**
N5

### Syntax
@LINE

**Line Usage**
- This system variable is Read-Only.
- Use this system variable as a debugging tool.

See also:

Line Executed

---

## Line_Executed

<!-- src: System_Variable_Line_Executed.htm -->

Line_Executed

### Function
This system variable contains the number of lines executed since the script began running.

**Type/Size**
N5

### Syntax
@Line_Executed

**Line_Executed Usage**
- This system variable is Read-Only.
- Use this system variable as a debugging tool.

See also:

Line

---

## Magstatus

<!-- src: System_Variable_Magstatus.htm -->

Magstatus

### Function
This system variable contains the Magnetic Card Entry Status Flag. The flag indicates whether data was input by swiping a card through a magnetic card reader.

**Type/Size**
A1

### Syntax
@Magstatus

**Magstatus Usage**
- This system variable is Read-Only.
- The Magnetic Card Entry Status Flag will be either of the following settings:
Flag Description
Y indicates that data was input by swiping a card through a magnetic card reader
N indicates that data was input by means other than a magnetic card reader, such as via keyboard entry
- @Magstatus is best used after issuing an Input or WindowInput/Edit command.

**Magstatus Example**
This event captures credit card information, entered manually from a keyboard or electronically from a magnetic card reader. The script uses the @Magstatus system variable to determine the source from which the information is captured.
event : 1
var cardholder_name : a20
var account_num : a19
var expire_date : n4
var track1_data : a79
var track2_data : a79
window 3, 78
touchscreen 16
displayMSinput 1, 2, cardholder_name{m2, 2, 1, *}, \
"Read Credit Card or Enter Guest Name", \
2, 2, account_num{m2, 1, 1, *}, "Enter Account Number", \
3, 2, expire_date{m2, 3, 1, 4}, "Enter Expiration Date (YYMM)", \
0, 0, track1_data{m1, *}, " "
windowinput
waitforclear
window 4, 40
display 1, 2, "Cardholder: ", cardholder_name
if @MAGSTATUS = "Y"
display 2, 2, "As read from credit card."
else
display 2, 2, "As entered from keyboard."
endif
waitforclear
endevent

See also:

DisplayMSInput

---

## Max_Lines_To_Run

<!-- src: System_Variable_Max_Lines_To_Run.htm -->

Max_Lines_To_Run

### Function
This system variable is a debugging tool that can be set to the maximum number of lines in the script to run.

**Type/Size**
N5

### Syntax
@Max_Lines_To_Run = # of lines

**Max_Lines_To_Run Usage**
- This system variable has Read-Write attributes.
- This system variable should be set before the lines in the script that are being debugged.

---

## Maxdtlr

<!-- src: System_Variable_Maxdtlr.htm -->

Maxdtlr

### Function
This system variable contains the maximum size string required to format the transaction detail held in the @Trdtlr system variable.

**Type/Size**
N9

### Syntax
@Maxdtlr

**Maxdtlr Usage**
This system variable is Read-Only.

See also:

Dtl_Mlvl

Dtl_Name

Dtl_Objnum

Dtl_Plvl

Dtl_Qty

Dtl_Seat

Dtl_Slvl

Dtl_Status

Maxdtlt

Trdtlr

---

## Maxdtlt

<!-- src: System_Variable_Maxdtlt.htm -->

Maxdtlt

### Function
This system variable contains the maximum size string required to format the transaction detail held in the @Trdtlt system variable.

**Type/Size**
N9

### Syntax
@Maxdtlt

**Maxdtlt Usage**
This system variable is Read-Only.

See also:

Dtl_Mlvl

Dtl_Name

Dtl_Objnum

Dtl_Plvl

Dtl_Qty

Dtl_Seat

Dtl_Slvl

Dtl_Status

Trdtlr

---

## Minute

<!-- src: System_Variable_Minute.htm -->

Minute

### Function
This system variable contains the current minute of the current hour.

**Type/Size**
N2

### Syntax
@Minute

**Minute Usage**
- This system variable is Read-Only.
- A value returned will be from 0 to 59.

---

## MLVL

<!-- src: System_Variable_MLVL.htm -->

MLVL

### Function
This variable returns a value representing the current main level.

**Type/Size**
N2

### Syntax
@MLVL

**MLVL Usage**
This system variable is Read-Only.

**MLVL Example**
event inq : 1
Errormessage "Current main level is is ", @mlvl
endevent

---

## Month

<!-- src: System_Variable_Month.htm -->

Month

### Function
This system variable contains the current month of the current year.

**Type/Size**
N2

### Syntax
@Month

**Month Usage**
- This system variable is Read-Only.
- The value returned will be from 1 to 12.

**Month Example**
See the example for @Day

See also:

Day

Year

---

## Numdsc

<!-- src: System_Variable_Numdsc.htm -->

Numdsc

### Function
This system variable contains the number of active discounts posted to the current guest check.

**Type/Size**
N1

### Syntax
@Numdsc

**Numdsc Usage**
This system variable is Read-Only.

---

## Numdtlr

<!-- src: System_Variable_Numdtlr.htm -->

Numdtlr

### Function
This system variable contains the number of transaction detail entries posted during the current service round on the guest check.

**Type/Size**
N3

### Syntax
@Numdtlr

**Numdtlr Usage**
This system variable is Read-Only.

See also:

Dtl Taxtype

Dtl Ttl

Dtl Type

Dtl_Mlvl

Dtl_Name

Dtl_Objnum

Dtl_Plvl

Dtl_Qty

Dtl_Seat

Dtl_Slvl

Dtl_Status

Numdtlt

---

## Numdtlt

<!-- src: System_Variable_Numdtlt.htm -->

Numdtlt

### Function
This system variable contains the number of transaction detail entries posted to the current guest check.

**Type/Size**
N3

### Syntax
@Numdtlt

**Numdtlt Usage**
- This system variable is Read-Only.
- This system variable is used to provide the maximum array limit for the @Dtl_* system variables.

**Numdtlt Example**
See the example for @Dtl_Mlvl

See also:

Dtl_Mlvl

Dtl_Name

Dtl_Objnum

Dtl_Plvl

Dtl_Qty

Dtl_Seat

Dtl_Slvl

Dtl_Status

Numdtlr

---

## Numsi

<!-- src: System_Variable_Numsi.htm -->

Numsi

### Function
This system variable contains the number of active sales itemizers defined in the Sales|Descriptor File with a non-blank descriptor.

**Type/Size**
N1

### Syntax
@Numsi

**Numsi Usage**
This system variable is Read-Only.

---

## Numsvc

<!-- src: System_Variable_Numsvc.htm -->

Numsvc

### Function
This system variable contains the number of active service charge itemizers defined for the Revenue Center.

**Type/Size**
N1

### Syntax
@Numsvc

**Numsvc Usage**
- This system variable is Read-Only.
- This system variable will always return the value 1.

---

## Numtax

<!-- src: System_Variable_Numtax.htm -->

Numtax

### Function
This system variable contains the number of active tax rates with a non-blank tax collected name.
Note: This variable returns a value based on information entered in the following fields on the Tax Rates | General form in POS Configurator:
- Taxable Sales Name 2800
- Tax Collected Name 3700

**Type/Size**
N1

### Syntax
@Numtax

**Numtax Usage**
This system variable is Read-Only.

---

## Order_Type_Name

<!-- src: System_Variable_Order_Type_Name.htm -->

Order_Type_Name

### Function
This system variable contains the name of the active order type on the current guest check.

**Type/Size**
A16

### Syntax
@Order_type_name

**Order_Type_Name Usage**
This system variable is Read-Only.

---

## Ordertype

<!-- src: System_Variable_Ordertype.htm -->

Ordertype

### Function
This system variable contains the object number of the active order type on the current guest check.

**Type/Size**
N1

### Syntax
@Ordertype

**Ordertype Usage**
This system variable is Read-Only.

---

## Ordr

<!-- src: System_Variable_Ordr.htm -->

Ordr

### Function
This system variable is an array containing the object number of the order device (e.g., remote printer) defined for the system.

**Type/Size**
N7

### Syntax
@Ordr[expression]

**Ordr Usage**
- This system variable is Read-Only.
- The array limits for the expression are from 1 to 15.
- This system variable can be used as an argument to the StartPrint[WithStatus] commands.

**Ordr Example**
The example below starts a print job at a remote order printer.
sub print_message
startprint @ordr1
printline "============================"
printline "Message from ", sender_name
printline "============================"
for rowcnt = 1 to 136
if len(kitchen_msg[rowcnt]) > ""
printline kitchen_msg[rowcnt]
endif
endfor
printline "======= END MESSAGE ========"
endprint
endsub

See also:

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Parent_Dtl_Id

<!-- src: System_Variable_Parent_Dtl_Id.htm -->

Parent_Dtl_Id

### Function
This variable returns the detail identification value associated with the parent transaction detail entry. Discounts, touch refills, and touch returns have a parent menu item.

MICROS recommends that you are specific as possible when validating menu items and parent items.

**Type/Size**
N1

### Syntax
@Parent_Dtl_Id

**Parent_Dtl_Id Usage**
This system variable is Read-Only.

---

## Platform

<!-- src: System_Variable_Platform.htm -->

Platform

### Function
This system variable contains a character string identifying the hardware platform on which the script is running.

**Type/Size**
A4

### Syntax
@Platform

**Platform Usage**
- This system variable is Read-Only.
- The string returned is "3700".

---

## PMSBuffer

<!-- src: System_Variable_PMSBuffer.htm -->

PMSBuffer

### Function
This system variable contains a string that points to the entire message received from the third-party system communicating with the 3700 System.

**Type/Size**
String; size depends on the data returned from the third-party system (e.g., PMS)

### Syntax
@Pmsbuffer

**PMSBuffer Usage**
- This system variable has Read-Write attributes.
- The size of data in the PMS buffer is formatted as a string, which can be up to 32,768 bytes in length.
- This system variable is a debugging tool. For example, if the PMS message received by the 3700 System is suspected of being formatted incorrectly, using @Pmsbuffer the message can be displayed in an ISL-defined window as it is being received.
- Issuing @Pmsbuffer is valid only after a message has been received from the third-party system (e.g., PMS).

See also:

Show_PMS_Messages

---

## PMSNumber

<!-- src: System_Variable_PMSNumber.htm -->

PMSNumber

### Function
This system variable contains the PMS object number, defined in the Interfaces form, to which the script is linked.

**Type/Size**
N7

### Syntax
@PMSNUMBER

**PMSNumber Usage**
- This system variable has Read-Write attributes.
- In order to link the script file to a PMS, this object number is contained in the name of the script file. Thus, if you are running the script pms1.isl, then @PMSNUMBER will be set to 1.

---

## PMSSeqNum

<!-- src: System_Variable_PMSSeqNum.htm -->

PMSSeqNum

### Function
This system variable provides the interface sequence number (interface_def.interface_seq) of the current interface. This value is used when executing a keyboard macro that runs another SIM inquire (INQ) event.

**Type/Size**
N9

### Syntax
@PMSSeqNum

Note:
This variable can be used to look up the sequence number from the database. However, this does ot work for interfaces that need to run in BSM mode.
Currently, the interface sequence number must be looked up by the installer (via dbiSQL) and entered into a configuration file.

**PMSSeqNum Usage**
- This system variable is read-only.

**PMSSeqNum Example**

Event inq : 1 //call inquire event 2
loadKybdMacro key(24,(16384 + 2) + @PMSSeqNum)
EndEvent // inq : 1

Event inq : 2
waitForClear " Running inquire event 2"
EndEvent : 2

---

## Prefix_Dtl_Name

<!-- src: System_Variable_Prefix_Dtl_Name.htm -->

Prefix_Dtl_Name

### Function
This system variable can be used to modify the behavior of @Dtl_Name[ ] when used to access the name of menu items in the check detail. When @Prefix_Dtl_Name is set to a non-zero value, @Dtl_Name[ ] prefixes the menu item name with the menu level prefix for the items current pricing level.
This behavior requires that the menu item be configured to print the menu level name (Sales | Menu Item Classes | Print/Display). The prefix of "main" or "sub" will depend on whether the Use sub menu level pricingl option has been selected (Sales | Menu Item Classes | Price / Totals).

**Type/Size**
N7

### Syntax
@Prefix_Dtl_Name = integer

**Prefix_Dtl_Name Usage**
- This system variable has Read-Write attributes.
- By default, @Prefix_Dtl_Name is 0 (zero), preserving the default behavior of @Dtl_Name[ ].

**Prefix_Dtl_Name Example**
The following example will only display the Menu Level prefix if the Menu level name option (Sales | Menu Item Classes | Print / Display) is set for the menu item.

Event mi
@Prefix_Dtl_Name = 0 // Display name without the prefix.
ErrorMessage "MI name: ", @Dtl_Name[@NumDtlt]
@Prefix_Dtl_Name = 1 // Display name with the prefix.
ErrorMessage "Prefixed MI name: ", @Dtl_Name[@NumDtlt]
Endevent

---

## Prevpay

<!-- src: System_Variable_Prevpay.htm -->

Prevpay

### Function
This system variable contains the total amount tendered thus far on the current guest check.

**Type/Size**
$12

### Syntax
@Prevpay

**Prevpay Usage**
This system variable is Read-Only.

---

## Printing

<!-- src: System_Variable_Printing_Category.htm -->

Chk
Dwoff
Dwon
Header
Jnl
Ordr
Printstatus
Rcpt
Redoff
Redon
Trailer
Vald

---

## Printstatus

<!-- src: System_Variable_Printstatus.htm -->

Printstatus

### Function
This system variable sets the Print Status Flag to indicate whether a supervised print job has completed successfully or failed.

**Type/Size**
A1

### Syntax
@Printstatus

**Printstatus Usage**
- This system variable is Read-Only.
- The Print Status Flag will be either of the following settings:
Flag Description
Y indicates that a supervised print job completed successfully
N indicates that a supervised print job failed
- Using the StartPrintWithStatus command to execute supervised print jobs will cause the @Printstatus system variable to be set. Once set, the value can be used as a condition to determine whether the print job completed successfully or failed.

**Printstatus Example**
The event procedure below uses the setting of @Printstatus to determine which message to display after issuing the Printline command.
event inq : 1
startprintwithstatus @chk
printline "this is a line"
endprint
if @printstatus = "Y"
waitforclear "Print successful"
else
waitforclear "Print failed"
endif

See also:

PrintLine

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Rcpt

<!-- src: System_Variable_Rcpt.htm -->

Rcpt

### Function
This system variable contains the object number of the Customer Receipt Printer defined for the UWS.

**Type/Size**
N7

### Syntax
@Rcpt

**Rcpt Usage**
- This system variable is Read-Only.

See also:

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Redoff

<!-- src: System_Variable_Redoff.htm -->

Redoff

### Function
This system variable returns red ink to black ink (or default ink, e.g., blue).

**Type/Size**
A1

### Syntax
@Redoff

**Redoff Usage**
- This system variable is Read-Only.
- @Redoff is also known as a print directive and can be an argument of the Printline command.
- All new lines of text print default ink (i.e., black, blue, etc.).

**Redoff Example**
The ISL statement below prints "chit" and "-------------" in double-wide characters and red ink, then turns off these print directives.
startprint printer
printline "----------------------------"
printline @dwon, @redon, "chit"
printline "----------------------------"
@dwoff, @redoff
endprint

See also:

PrintLine

Redon

---

## Redon

<!-- src: System_Variable_Redon.htm -->

Redon

### Function
This system variable prints the expression that follows it in red ink.

**Type/Size**
A1

### Syntax
@REDON

**Redon Usage**
- This system variable is Read-Only.
- @REDON is also known as a print directive and can be an argument of the Printline command.
- Characters in red and black ink can print on the same line.
- This variable works only for impact printers equipped with 2-color ribbons.

**Redon Example**
The ISL statement below will print "Print line" in double-wide characters and red ink.
Printline @dwon, @redon, "Print line" //prints double-wide in red ink

See also:

PrintLine

Redoff

---

## ReturnStatus

<!-- src: System_Variable_ReturnStatus.htm -->

ReturnStatus

### Function
This system variable is used to determine the current return status of the transaction.

**Detail**
Variable: @RETURNSTATUS
Values: Y or N. If the value Y is returned OPS is in either Return or Transaction Return mode.

### Argument/Description
This variable is required for certain interfaces, which require the current return status of POS Operations.
When invoked, an INQ event has no internal mechanism for checking the current return status of OPS. Return status determines (along with Void status) whether the item will be added to or subtracted from the guest check.

---

## RVC

<!-- src: System_Variable_RVC.htm -->

RVC

### Function
This system variable contains the number of the Revenue Center to which the script is linked by its Revenue Center PMS Link

**Type/Size**
N3

### Syntax
@RVC

**RVC Usage**
- This system variable is Read-Only.
- This system variable will be set to the object number of the Revenue Center to which the current UWS is assigned.

---

## RVCName

<!-- src: System_Variable_RVCName.htm -->

RVCName

### Function
This system variable contains the name of the Revenue Center to which the script is linked by its Revenue Center PMS Link

**Type/Size**
A16

### Syntax
@RVCName

**RVCName Usage**
- This system variable is Read-Only.
- This system variable will be set to the name of the Revenue Center to which the current UWS is assigned.

---

## RxMsg

<!-- src: System_Variable_RxMsg.htm -->

RxMsg

### Function
This system variable contains the Event ID assigned to the response message sent by a third-party system to the 3700 System.

**Type/Size**
A32

### Syntax
@RxMsg

**RxMsg Usage**
- This system variable is Read-Only.
- When either the WaitForRxMsg or GetRxMsg commands are executed, the ISL waits for a return event. The first field of the Application_Data segment of the response message is assumed to be the Event ID of the return event. The @RxMsg system variable contains that Event ID.

**RxMsg Example**
In the event below, the @RxMsg system variable is used to verify that the Event ID in the returned message is the correct one.
event inq : 1
txmsg "ver_req" // Transmit string requesting version of system software
getrxmsg // Wait for response
if @rxmsg = "ver_rsp"
rxmsg version_s // Format message received
waitforclear version_s // Display it
elseif @rxmsg = "ver_err"
errormessage "Version number invalid"
exitcancel
endif
endevent

See also:

GetRxMsg

WaitForRxMsg

---

## Script

<!-- src: System_Variable_Script_Category.htm -->

Idle_Seconds
Line
Line_Executed
Max_Lines_To_Run
PMSBuffer
PMSNumber
RVC
RVCName
RxMsg System Variable
Show_PMS_Messages
Strict_Args
Trace
Varused
Varspace
Warnings_Are_Fatal

---

## Seat

<!-- src: System_Variable_Seat.htm -->

Seat

### Function
This system variable contains the number of the active seat on the current guest check.

**Type/Size**
N9

### Syntax
@Seat

**Seat Usage**
This system variable is Read-Only.

---

## Second

<!-- src: System_Variable_Second.htm -->

Second

### Function
This system variable contains the current second of the current minute.

**Type/Size**
N2

### Syntax
@Second

**Second Usage**
- This system variable is Read-Only.
- A value from 0 to 59 is valid.

---

## ServerName

<!-- src: System_Variable_ServerName.htm -->

ServerName

### Function
This variable returns the PC name of the server. This value is the LAN Node Address of the server as entered in POS Configurator.

**Type/Size**
A15

### Syntax
@ServerName

**ServerName Usage**
This system variable is Read-Only.

**ServerName Example**
event inq : 1
Errormessage "Current Server is ", @servername
Endevent

---

## Show_PMS_Messages

<!-- src: System_Variable_Show_PMS_Messages.htm -->

Show_PMS_Messages

### Function
This system variable, when set to a non-zero value, outputs all PMS messages to the 3700d.log file, a file that contains debugging messages from all of the 3700 processes.

**Type/Size**
N5

### Syntax
@Show_PMS_Messages = integer

**Show_PMS_Messages Usage**
- This system variable has Read-Write attributes.
- @Show_PMS_Messages can be set to any integer. However, setting the system variable to 0, will disable its function.
- This system variable can be placed anywhere in a script.
- Using @Show_PMS_Messages is another method of debugging PMS messages received by the 3700 System. @PMSbuffer is also useful for debugging PMS messages; this system variable contains the actual PMS message received by the 3700 System.

See also:

PMSBuffer

---

## SI

<!-- src: System_Variable_SI.htm -->

SI

### Function
This system variable is an array containing the sales itemizer totals posted to the current guest check.

**Type/Size**
$12

### Syntax
@SI[expression]

**SI Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.
- This system variable will return the totals posted to the sales itemizer specified by the array index. For example, if the array index references @SI[1], any totals posted to Sales Itemizer #1 will be returned.

---

## SLVL

<!-- src: System_Variable_SLVL.htm -->

SLVL

### Function
This variable returns a value representing the current sub level.

**Type/Size**
N2

### Syntax
@SLVL

**SLVL Usage**
This system variable is Read-Only.

**SLVL Example**
event inq : 1
Errormessage "Current sub level is is ", @slvl
Endevent

---

## Srvprd

<!-- src: System_Variable_Srvprd.htm -->

Srvprd

### Function
This system variable contains the active serving period.

**Type/Size**
N9

### Syntax
@Srvprd

**Srvprd Usage**
This system variable is Read-Only.

---

## Strict_Args

<!-- src: System_Variable_Strict_Args.htm -->

Strict_Args

### Function
This system variable, when set to a non-zero value, will check whether the minimum or maximum number of variables is specified if the RxMsg, Fread, Split, and SplitQ commands are used.

**Type/Size**
N9

### Syntax
@Strict_Args

**Strict_Args Usage**
This system variable has Read-Write attributes.

See also:

FRead

RxMsg

Split

SplitQ

---

## SustainCustomText

<!-- src: System_Variable_SustainCustomText.htm -->

SustainCustomText

### Function
This variable allows the rear display text to be sustained until one of the following occurs:
- The display is cleared via the ClearRearArea command
- A non-zero total is displayed
- The @SustainCustomText is reset to zero.

**Type/Size**
N1

### Syntax
@SustainCustomText

**SustainCustomText Usage**
This system variable can be edited.

---

## Svc

<!-- src: System_Variable_Svc.htm -->

Svc

### Function
This system variable contains the total amount of service charges posted to the current guest check.

**Type/Size**
$12

### Syntax
@Svc

**Svc Usage**
- This system variable is Read-Only.
- In the 3700 System, the @Chgtip amount is included in the @Svc system variable

---

## SvcI

<!-- src: System_Variable_SvcI.htm -->

SvcI

### Function
This system variable provides access to the current amount in the service charge itemizer. Totals are affected by the reset itemizer.

**Type/Size**
$12

### Syntax
@SvcI[Expression]

**SvcI Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.
- This variable will return the totals posted to the service charge itemizer specified by the array index. For example, if the array index references @SvcI[1], any totals posted to Service Charge Itemizer #1 will be returned.

---

## SvcIttl

<!-- src: System_Variable_SvcIttl.htm -->

SvcIttl
### Function
This system variable provides access to the total amount of each service charge in the service charge itemizer. Totals are affected by the reset itemizer.

**Type/Size**
$12

### Syntax
@SvcIttl[Expression]

**SvcIttl Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.
- This variable will return the sum of the service charges posted to the service charge itemizer specified by the array index. For example, if the array index references @SvcIttl[1], any service charge totals posted to Service Charge Itemizer #1 will be returned.

---

## System

<!-- src: System_Variable_System_Category.htm -->

Platform
PMSSeqNum
SustainCustomText
Version
Wsid
Wsname
WSType

---

## Tax

<!-- src: System_Variable_Tax.htm -->

Tax

### Function
This system variable is an array containing the totals posted to the active tax rate on the current guest check. The value is subject to the prorate command.

**Type/Size**
$12

### Syntax
@Tax[expression]

**Tax Usage**
- This system variable is Read-Only.
- The array limits for the expression are from 1 to 8.

See also:

Taxrate

---

## Taxrate

<!-- src: System_Variable_Taxrate.htm -->

Taxrate

### Function
This system variable is an array containing the tax rate defined for the specified Tax Table.

**Type/Size**
A12

### Syntax
@Taxrate[expression]

**Taxrate Usage**
- This system variable is Read-Only.
- The array limits for the expression are from 1 to 8.
- The value returned is a string instead of an amount, since the percentage may be any number of decimal digits (i.e., 5.1265).

See also:

Tax

---

## Tblid

<!-- src: System_Variable_Tblid.htm -->

Tblid

### Function
This system variable contains the table ID assigned to the current guest check.

**Type/Size**
A4

### Syntax
@Tblid

**Tblid Usage**
This system variable is Read-Only.

See also:

Tblnum

---

## Tblnum

<!-- src: System_Variable_Tblnum.htm -->

Tblnum

### Function
This system variable contains the object number of the table ID assigned to the current guest check.

**Type/Size**
N7

### Syntax
@TBLNUM

**Tblnum Usage**
This system variable is Read-Only.

**Tblnum Example**
This event is used to send to the PMS a message indicating which table has just paid its check.
event final_tender
txmsg "CHECK_PAID", @cknum, @tblnum
// Here we do a 'getrxmsg' to receive the message to fulfill the requirements of the protocol, but do not process any data associated with the message.
getrxmsg
endevent

---

## TblObjNum

<!-- src: System_Variable_TblObjNum.htm -->

TblObjNum

### Function
This system variable is used to return the table number (i.e., object number) assigned through POS Configurator. The variable should be used in place of the @TblNum variable, which reported the database sequence number, rathe than the table object number.

**Type/Size**
N9

### Syntax
@tblobjnum

**TblObjNumExample**
Event Final_Tender
InfoMessage "Table Object Number", @tblobjnum
EndEvent

---

## Tender/Media

<!-- src: System_Variable_Tender_Media_Category.htm -->

CcAuth_Count
Ccdate
Ccnumber
Gstrmng
Gstthistender
Tmdnum
Tmdtypedef

---

## Test_Dsvc_Ttl

<!-- src: System_Variable_Test_Dsvc_Ttl.htm -->

Test_Dsvc_Ttl

### Function
This system variable is used to return value of a discount or service charge. It is initialized to zero at the beginning of each SIM event and also prior to running a Test_Dsvc test.

**Type/Size**
$12

### Syntax
@Test_Dsvc_Ttl

**Test_Dsvc_Ttl Usage**
This variable is read only.

---

## Tmdnum

<!-- src: System_Variable_Tmdnum.htm -->

Tmdnum

### Function
This system variable contains the number assigned to the tender/media associated with this posting.

**Type/Size**
N9

### Syntax
@TMDNUM

**Tmdnum Usage**
This system variable is Read-Only

---

## Tmdtypedef

<!-- src: System_Variable_Tmdtypedef.htm -->

Tmdtypedef

### Function
This system variable contains the Tender/Media Type Definition of the tender referenced by the Tmed Event.

**Type/Size**
A14

### Syntax
@TMDTYPEDEF

**Tmdtypedef Usage**
- This system variable is Read-Only.
- This system variable is valid only when executed in a tender/media event (i.e., Event Tmed).
- The value returned is a string containing the hexadecimal digits representing the tender type programmed for the tender in the database (e.g., "A0409A22280000").
- This system variable is useful for determing the characteristics of the tender. For example, a script could be designed to analyze the hexadecimal string, to determine if the Assume paid in full option is set for a particular tender. If the @Tmdtypedef variable returned the "A0409A22280000" string, the 1st digit is A or 1010 in hex. When the 1st digit is A (or 1010 in hex), the first four type definition settings would be as follows:

**Type Definition**  |  **Position**  |  **Hex=Option Setting**  |

TMED_OPEN_CASH_DWR |  1 |  1=On |

TMED_AMT_REQD |  2 |  0=Off |

TMED_ASSUME_PAID_IN_FULL |  3 |  1=On |

TMED_ENDORSEMENT_REQD |  4 |  0=Off |

Refer to the Type Definition Table for a listing of the type definitions and their position numbers.

**Tmedtypedef Table**

TMED_OPEN_CASH_DWR=1 |  TMED_ENABLE_PMS=31 |

TMED_AMT_REQD=2 |  TMED_NO_TRLR_MULTI_ROUND=32 |

TMED_ASSUME_PAID_IN_FULL=3 |  TMED_PMS_DO_NOT_NET_CHG=33 |

TMED_ENDORSEMENT_REQD=4 |  TMED_PMS_OUTLET_CC=34 |

TMED_REF_REQD=5 |  TMED_PRINT_MEMO_CHK=35 |

TMED_VALD_REQD=6 |  TMED_PRINT_SEAT_CHK=36 |

TMED_PRMPT_DURING_KEYED_CA=7 |  TMED_INC_SINGLE_FILTER=37 |

TMED_PAYMENT_IS_DEBIT_CARD=8 |  TMED_PRNT_ON_RCPT_PRINTER=38 |

TMED_CHG_TIP_REQD=9 |  TMED_PRINT_PERSONAL_CHK=39 |

TMED_POST_GROSS_RCPTS=10 |  TMED_REQUIRES_CRDT_AUTH=40 |

TMED_POST_CHRGD_RCPTS=11 |  TMED_CAEDC_CREDIT_FLAG=41 |

TMED_AUTO_SVC_EXMPT=12 |  TMED_DONT_SAVE_PMS_RSP=42 |

TMED_RSVD_03=13 |  TMED_PRINT_SHARED_CHK=43 |

TMED_DD_DFLT_SVC_TTL=13 |  TMED_TRUMP_COUPON=44 |

TMED_RSVD_04=14 |  TMED_WEIGHED_MOD_10_CHK=45 |

TMED_OVERRIDE_SIGN_OUT=14 |  TMED_DONT_CHK_EXPDATE=46 |

TMED_PROMPT_FOR_CASHBACK=15 |  TMED_PRNT_W_LOOKUP=47 |

TMED_PIN_REQD=16 |  TMED_DONT_VAL_EXPDATE=48 |

TMED_HALO=17 |  TMED_TIP_MUST_EXCEED_TNDR=49 |

TMED_CHAIN_ORDR=17 |  TMED_SORT_MI_BY_SEAT=50 |

TMED_HALO_AMT_ENTRY=18 |  TMED_PRMPT_FOR_ISSUE_NUM=51 |

TMED_DO_NOT_FIRE_ORDR=18 |  TMED_SUSPEND_TRANS=51 |

TMED_EMPL_MEAL_TIP=19 |  TMED_PRMPT_FOR_START_DATE=52 |

TMED_REPRINT_CHK=19 |  TMED_PRMPT_FOR_OPT_LINE_PRNT=53 |

TMED_PRINT_SLS_ITMZRS=20 |  TMED_CREDIT_FINAL_AMT_REQD=54 |

TMED_PRINT_SUM_TTLS=21 |  TMED_ITEM_SHAREABLE=55 |

TMED_PRINT_TRAILER=22 |  TMED_OB_TIPS_PAID=56 |

TMED_PRINT_CHK=23 |  TMED_PRINT_FCR_CHECK=57 |

TMED_PRINT_VAT_STTL=24 |  TMED_POST_FCR_CREDIT=58 |

TMED_REQUIRE_EXP_DATE=25 |  TMED_PRINT_THAI_TAX_ACC_REC_LINE=59 |

TMED_ALLOW_USE_W_RECALL=26 |  TMED_PRINT_THAI_TAX_INVOICE_LINE=60 |

TMED_ALLOW_USE_W_CUR_CNV=27 |  TMED_ALLOW_WITH_EURO=61 |

TMED_PMS_POST_ZERO_TTL=28 |  TMED_SEND_ORDER=62 |

TMED_PMS_2_REF_LINES=29 |  TMED_OB_MASK_CC_NUMBER=63 |

TMED_PMS_19_REF_NUM=30 |  TMED_OB_MASK_CC_EXP=64 |

---

## Tndttl

<!-- src: System_Variable_Tndttl.htm -->

Tndttl

### Function
This system variable contains the total for this posting, which can be reduced.

**Type/Size**
$12

### Syntax
@TNDTTL

**Tndttl Usage**
- This system variable has Read-Write attributes.
- This system variable must be accessed within a tender/media event.
- The purpose of this system variable is to allow the total due on a check to be updated if neccessary. This system variable is best used in an environment where some form of credit limit is applied to purchases, such as in a student meal plan or a frequent diner program for hotel patrons. In a student meal plan, students may have a set amount of credit applied to each meal. For example, assume that each student meal credit limit is $4.50 per meal. If a student surpasses this amount with a purchase of $6.00, the @TNDTTL ($6.00) can be overwritten with the credit limit of $4.50. Then the student can cover the difference of $1.50.

**Tndttl Example**
In the example that follows, the tender total is reduced from $6.00 to $4.50, the allowable student meal credit.
event tmed : 1
txmsg "POST", @tndttl // send over $6.00
waitforrxmsg
endevent

event rxmsg: POST
var new_tnddtl : $10
rxmsg new_tnddtl // receive $4.50
if new_tnddtl > 0
@tndttl = new_tnddtl
exitcontinue
else
exitcancel // cancel
endevent

---

## Touchscreen

<!-- src: System_Variable_Touchscreen_Category.htm -->

Alphascreen
Center
Wcols
Wrows

---

## Trace

<!-- src: System_Variable_Trace.htm -->

Trace

### Function
This system variable must be set to a non-zero value in order to output each executed ISL statement to the 3700d.log file.

**Type/Size**
N5

### Syntax
@TRACE = integer

**Trace Usage**
- This system variable has Read-Write attributes.
- The primary usage of this feature is debugging.

---

## Trailer

<!-- src: System_Variable_Trailer.htm -->

Trailer

### Function
This system variable is used to print additional trailer information. This information can be printed in the trailer of customer receipts, guest checks, and credit card vouchers. It can include text, bar codes, estimated tip amounts, etc.
Note: The StartPrint command should not be used in a @trailer/@header event.

**Type/Size**
A32

### Syntax
@Trailer

**Trailer Usage**
- This system variable is read-write.
- The @trailer system variable is a string array, having 16 elements.
- The @Trailer[] array is unique to each event. This means that each event can begin writing to the array starting at index 1, rather than a the next available index.
- This variable is only used with the Print_trailer event. All transaction system variables are valid in this event. User input is allowed, as are file operations and display manipulation.

**Trailer Example**
The following SIM script will be called by the restaurant check trailer:

event print_trailer : chk_grat
.@trailer [1]=" Gratuity"
.@trailer [2]=" Included"
.@trailer [3]=" After 8 PM"

The trailer definition might look like this:

**line [1] ="THANK YOU FOR DINING WITH US
line [2] = "************************************************"
line [3] = "@@chk_grat "
line [4] = " "
line [5] = " "
line [6] = " "**
When the guest check prints, the system prints the first line, "THANK YOU FOR DINING WITH US", then the separating stars and then the last three SIM script lines. It will look something like this:

See also:

Header

---

## Trainingmode

<!-- src: System_Variable_Trainingmode.htm -->

Trainingmode

### Function
This system variable contains the Training Mode Status of an employee.

**Type/Size**
N3

### Syntax
@TRAININGMODE

**Trainingmode Usage**
- This system variable is Read-Only.
- The Training Mode Status will be either of the following settings:
Status Description
Zero indicates that the employee is not in training mode
Non-zero indicates that the employee is in training mode

---

## Transaction Detail

<!-- src: System_Variable_Transaction_Detail_Category.htm -->

Beverage_Reqd

Chk_Autofire_Time
Chk_Delayed_Order
Chk_Future_Order

Chk_Open_Time
Ckid
Cknum
Ckseqnum
COM_Active
CustomerInfo
CustomerInfoLine
CustomerSeq
Dtl_Autofire_Time
Dtl_Charge_Tip_Amount

Dtl_Charge_Tip_Name

Dtl_Famgrp
Dtl_Has_Charge_Tip
Dtl_Id
Dtl has Printed
Dtl_Is_Combo
Dtl_Is_Combo_Main
Dtl_Is_Combo_Parent
Dtl_Is_Combo_Side
Dtl is cond
Dtl_is_default_cond
Dtl_is_om
Dtl_is_om_base
Dtl_is_om_container
Dtl_is_om_section
Dtl_is_om_specialty
Dtl_is_om_topping
Dtl is on hold
Dtl_is_void
Dtl_Majgrp
Dtl_Mlvl
Dtl_Name
Dtl_Name_Two
Dtl_Object
Dtl_Plvl
Dtl_prefix
Dtl_Prep_Time
Dtl_PrtGstChk
Dtl_PrtRcpt
Dtl_Qty
Dtl_Seat
Dtl_Slvl
Dtl_Status
Dtl_Taxtype
Dtl_Ttl
Dtl_Type
Dtl_Typedef
Filter_active
Filter_mask
Grpnum
Gst
InEditClosedCheck
InReopenClosedCheck
Instandalonemode
Maxdtlr
Maxdtlt
MLVL
Numdtlr
Numdtlt
Numsi
Numtax
Ordertype Order_Type_Name
Parent_Dtl_Id
Prefix_Dtl_Name
Prevpay
ReturnStatus
Seat
SI
SLVL
Srvprd
Tax
Taxrate
Tblid
Tblnum
Tblobjnum
Tndttl
Trdtlr
Trdtlt
Ttldue
Txbl
VoidStatus
Workstation transaction number

---

## Trdtlr

<!-- src: System_Variable_Trdtlr.htm -->

Trdtlr

### Function
This system variable contains transaction detail posted to the current guest check during this service round.

**Type/Size**
Various (see Usage)

### Syntax
@Trdtlr

**Trdtlr Usage**
- This system variable is Read-Only.
- The transaction detail information is designed to provide enough detail, to display or print a basic guest check. If more information is required, it should be exported from the appropriate database files with the 3700 SQL module.
- The transaction detail will be preceded by a Number of Detail Entries field. This field is of the type and size N3, and indicates how many detail entries follow.
- When partial payments are posted to a PMS using prorated itemizers, all the detail on the guest check will be transferred, not just the detail associated with this partial payment. If selective detail is required, the guest check should be split at the POS prior to being posted to the PMS.

**Transaction Detail Table**

Field/Type and Size |  Description |

Detail Type/A1 |  Indicates type of detail entry: |

I = Check Information Detail |

M = Menu Item |

D = Discount |

S = Service Charge |

T = Tender/Media |

R = Reference Number |

Status/A8 |  Check Detail Status Flag |

Number/N7 |  Object number; set to 0 for reference numbers and check information detail. |

Quantity/N5 |  Quantity; set to 0 for reference numbers and check information detail. |

Main Sales Level/N1 |  Main sales level (between 1 and 4); set to 0 for reference numbers and check information detail. |

Sub Sales Level/N1 |  Sub sales level (between 1 and 4); set to 0 for reference numbers and check information detail. |

Total/$12 |  Total; set to 0 for reference numbers and check information detail. |

Name/A24 |  Contains the detail's name (menu item, discount, etc.). For reference numbers; this contains the actual reference number. |

See also:

Dtl_Mlvl

Dtl_Name

Dtl_Objnum

Dtl_Plvl

Dtl_Qty

Dtl_Seat

Dtl_Slvl

Dtl_Status

Maxdtlr

Trdtlt

---

## Trdtlt

<!-- src: System_Variable_Trdtlt.htm -->

Trdtlt

### Function
This system variable contains all the transaction detail from the current guest check.

**Type/Size**
Various (see Usage)

### Syntax
@Trdtlt

**Trdtlt Usage**
- This system variable is Read-Only.
- The transaction detail information is designed to provide enough detail to display or print a basic guest check. If more information is required, it should be exported from the appropriate database files with the 3700 SQL module.
- Each transaction detail entry comprises the fields described in the Transaction Detail Table under the System Variable.
- The transaction detail will be preceded by a Number of Detail Entries field. This field is of the type and size N3, and indicates how many detail entries follow.
- When partial payments are posted to a PMS using prorated itemizers, all the detail on the guest check will be transferred, not just the detail associated with this partial payment. If selective detail is required, the guest check should be split at the POS prior to being posted to the PMS.

See also:

Maxdtlt

Trdtlr

---

## Tremp

<!-- src: System_Variable_Tremp.htm -->

Tremp

### Function
This system variable contains the number of the Transaction Employee, who is the employee posting sales to the current guest check.

**Type/Size**
N9

### Syntax
@Tremp

**Tremp Usage**
- This system variable is Read-Only.
- Typically, the Transaction Employee is also the Check Employee, or the person who originally began the check. However, managers and cashiers may be privileged to be the Transaction Employee if they must post sales to another employee's check. Depending on the options enabled in the RVC Posting form, sales totals and tender totals will post to either the Check Employee or the Transaction Employee and to their corresponding Cashier Totals, if there is a link.

See also:

Ckemp

---

## Tremp_chkname

<!-- src: System_Variable_Tremp_chkname.htm -->

Tremp_chkname

### Function
This system variable contains the transaction employee’s check name.

**Type/Size**
A8

### Syntax
@TREMP_CHKNAME

**Tremp_chkname Usage**
This system variable is Read-Only.

---

## Tremp_fname

<!-- src: System_Variable_Tremp_fname.htm -->

Tremp_fname

### Function
This system variable contains the transaction employee’s first name.

**Type/Size**
A8

### Syntax
@TREMP_FNAME

**Tremp_fname Usage**
This system variable is Read-Only.

---

## Tremp_lname

<!-- src: System_Variable_Tremp_lname.htm -->

Tremp_lname

### Function
This system variable contains the transaction employee’s last name.

**Type/Size**
A16

### Syntax
@TREMP_LNAME

**Tremp_lname Usage**
This system variable is Read-Only.

---

## Ttldue

<!-- src: System_Variable_Ttldue.htm -->

Ttldue

### Function
This system variable contains the total due for the current guest check.

**Type/Size**
$12

### Syntax
@Ttldue

**Ttldue Usage**
This system variable is Read-Only.

---

## Txbl

<!-- src: System_Variable_Txbl.htm -->

Txbl

### Function
This system variable is an array containing the taxable sales itemizer on the current guest check.

**Type/Size**
$12

### Syntax
@Txbl[expression]

**Txbl Usage**
- This system variable is Read-Only.
- The array limits of the expression are from 1 to 8.

---

## Userentry

<!-- src: System_Variable_Userentry.htm -->

Userentry

### Function
This system variable contains the data entered by an operator prior to pressing the SIM Inquiry key.

**Type/Size**
A20

### Syntax
@Userentry

**Userentry Usage**
- This system variable is Read-Only.
- @Userentry will contain the data entered prior to pressing the SIM Inquiry key. For example, if an operator enters "123" then presses the SIM Inquiry key, @Userentry will contain "123".

---

## UWSSerialNum

<!-- src: System_Variable_UWSSerialNum.htm -->

UWSSerialNum

### Function
This variable allows SIM access to the next user workstation Thai tax serial number. In addition, an index is required (e.g., @uwsserialnum[1]) within the range of 1 to 2. Index 1 will return the next serial number 1 for the current workstation, and index 2 will return the next serial number for the current workstation.

**Type/Size**
N9

### Syntax
@uwsserialnum

**UWSSerialNum Usage**
This system variable is Read-Only.

---

## Vald

<!-- src: System_Variable_Vald.htm -->

Vald

### Function
This system variable contains the object number of the Validation Printer assigned to the UWS.

**Type/Size**
N7

### Syntax
@Vald

**Vald Usage**
- This system variable is Read-Only.
- This system variable can be used as an argument to the StartPrint[WithStatus] commands.

See also:

StartPrint[WithStatus]...EndPrint[FF/NOFF]

---

## Validate_Mag_Track

<!-- src: System_Variable_Validate_Mag_Track.htm -->

Validate_Mag_Track

### Function
This system variable allows users to swipe and read magnetic card data when installed as part of a SIM input command.

**Type/Size**
N1

### Syntax
@Validate_Mag_Track

Note
When a SIM event is executed, the variable defaults to a state of 1 (true), which validates track 2 data.
The variable may be set to 0 (false), which directs the script to bypass track 2 validation. This allows sites to read a magnetic identification card with blank track 2 data.

**Validate_Mag_Track_Example**

Event inq: 1
var account_num: a19
var track1_data: a79
var track2_data: a79
@validate_mag_track = 0 // disable track 2 validation
Window 1, 40
displayMSinput 1, 2, accountnum{m1, 1, 1, 19}, "Enter Account Number", 0, 0, track1_data{m1,*},""
windowinput
waitforclear
window 2, 40
display 1, 2, "Account Number", account_num
if@MAGSTATUS = "Y"
display 2, 2, "As read from credit card."
else
display 2, 2, "As entered from keyboard."
endif
waitforclear
EndEvent

---

## Varspace

<!-- src: System_Variable_Varspace.htm -->

Varspace

### Function
This system variable contains the total amount in bytes, of variable space available to the script.

**Type/Size**
N9

### Syntax
@VARSPACE

**Varspace Usage**
This system variable is Read-Only.

See also:

Varused

---

## Varused

<!-- src: System_Variable_Varused.htm -->

Varused

### Function
This system variable contains the number of bytes of variable space used by the script at the points where variables are referenced.

**Type/Size**
N9

### Syntax
@Varused

**Varused Usage**
This system variable is Read-Only.

---

## Version

<!-- src: System_Variable_Version.htm -->

Version

### Function
This system variable contains the version designation of the SIM.

**Type/Size**
N5

### Syntax
@Version

**Version Usage**
This system variable is Read-Only.

**Version Example**
The event below draws a window and displays the SIM version number.
event inq : 1
window 1, 30
display 1, @center, "The SIM Ver is: ", @version
endevent

---

## VoidStatus

<!-- src: System_Variable_VoidStatus.htm -->

VoidStatus

### Function
This system variable is used to determine the current void status of the transaction.

**Detail**
Variable: @VOIDSTATUS
Values: Y or N

### Argument/Description
This variable is required for the Diebold interface, which uses INQ events to apply discounts/service charges to a guest check.
When invoked, an INQ event has no internal mechanism for checking the current void status of OPS. Void status determines whether the discount/ service charge will be addded to or subtracted from the guest check. This variable provides that system check for the user, displays a message box, and prompts for confirmation prior to completing the transaction.

**VoidStatus Example**
Event Inq : 1
if (@VOIDSTATUS = "Y")
infoMessage "Test @VOIDSTATUS",
"OPS is in void or transaction void mode"
else
infoMessage "Test @VOIDSTATUS",
"OPS is not in void or transaction void mode"
endif
endevent // inq: 1

---

## Warnings_Are_Fatal

<!-- src: System_Variable_Warnings_Are_Fatal.htm -->

Warnings_Are_Fatal

### Function
This system variable interrupts script processing with a fatal error if variable overflow occurs.

**Type/Size**
N9

### Syntax
@Warnings_Are_Fatal

**Warnings_Are_Fatal Usage**
- This system variable has Read-Write attributes.
- By default, no error is reported when strings, reals, or integers overflow the variables to which they are assigned; the values are truncated to fit the variables. The @Warnings_Are_Fatal system variable can be set to handle the instance when the script writer wants the ISL to report a fatal error if a variable overflow occurs. If @Warnings_Are_Fatal is set equal to 1, variable overflow will cause a fatal error, thereby interrupting script processing.
- Specify @Warnings_Are_Fatal at the top of the script.

**Warnings_Are_Fatal Example**
@Warnings_Are_Fatal = 1
event tmed : 9
var room : a6
var guest_name : a20
window 4, 22, "Room Charge"

---

## Wcols

<!-- src: System_Variable_Wcols.htm -->

Wcols

### Function
This system variable contains the number of columns in the ISL-defined window currently displayed.

**Type/Size**
N9

### Syntax
@Wcols

**Wcols Usage**
This system variable is Read-Only.

---

## Weekday

<!-- src: System_Variable_Weekday.htm -->

Weekday

### Function
This system variable contains the day of the week.

**Type/Size**
N1

### Syntax
@Weekday

**Weekday Usage**
- This system variable is Read-Only.
- Valid values range from 0 - 6, where 0 is Sunday.

---

## Workstation transaction number

<!-- src: System_Variable_Workstation_transaction_number.htm -->

Workstation transaction number

### Function
Prints the Workstation Transaction Number on the guest check after it is tendered. The workstation transaction number increments following the completion of each transaction.

**Syntax:**
@trans_number

**Workstation transaction number Example:**
event tmed : 101
startprint @chk
printinline "Trans Number", @trans_number
endprint
endevent

---

## Wrows

<!-- src: System_Variable_Wrows.htm -->

Wrows

### Function
This system variable contains the number of rows in the ISL-defined window currently displayed.

**Type/Size**
N9

### Syntax
@Wrows

**Wrows Usage**
This system variable is Read-Only.

---

## Wsid

<!-- src: System_Variable_Wsid.htm -->

Wsid

### Function
This system variable contains the UWS ID number.

**Type/Size**
N9

### Syntax
@Wsid

**Wsid Usage**
This system variable is Read-Only.

---

## Wsname

<!-- src: System_Variable_Wsname.htm -->

Wsname

### Function
This system variable contains the name assigned to the UWS in the 3700 Devices form.

**Type/Size**
A16

### Syntax
@Ws_name

**Wsname Usage**
This system variable is Read-Only.

See also:

Wsid

---

## WSType

<!-- src: System_Variable_WSType.htm -->

WSType

### Function
This system variable supports a single version of a SIM script executing on all RES-supported OS Platforms (Win 32, PPC2000/2002, and CE.net).

**Type/Size**
N1

### Syntax
@WSType

**WSType Usage**
- This system variable is Read-Only.
- The workstation types are as follows:
1 = PCWS
2 = HHT
3 = WS4

**WSType Example**

The following example illustrates opening a file for read access on a PCWS, HHT, or WS4 Device:

\\ Win32 Device
if @WSType = 1
Tmed_def_filename = "…\etc\tmed_def.cfg"
\\ Hand-Held Device
elseif @WSType = 2
Tmed_def_filename = "…micros\etc\tmed_def.cfg"
\\ WS4 Device
elseif @WSType = 3
Tmed_def_filename = "…cf\micros\etc\tmed_def.cfg"
Endif

Fopen file_number, Tmed_def_filename, read

---

## Year

<!-- src: System_Variable_Year.htm -->

Year

### Function
This system variable contains the current year.

**Type/Size**
N2

### Syntax
@Year

**Year Usage**
This system variable is Read-Only.

**Year Example**

See the example for @Day

See also:

Day

Month

---

## Yearday

<!-- src: System_Variable_Yearday.htm -->

Yearday

### Function
This system variable contains the number representing the current day of the year.

**Type/Size**
N3

### Syntax
@Yearday

**Yearday Usage**
- This system variable is Read-Only.
- A valid value will be from 1 to 365.
