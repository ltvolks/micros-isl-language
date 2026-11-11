// **************************************************************************
// DisplayPagedWindow
//  ISL Paging Window
//  Display info from a large array a screen at a time using the ISL Window
//  Max # of records is 12 per window
//
//      Arguments
//          title      : Title of window
//          numrecs : Number of records in array
//          pagearray : reference to array containing items to display
// Usage:
//  var displayarray[16] : A72
//  displayarray[1] = "Some Text to display"
//  ...
//  call DisplayPagedWindow("Check Info", 16, displayarray[])
// **************************************************************************
sub DisplayPagedWindow(var title : A78, var numrecs : N3, ref pagearray[])

  var pagesize  : N3
  var pages     : N3
  var pagecount : N3
  var remainder : N3
  var cnt       : N3
  var lastrow   : N3
  var record    : N3 = 1
  var formattedRecord : A72

  pagesize = 12
  pages = numrecs / pagesize
  remainder = numrecs % pagesize
  if remainder > 0
    pages = pages + 1
  endif



  for pagecount = 1 to pages
    window pagesize, 78, title
    if pagecount = pages and remainder <> 0
      lastrow = remainder
    else
      lastrow = 12
    endif

    for cnt = 1 to lastrow

      if len(pagearray[record]) > 72
        format formattedRecord as pagearray[record]{69}, "..."
      else
        format formattedRecord as pagearray[record]
      endif
      display cnt, 2, formattedRecord
      record = record + 1
    endfor
    waitforconfirm "ENTER to page through, CLEAR to Cancel"
    windowclear
  endfor
endsub
