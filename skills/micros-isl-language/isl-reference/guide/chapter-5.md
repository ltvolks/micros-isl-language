# Chapter 5: ISL Printing

Getting Started with ISL Printing Printing in ISL is accomplished using the StartPrint, PrintLine, and EndPrint directives (or their variants). The following printing options are supported:

o Printing can be supervised or unsupervised o Backup printers may be specified o Printouts can end with Form Feeds or not o Printing text in double-wide characters and red ink is also supported

This chapter focuses on how to start print jobs and direct your print jobs to System printers. And in performing these tasks, the other options available to you are covered as well, including detecting the status of print jobs, redirecting print jobs to ISL- defined backup printers, and defining a reference line for print error messages.

ISL Print Commands and System Variables All of the commands and system variables associated with ISL printing are discussed. Complete descriptions, including syntax and examples, of all commands discussed in this section are provided in the SIM Online Help. For more information about system variables and their use, refer to Chapter 6, “System Variables”.

## Starting an ISL Print Job

### ISL StartPrint Commands

Both supervised and unsupervised printing supported by the ISL are consistent in behavior with the 3700 System. Supervised print jobs include guest checks, customer receipts, and validation chits, while both local backup and remote order printing, as well as journal printing are considered unsupervised print jobs.

- These types of print jobs are initiated by variations of the StartPrint command described in this section. These variations are designed to accommodate:
- The type of print job (supervised or unsupervised) and
- The ability to detect whether a print job completed successfully by using the @PRINTSTATUS system variable.

Printing in ISL is started using one of the commands in the table below. The StartPrint and StartPrintWithStatus commands are used to print to a standard MICROS printer. These printers will print a maximum of 32 characters per line, and understand special formatting.

```text
                                                              Sets        Form   Backup    Reference
Command                   Supervised     Unsupervised      @Printstatus   Feed   Printer   Line
StartPrint…                              ®                 ®a             ®      ®         ®
StartPrintWithStatus…     ®                                ®b             ®                ®
a.Always set to “Y”.
b.Set to either “Y”, for Yes (Complete), or “N” for “No” (Failed).
```

