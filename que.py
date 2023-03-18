import string



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
        self.keyword_set={"def","not","and","or","declare","print","return","if","else","while","int","input"}                   #TODO
        self.final_state_set=   {  
                                    2:"number",
                                    4:"id",         
                                    5:"addOparator",
                                    6:"mulOp",
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
        state=0
        rec_string=""
        white_char_offset = 0
        line_offset = 0

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

                    #print("current line:", self.current_line)

                if in_read == "":                           # if eof
                    in_id = 23
                    
                else:
                    in_id = 22                              # if white character except eof
            elif in_read in self.symbol_dict:
                in_id = self.symbol_dict[in_read]
                rec_string+=in_read                         # adding character to the recognised string
            else:

                
                rec_string+=in_read+file.read(9)                       # reading the next 9 characters to see if rec_string is "__main__"
                #print("teeeeeeeest:",rec_string)
                if rec_string=="\"__main__\"":
                    self.current_char = file.tell()
                    file.close()
                    return Token("keyword", rec_string, self.current_line+line_offset)
                
                print("Error: unknown character", in_read, "at line", self.current_line)
                file.close()
                exit(1)

            state = self.state_list[state][in_id]
            
                               
            
            #print(in_read)
            #print(state)

            if state == 0:                                        #NOTE: maybe improveivanb;ele
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
                        print("Error: ID", rec_string, "at line", self.current_line, "is too long (max 30 characters)")
                        exit(1)
                
                #elif state==2 and (int(rec_string)<-(2**32-1) or int(rec_string)>2**32-1):                       #making sure that number is between -(2^32)-1 and 2^32-1                                 
                    #print("Error: NUMBER", rec_string, "at line", self.current_line, "is out of range (-(2^32)-1 to 2^32-1)")
                    #exit(1)


                return Token(self.final_state_set[state], rec_string, self.current_line+line_offset)              # return token
                
            elif state == 99:                                    # if error


                rec_string+=file.read(6)                            # reading the next 6 characters to see if rec_string is  #declare
                #print("teeeeeeeest:",rec_string,"teeeeeeeest:")

                if rec_string=="#declare":
                    self.current_char = file.tell()
                    file.close()
                    return Token("keyword", rec_string, self.current_line+line_offset)
                
                else:
                    rec_string+=file.read(1)                       # reading the next character to see if rec_string is __name__
                    if rec_string=="__name__":
                        self.current_char = file.tell()
                        file.close()
                        return Token("keyword", rec_string, self.current_line+line_offset)



                
                print("Error: unexpected character", in_read, "at line", self.current_line)             #if nothing from the above then its an error
                file.close()
                exit(1)     




#############################################################################################################



class syntax:

    def __init__(self,file_name):
        self.file_name = file_name
        self.lex = Lex(file_name)
        self.tkn_queue = []







    def startRule(self):
        self.def_main_part()
        self.call_main_part()



    def def_main_part(self):

        if not self.def_main_function():                #making sure that the program has at least one main function
            print("Error: no main function found")
            exit(2)

        while(self.def_main_function()):
            pass




    def def_main_function(self,tkn_):
        
        tkn= self.tkn_queue.pop(0) if self.tkn_queue else self.lex.next_token()         


        if tkn.recognized_string == "def":                    #checking if the token's string is def
            tkn = self.lex.next_token()
            if tkn.family == "id":                                #checking if the token's family is id
                tkn = self.lex.next_token()
                if tkn.recognized_string == "(":                      #checking if the token's string is (
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == ")":                      #checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":                      #checking if the token's string is :
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "#{":                     #checking if the token's string is #{


                               
                               
                                if tkn.recognized_string == "#}":                         #checking if the token's string is #}
                                    return True
                                else:
                                    print("Error: expected #} at line", tkn.line_number)
                                    exit(2)
                            else:
                                print("Error: expected #{ at line", tkn.line_number)
                                exit(2)
                        else:
                            print("Error: expected : at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error: expected ) at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error: expected ( at line", tkn.line_number)
                    exit(2)
            else:
                print("Error: expected id at line", tkn.line_number)
                exit(2)
        else:
            return False

    

    def def_function(self,tkn_):
        tkn = tkn_
        if tkn.recognized_string =="def":                    #checking if the token's string is def
            tkn = self.lex.next_token()
            if tkn.family=="id":                                #checking if the token's family is id
                tkn = self.lex.next_token()
                if tkn.recognized_string == "(":                      #checking if the token's string is (
                    tkn = self.lex.next_token()
                    if self.id_list(tkn):                                   #calling id_list                         #NOTE
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ")":                      #checking if the token's string is )
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == ":":                      #checking if the token's string is :
                                tkn = self.lex.next_token()
                                if tkn.recognized_string == "#{":                     #checking if the token's string is #{
                                    
                                    tkn = self.lex.next_token()
                                    #NOTE
                                    if self.declarations(tkn):                                  #calling declarations
                                        tkn=self.lex.next_token()
                                        
                                        while(self.def_function(tkn)):
                                            tkn=self.lex.next_token()
                                        if(self.statements()):                                  #calling statements
                                            tkn=self.lex.next_token()
                                        
                                            if tkn.recognized_string == "#}":                         #checking if the token's string is #}
                                                return True
                                            else:
                                                print("Error: expected #} at line", tkn.line_number)
                                                exit(2)
                                        else:
                                            print("Error: expected statements at line", tkn.line_number)
                                            exit(2)
                                    else:
                                        print("Error: expected declarations at line", tkn.line_number)
                                        exit(2)
                                else:
                                    print("Error: expected #{ at line", tkn.line_number)
                                    exit(2)
                            else:
                                print("Error: expected : at line", tkn.line_number)
                                exit(2)
                        else:
                            print("Error: expected ) at line", tkn.line_number)
                            exit(2)
                    else:
                        print("Error: expected id at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error: expected ( at line", tkn.line_number)
                    exit(2)
            else:
                print("Error: expected id at line", tkn.line_number)
                exit(2)
        else:
            return False
            
    



    def declarations(self,tkn):

        while(True):

            maybe_tkn= self.declaration_line(tkn)
            if maybe_tkn:
                return maybe_tkn
            else:
                return self.lex.next_token()

    



    def declaration_line(self,tkn):

        if tkn.recognized_string == "#declare":                     #checking if the token's string is #declare
            tkn = self.lex.next_token()
            maybe_tkn=self.id_list(tkn)                                          #calling id_list
            if maybe_tkn:
                return maybe_tkn
            else:
                return self.lex.next_token()

        else:
            return None                                             #returning None if the token's string is not #declare




    def statement(self):
        tkn=self.lex.next_token()

        if (self.simple_statement(tkn)):
            return True
        elif (self.structured_statement(tkn)):
            return True





    def statements(self):
        pass

    def simple_statement(self,tkn_):
        pass

    def structured_statement(self,tkn_):
        pass

    def assignment_stat(self):
        pass

    def print_stat(self):
        pass

    def return_stat(self):
        pass

    def if_stat(self):
        pass

    def while_stat(self):
        pass

    def id_list(self):
        pass

    def expression(self):
        pass

    def term(self):
        pass

    def factor(self):
        pass

    def idtail(self):
        pass

    def actual_par_list(self):
        pass

    def optional_sign(self):
        pass

    #def

        


    def test(self,tkn):
        tkn=self.lex.next_token()
        tkn=self.lex.next_token()



          
           

if  __name__ == '__main__':
    lex = Lex("test.txt")


    #for i in range(100):

        #tnk=lex.next_token()
        #print("token:",tnk.family,tnk.recognized_string,tnk.line_number)
    #syn=syntax("test.txt")
  
