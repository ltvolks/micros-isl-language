# Appendix A: Windows DLL Access

This appendix describes DLLs and how to access them using SIM.

## What is a DLL?

### Dynamic Linking

The 3700 System Interface Module (SIM) can use Windows Dynamic-Link Libraries (DLLs). DLLs are modules that contain functions and data. They provide a way of separating applications into small manageable pieces that can be easily modified and reused.

Dynamic linking provides a means of giving applications access to function libraries at run time. DLLs are not copied into an application’s executable files. Instead, they are linked to an application when it is loaded and executed. Dynamic link libraries reside in their own separate files. Applications load them into memory when they are needed, and share a single copy of the DLL code in physical memory. A single DLL can be used by several applications simultaneously. This in turn saves memory and reduces swapping.

Windows allows only a single instance of a DLL to be loaded into memory at any time. When a DLL is being loaded, Windows checks all the modules already in memory. If it doesn’t find a match, then it loads the DLL. If it does find a match, and the matching module is a DLL, it doesn’t load it again.

- The following are steps that an application takes when calling a function in a DLL:
- The application uses the LoadLibrary or LoadLibraryEx function to load the DLL at runtime. This, for example, can be a .EXE or a .DLL.
- The application calls the GetProcAddress function to get the addresses of the exported DLL functions and it is mapped into the address space of the calling process.
- The application then calls the exported DLL functions using the function pointers returned by GetProcAddress.

DLLs can define two kinds of functions: exported and internal. The exported functions can be called by other applications. Internal functions can only be called from within the DLL where they are defined. DLLs can contain code, data, and resources such as bitmaps, icons, and cursors. These are stored as executable programs.

## Using DLLs

### Sharing Components

DLLs are used for three general purposes:

- Sharing components
- Encapsulating (hiding) data and code
- Performing system-level operations

- DLLs provide an easy way for multiple applications to share components. These components can be:
- Code - a DLL provides one copy of its code for all applications that need it.
- Data - by storing and retrieving data, applications can communicate with each other. The DLL provides a function for applications to store and retrieve data in its data segment.
- Custom Controls - these can be placed in DLLs for use by multiple applications. They can be written by developers and marketed as separate DLLs or used in applications.
- Resources - icons, bitmaps, fonts, and cursors can be placed in DLLs. Device divers are also DLLs that provide system resources.

### Encapsulating (hiding) data and code

DLLs can be used to hide data and code. A DLL can implement an abstract data type (ADT), which can be used by applications. The applications can use the ADT without knowing anything about the actual implementation. When changes are made to the data structures and internal code, the applications that use the DLL don’t have to be modified or recompiled.

### Performing system-level operations

DLLs can be used to perform low-level operations. Operations such as interrupt service routines can be placed in fixed-code segments of DLLs. If an application needs to issue interrupts, the code can be placed in a DLL rather than in the application. Also, a DLL can be written as a device driver for certain pieces of hardware; a mouse or a keyboard for example.

## 3700 SIM DLL Support

### Customization

The 3700 System Interface Module allows you to reap the benefits of DLLs. You can write or use existing DLLs to further enhance the capabilities of the 3700 POS operations module. Using four SIM commands, you can create a SIM script to access an externally created DLL.

- This functionality considerably broadens the scope of the 3700 SIM feature. Some advantages of this feature are:
- The ability to write SIM scripts to customize your 3700 PMS interface.
- The opportunity to take advantage of third party development.
- A wider range of creativity.
- Faster turn around time.

Using DLLs gives you the flexibility of customization. Now you are no longer confined to the text based window that SIM uses for input and output. For example, you could create a custom interface to a PMS that returns guest information to the 3700 POS operations module.

Third Party Development If you are not interested in writing your own DLLs, you can take advantage of DLLs that can be, or already have been, written by a third party for 3700 SIM.

### Creativity

Using the resources available with DLLs, you can use fonts, bitmaps, cursors etc. to create appealing user interfaces.

Faster Turn Around Time Using DLLs can increase the turn around time of certain system requests. For example, you could create a dll to connect to the 3700 database and perform a custom query on guest check information.

DLLs give you virtually unlimited flexibility when creating scripts to enhance the functionality of the POS operations module.

## Using 3700 SIM DLL Commands

### DLLLoad

Three commands allow SIM to access DLLs. They enable a SIM script to call an externally created DLL. These three commands are:

o DLLLoad - loads the external DLL o DLLCall - calls a function contained in the DLL using the standard calling convention (STDCALL) o DLLFree - frees a loaded DLL o DLLCall_CDECL - calls a function contained in the DLL using the Pascal calling convention (CDECL)

