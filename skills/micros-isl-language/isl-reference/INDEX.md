# ISL Reference Index

Search: `grep -n -i '^## <name>' reference/*.md` to find an entry; `grep -n -i -A40 '^## <name>$' reference/<file>.md` to read it.

| File | Contents |
|---|---|
| guide/*.md | SIM Guide narrative (concepts, structure), one file per chapter, appendix and glossary |
| reference/commands.md | Language commands (syntax, args, examples) |
| reference/errors.md | Error messages |
| reference/events.md | Event types and triggers |
| reference/functions.md | Built-in functions |
| reference/keys.md | Key names and codes |
| reference/specifiers.md | Input/output format specifiers |
| reference/sysvars.md | System variables (@Name) |

## commands (101)

Beep, Break, Call, ClearArray, ClearChkID, ClearChkInfo, ClearIslTs, ClearKybdMacro, ClearRearArea, ContinueOnCancel, Debug, DiscardGlobalVar, Display, Display_Rear_Area, DisplayInput, DisplayInverse, DisplayIslTs, DisplayMSInput, DLLCall, DLLCall_CDECL, DLLFree, DLLLoad, EditDetail, ErrorBeep, ErrorMessage, Event...EndEvent, ExitCancel, ExitContinue, ExitOnCancel, ExitWithError, FClose, FOpen, For...EndFor, ForEver...EndFor, Format, FormatBuffer, FormatQ, FRead, FReadBfr, FReadLn, FSeek, FWrite, FWriteBfr, FWriteLn, GetEnterOrClear, GetRxMsg, If...Else[If]...EndIf, InfoMessage, Input, InputKey, Item Discount, LineFeed, ListDisplay, ListInput, ListPrint, LoadDbKybdMacro, LoadKybdMacro, LoadMAGInfo, LowerCase, MakeAscii, Mid, MSleep, PrintLine, Prompt, ProRate, RegIdleEvent, RetainGlobalVar, Return, RxMsg, SaveChkInfo, SaveRefInfo, SetIslTsKey, SetIslTsKeyx, SetSignOn[Left/Right], SetString, Split, SplitQ, StartPrint[WithStatus]...EndPrint[FF/NOFF], Sub... EndSub, System, Test_Dsvc, Touchscreen, TxMsg, UpperCase, Use[Compat/ISL]Format, Use[ISL/STD]TimeOuts, UseFilteredDetail, UseUnFilteredDetail, Var, VoidDetail, WaitForClear, WaitForConfirm, WaitForEnter, WaitForRxMsg, While...EndWhile, Window, Window[Edit/Input][WithSave], WindowClear, WindowClose, WindowScrollDown, WindowScrollUp

## errors (96)

Array Index Out of Range, Bad sys var index, Break with too many endfor, Break without endfor, Call has no arguments, Can not evaluate, Command outside procedure, Decimal overflow, Display column or row out of ran, Divide by zero, Duplicate variable def, Encountered non-hex data, Endsub nesting mismatch, Evaluation nesting, Event inside procedure, Event type must be word, Exceeded max array or variable size, expected ..., encountered..., Expected array in call, Expected decimal, Expected end of line, Expected format token, Expected operand, Expected string, Format needs string, Format too long, Integer overflow, Invalid decimal operation, Invalid first token, Invalid input fmt spec, Invalid list size, Invalid output format, Invalid pms send, Length invalid, List value too big, Loop variable constant, Loop variable not int, Max lines executed, Max macro keys, Max ref info, Max window input entries, Memory allocation, Must have list var, Name is a reserved word, New tndttl exceeds original, No arrays in sub var, No isl file, No match for endfor, No match for endwhile, No match for event, No number in sys var, No ops on strings, No pms message received, No touchscreen keys defined, Not a variable, Not enough input data, Not enough list data, Not enough variables, Numeric entry required, Print already started, Print not started, Reading ord dvc table, Reading tbl def, Require array for list, Script memory allocation error, Start position invalid, String overflow, Sub array ref invalid, Sub has no arguments, Sub statement in procedure, Sys var not assignable, System variable declaration, Too few args in call, Too few arguments, Too many args in call, Too many arguments, Too many nested calls, Too many touchscreens keys, Undefined call, Undefined function, Undisplayable variable, Unexpected data after call, Unexpected data after sub, Unexpected data is sub, Unexpected end of line, Unexpected token type, Unknown command, Unknown system variable, Unmatched endevent, Unmatched endfor, Unmatched if, Value not key definition, Variable undefined, Window columns out of range, Window has not been defined, Window rows out of range

## events (31)

Event Begin_Check, Event ClockIn, Event ClockOut, Event Dsc, Event Dsc_Error_Correct_Items, Event Dsc_Void, Event Dtl_Changed, Event Exit, Event Final_Tender, Event Idle_No_Trans, Event Init, Event Inq, Event mi, Event mi_error_correct_items, Event mi_return, Event mi_void_items, Event Pickup_Check, Event Pretender, Event Print_Header/Trailer, Event RxMsg, Event SignIn, Event SignOut, Event Srvc_Total, Event Svc, Event Svc_Error_Correct_Items, Event Svc_Void, Event Tmed, Event Tndr, Event Tndr_Error_Correct_Items, Event Tndr_Void, Event Trans_Cncl

## functions (28)

Abs, ArraySize, Asc, Bit, Chr, ClearChkID, ClearChkInfo, ClearRearArea, DisplayRearArea, DisplayTouchscreen, Env, Feof, FTell, GetHex, GetMaxDiscount, Instr, KDS Functions, Key Function, KeyNumber Function, KeyType Function, Len, MakeKeys Function, Mid Function, One_Time_Auto_Discounts, Remove Auto Discounts, ToInteger, Trim, VarSize

## sysvars (221)

Alphascreen, Autosvc, BackUpServerName, Beverage_Reqd, Bootserialnum, Bootserialstr, Cashier, Cashier_Name, CCAuth_Count, Ccdate, Ccnumber, Center, Chgtip, Chk, Chk_Autofire_Time, Chk_Delayed_Order, Chk_Future_Order, Chk_Open_Time, Ckemp, Ckemp_chkname, Ckemp_fname, Ckemp_lname, Ckemplopt, Ckid, Cknum, CkSeqNum, COM_Active, Commands by Category, CustomerInfo, CustomerInfoLine, CustomerSeq, Data Entry, Date and Time, Day, Dbmemlen, Dbmemsize, DepDscI, Discount/Service Charge, Dsc, DscI, DscIttl, Dtl_Autofire_Time, Dtl_Charge_Tip_Amount, Dtl_Charge_Tip_Name, Dtl_Dining_Course, DTL_DSC_ITTL, DTL_DSC_STTL, Dtl_Famgrp, Dtl_Has_Charge_Tip, Dtl_has_printed, Dtl_Id, dtl_is_auto_discount, Dtl_Is_Combo, Dtl_Is_Combo_Main, Dtl_Is_Combo_Parent, Dtl_Is_Combo_Side, Dtl_is_cond, dtl_is_coupon, Dtl_is_default_cond, Dtl_is_om, Dtl_is_om_base, Dtl_is_om_container, Dtl_is_om_section, Dtl_is_om_specialty, Dtl_is_om_topping, Dtl_is_on_hold, Dtl_is_void, Dtl_Majgrp, Dtl_MajGrp_ObjNum and DTL_FamGrp_ObjNum, Dtl_Mlvl, Dtl_Name, Dtl_name_two, Dtl_Object, Dtl_Objnum, Dtl_Ord_Dev_Output, Dtl_Plvl, Dtl_prefix, Dtl_Prep_Time, Dtl_PrtGstChk, Dtl_PrtRcpt, Dtl_Qty, Dtl_Seat, Dtl_Selected, Dtl_Sequence, Dtl_Slvl, Dtl_Status, Dtl_Taxtype, Dtl_Ttl, Dtl_Type, Dtl_Typedef, Dwoff, Dwon, Emplopt, Employee, Fieldstatus, File I/O, File_Bfrsize, File_Errno, File_Errstr, File_Separator, Filter_active, Filter_mask, Function Keys, Groupseqnum, Grpnum, Gst, Gstrmng, Gstthistender, Guestseqnum, Hour, Idle_Seconds, InBackupMode, InEditClosedCheck, Inputstatus, InReopenClosedCheck, Instandalonemode, Jnl, Key_Cancel, Key_Clear, Key_Down_Arrow, Key_End, Key_Enter, Key_Exit, Key_Home, Key_Left_Arrow, Key_Page_Down, Key_Page_Up, Key_Right_Arrow, Key_Up_Arrow, Lastauthemp, Lastauthemp_fname, Lastauthemp_lname, Line, Line_Executed, Magstatus, Max_Lines_To_Run, Maxdtlr, Maxdtlt, Minute, MLVL, Month, Numdsc, Numdtlr, Numdtlt, Numsi, Numsvc, Numtax, Order_Type_Name, Ordertype, Ordr, Parent_Dtl_Id, Platform, PMSBuffer, PMSNumber, PMSSeqNum, Prefix_Dtl_Name, Prevpay, Printing, Printstatus, Rcpt, Redoff, Redon, ReturnStatus, RVC, RVCName, RxMsg, Script, Seat, Second, ServerName, Show_PMS_Messages, SI, SLVL, Srvprd, Strict_Args, SustainCustomText, Svc, SvcI, SvcIttl, System, Tax, Taxrate, Tblid, Tblnum, TblObjNum, Tender/Media, Test_Dsvc_Ttl, Tmdnum, Tmdtypedef, Tndttl, Touchscreen, Trace, Trailer, Trainingmode, Transaction Detail, Trdtlr, Trdtlt, Tremp, Tremp_chkname, Tremp_fname, Tremp_lname, Ttldue, Txbl, Userentry, UWSSerialNum, Vald, Validate_Mag_Track, Varspace, Varused, Version, VoidStatus, Warnings_Are_Fatal, Wcols, Weekday, Workstation transaction number, Wrows, Wsid, Wsname, WSType, Year, Yearday

## specifiers (19)

(-) Specifier, (Mn, field, start, count | *) Specifier, (Mn,*) Specifier, Binary, Decimal, Equality (=), format_string, Hexadecimal (X), Input Specifiers, Leading/Trailing Spaces(*), Left Justification (<), Octal (O), Output Specifiers, Plus, Quotes ("), Right Justification, Size, Space (^), Zero (0)

## keys (13)

Check Begin & Pickup Keys, Check Operations Keys, Course Keys, Function Keys, Key Types, Manager Keys, Movement Keys, NLU Keys, Non-Sales Keys, Numeric Keys, Seat Keys, Touchscreen/Keyboard Keys, Transaction Keys