Supervised and Unsupervised Printing The StartPrint[WithStatus command should be used for supervised print jobs only, such as guest checks and customer receipts. When this command is used, the system will wait until the print job is completed before continuing with the script. Then, the completion status of the print job will be stored in the system variable @PRINTSTATUS. If the print job fails, the script can be designed to check @PRINTSTATUS and reroute the print job to another printer.

On the other hand, the StartPrint command is defined for unsupervised print jobs only, like journal printing. After executing the StartPrint command, for example, the system would immediately return to processing the script, and let the print job execute in the background. The system variable @PRINTSTATUS always returns successful results for these commands.

Form Feeds To force continuous paper to the beginning of a new line, the StartPrint commands can be issued with a Form Feed (FF) command. To turn off the Form Feed feature, a No Form Feed (NOFF) command is provided.

Backup Printing and Reference Lines The commands used for unsupervised print jobs also allow for the specification of a backup printer in case the print job fails. This backup printer overrides any backup printer already programmed in the database for the specified printer.

In addition, you can also specify text, called a reference line, to appear in printer error messages returned when both supervised and unsupervised print jobs fail.

### Specifying an ISL Printer

When specifying a StartPrint command, you have two options for defining a printer: an object number or a system variable.

Using Object Numbers All printing requires that a printer be specified by the StartPrint[WithStatus] commands. A printer can be identified either by its device table entry number (Object Number), a system variable, or a user-defined integer variable. For example, if the print job goes to device 8 in the Device Table, using the object number, the StartPrint command would be written as follows:

```isl
StartPrint 8
```

Although using this method is valid, it has a primary disadvantage. For instance, the destination printer for ISL print jobs may differ for each UWS. Thus, each script would need to specify the printer to which each UWS must print, limiting the flexibility of the script.

Considerations

- Although it is legal to specify a printer object number of 0, all print jobs printing to 0 will not print—anywhere.
- An invalid object number value (-1) will generate an ISL error.

Using System Variables A more efficient method of specifying printers is through the use of system variables. These system variables return the value of the object number of the printer. For example, the @CHK system variable will return the object number of the printer defined as the Check Printer for that UWS in the database. Since each UWS will have a different entry for its Check Printer, the ISL command “startprint @chk” will specify a different printer for each UWS. For example, on UWS #1, @CHK is 8 but, on UWS #2, @CHK is 12. Using a system variable instead of the object number to specify a printer, means that each UWS can use the same script, yet still print to different printers. Another advantage of using the system variable is that the database backup printer is used. Please refer to “Backup Printing” on page 5-11.

ISL Printer System Variables The printer system variables available in ISL include the following:

| System Variable | Description |
| --- | --- |
| @CHK | Guest Check Printer |
| @RCPT | Customer Receipt Printer |
| @JNL | Journal Printer |
| @ORDR[1…15] | Remote Order or Local Backup Printer |
| @VALD | Validation Printer |

A table describing all options available with each valid ISL printer is provided with the detail description of the StartPrint[WithStatus] command. See StartPrint[WithStatus]...EndPrint[FF/NOFF] commands in the SIM Online Help.

## Detecting the Status of Print Jobs

StartPrint commands with [WithStatus] allow you to determine if a supervised print job has completed successfully. The WithStatus command returns a flag via the @PRINTSTATUS system variable: “Y” means the print job completed successfully, “N” means the print job failed.

Note       This feature is not supported for unsupervised print jobs (order and journal printing). In the case of unsupervised print jobs, its print status is always set to “Y,” regardless of how the print job is completed.

The PrintStatus System Variable Basically, the way in which the status can be returned is a function of how each command operates. When using the StartPrint…EndPrint command, the script will immediately continue executing after the EndPrint command. That is, printing occurs at the same time the script is being executed, so these commands do not allow for the print status to be set.

However, when EndPrint is used with a WithStatus command, SIM will wait for the print job to completely generate before returning control to the script. Because SIM knows whether or not the print job completed successfully, the @PRINTSTATUS can be set to “Y” or “N”.

For example, you may want to abort a supervised print job if the printer runs out of paper or has a paper jam while generating a validation chit. In either of these instances of printer failure, the @PRINTSTATUS returned by the StartPrintWithStatus command would be “N”. With this status, the script could redirect the print job to another printer, or prompt the operator to fix the problem (e.g., check the printer), based on the print status.

## Using Print Directives

### The Printline Command

The ISL Print Directives consist of one-byte values sent to the printer, defined by the StartPrint command, to change the print type of the expression that follows it. These directives are similar in function to standard parallel printer escape sequences: Each print directive is a non-printable character and is included in the print data sent to the printer.

Print Directives are actually system variables, and are arguments of the Printline command. This command allows the ISL to print information provided as a text string or variable.

The Printline command prints a line on the selected printer defined by the StartPrint command, which must be issued before Printline. Depending on the print directives specified in the Printline statement, the expression will print in double-wide characters or red ink.

### Print Type System Variables

Several system variables that evaluate to these print directives are provided by the ISL to facilitate printing expressions in double-wide characters and in red ink. These directives are described in the table that follows.

| Print Directive | Description |
| --- | --- |
| @DWON | Prints the following text or variable fields double-wide. Single- and double-wide characters may be mixed on the same line. |
| @DWOFF | Returns printing to single-wide (the default). New lines always print single-wide. |
| @REDON | Prints the expression that follows it in red ink. Characters in red and black ink can print on the same line. |
| @REDOFF | Returns printing to default ink (blue, black, etc.) All new lines default to black. |

Considerations

- Print directives (@DWON and @DWOFF) may be inserted between expressions, but only affect the expression to the right.
- The print directives are reinitialized at the end of each printed line.
- If no print directives are specified, then printing will be in black and single-wide.

Example The following example illustrates how the same expression can be printed in four different ways by using a combination of these print directives:

```isl
Printline "Print line"//prints in black

Printline @redon, "Print line"//prints in red

Printline @dwon, "Print line"//prints in black,

// double-wide

Printline @dwon, @redon, "Print line"//prints double- wide // in red ink
```

### Print Directives and Subroutines

Since the print directives are normal ISL strings, they can be passed as arguments to subroutines.
The following example prints an array of data and displays a header using a print directive passed in as a parameter to the subroutine:

```isl
sub print_list( var printer : N9, var listsize : N5, ref list[], ref header_string, var directive : A1 )
  if printer = 0
    errormessage "Printer is 0. Cannot print."
    exitcancel
  endif

  startprint printer
    printline "----------------------------"
    printline directive, header_string
    printline "----------------------------"
    listprint listsize, list
  endprint
endsub
```

Our subroutine could be invoked in the following fashion:

```isl
event inq : 1
   .
   .
   .
   print_list( @chk, sz, data[], “NORMAL
      HEADER”,@redoff
   .
   .
   .
   print_list( @rcpt, sz, data[], “RED HEADER”, @redon)
```

endevent

## Backup Printing

Backup printing is supported for unsupervised print jobs only. That is, whenever the StartPrint command is issued, an unsupervised print job will occur. If the print job is unable to complete successfully, it will go to the backup printer defined in the 3700 for each printer type (i.e., @chk, @rcpt, ...).

However, there are instances when a backup printer different from the one defined in the 3700 should be specified. To accommodate these instances, the StartPrint command accepts an optional second argument. This optional argument specifies the object number of the backup printer, overriding the backup printer programmed in the 3700 database.

For example, if the Check Printer is normally backed up by the Customer Receipt Printer but the script requires that a print job to the Check Printer back up to the Journal Printer, the following command should be issued:

STARTPRINT @chk, @jnl// back up to @jnl instead of @rcpt

Considerations

- All supervised print jobs (StartPrintWithStatus) do not have a backup, and therefore, do not accept a backup argument.
- SIM will only route the print job to the backup printer defined in the 3700 Database if the primary printer specified is a system variable. Otherwise, the ISL does not know to which printer type the job should be re-routed. For example, assume that the @CHK system variable equals 2.

- STARTPRINT @chk// ISL can determine backup printer STARTPRINT 2// ISL cannot determine backup printer In the first line, SIM will correctly determine the backup for the Check Printer, since “@chk” is explicitly specified. In the second line, the number 2 is used instead, and ISL cannot correctly determine the backup printer, and so, no backup is used.
- All unsupervised print jobs in the 3700 system can only accept up to 4096 characters of print data. Any print jobs with more than 4096 characters will generate an error. If a script must perform a print job greater than 4096 characters, it should use supervised print, and perform its own backup printing by using the @PRINTSTATUS system variable.

## Reference Strings

Whenever the SIM is performing a print job and an error occurs during printing (paper out, door open), an error message will appear on the display of the UWS explaining the error. Included in this error message is a line of text identifying the print job.

Normally, ISL will leave this line blank. However, this reference line can be specified in both the StartPrint and StartPrintWithStatus commands.

```isl
STARTPRINT @chk   // use default backup STARTPRINT @chk, @rcpt // no reference line

STARTPRINT @chk, @rcpt, "Printing Customer Coupon" //ref line

STARTPRINTWITHSTATUS @chk   // no reference line STARTPRINTWITHSTATUS @chk, "Printing Customer Coupon" //ref line
```