DLLLoad loads the external DLL. It needs to be called only once during the lifetime of the SIM script. The syntax is: DLLLoad handle, name

where handle is a SIM N9 variable, and name is a SIM string expression. The ‘name’ parameter is used to identify the DLL, and the resulting handle is stored in the ‘handle’ variable. An example of this would be: var dll_handle:N9 DLLLoad dll_handle, “myops.dll”

If the command fails, then dll_handle will be 0. If not, then dll_handle is the handle used for any further accesses for the other DLL functions.

This function is just a wrapper around the Windows LoadLibrary() function. All the rules which apply to path settings apply here.

If the DLL is already loaded, then Windows will prevent it from being loaded again.

### DLLFree

DLLs should be included in the following locations for each workstation platform:

- Win32 — \Micros\RES\POS\Bin
- HHT — \Micros\RES\CAL\HHT\MICROS\Bin
- WinCE — \Micros\RES\CAL\WS4\Files\CF\Micros\Bin

Note: When using SIM on a Win CE platform, be sure to include the full path to the DLL in the script. Do NOT place the DLL in the Windows folder as this folder is not saved to disk during a reboot.

This command is used to free a loaded DLL. The syntax is: DLLFree handle

where handle is the handle obtained in a DLLLoad command.

This function is automatically called when OPS exits, or the SIM script is reread. It can be called to free up resources loaded by the DLL.

### DLLCall

The DLLCall command is used to call a function contained in the DLL. The syntax for this command is: DLLCall handle, dll_name( [parm1 [parm2 [parm3...]]] )

or DLLCall_CDECL handle, dll_name( [parm1 [parm2[ parm3…]]] )

where handle is the previously loaded library handle, dll_name is the name of the function, and parm# are the optional parameters.

- This command performs two tasks:
- The first is to get the address of the function using the Windows GetProcAddress() function. If this function fails, then an ISL error will be generated.
- The second is to call the DLL function.

Since it is not possible for SIM to check the validity of the parameters, it is up to the SIM script writer to ensure that the proper number, type, and calling convention is used.

Note that it is not possible for a DLL to return a value back to SIM. More specifically, if one is returned, it is ignored. Passing information back to the SIM script should be done using references, which are explained in the sections that follow.

### Parameter Passing

There are only three types of variables in SIM: integer, monetary, and string. Therefore, only these types may be used as parameters to the DLL. However, each type may be passed in by value or by reference, and each type may also be passed in as an array. Therefore, there are 12 possible parameter types.

To pass by reference, place the string “ref” before the parameter. For example: // Pass by value DLLCall handle, my_function( count )

```isl
// Pass by reference DLLCall handle, my_function( ref count )
```

Only variables can be passed in by reference. Complex expressions must be passed in by value. // Will generate an error DLLCall handle, my_function( ref count + 1 ) DLLCall handle, my_function( ref (1 + 3 ) )

When generating the parameter list, SIM will dynamically allocate data for each parameter, and this allocated data (or a reference to it) will be passed to the DLL. No references to the stored copy of the data will be passed. If by reference, SIM will copy in the new values to the data variables once the function has completed. Therefore, do not pass in huge arrays by reference when not needed, since SIM will attempt to copy in each array element, even if it has not changed.

All pointers passed to the DLL are passed in as 32-bit pointers. All strings are C nul- terminated strings. All integer values are signed. All arrays are passed as a pointer to a list of pointers or integers. The length of the array must either be passed in as an argument, or known prior by the DLL.

Though there are 12 ways of passing in parameters, there are only five separate ways to declare them in C.

| 1. | int a | // integer |
| --- | --- | --- |
| 2. | `int *a` | // integer pointer |
| 3. | int a[] | // array of integers |
| 4. | `char *a` | // string pointer |
| 5. | `char *a[]` | // array of string pointers |

The following table lists the different possibilities, and how they map to the parameter type.

```text
SIM Type                  C Declaration         Comments
integer                            int a
integer by reference               int *a
integer array                      int a []
integer array by reference         int a []          same as integer array
string                             char *a
string reference                   char *a           same as string
string array                       char *a []
string array by reference          char *a []        same as string array
amount                             char *a
amount by reference                char *a           same as amount
amount array                       char *a
amount array by reference          char *a           same as amount array
```

#### Integers

