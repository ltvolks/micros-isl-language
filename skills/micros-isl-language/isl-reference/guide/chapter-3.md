# Chapter 3: Writing Scripts

This section introduces you to the process of script writing.

If you are familiar with this process, this section provides the specific conventions and formats you need to know in order to write scripts with the ISL. And if you are new to script writing, this section includes the information you need to begin using scripts for the first time.

Specifically, this chapter covers:
- What a script is
- Why you use scripts
- What the parts of a script are
- How to write a script
- What is proper script writing style
- How to test a script
- How to document your script for others
- How to encrypt your scripts

## What is a Script?

The means by which the ISL issues instructions to the SIM is through small programs known as scripts. A script is an ASCII text file that you create in any common ASCII text editor, such as Edit, the Notepad Windows editor. These scripts can contain one or more events to implement SIM applications.

### Structure of a Script

A separate script must be maintained for each SIM Interface defined for a System. The script is linked to a SIM Interface through 3700 database programming. Once you form this relationship through database programming, the script can be executed by the SIM. For specific programming requirements, refer to “Programming the 3700 System for SIM” on page 2-9.

The basic structure of your scripts should be written in a format similar to the sample script below. When writing your script, keep the following structure in mind. A brief description of each part follows the diagram.

Comments
Comments are used to document the purpose and scope of events included in the script. Place comments anywhere in the script, but make sure each comment line is preceded by two backslash characters “//” (see page 3-9).

Global Variable Declarations
Global variables are initialized at the beginning of each script and maintained for the duration of the script.

