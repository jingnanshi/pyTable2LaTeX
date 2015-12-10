--Applescript direct
--This script copyright 2009,2010 by Alan Munn <amunn@msu.edu>
--Version 1.1 2010/01/31
--Copy cells from Excel or other spreadsheet program and
-- use this script to paste the cells into your LaTeX source
-- in a variety of different table styles.
set mainList to {"cells","booktabs", "simple","longtable" }
choose from list mainList with prompt "Choose a table format"
if the result is not false then
	set tablestyle to result as text
	do shell script  "/usr/local/bin/csv2latex" & " " &  tablestyle
	tell application "System Events" to keystroke "v" using {command down}
end if
--End of Applescript
