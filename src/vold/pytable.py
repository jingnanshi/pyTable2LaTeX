# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:30:14 2015

@author: Jingnan Shi

TO-DO: add exceltoLatex convertion functions for: simple, cells, booktabs and longtable

"""

from Tkinter import *
import tkMessageBox
import table

class App:

    def __init__(self, master):
        # title
        title = Label(master,text= "pyTable",font=("Helvetica", 16))
        self.title = title
        
        # raw excel table
        t_raw_table = Text(master, width=40, height=24, 
                         wrap=WORD)
        self.text_raw = t_raw_table
        start_str = "Please delete this line and copy your excel table here"
        self.text_raw.insert(INSERT, start_str)
    
        # text box to display produced latex code
        t_latex_table = Text(master,state = DISABLED, width=40, height=24, 
                         wrap=WORD)
        self.text_texed = t_latex_table
        
        # options to select
        # label
        format_lab = Label(master,text = "Choose the format of your table: ")
        self.format_lab = format_lab
        
        # raw data format   
        format_list = Listbox(master,selectmode = SINGLE,exportselection = False, height=2)
        self.formats = ["csv","excel"]
        format_list.insert(0,self.formats[0])
        format_list.insert(1,self.formats[1])
        self.format_list = format_list
        
        # label
        style_lab = Label(master,text = "Choose the LaTeX style you want: ")
        self.style_lab = style_lab
        
        # style: booktabs, longtable, simple, cells
        #scrollbar = Scrollbar(master)
        
        style_list = Listbox(master,exportselection = False, selectmode = SINGLE,height=4) 
        self.styles = ["simple","booktabs","cells","longtable"]
        style_list.insert(0, self.styles[0])        
        style_list.insert(1, self.styles[1])
        style_list.insert(2, self.styles[2])
        style_list.insert(3, self.styles[3])
        self.style_list = style_list
        
        # math? checkbox
        self.math_var = IntVar()
        math = Checkbutton(master, variable = self.math_var, text = "math?")
        self.math_check = math
        
        # convert button
        convert_button = Button(master, text="Convert", command=self.convert,
                                padx = 2, pady = 2)
        self.convert_button = convert_button
        
        # positioning the tk widgets
        self.title.grid(row=0,column=1)
        self.text_raw.grid(row=1,column=0,rowspan=18)
        self.text_texed.grid(row=1,column=2,rowspan=18)

        self.format_lab.grid(row=1,column=1)        
        self.format_list.grid(row=2,column=1)
        
        self.style_lab.grid(row=3,column=1)
        self.style_list.grid(row=4,column=1)
        self.math_check.grid(row=5,column=1)
        self.convert_button.grid(row=15,column=1)

        # menu
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save Table To", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.showAbout)
        menubar.add_cascade(label="Help", menu=helpmenu)

        master.config(menu=menubar)

    def donothing(self):
        pass

    def showAbout(self):
        """ show about info
        """
        tkMessageBox.showinfo("About", "Made by Jingnan Shi - jshi@g.hmc.edu")

    def convert(self):
        """ function called when convert is called
        """
        print "convert"
        print self.math_var.get()
        print self.getRawString()
        print self.escapeLaTeX(self.getRawString())
        self.updateEndText(self.rawToLaTeX(self.getRawString()))
        
       
    def getRawString(self):
        """ get the raw table string in the app
        """
        raw = self.text_raw.get("1.0", 'end-1c')
        return raw

    def updateEndText(self, string):
        """ update the text on the finished table text
        """
        self.text_texed.config(state=NORMAL)
        self.text_texed.delete(1.0, END)
        self.text_texed.insert(END, string)
        

    def cleanRawString(self,string):
        """ clear string out of the trailling whitespace characters
        """
        pass

    def rawToLaTeX(self,string):
        """ convert raw to latex
        """
        try:
            format_index = self.format_list.curselection()[0]
            raw_format = self.formats[format_index]
        except IndexError:
            print "Format not selected!"
            return

        if (raw_format == "csv"):
            return self.delimToLaTeX(string, ',','\n')
        else:
            return self.delimToLaTeX(string, '\t','\r')
        

    def escapeLaTeX(self,string):
        """ escape the special characters present in the string
        """
        string_to_escape = "{([&$#%])}"
        special_symbol_map = {'\\': '\\textbackslash', '~': '\\textasciitilde'}
        new_str_list = map(lambda x: "\\" + x if x in string_to_escape else x,
                    string)
        new_symbolfied_list = map(lambda x: special_symbol_map[x] if x == '\\' or x == '~' else x, 
                    new_str_list)
        return ''.join(new_symbolfied_list)
    
    def delimToLaTeX(self,string,delim,linechange):
        """ convert csv raw table to LaTeX
            input: raw csv format string
            output: a string in latex format
            line change character: \n 
            cell separate character: ,
        """
        # get style speciation
        try:
            style_index = self.style_list.curselection()[0]
            style = self.styles[style_index]
        except IndexError:
            print "Style not selected!"
            return

        # clearn the raw string 

        # generate a list of lists with each element is a list that represents a row
        text = self.escapeLaTeX(string)
        text = text.split(linechange)
        # split each row into cells by commas
        text = map(lambda x: x.split(delim), text)
        print text

        # calculate the row number
        rows = len(text)

        # calculate the column number
        # if text[1] does not exist, that means this is not a proper table
        try:
            cols = len(text[1])
        except IndexError:
            print "This is not a table! No columns exist!"
            return

        # convert each cell by math indicator
        for i in range(rows):
                for j in range(cols):
                    cell = text[i][j]
                    text[i][j] = self.convertCell(cell,self.math_var.get())

        # generate a new table based of the lol
        # check each cell
        new_text = map(lambda x: ' & '.join(x), text)
        print new_text
        new_text_str = ' \\\\ \n'.join(new_text) + ' \\\\ \n \n'
        
        # cell style
        if (style == 'cells'):
            pass
            
        # simple style
        if (style == 'simple'):                                          
            new_text_str = '\\begin{} \n \n'.format('{tabular}' + '{'+'l'*cols+'}') + new_text_str + '\\end{tabular}'
        
        # booktabs
        if (style == 'booktabs'):
            midrule_index = new_text_str.find('\n')+1
            top = '\\toprule \n' + new_text_str[:midrule_index]
            bottom =  new_text_str[midrule_index:] + '\\bottomrule \n'
            new_text_str =  top + '\\midrule \n' + bottom
            new_text_str = '\\begin{} \n \n'.format('{tabular}' + '{'+'l'*cols+'}') + new_text_str + '\\end{tabular}'

        # longtable
        if (style == 'longtable'):
            mid_index = new_text_str.find('\n')+1
            first_row = new_text_str[:mid_index]
            rest = new_text_str[mid_index:]
            top = first_row + '\\endfirsthead \n'+ first_row  + '\\endhead'
            top = top + '\\multicolumn{} \n'.format('{' + str(cols) + '}' + '{'+'l'*cols+'}'+'{{Continued\ldots}}')
            top = top + '\\endfoot \n\\hline \n\\endlastfoot \n \n'
            new_text_str = top + rest
            new_text_str = '\\begin{} \n \n'.format('{longtable}' + '{'+'l'*cols+'}') + new_text_str + '\\end{longtable}'

        return new_text_str


    
    def convertCell(self, cell, is_math = False):
        """ convert cell string to latex format
            first tokenize string by spaces
            if is_math = true, add $ $ around numbers
            
            TESTED
        """
        new_cell = cell
        if (is_math):
            # separate the cell into a list using space
            new_cell_list = new_cell.split(' ')
            # check each element; if number, add $$ around
            for index in range(len(new_cell_list)):
                if (self.is_number(new_cell_list[index])):
                    new_cell_list[index] = '$' + new_cell_list[index] + '$'
            new_cell = ' '.join(new_cell_list)
        return new_cell
    
    def is_number(self,s):
        """ if s is a number, return True
            TESTED
        """
        if (self.is_float(s) or self.is_int(s)):
            return True
        return False

    def is_float(self,s):
        """ if s is a float, return True
            TESTED
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_int(self,s):
        """ if s is an int, return True
            TESTED
        """
        try:
            int(s)
            return True
        except ValueError:
            return False



root = Tk()
 
app = App(root)
try:
    root.mainloop()
except TclError:
    print 'tclerror'