Event Declaration
ISL is event-oriented. Almost all ISL statements will be contained in events or subroutines called by those events (see Event...EndEvent Command in the SIM Online Help.

There are several types of events:
- Event inq - this event is executed when a SIM inquiry key is presssed. This key must be programmed in the 3700 database.
- Event tmed - this event is executed when a SIM tender key is pressed. This key must be programmed in the 3700 database.
- Event rxmsg - this event is executed when a response is received from the third- party system interfaced to the 3700 System.
- Event final_tender - this event is executed whenever the last tender event has occurred, but before a check has closed.
- Event print_header - this event will print additional header or trailer information on custom receipts, guest checks, and credit card vouchers.
- Event print trailer - this event will print additional trailer information on custom receipts, guest checks, and credit card vouchers.
- Event srvc_total - this event is executed when a check is service totalled.
- Event trans_cncl - this event is executed when a SIM transaction cancel key is pressed.
- Event init - this event is executed when POS operations is started. This event should be used to perform any initialization required by the script. No user input is allowed in this event.
- Event exit - this event executes when POS operations is exiting. No user input is allowed in this event.
- Event idle_no_trans - this event is used to run SIM scripts in the background, when POS operations is idle and no one is signed in. If an employee should sign in, this event won’t be called until the employee signs out again. The frequency at which the SIM script is called is determined by the @Idle_Seconds system variable.

Local Variable Declaration Commands
Local variables are purged after each event completes execution; the event terminates after an EndEvent, ExitCancel, ExitContinue, or any other command that causes the event to stop executing, successfully or not.

Subroutine Declaration
Subroutine procedures are called from other event or subroutine procedures, allowing common code to be used by multiple events. As a script writing convention, we recommend that you place all subroutines after all events in the script. See Sub..Endsub Command in the SIM Online Help.

## Creating Scripts

Scripts consist of one or more events. Each event within the script represents a task that you want the SIM to perform. For instance, in Chapter One we discuss several different types of SIM applications. Each of these applications can exist as separate events within the same script.

### Guidelines for Creating Scripts

When you begin to develop your SIM applications, use the guidelines below to create the script.

- Understand the tasks that you want your script to perform.
- Outline the structure of the script. In plain English, write down the steps you
       want to automate in each event. Carefully note each detail about the tasks that
       the event will accomplish.
- Write a brief description of the task each event or subroutine performs. For
       future reference, this description should appear as a comment before each
       event and subroutine in the script.
- Note any input and output. Does the user enter data? Do you need to generate
       a guest check, remote order chit, etc.?
- Think about what assumptions your making about the environment. For
       instance, if the application applies a discount to a check total greater than or
       equal to $50.00, you should test for this case in the script before applying the
       discount.
- Protect yourself against the user. The event should not allow users to get stuck
            or to perform a task that they should not. For example, if you request input
            from an operator and the operator gives you incorrect input, then you should
            issue an error to force the operator to enter the requested information.
- Determine what variables (global, local) you need to declare. For a discussion of
  user variables, refer to “User Variables” on page 4-10.
- Determine whether some of the events in the script perform similar tasks. If they
  do, you should consider creating a subroutine to save time in writing the script and
  to make the script process instructions more efficiently.

### Examples of Scripts

- Translate the instructions you write into one or more lines of code.
- Consult the ISL Quick Reference in the SIM Online Help to determine what commands, functions, and system variables allow you to perform the desired task.
- Learn what considerations are involved in writing ISL statements. “Script Writing Style” on page 3-9 covers these guidelines.
- Review the detail descriptions of the required language elements. The examples provided with detail descriptions can be helpful as templates from which you can build your own ISL statements.

#### Charge Posting

This script posts a charge to a PMS system and waits for the response.

```isl
var guest_id:a20

event tmed : 1                                 //PMS room charge key is
  // Tender key #1
  input guest_id, "Guest posting, enter name or room #"
  txmsg "CHG_POSTING", guest_id, @TNDTTL, @CHKNUM,@RVC
  waitforrxmsg
endevent

event rxmsg : chg_posting
  var status : a1
  var message : a20,
  var temp_tndttl : $12

  rxmsg status, message

  if status="P"                                          //Posting approved
    saverefinfo message

    exitcontinue
  endif

  if status = "E"                                         //Error
    exitwitherror message
  endif
endevent
```

#### Charge Denial

This script places a window with the title “Charge Denied” on the screen, and provides text in it with the reason why the charge was denied. The operator is then prompted to press the [Clear] key before cancelling the operation.

```isl
event rxmsg : denial_msg
  var reason_text : a32
  rxmsg reason_text
  window 3, 34, "Charge Denied"
  display 2,@CENTER, reason_text
  waitforclear
  exitcancel
endevent
```

#### Address and Phone Number Entry

This example prompts the operator to enter a customer’s address and phone number.

```isl
var phone_num : N7                                 //Global variable, keep phone
// number around.
event inq : 1                                      //Use Inquiry key #1 to get guest info.
  var cust_name : A32
  var addr1 : A32
  var addr2 : A32
  var addr3 : A32
  var special_instructions : A32

  window 7, 50, "Customer Info"
  display 2,2, "Phone Number:"
  displayinput 2, 18, phone_num{:###-####}, "Enter phone number"
  display 3,2, "Customer name:"
  displayinput 3,18,cust_name, "Enter customer's name"
  display 4,2, "Address Line 1:"
  displayinput 4,18,addr1, "Enter address"
  display 5,2, "Address Line 2:"
  displayinput 5,18,addr2, "Enter address"
  display 6,2, "Address Line 3:"
  displayinput 6,18,addr3, "Enter address"
  display 7,2, "Instructions:"
  displayinput 7,18,special_instructions, "Enter instructions"
  windowinput

  // send information to a third party system
  txmsg phone_num, cust_name, addr1, addr2, addr3, special_instructions

  waitforrxmsg
endevent
```

## Script Writing Style

Before you begin writing your first script, review the style conventions in this section.
            For readability, you should apply these conventions in your script writing.

### Case

ISL statements are case-insensitive and the use of case in examples is purely for clarity and the author’s choice of style. However, quoted strings are case-sensitive.

### Length of Variables

The maximum character length for all variable names (user variables, subroutines, etc.) is 255.

```text
Comments (//)
```

Declarations and commands will always be on their own line and should be the first non-white space characters. A comment may be placed on a line by beginning the comment with “//” characters. All characters to the right of the comment identifier “// ” are ignored. For example:

```isl
Window 2,19, "ROOM INQUIRY"//Create window //Prompt for room number
```

```isl
Display 2,2,          "Enter Room Number"
```

A comment may reside on its own line or to the right of a command and its arguments. Lines should be terminated with an ASCII carriage return, or an ASCII linefeed, or a carriage return/line feed pair.

### Continuation Lines (`\`)

A line continuation character “\” is provided to allow commands to continue from one line to the next. For example, a command that overflows several lines might be: TxMsg field1, field2, field3, field4, \ field5, field6, field7, field8, field9

It is not possible to break apart a string with a line continuation character:

```text
Correct:
    errormessage “Choose a number between 1 ”,\
                 “and 10”
Incorrect:
    errormessage “Choose a number between 1\
                 and 10”
```

Line continuation characters may not be followed by comments or any other commands.

### Whitespace

Whitespace in ISL is defined as spaces or tab characters inserted into a program to either separate commands from their arguments or to improve program readability. For example, the programmer might find it easier to write: numrow = ( ( ( num_guest - 1 ) * 2 ) + header )

instead of: numrow=(((num_guest-1)*2)+header)

Whitespace can be placed anywhere in a script between two distinct language elements. Language elements are: commands, functions, system variables, user- defined variables, input/output specifiers, comments (//), relational and boolean operators, and commas. A language element is an indivisible piece of information which, if broken apart with whitespace, will generate an ISL token error. For a complete listing of error messages, please see SIM Online Help.

For example, the number -125.99 cannot be written as -125. 9 9. The command WaitForClear cannot be written as Wait For Clear.

The table below shows examples of the incorrect use of whitespace. This incorrect usage will produce error messages.

```text
                             Incorrect Use of                Correct Use of
ISL Language
                               Whitespace                     Whitespace
Within a variable name     num        _   columns = 1       num_columns = 1
Within a numeric value     - 19 8.         45                -198.45
Within a command           A     12                         A12
format specifier           N     5                          N5
                           $     12                         $12
Within a comment           /      / comment...              // comment...
delimiter
Within double-character    a <   > b                        a<>b
relational operators       count <          = 5             count     <=   5
Between the @ and a        @     TNDTTL                     @TNDTTL
System Variable name       @     YEAR                       @YEAR
```

The following table shows examples of where whitespace increases program readability:

| No Whitespace | With Whitespace |
| --- | --- |
| var count[10]:N5 | var count[ 10 ] : N5 |
| display 1,2,"Room is ",room | display 1, 2, "Room is ", room |
| txmsg "CHG",guest,@tndttl+1.00 | txmsg "CHG", guest, @tndttl + 1.00 |

## Writing and Editing Scripts

### Storing the Script

Your scripts should be composed in an ASCII text file and saved with a the filename pmsxxx.isl.

Note          There is no need to compile the script or to process it in any other way before the SIM can read it.

In order for SIM to access the script, you must make sure the script has been assigned the filename pms###.isl and stored in the \micros\res\pos\etc directory. The # must match the interface object number in the 3700 database.

### If You Edit the Script…

Also keep in mind that if you edit the script, you must save it as an ASCII text file.

### Avoiding Errors

- To avoid errors when writing and editing scripts, follow these basic guidelines:
- Make sure the script has been assigned the filename pms###.isl and stored in the \micros\res\pos\etc directory.
- Check your 3700 database programming.
- Review the structure of the script.

- Are all global variables declared at the beginning of the script?

- Within each event, have you declared all local variables before issuing the first command?

- Are the subroutines that you call in events also within the same script? Does the called subroutine have the same name as the actual subroutine?

- Look at your programming style. See “Script Writing Style” on page 3-9.

- Check that events correspond to the correct SIM Inquiry or SIM Tender keys initiating the event or tender event, respectively. For further details about creating these keys, refer to “Programming the 3700 System for SIM” on page 2-9

- Check the script for syntax errors. For instance, make sure that if a command has a corresponding command ending the task, include it. For example, the Event command must be used with the EndEvent command, which should always be the last line of an event procedure.

## Testing Scripts

### Detecting Errors in Logic

Before you use the SIM application in a live environment, we recommend that you test it for errors.

When you run the script, any errors in syntax are detected by the SIM, and an ISL error message is displayed. However, some errors in logic may not be caught by running the script.

Scripts make no assumptions, and execute your instructions exactly as you have specified them. So it is possible for you to run a script and detect no syntax errors, but still have problems with the logic. This is why we recommend that you step through each task in your script.

### Stepping Through the Script

- Follow these steps to test your script:
- Print the script for reference.
- Mark through each step of the script as you test and correct it. This procedure helps you to track the steps that you test.
- Execute each event in the script. Remember, there are several events: SIM Inquiry key, SIM Tender key, Final Tender, Message response, Header/Trailer.

- Make sure that the SIM Inquiry or SIM Tender key you press executes the correct event. The key should be linked to a corresponding event in the script.

- Test whether communications are active between the two systems and that each system responds appropriately to messages sent to it by the other.

- Make sure you have entered your header/trailer information in the Sales|Descriptors form.
- Test each step of the event, such as the flow and logic of If…EndIf and For loop statements.

- Check any assumptions you make in the script. For instance, if a condition must exist in order for the next step to occur, check the condition. You might need to display an error message or perform another step until this condition is met.

- Check the logic of each task. For example, if the script collects data from the user before querying a third-party database, you should make sure that the script prompts the user for data entry before starting the query.

- Correct any detected syntax errors. The ISL error message will provide the number of the line in the script where the error is found.

- Verify inputs and outputs. For example, if the script calls for a coupon to be generated when an operator closes a guest check, test for this case.

- Insure that the script handles all error conditions and presents a meaningful error to the user.

## Encrypting Scripts

### Encryption Program Files

Once you’ve created a script, you can use the ISL Encryption Program to code the script so that it is unreadable by anyone. This program converts the script into an encoded decimal format. Once encrypted, the script cannot be converted back to a readable format.

You’ll find instructions in this section that describe how to install the Encryption Program and how to use the Encryption Program in both interactive or command line modes.

The following files are related to the encryption process:

| File | Description |
| --- | --- |
| ISLCRYPT.EXE | The executable program that encrypts an ISL script |
| ISLCRYPT.DOC | A README.DOC file containing summary information on using the encryption program |

### Installing ISLCRYPT.EXE

- Complete the following steps to install the encryption program.
- Create a new directory called isl. For example:

`c:\>md isl`

- Copy ISLCRYPT.EXE from the distribution diskette to c:\isl. For example:

`c:\>copy a:\islcrypt.exe c:\isl`

### Command Syntax

[path]islcrypt [[path]/input_file] [path]/output_file \ [ “user_description” ] ]

```text
Parameter                                    Description
islcrypt                   The utility file name
input_file                 The ISL script file name you wish to encrypt
output_file                The encrypted ISL script file name
“user_description”         the user-defined text embedded in the file for
                           identification
Guidelines
    o Both the program and script may be located in any directory. See the following
      example:
              File                                       Location
islcrypt.exe                       c:\isl
script file                        c:\3700\etc\pms1.isl
```

- The output_file and user_description are optional. The output_file name is required when using the user_description.
- The user_description must be enclosed in quotes (for example, “PMS Interface Script”). The number of characters is limited to the DOS Command Line maximum. If no user_description is given, “Micros Encrypted ISL Script File” will be embedded in the file.
- It is recommended that the output_file always be specified. If the output_file is not specified, the input_file will become the encrypted file. It is also recommended to enter a user_description, since once the file is encrypted, the file cannot be read by standard editing programs and the user_description will be the only way of identifying the script.
- In order to access both the encryption program and the script, you must specify the full directory path name. If the full path name is not given, an error message will occur. All errors are listed in “Error Messages” on page 3-20

### Using the Encryption Program

The Utility is run from the DOS command line or through interactive system prompts.

Before You Begin Prior to using the Encryption Program, perform the following precautionary steps:

o Make a backup of the original script. Note the name of the original file, and of its backup.

Warning!         Once the script has been encrypted, there is no way to reverse the procedure.

- Verify that the backup script exists.
- Change to the directory holding the file to be encrypted.

Encrypting a Script in Command Line Mode This procedure allows you to encrypt a script by entering the command syntax at a DOS prompt.

To encrypt a script in command line mode complete the following steps:

1. Take the precautionary steps in "Before You Begin." 2. Enter the command syntax at the prompt. For example:

c:\isl\islcrypt script.isl script.xsl “PMS Interface Script” Encrypting a Script in Interactive Mode An alternative to command line mode is encrypting a script using the interactive mode. In this mode, the user is prompted to enter the command syntax by the Encryption Program.

To encrypt a script in interactive mode complete the following steps:

1. Take the precautionary steps in “Before You Begin” on page 3-19.

2. Change to the directory where ISLCRYPT.EXE is stored. For example:

`c:\>cd isl`

### Error Messages

3. Enter islcrypt at the prompt. The encryption program will prompt ‘Input filename?’

4. Enter the full directory path of the input_file. The Encryption Program will prompt ‘Output filename?’

5. Enter the full directory path of the output_file. The Encryption Program will prompt ‘File description?’

6. Enter a unique description of the output_file within quotes.

Viewing an Encrypted Script To view the description of an encrypted script complete the following steps:

1. Change to the directory where the encrypted script is stored.

2. Enter type pms1.isl at the prompt. The encrypted script will be displayed in the following format: ‘!!!PMS Interface Script’.

The following are possible error messages associated with the encryption process:

```text
Message                       Description                           Action
islcrypt: not found        This error message indicates        Check the directory path. Then
                           that the Encryption Program         re-enter the command syntax
                           cannot be found because the         with the correct full directory
                           full directory path was not         path.
                           specified, or incorrectly
                           specified, in the command
                           syntax.
Error: Cannot Access       This error message indicates        Check the directory path and
file ‘[path]/input_file’   that the input_file does not        the source directory for the
                           exist, or the full directory path   input_file. Then, re-enter the
                           for the input_file was not          command syntax with the
                           specified, or incorrectly           correct full directory path.
                           specified, in the command
                           syntax.
```

## Merging Scripts

We provide a utility that allows you to merge unencrypted scripts with encrypted scripts. The purpose of the ISL Merge Program is to allow you to distribute an unencrypted configuration file with an encrypeted script.

Configuration files, also scripts, provide the script designer with flexibility when distributing the same encrypted script to multiple sites. For example, some variable information in the script may vary from site to site, such as the name of a restaurant, address, or telephone number.

To make these changes, a user can change the unencrypted configuration file, then merge the configuration file with an encrypted script. The end result forms a complete encrypted output file, which is unique to the specifie site.

Example The script below prints out a custom coupon using the ISL. A chain of restaurants has several sites where the coupons will be distributed. Each site must have its unique name, address, and telephone number printed on each coupon.

```isl
event inq : 1
  //start the print job
  startprint @rcpt
    //print the site into
    printline "-----------------------------"
    printline site_name
    printline site_addr1
    printline site_addr2
    printline site_phone
    printline "-----------------------------"
    call print_coupon
  endprint
endevent
```

Since the same script is distributed to each site, it is not possible to embed the site information into the main script. Consequently, a separate script is created for each site that contais the site configuration parameters.

### Merge Program Files

```isl
//Set these variables to the site name, address,
//and phone number
var site_name : a40 = "My Restaurant"
var site_addr1 : a40 = "12345 Main Street"
var site_addr2 : a40 = "Baltimore, MD 21229"
var site_phone : a40 = "301-210-6000"
```

Using the ISL Merge Program, we can merge this configuration file with the main script.

The following files are related to the merge process:

| File | Description |
| --- | --- |
| ISLMERGE.EXE | The executable program that encrypts an ISL script |
| ISLMERGE.DOC | A README.DOC file containing summary information on using the encryption program |

Installing ISLMERGE.EXE

- Complete the following steps to install the merge program.
- Create a new directory called islmerge. For example: `c:\>md islmerge`
- Copy ISLMERGE.EXE from the distribution diskette to c:\islmerge. For example: `c:\>copy a:\islmerge.exe c:\islmerge`

### Command Syntax

[path]islcrypt [[path]/input_file] [path]/output_file \ [ “user_description” ] ]

