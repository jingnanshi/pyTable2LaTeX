# -*- coding: utf-8 -*-
"""

@author: Jingnan Shi
@contact: jshi@g.hmc.edu

To-do: TABLE environment FLOAT Checkbutton

"""
from Tkinter import *
import tkMessageBox
from table import Table
from tkFileDialog import *

class App:

    def __init__(self, master):
        # initialize Table object
        self.table = Table()
        self.master = master
        # title
        title = Label(master,text= "pyTable",font=("Helvetica", 16))
        self.title = title
        
        # raw excel/csv table
        t_raw_table = Text(master, width=40, height=24, 
                         wrap=WORD)
        self.text_raw = t_raw_table

        # http://stackoverflow.com/questions/5870561/re-binding-select-all-in-text-widget
        # Thank you, Bryan Oakley! 
        master.bind_class("Text","<Command-a>", self.selectall)

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

        self.formats = self.table.getFormats()
        for i in range(len(self.formats)):
            format_list.insert(i,self.formats[i])
        
        self.format_list = format_list
        # set focus
        self.format_list.select_set(0) 
        self.format_list.event_generate("<<ListboxSelect>>")
        
        # label
        style_lab = Label(master,text = "Choose the LaTeX style you want: ")
        self.style_lab = style_lab
        
        # style: booktabs, longtable, simple, cells
        #scrollbar = Scrollbar(master)
        
        style_list = Listbox(master,exportselection = False, selectmode = SINGLE,height=4) 
        self.styles = self.table.getStyles()
        for i in range(len(self.styles)):
            style_list.insert(i, self.styles[i])        

        self.style_list = style_list
        # set focus
        self.style_list.select_set(0) 
        self.style_list.event_generate("<<ListboxSelect>>")
        
        # math? checkbox
        self.math_var = IntVar()
        math = Checkbutton(master, variable = self.math_var, text = "math?")
        self.math_check = math
        
        # convert button
        convert_button = Button(master, text="Convert", command=self.convert,
                                padx = 3, pady = 2)
        self.convert_button = convert_button
        
        # copy from clipboard
        paste_from_clipboard = Button(master, text="Paste from Clipboard", command=self.pasteFromClipboard, padx = 2, pady = 2)
        paste_from_clipboard.grid(row=16,column=1)

        copy_to_clipboard = Button(master, text="Copy to Clipboard", command=self.copyToClipboard, padx = 2, pady = 2)
        copy_to_clipboard.grid(row=17,column=1)

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
        filemenu.add_command(label="Open", command=self.openFile)
        
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.showAbout)
        menubar.add_cascade(label="Help", menu=helpmenu)

        master.config(menu=menubar)

    def selectall(self, event):
        event.widget.tag_add("sel","1.0","end")

    def openFile(self):
        self.text_raw.delete(1.0,END)
        f = askopenfile(mode='r')
        # clear the unwanted \r
        f_text = f.read().replace('\r','')
        self.text_raw.insert(END,f_text)
        f.close()

    def pasteFromClipboard(self):
        """ paste from clipboard
        """
        self.text_raw.delete(1.0,END) 
        self.text_raw.insert(END, self.master.clipboard_get())


    def copyToClipboard(self):
        """ copy to clipboard
        """
        self.master.clipboard_clear() 
        self.master.clipboard_append(self.text_texed.get("1.0", 'end-1c'))

    def showAbout(self):
        """ show about info
        """
        tkMessageBox.showinfo("About", "Made by Jingnan Shi - jshi@g.hmc.edu")

    def convert(self):
        """ function called when convert is called
        """
        print "converting ........."

        # update the table
        print "Source format: " + self.getSelectedFormat()
        self.table.update(self.getRawString(), self.getSelectedFormat())      

        # get the latex table
        print "Target style: " + self.getSelectedStyle()
        latex_table =  self.table.getLaTeX(self.getSelectedStyle(),self.math_var.get())
        
        # update gui
        self.updateTargetText(latex_table)
       
    def getRawString(self):
        """ get the raw table string in the app
        """
        raw = self.text_raw.get("1.0", 'end-1c')
        return raw

    def updateTargetText(self, string):
        """ update the text on the finished table text
        """
        self.text_texed.config(state=NORMAL)
        self.text_texed.delete(1.0, END)
        self.text_texed.insert(END, string)

    def getSelectedFormat(self):
        """ return the GUI selected raw data format
        """
        try:
            # a bug in Tkinter 1.160 (Python 2.2) and earlier versions causes 
            # this list to be returned as a list of strings, instead of integers
            selected_list = map(int, self.format_list.curselection())
            format_index = selected_list[0]
            raw_format = self.formats[format_index]
            return raw_format
        except IndexError:
            print "Format not selected!"
            return 

    def getSelectedStyle(self):
        """ return the GUI selected latex style
        """
        try:
            # a bug in Tkinter 1.160 (Python 2.2) and earlier versions causes 
            # this list to be returned as a list of strings, instead of integers
            selected_list = map(int, self.style_list.curselection())
            style_index = selected_list[0]
            style = self.styles[style_index]
            return style
        except IndexError:
            print "Style not selected!"
            return style







