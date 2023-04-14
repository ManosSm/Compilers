#####################################################################
                # Christos Vasilakos    4857    cse94857
                # Emmanouil Smyrnakis   4793    cse94793
#####################################################################


import string
import sys



class Token:

    def __init__(self, family, recognized_string, line_number):
        self.family = family
        self.recognized_string = recognized_string
        self.line_number = line_number


class Lex:

    def __init__(self, file_name):
        self.file_name = file_name
        self.current_line = 1
        self.current_char = 0
        self.keyword_set={"def","not","and","or","declare","print","return","if","else","while","int","input"}
        self.final_state_set=   {  
                                    2:"number",
                                    4:"id",
                                    5:"addOperator",
                                    6:"mulOperator",
                                    8:"groupSymbol",
                                    12:"delimiter",
                                    14:"assignment",
                                    15:"relOperator",
                                    16:"relOperator",
                                    20:"EOF"
                                }
        self.symbol_dict=   {
                                "_":2,#
                                "+":3,#
                                "-":4,#
                                "*":5,#
                                "/":6,#
                                "<":7,#
                                ">":8,#
                                "!":9,#
                                "=":10,#
                                ";":11,#
                                ",":12,#
                                ":":13,#
                                "[":14,#
                                "]":15,#
                                "(":16,#
                                ")":17,#
                                "#":18,#
                                "{":19,#
                                "}":20,#
                                "$":21#
                            }

        

                            #0 are letters   1 are digits    22 blank char except eof    23 eof   99 error
        self.state_list = [
                            [3,1,99,5,5,6,7,17,18,19,13,12,12,12,8,8,8,8,9,99,99,99,0,20],#0
                            [2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],#1
                            [-1],#2 (-1 is the current_char offset)
                            [3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],#3
                            [-1],#4
                            [0],#5
                            [0],#6
                            [99,99,99,99,99,99,6,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99],#7
                            [0],#8
                            [99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,8,8,10,99,99],#9
                            [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,10,10,10,10,99],#10
                            [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,0,10,99],#11
                            [0],#12
                            [14,14,14,14,14,14,14,14,14,14,15,14,14,14,14,14,14,14,14,14,14,14,14,14],#13
                            [-1],#14
                            [0],#15
                            [-1],#16
                            [16,16,16,16,16,16,16,16,16,16,15,16,16,16,16,16,16,16,16,16,16,16,16,16],#17
                            [16,16,16,16,16,16,16,16,16,16,15,16,16,16,16,16,16,16,16,16,16,16,16,16],#18
                            [99,99,99,99,99,99,99,99,99,99,15,99,99,99,99,99,99,99,99,99,99,99,99,99],#19
                            [0]#20
                        ]

    def next_token(self):
        file = open(self.file_name)
        file.seek(self.current_char)
        state=0                     # the current state of the automaton
        rec_string=""               # the string that will be returned as a token
        white_char_offset = 0       # if rec_string's final character is a white character we increase the current_char by 1.
        line_offset = 0             # if the current char is a new line then the line number should be decreased by 1. It is needed as the token that will be returned will be in the previous line

        while 1:
            line_offset = 0
            in_read = file.read(1)
            in_id = 99

            if in_read.isalpha():                           # if letter
                in_id = 0
                rec_string+=in_read                         # adding character to the recognised string
            elif in_read.isnumeric():                       # if number
                in_id = 1
                rec_string+=in_read                         # adding character to the recognised string
            elif in_read in string.whitespace:              # if a white character
                white_char_offset = 1
                if in_read == "\n":                         # if changed line
                    line_offset= -1
                    self.current_line += 1

                    

                if in_read == "":                           # if eof
                    in_id = 23
                    
                else:
                    in_id = 22                              # if white character except eof
            elif in_read in self.symbol_dict:
                in_id = self.symbol_dict[in_read]
                rec_string+=in_read                         # adding character to the recognised string
            else:

                
                rec_string+=in_read+file.read(9)            # reading the next 9 characters to see if rec_string is "__main__"
                
                if rec_string=="\"__main__\"":
                    self.current_char = file.tell()
                    file.close()
                    return Token("keyword", rec_string, self.current_line+line_offset)
                
                print("Error 0: unknown character", in_read, "at line", self.current_line)
                file.close()
                exit(1)

            state = self.state_list[state][in_id]
            
                               
            


            if state == 0:                                      
                white_char_offset = 0
                rec_string = ""

            elif state in self.final_state_set:                   # if state is final

                rec_string = rec_string[0:(len(rec_string) + self.state_list[state][0] + white_char_offset)]    # black box magic
                self.current_char = file.tell() + self.state_list[state][0] + white_char_offset
                file.close()

                if state==4:                                                                                    # if state is id

                    if rec_string in self.keyword_set:                                                          # check if the string is a keyword
                        return Token("keyword", rec_string, self.current_line+line_offset)
                 
                    elif len(rec_string)>30:                                                                    #check if id is larger than 30 characters
                        print("Error 1: ID", rec_string, "at line", self.current_line, "is too long (max 30 characters)")
                        exit(1)
                
                elif state==2 and (int(rec_string)>2**32-1):                                #making sure that number is smaller than 2^32-1                                 
                    print("Error 2: NUMBER", rec_string, "at line", self.current_line, "is out of range (-(2^32)-1 to 2^32-1)")
                    exit(1)


                return Token(self.final_state_set[state], rec_string, self.current_line+line_offset)              # return token
                
            elif state == 99:                                       # if error


                rec_string+=file.read(6)                            # reading the next 6 characters to see if rec_string is  #declare
                

                if rec_string=="#declare":
                    self.current_char = file.tell()
                    file.close()
                    return Token("keyword", rec_string, self.current_line+line_offset)
                
                else:
                    rec_string+=file.read(1)                        # reading the next character to see if rec_string is __name__
                    if rec_string=="__name__":
                        self.current_char = file.tell()
                        file.close()
                        return Token("keyword", rec_string, self.current_line+line_offset)                 



                
                print("Error 3: unexpected character", in_read, "at line", self.current_line)             #if nothing from the above then its an error
                file.close()
                exit(1)     



