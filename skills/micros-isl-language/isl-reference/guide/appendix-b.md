# Appendix B: Database Access

This appendix provides instructions for accessing the system database from any client platform.

## About the Database Utility

### Available Functions

Database access is available from any client platform through the newly added MDSSysUtils application. This utility, which incorporates the functionality of the MICROS add-on application SIMODBC.dll, is automatically included and installed with the RES 3000 Version 3.2 software system.

Although designed for use with the MICROS Workstation 4 (WS4), the functions in the MDSSysUtilsProxy.dll will also work on the Win32 and MICROS hand-held (HHT) devices. It is, in fact, the preferred way to access the database on all supported platforms since it takes advantage of the MICROS network transport layer.

With MDSSysUtilsProxy.dll, SIM users are not limited to MICROS products, but can use the utility to query the database of third-party applications as well.

To be consistent with the rest of the MDS System, the calling convention of the API function has changed from _stdcall to _cdecl. Consequently, SIM developers will now use the DLLCALL_CDECL SIM command instead of DLLCALL.

The following functions are available through the MDSSysUtilsProxy.dll:

sqlExecuteQuery

sqlGetRecordSet

sqlCloseConnection

sqlIsConnectionOpen

sqlInitConnection

sqlGetFirst

sqlGetLast

sqlGetNext

sqlGetPrev

sqlGetLastErrorString

The following is a reference of the SIMODBC API: BOOL MDSSYSUTILSPROXY_API sqlExecuteQuery ( const char *szCmd ); BOOL MDSSYSUTILSPROXY_API sqlGetRecordSet ( const char *szCmd ); BOOL MDSSYSUTILSPROXY_API sqlCloseConnection ( ); BOOL MDSSYSUTILSPROXY_API sqlIsConnectionOpen ( int *isOpen ); BOOL MDSSYSUTILSPROXY_API sqlInitConnection ( const char *szDbName, const char *szConnInfo, const char *szLicenseKey ); void MDSSYSUTILSPROXY_API sqlGetFirst( char *szOutRecordData ); void MDSSYSUTILSPROXY_API sqlGetLast( char *szOutRecordData ); void MDSSYSUTILSPROXY_API sqlGetNext( char *szOutRecordData ); void MDSSYSUTILSPROXY_API sqlGetPrev( char *szOutRecordData ); void MDSSYSUTILSPROXY_API sqlGetLastErrorString( char *szoutErrorString );

## Sample File

The following sample demonstrates how the functions are used to obtain access to the database:

```isl
var hODBCDLL : N12 = 0

event inq : 1
var constatus : N9
var sql_cmd : A2000
var emp_id : A10 = "900"
var fn : N12 = 0

// --------------------- Load SIMODBC.dll ------------------- if hODBCDLL = 0 DLLLoad hODBCDLL, "MDSSysUtilsProxy.dll endif

if hODBCDLL = 0
exitwitherror "Unable to Load MDSSysUtilsProxy.dll"
endif // -----------------------------------------------------------
```

```isl
// Connect to micros 3700 database
DLLCALL_CDECL hODBCDLL, sqlIsConnectionOpen(ref constatus)
if constatus = 0
  DLLCALL_CDECL hODBCDLL, sqlInitConnection("micros","ODBC;
  UID=custom;PWD=custom", "")
endif
```

```isl
sql_cmd = "select * from micros.mi_def"
```

DLLCALL_CDECL hODBCDLL, sqlGetRecordSet(sql_cmd) sql_cmd = ““ DLLCALL_CDECL hODBCDLL, sqlGetLastErrorString(ref sql_cmd) if (sql_cmd <> ““) ErrorMessage “Error From SQL -> “, sql_cmd endif

```isl
sql_cmd = ""
DLLCALL_CDECL hODBCDLL, sqlGetFirst(ref sql_cmd)
```

if sql_cmd = ““ exitwitherror “There Is No Matching Record” endif

```isl
if (@WSTYPE <> 3)
  fopen fn, "sqldataout.txt", Write
else
  fopen fn, "\cf\micros\etc\sqldataout.txt", Write
endif

while sql_cmd <> ""
  fwrite fn, sql_cmd
  DLLCALL_CDECL hODBCDLL, sqlGetNext(ref sql_cmd)
endwhile
fclose fn

// Execute query that doesn't return a recordset // -------------------------------------------------------
```

```text
format sql_cmd as “update micros.emp_def   “, \
                  “ set id = 999”,            \
                  “ where id = 999”
```

```isl
DLLCALL_CDECL hODBCDLL, sqlExecuteQuery(sql_cmd)
```

sql_cmd = ““ DLLCALL_CDECL hODBCDLL, sqlGetLastErrorString(ref sql_cmd) if (sql_cmd <> ““) ErrorMessage “Error From SQL -> “, sql_cmd endif

endevent
