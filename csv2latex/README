csv2latex Version 1.0 2009/09/13

Spreadsheet tables to LaTeX
Original script written by Tom Counsell; Modified by Alan Munn <amunn@msu.edu>
Released under the Gnu Public Licence
Copyright 2005 by Tom Counsell
Copyright 2009, 2010 by Alan Munn

Contents

This package contains csv2latex, csv2latex.scpt (An Applescript) and a macro for TeXShop. The installer only installs csv2latex itself.  The Applescript or TeXShop macro must be installed by you directly.

1. csv2latex
This is a ruby script, originally written by Tom Counsell <tom@counsell.org> as xl2latex.rb and modified and renamed by Alan Munn <amunn@msu.edu>

The script allows for four command-line arguments corresponding to the table style required:

cells	converts the clipboard text simply to latex table cells

simple	creates a simple tabular environment around the cells

booktabs	assumes the first line is a header, and places \toprule, \midrule and \bottomrules in the appropriate places within a tabular environment

longtable	assumes the first line is a header, creates the appropriate longtable header information and places the cells in a longtable environment

If no argument is given, the script produces the simple tablestyle.

2. csv2latex.scpt
This is an Applescript for use with Applescript-aware text editors such as TextWrangler or BBEdit.

3. TeXShop/csv2latex.plist
This is a macro for use with TeXShop.

Installation:

The installer install csv2latex in /usr/local/bin.

For use with editors other than TeXShop:

Install the Applescript csv2latex.scpt into the scripts folder of your editor.

For use with TeXShop:

Within TeXShop, open the Macro Editor.

Choose 'Add macros from file' from the Macros menu, and open the csv2latex.plist file contained in the csv2latex TeXShop folder. This will add a macro called 'Paste Spreadsheet Cells' to the bottom of your macros menu.  Once the macro is added you can move it to any location in the list by dragging its name in the lefthand panel of the macro editor. 

How to use:

With TeXShop

Select a range of cells in your spreadsheet application, and copy them to the clipboard.

Within TeXShop, choose Paste Spreadsheet Cells from the Macro menu.  You will be asked to choose a table style: these correspond to the table styles described above.

Doubleclick on the table style you want or single click, and click OK, and the selected cells will be pasted into the current window.

With other editors:

Select a range of cells in your spreadsheet application, and copy them to the clipboard.

In your editor, choose the csv2latex script. You will be asked to choose a table style: these correspond to the table styles described above.

Doubleclick on the table style you want or single click, and click OK, and the selected cells will be pasted into the current window.