| Parameter | Description |
| --- | --- |
| `unencrypted_source` | The utility file name |
| `encrypted_source` | The unencrypted ISL script file name you wish to merge; also called the configuration file |
| `new_encrypted_source` | The encrypted output file |

- Guidelines
- Both the program and script may be located in any directory. See the following example:

| File | Location |
| --- | --- |
| islmerge.exe | `c:\islmerge` |
| script file | `c:\3700\etc\pms1.isl` |

- The output_file and user_description are optional. The output_file name is required when using the user_description.
- Both the unencrypted_source and encrypted_source must be valid ISL scripts.
- The size of the new_encrypted_source may not exceed 64K.
- In order to access both the merge program and the source scripts, you must specify the full directory path name.

### Using the Merge Program

The Utility is run from the DOS command line.

- Before You Begin Prior to using the merge program, perform the following precautionary steps:
- Verify the file names and paths of the files to be merged.
- Change to the directory holding the islmerge program.

Merging a Script in Command Line Mode This procedure allows you to merge two scripts by entering the command syntax at a DOS prompt.

To merge two scripts in command line mode complete the following steps:

1. Take the precautionary steps in "Before You Begin." 1. Enter the command syntax at the prompt. For example:

c:\isl\islmerge script.isl script.xsl “PMS Interface Script
