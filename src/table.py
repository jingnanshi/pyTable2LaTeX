
import functions

class Table:

    def __init__(self):
        self.styles = ["simple","booktabs","cells","longtable"]
        self.formats = ["csv","excel"]

    def update(self,string,t_format):
        """ update the table
        """
        self.raw_string = string
        self.raw_format = t_format
        
    def getLaTeX(self,style,math_var):
        """ return the current latex string
        """
        if (self.raw_format == "csv"):
            self.latex = self.delimToLaTeX(self.raw_string, ',','\n',style,math_var)
        elif (self.raw_format == "excel"):
            self.latex = self.delimToLaTeX(self.raw_string, '\t','\r',style,math_var)
            
        return self.latex

    def getStyles(self):
        """ return available latex styles
        """
        return self.styles

    def getFormats(self):
        """ return available raw formats
        """
        return self.formats

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

    def delimToLaTeX(self,string,delim,linechange,style, math_var):
        """ convert table to latex using delimiter
        	delim: cell separator
        	linechange: linechange character
        """
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
                    text[i][j] = self.convertCell(cell,math_var)

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
                if (functions.is_number(new_cell_list[index])):
                    new_cell_list[index] = '$' + new_cell_list[index] + '$'
            new_cell = ' '.join(new_cell_list)
        return new_cell


    def cleanRawString(self,string):
        """ clear string out of the trailling whitespace characters
        """
        pass


    