#########################################################       intermidiate code       #########################################################

  
class Quad:

    def __init__(self, operator, op1, op2, op3):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __str__(self):
        return str(self.operator) + " " + str(self.op1) + " " + str(self.op2) + " " + str(self.op3)


class IntermediateCode:

    def __init__(self):

        self.quad_list = []
        self.temp_counter = 0
        self.label_counter = 0




    def genQuad(self, operator, op1, op2, op3):

        self.quad_list.append(Quad(operator, op1, op2, op3))
        self.label_counter += 1
    

    
    def nextQuad(self):

        return self.label_counter



    def newTemp(self):

        self.temp_counter += 1
        return "%" + str(self.temp_counter-1)



    def emptyList(self):                                                    #NOTE: MAYBE DELETE

        return []



    def makeList(self, label):

        return [label]



    def mergeList(self, list1, list2):

        return list1 + list2



    def backPatch(self, list, label):

        for i in list:
            self.quad_list[i].op3 = label
            





    




##########################################################      syntax      ##########################################################




class syntax:

    def __init__(self,file_name):
        self.file_name = file_name
        self.lex = Lex(file_name)
        self.inter = IntermediateCode()


    ###########################################################

    def test_program(self):                                     #NOTE: function to test the syntax of the program
        self.startRule()
        print("\n################################################\n\tProgram is syntactically correct\n################################################")

    ###########################################################

    def startRule(self):
        tkn = self.lex.next_token()                         

        maybe_tkn = self.def_main_part(tkn)                 #calling the def_main_part function        

        if not maybe_tkn:                                   #making sure that the program has a def_main_part
            print("Error  0: no def_main_part found")
            exit(2)
        tkn = maybe_tkn

        maybe_tkn = self.call_main_part(tkn)                #calling the call_main_part function
        if not maybe_tkn:                                   #making sure that the program has a call_main_part                               
            print("Error  1: no call_main_part found")
            exit(2)
        elif not (maybe_tkn.family == "EOF"):               #making sure that the program has no more tokens after the call_main_part
            print("Error  2: unexpected token",maybe_tkn.recognized_string,"at line",maybe_tkn.line_number)
            exit(2)



    def def_main_part(self, tkn):                   

        if not self.def_main_function(tkn):                #making sure that the program has at least one main function 
           return None

        tkn = self.lex.next_token()

        while(self.def_main_function(tkn)):
            tkn = self.lex.next_token()

        return tkn




    def def_main_function(self,tkn):

        if tkn.recognized_string == "def":                    #checking if the token's string is def
            tkn_func = self.lex.next_token()
            if tkn_func.family == "id":                                #checking if the token's family is id
                tkn = self.lex.next_token()
                if tkn.recognized_string == "(":                      #checking if the token's string is (
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == ")":                      #checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":                      #checking if the token's string is :
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "#{":                     #checking if the token's string is #{


                                tkn = self.lex.next_token()

                                tkn = self.declarations(tkn)                        #calling declarations
                                
                                while(self.def_function(tkn)):                      #calling def_function   
                                    tkn = self.lex.next_token()

                                self.inter.genQuad("begin_block", tkn_func.recognized_string, "_", "_")
                                maybe_tkn = self.statements(tkn)                    #calling statements  

                                if maybe_tkn:
                                    tkn = maybe_tkn
                                    if tkn.recognized_string == "#}":                         #checking if the token's string is #}
                                        self.inter.genQuad("end_block", tkn_func.recognized_string, "_", "_")
                                        return True

                                    else:   
                                        print("Error 3: expected #} at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error 4: expected statement at line", tkn.line_number)
                                    exit(2)         
                            else:
                                print("Error 5: expected #{ at line", tkn.line_number)
                                exit(2)
                        else:
                            print("Error 6: expected : at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 7: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 8: expected ( at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 9: expected id at line", tkn_func.line_number)
                exit(2)
        else:
            return False

    

    def def_function(self,tkn):
        
        if tkn.recognized_string == "def":                    #checking if the token's string is def
            tkn_func = self.lex.next_token()
            if tkn_func.family =="id":                                #checking if the token's family is id
                tkn = self.lex.next_token()
                if tkn.recognized_string == "(":                      #checking if the token's string is (
                    tkn = self.lex.next_token()


                    
                    tkn=self.id_list(tkn)                                   #calling id_list                     

                        
                    if tkn.recognized_string == ")":                        #checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":                      #checking if the token's string is :
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "#{":                     #checking if the token's string is #{
                                tkn = self.lex.next_token()
                                

                                tkn = self.declarations(tkn)                         #calling declarations                        


                                while(self.def_function(tkn)):                      #calling def_function

                                    tkn = self.lex.next_token()

                                self.inter.genQuad("begin_block", tkn_func.recognized_string, "_", "_")
                                maybe_tkn = self.statements(tkn)                    #calling statements

                                if maybe_tkn:                                       #if maybe_tkn is not None
                                    tkn = maybe_tkn
                                



                                    if tkn.recognized_string == "#}":                    #checking if the token's string is #}
                                        self.inter.genQuad("end_block", tkn_func.recognized_string, "_", "_")
                                        return True
                                    else:
                                        print("Error 10: expected #} at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error 11: expected statements at line", tkn.line_number)
                                    exit(2)
                            else:
                                print("Error 12: expected #{ at line", tkn.line_number)
                                exit(2)
                        else:
                            print("Error 13: expected : at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 14: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 15: expected ( at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 16: expected id at line", tkn_func.line_number)
                exit(2)
        else:
            return False
            
    





    def declarations(self,tkn):

        while(True):

            maybe_tkn = self.declaration_line(tkn)                  #calling declaration_line

            if maybe_tkn:                                           #if maybe_tkn is not None
                tkn = maybe_tkn
            else:                                                   #if maybe_tkn is None
                return tkn




    def declaration_line(self,tkn):

        if tkn.recognized_string == "#declare":                     #checking if the token's string is #declare
            tkn = self.lex.next_token()
            maybe_tkn = self.id_list(tkn)                           #calling id_list
           
            if maybe_tkn:                                           #if maybe_tkn is not None
                return maybe_tkn
            else:                                                   #if maybe_tkn is None                      
                return tkn

        else:
            return None                                             #returning None if the token's string is not #declare




    def statement(self,tkn):                                                        

        if self.simple_statement(tkn):                              #calling simple_statement 
            return self.lex.next_token()
        else:
            maybe_tkn = self.structured_statement(tkn)              #calling structured_statement
            if maybe_tkn:
                return maybe_tkn
            return None
        




    def statements(self,tkn):

        maybe_tkn = self.statement(tkn)                         #calling statement      
        if not maybe_tkn:                                       #making sure there is at least one statement
            return None

        tkn = maybe_tkn

        while(True):                                    #checking if there are more main  function calls

            maybe_tkn = self.statement(tkn)                     #calling statement
            
            if maybe_tkn:                                       #if maybe_tkn is not None
                tkn = maybe_tkn
            else:                                               #if maybe_tkn is None
                return tkn

        




    def simple_statement(self,tkn):
        
    
        if self.assignment_stat(tkn):                     #calling assignment_stat 
            return True
        elif self.print_stat(tkn):                        #calling print_stat
            return True
        elif self.return_stat(tkn):                       #calling return_stat
            return True
        else:
            return False
        



    def structured_statement(self,tkn):
        
        maybe_tkn = self.if_stat(tkn)                    #calling if_stat
        if maybe_tkn:                                    #if maybe_tkn is not None
            return maybe_tkn
        else:                                            #if maybe_tkn is None
            maybe_tkn = self.while_stat(tkn)             #calling while_stat
            if maybe_tkn:                                #if maybe_tkn is not None
                return maybe_tkn
            return  None



    def assignment_stat(self,tkn):

        if tkn.family == "id":                          # checking if the token's family is id
            tkn = self.lex.next_token()
            if tkn.recognized_string == "=":            # checking if the token's string is =
                tkn = self.lex.next_token()
                maybe_tkn = self.expression(tkn)        # calling expression

                if maybe_tkn:                           # checking if it's an expression and reads it
                    tkn = maybe_tkn
                    if tkn.recognized_string == ";":    # checking if the token's string is ;
                        return True
                    else:
                        print("Error 17: expected ; at line", tkn.line_number)
                        exit(2)
                elif tkn.recognized_string == "int":               # checking if the token's string is int
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == "(":                    # checking if the token's string is (
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == "input":                # checking if the token's string is input
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "(":                    # checking if the token's string is (
                                tkn = self.lex.next_token()
                                if tkn.recognized_string == ")":                    # checking if the token's string is )
                                    tkn = self.lex.next_token()
                                    if tkn.recognized_string == ")":                    # checking if the token's string is )
                                        tkn = self.lex.next_token()
                                        if tkn.recognized_string == ";":                    # checking if the token's string is ;
                                            return True
                                        else:
                                            print("Error 18: expected ; at line", tkn.line_number)
                                            exit(2)
                                    else:
                                        print("Error 19: expected ) at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error 20: expected ) at line", tkn.line_number)
                                    exit(2)
                            else:
                                print("Error 21: expected ( at line", tkn.line_number)
                                exit(2)
                        else:
                            print("Error 22: expected the input keyword at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 23: expected ( at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 24: expected an expression or input method at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 25: expected = at line", tkn.line_number)
                exit(2)
        else:
            return False




    def print_stat(self,tkn):
        if tkn.recognized_string == "print":                        # checking if the token's string is the keyword print
            tkn = self.lex.next_token()
            if tkn.recognized_string == "(":                        # checking if the token's string is (
                tkn = self.lex.next_token()
                maybe_tkn = self.expression(tkn)                    # calling expression
                if maybe_tkn:                                       # checking if it's an expression
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":                # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ";":            # checking if the token's string is ;
                            return True
                        else:
                            print("Error 26: expected ; at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 27: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 28: expected an expression at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 29: expected ( at line", tkn.line_number)
                exit(2)
        else:
            return False



    def return_stat(self,tkn):
        
        if tkn.recognized_string == "return":                       # checking if the token's string is the keyword return
            tkn = self.lex.next_token()
            if tkn.recognized_string == "(":                        # checking if the token's string is (
                tkn = self.lex.next_token()
                maybe_tkn = self.expression(tkn)                    # calling expression
                if maybe_tkn:                                       # checking if it's an expression
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":                # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ";":            # checking if the token's string is ;
                            return True
                        else:
                            print("Error 30: expected ; at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 31: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 32: expected an expression at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 33: expected ( at line", tkn.line_number)
                exit(2)
        else:
            return False





    def if_stat(self,tkn):
           
        if tkn.recognized_string == "if":       # checking if the token's string is the keyword if
            tkn = self.lex.next_token()
            if tkn.recognized_string == "(":        # checking if the token's string is (
                tkn = self.lex.next_token()             # calling next token before going inside any methods
                maybe_tkn = self.condition(tkn)         # calling condition
                if maybe_tkn:                           # checking if it's a condition
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":        # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":        # checking if the token's string is :





                            tkn = self.lex.next_token()                 # calling next token before going inside any methods
                            maybe_tkn= self.statement(tkn)              # calling statement
                            if maybe_tkn:                               # checking if it's a statement 
                                tkn = maybe_tkn   
                                    
                            elif tkn.recognized_string == "#{":         # checking if the token's string is #{
                                tkn2 = self.lex.next_token()                # calling next token before going inside any methods
                                maybe_tkn = self.statements(tkn2)           # calling statements
                                if maybe_tkn:                               # checking if there are statements 
                                    tkn2 = maybe_tkn
                                    if tkn2.recognized_string == "#}":          # checking if the token's string is #}
                                        tkn = self.lex.next_token()
                                        
                                    else:
                                        print("Error 34: expected #} at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error 35: expected statements at line", tkn.line_number)
                                    exit(2)
                            else:
                                print("Error 36: expected a statement or #{ at line", tkn.line_number)
                                exit(2)


                            if tkn.recognized_string == "else":         # checking if the token's string is else
                                tkn = self.lex.next_token()
                                if tkn.recognized_string == ":":        # checking if the token's string is :
                                    tkn = self.lex.next_token()                 # calling next token before going inside any methods
                                    maybe_tkn = self.statement(tkn)             # calling statement

                                    if maybe_tkn:                               # checking if it's a statement
                                        return maybe_tkn
                                    elif tkn.recognized_string == "#{":         # checking if the token's string is #{
                                        tkn = self.lex.next_token()                 # calling next token before going inside any methods
                                        maybe_tkn = self.statements(tkn)            # calling statements
                                        if maybe_tkn:                               # checking if there are statements
                                            tkn = maybe_tkn
                                            if tkn.recognized_string == "#}":           # checking if the token's string is #}
                                                return self.lex.next_token()
                                            else:
                                                print("Error 37: expected #} at line", tkn.line_number)
                                                exit(2)
                                        else:
                                            print("Error 38: expected statements at line", tkn.line_number)
                                            exit(2)
                                    else:
                                        print("Error 39: expected a statement or #{ at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error 40: expected : at line", tkn.line_number)
                                    exit(2)
                            else:
                                return tkn







                        else:
                            print("Error 41: expected : at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 42: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 43: expected a condition at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 44: expected ( at line", tkn.line_number)
                exit(2)
        else:
            return None





    def while_stat(self,tkn):                   
        
        if tkn.recognized_string == "while":        # checking if the token's string is the keyword while
            tkn = self.lex.next_token()
            if tkn.recognized_string == "(":            # checking if the token's string is (
                tkn = self.lex.next_token()                 # calling next token before going inside any methods
                maybe_tkn = self.condition(tkn)             # calling condition
                if maybe_tkn:                                   # checking if it's a condition                        
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":                # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":                # checking if the token's string is :
                            
                            tkn = self.lex.next_token()                     # calling next token before going inside any methods
                            maybe_tkn = self.statement(tkn)                 # calling statement

                            if maybe_tkn:                                   # checking if it's a statement
                                return maybe_tkn
                            elif tkn.recognized_string == "#{":             # checking if the token's string is #{
                                
                                tkn = self.lex.next_token()                     # calling next token before going inside any methods
                                maybe_tkn = self.statements(tkn)                # calling statements
                                if maybe_tkn:                                   # checking if there are statements 

                                    tkn = maybe_tkn
                                    if tkn.recognized_string == "#}":               # checking if the token's string is #}
                                        return self.lex.next_token()
                                    else:
                                        print("Error 45: expected #} at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error 46: expected statements at line", tkn.line_number)
                                    exit(2)
                            else:
                                print("Error 47: expected a statement or #{ at line", tkn.line_number)
                                exit(2)
                        else:
                            print("Error 48: expected : at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 49: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 50: expected a condition at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 51: expected ( at line", tkn.line_number)
                exit(2)
        else:
            return None




    def id_list(self,tkn):

        if tkn.family == "id":                      # checking if the token's family is id
            tkn = self.lex.next_token()
            while tkn.recognized_string == ",":     # checking if the token's string is ,
                tkn = self.lex.next_token()         # calling next token before going inside any methods
                if tkn.family == "id":              # checking if the token's family is id
                    tkn = self.lex.next_token()
                else:
                    print("Error 52: expected an id at line", tkn.line_number)
                    exit(2)
            return tkn
        else:
            return tkn








    def expression(self,tkn):
       
        tkn = self.optional_sign(tkn)                                   # checking if it's an optional_sign
        
        maybe_term = self.term(tkn)                                      # calling term
        maybe_tkn = maybe_term[0]

        if maybe_tkn:                                                   # checking if it's a term
            tkn = maybe_tkn


            while tkn.family == "addOperator":                          # checking if the token's family is addOperator
                tkn = self.lex.next_token()                             # calling next token before going inside any methods
                maybe_tkn=self.term(tkn)                                # calling term
                if maybe_tkn:                                           # checking if it's a term
                    tkn = maybe_tkn
                else:
                    print("Error 53: expected a term at line", tkn.line_number)
                    exit(2)
            return tkn
        else:
            return None

    




    def term(self,tkn):
            
        maybe_tkn = self.factor(tkn)
        if maybe_tkn:                                           # checking if it's a factor       
            tkn = maybe_tkn
            while tkn.family == "mulOperator":                  # checking if the token's family is mulOperator
                tkn = self.lex.next_token()                     # calling next token before going inside any methods
                maybe_tkn = self.factor(tkn)
                if maybe_tkn:                                   # checking if it's a factor
                    tkn = maybe_tkn
                else:
                    print("Error 54: expected a factor at line", tkn.line_number)
                    exit(2)
            return tkn
        else:
            return None




    def factor(self,tkn):
        
        if tkn.family == "number":                              # checking if the token's family is number
            return self.lex.next_token()

        elif tkn.recognized_string == "(":                      # checking if the token's string is (
            tkn = self.lex.next_token()
            maybe_tkn = self.expression(tkn)                    # calling expression
            if maybe_tkn:
                tkn = maybe_tkn
                if tkn.recognized_string == ")":                # checking if the token's string is )
                    return self.lex.next_token()
                else:
                    print("Error 55: expected ) at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 56: expected expression at line", tkn.line_number)
                exit(2)
            
        elif tkn.family == "id":                                # checking if the token's family is id
            tkn = self.lex.next_token()
            return self.idtail(tkn)

        else:                                                   # if none of the above           
            return None 




    def idtail(self,tkn):

        if tkn.recognized_string == "(":                            # checking if the token's string is (
            tkn = self.lex.next_token()                             # calling next token before going inside any methods
            maybe_tkn = self.actual_par_list(tkn)                   # calling actual_par_list
            if maybe_tkn:                                           # if maybe_tkn is not None
                tkn = maybe_tkn
                if tkn.recognized_string == ")":                    # checking if the token's string is )
                    return self.lex.next_token()
                else:
                    print("Error 57: expected ) at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 58: expected actual_par_list at line", tkn.line_number)
                exit(2)
        else:
            return tkn    
        





    def actual_par_list(self,tkn):


        maybe_tkn = self.expression(tkn)                            #calling expression


        if maybe_tkn:                               
            tkn = maybe_tkn
            while tkn.recognized_string == ",":     
                tkn = self.lex.next_token()    

                maybe_tkn = self.expression(tkn)                     #calling expression     
                if maybe_tkn:              
                    tkn = maybe_tkn
                else:
                    print("Error 59: expected an expression at line", tkn.line_number)
                    exit(2)
            return tkn
        else:
            return tkn





    def optional_sign(self,tkn):
        
        if tkn.family == "addOperator":
            return self.lex.next_token()
        else:
            return tkn
        
    


    def condition(self,tkn):
        
        maybe_tkn=self.bool_term(tkn)                             #calling bool_term
        if maybe_tkn:
            tkn=maybe_tkn
            while tkn.recognized_string == "or":                  # checking if the token's string is or
                tkn=self.lex.next_token()
                maybe_tkn=self.bool_term(tkn)                     #calling bool_term
                if maybe_tkn:
                    tkn=maybe_tkn
                else:
                    print("Error 60: expected a bool_factor at line", tkn.line_number)
                    exit(2)
            return tkn
        else:
            return None





    def bool_term(self,tkn):
        
        maybe_tkn=self.bool_factor(tkn)                             #calling bool_factor
        if maybe_tkn:
            tkn=maybe_tkn
            while tkn.recognized_string == "and":                   # checking if the token's string is and
                tkn=self.lex.next_token()
                maybe_tkn=self.bool_factor(tkn)                     #calling bool_factor
                if maybe_tkn:
                    tkn=maybe_tkn
                else:
                    print("Error 61: expected a bool_factor at line", tkn.line_number)
                    exit(2)
            return tkn
        else:
            return None



    def bool_factor(self,tkn):

        if tkn.recognized_string == "not":
            tkn=self.lex.next_token()
            if tkn.recognized_string == "[":
                tkn=self.lex.next_token()
                maybe_tkn=self.condition(tkn)                   #calling condition
                if maybe_tkn:
                    tkn=maybe_tkn
                    if tkn.recognized_string == "]":
                        return self.lex.next_token()
                    else:
                        print("Error 62: expected ] at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 63: expected a condition at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 64: expected [ at line", tkn.line_number)
                exit(2)
        elif tkn.recognized_string == "[":
            tkn=self.lex.next_token()
            maybe_tkn=self.condition(tkn)                       #calling condition
            if maybe_tkn:
                tkn=maybe_tkn
                if tkn.recognized_string == "]":
                    return self.lex.next_token()
                else:
                    print("Error 65: expected ] at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 66: expected a condition at line", tkn.line_number)
                exit(2)
        else:
            maybe_tkn=self.expression(tkn)                      #calling expression
            if maybe_tkn:
                tkn=maybe_tkn
                if tkn.family == "relOperator":                 #checking if the token's family is relOperator
                    tkn=self.lex.next_token()
                    maybe_tkn=self.expression(tkn)              #calling expression
                    if maybe_tkn:
                        return maybe_tkn
                    else:
                        print("Error 67: expected an expression at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 68: expected a relOperator at line", tkn.line_number)
                    exit(2)
            else:
                return None





    def call_main_part(self,tkn):
        
        if tkn.recognized_string == "if":
            tkn = self.lex.next_token()
            if tkn.recognized_string == "__name__":
                tkn = self.lex.next_token()
                if tkn.recognized_string == "==":
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == "\"__main__\"":
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":
                            tkn = self.lex.next_token()


                            if not self.main_function_call(tkn):                #making sure that the program has at least one main function
                                print("Error 69: no main function call found at line", tkn.line_number)
                                exit(2)

                            tkn = self.lex.next_token()

                            while(self.main_function_call(tkn)):                 #checking if there are more main  function calls
                                tkn = self.lex.next_token()
                            
                            return tkn
        

                        else:
                            print("Error 70: expected : at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error 71: expected \"__main__\" at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 72: expected == at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 73: expected __name__ at line", tkn.line_number)
                exit(2)
        else:
            return None

            

    



    def main_function_call(self, tkn_func):

        if tkn_func.family == "id":                                  # checking if the token's family is id
            tkn = self.lex.next_token()
            if tkn.recognized_string == "(":                    # checking if the token's string is (
                tkn = self.lex.next_token()
                if tkn.recognized_string == ")":                # checking if the token's string is )
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == ";":
                        self.inter.genQuad("call", tkn_func.recognized_string, "_", "_")
                        return True
                    else:
                        print("Error 74: expected ; at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 75: expected ) at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 76: expected ( at line", tkn.line_number)
                exit(2)
        else:
            return False


     
           

if  __name__ == '__main__':
    
    file_name = ""
    try: 
        file_name = sys.argv[1]

    except:
        print("############# NO ARGS were passed #############")
        f_name_in = input("Enter number or file name: \n\n 1: test1.cpy\n 2: test2.cpy\n 3: test3.cpy\n 4: test4.cpy\n 5: test5.cpy\n or enter file path \n\n")
        

        if(f_name_in == "1"):
            file_name = "test1.cpy"
        elif(f_name_in == "2"):
            file_name = "test2.cpy"
        elif(f_name_in == "3"):
            file_name = "test3.cpy"
        elif(f_name_in == "4"):
            file_name = "test4.cpy"
        elif(f_name_in == "5"):
            file_name = "test5.cpy"
        else:
            file_name = f_name_in

    syn = syntax(file_name)

    syn.test_program()
    for q in syn.inter.quad_list:
        print(q)


    #--------------------for testing the lex--------------------#
    #lex = Lex("test.txt")
    #for i in range(100):

        #tnk=lex.next_token()
        #print("token:",tnk.family,tnk.recognized_string,tnk.line_number)
    #syn=syntax("test.txt")


  