By value N1-N9 integers are passed in as 32-bit signed values. N10 and above are passed in as pointers to a string which contains the numeric value expressed as a string. For example, an N12 numeric variable whose value is 12345 will be passed in as “12345”. If the number is negative, then a “-” will be the first character in the string. (The reason for this is that a 32-bit integer can only have 9 digits.)

#### By value examples

```isl
var a:N9 = 4
var b:N10 = 3012108000
DLLCall handle, my_function( a, 10, (1 + a) * 10, b )
```

#### The dll prototype should look as follows

void my_function( int p1, int p2, int p3, char *p4 );

#### The dll function should expect these parameters

4 10 50 “3012108000”

By reference N1-N9 integers are passed in as pointers to a 32-bit value. The DLL can change this value, and this change will be reflected in the variable. N10 variables are passed in as strings. The length of the string is guaranteed to be the length of the string variable. An N12 variable with a value of “123” will be passed in as “123”, but the space occupied by the string will be at least 13. This means that the DLL can safely copy in a string longer than “123”.

#### By reference examples

```isl
var a:N9 = 12
var b:N12 = 3012108000
DLLCall handle, my_function( ref a, ref b )
```

#### The dll prototype should look like

void my_function( int *p1, char *p2 )

#### The dll function should expect these parameters

pointer to 12 “3012108000”

Strings All string parameters are passed in as a pointer. When by reference, SIM will copy the string data back into the original variable.

By value The string parameter is passed in as a pointer to a nul-terminated string.

#### By value examples

```isl
var a:A20 = "12345"
DLLCall handle, my_function( a, "hello" )
```

#### The dll prototype should look like

void my_function( char *p1, char *p2 )

#### The dll function should expect these parameters

“12345” “hello”

By reference The string parameter is passed in as a pointer to a nul-terminated string. However, the memory reference will be guaranteed to have allocated enough space for the declared string. For example, if a string is declared as A20 but is set to “12345”, then the string passed in will be “12345”, but will have 20 characters allocated (not including the nul terminator) The DLL can then write up to 20 characters into the string.

#### By reference example

```isl
var a:A20
```

#### DLLCall handle, my_function( ref a )

#### The dll prototype should look as follows

void my_function( char *p1 )

#### The dll should expect these parameters

““

The dll could copy a string of up to 20 characters in. memset( p1, ‘-’, 20 ) p1[ 20 ] = 0

A-10                                                                            Windows DLL Access Monetary Data All SIM monetary data ($ variables) are kept as strings internally. Each string consists of the digits which make up the value. There is no representational difference between monetary amounts and numeric data N10 and greater.

The difference between the two is determined by the operations allowed on the values. The operations involved are the assignment and arithmetic ones. Therefore, monetary amounts are passed to the DLL as numeric strings. However, they will have the decimal point inserted into the proper place.

By value The string parameter is passed in as a pointer to a nul-terminated string. A ‘-’ will be placed at the beginning of the string if it is negative.

By value example var a:$12 = 12.34 DLLCall handle, my_function( a, a + 1.11, 5.67 )

The dll prototype should look as follows: void my_function( char *p1, char *p2, char *p3 )

“12.34” “13.45” “5.67”

By reference The string parameter is passed in as a pointer to a 0-padded nul-terminated string. The string will be padded with as many zeroes to make it the same as it’s declared length. A $12 variable string will have 12 digits and 1 decimal point. (The nul is not included)

By reference example var a:$12 = 12.34 DLLCall handle, my_function( ref a )

The dll prototype should look like: void my_function( char *p1 )

The dll should expect these parameters: “0000000012.34”

Array References All arrays are passed in as an array of pointers or integers. As with SIM subroutine calls, all arrays must have a [] following them. Note that arrays and arrays by reference use the same declaration. The only difference between the two is that the values are copied back to the variables when the function is done.

N1-N9 numeric values are passed in as integers. var array[ 20 ] : N9

```isl
// Passing in by value. // DLL prototype should be: void my_function( int array[] ); DLLCall handle, my_function( array[] )

// Passing in by reference. // DLL prototype should be: void my_function( int *array[] ); DLLCall handle, my_function( ref array[] )
```

All other types are passed in as strings. var array1[ 20 ] : $12 var array2[ 40 ] : A40

```isl
// Passing in by value // DLL prototype should be: // void my_function( char *array1[], char *array2[] ); DLLCall handle, my_function( array1[], array2[] )

// Passing in by reference // DLL prototype should be: // void my_function( char *array1[], char *array2[] ); DLLCall handle, my_function( ref array1[], ref array2[])
```
