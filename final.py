#####################################################################
                # Christos Vasilakos    4857    cse94857
                # Emmanouil Smyrnakis   4793    cse94793
#####################################################################


import string
import sys




class Token:
    #Α
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



    def backpatch(self, list, label):

        for i in list:
            self.quad_list[i].op3 = label
            

##########################################################      symbol table     ##########################################################

class Entity:

    def __init__(self, name):
        self.name = name



class Constant(Entity):

    def __init__(self, name, data_type, value):
        super().__init__(name)
        self.data_type = data_type
        self.value = value

    def __str__(self):
        return "Constant:\t" + str(self.name) + "/" + str(self.data_type) + "/" + str(self.value)

class Variable(Entity):
    
        def __init__(self, name, data_type, offset):
            super().__init__(name)
            self.data_type = data_type
            self.offset = offset

        def __str__(self):
            return "Variable:\t" + str(self.name) + "/" + str(self.data_type) + "/" + str(self.offset)

class FormalParameter(Entity):

    def __init__(self, name, data_type, mode):
        super().__init__(name)
        self.data_type = data_type
        self.mode = mode

    def __str__(self):
        return str(self.name) + "/" + str(self.data_type) + "/" + str(self.mode)

class Procedure(Entity):

    def __init__(self, name):
        super().__init__(name)
        self.starting_quad = None
        self.frame_length = None
        self.formal_parameters = []

    def __str__(self):

        form_par_str = ""
        if len(self.formal_parameters) != 0:
            form_par_str = "/ ["
            for i in self.formal_parameters:
                form_par_str += str(i) + " , "
            form_par_str += "\b\b\b] "
        return "Main function:\t" + str(self.name) + "/" + str(self.starting_quad) + "/" + str(self.frame_length) + form_par_str


    


class TemporaryVariable(Variable):
        
    def __init__(self, name, data_type, offset):
        super().__init__(name, data_type, offset)

    def __str__(self):
        return "Temporary variable:\t" + str(self.name) + "/" + str(self.data_type) + "/" + str(self.offset)

class Parameter(FormalParameter):

    def __init__(self, name, data_type, mode, offset):
        super().__init__(name, data_type, mode)
        self.offset = offset

    def __str__(self):
        return "Parameter:\t" + str(self.name) + "/" + str(self.data_type) + "/" + str(self.mode) + "/" + str(self.offset)

class Function(Procedure):
    
        def __init__(self, name, data_type):
            super().__init__(name)
            self.data_type = data_type

        def __str__(self):

            form_par_str = ""
            if len(self.formal_parameters) != 0:
                form_par_str = "/ ["
                for par in self.formal_parameters:
                    form_par_str += str(par) + " , "
                form_par_str += "\b\b\b] "
            return "Function:\t" + str(self.name) + "/" + str(self.starting_quad) + "/" + str(self.frame_length) +  form_par_str + "/" + str(self.data_type)





########################

class Scope:

    def __init__(self, level):
        self.level = level
        self.entity_list = []

    def __str__(self):
        ent_lst_str = ""
        for entity_ in self.entity_list:
            ent_lst_str += "\t" + str(entity_) + "\n"
        return "level " + str(self.level) + ":\n" + ent_lst_str
    
    


########################

class SymbolTable:

    def __init__(self):
        self.scope_list = []
    
    def addEntity(self, entity):
        self.scope_list[-1].entity_list.append(entity)

    def addScope(self):
        scope = Scope(len(self.scope_list))
        self.scope_list.append(scope)
       
    def removeScope(self):
        self.scope_list.pop()

    def updateField(self, next_quad):
        count = 0
        if next_quad:
            self.scope_list[-2].entity_list[-1].starting_quad = next_quad
        else:
            for entity_ in self.scope_list[-1].entity_list:
                if isinstance(entity_, Procedure):
                    continue
                count += 1

            self.scope_list[-2].entity_list[-1].frame_length = 12 + 4*count

    def addFormalParameter(self, formal_parameter):
        self.scope_list[-2].entity_list[-1].formal_parameters.append(formal_parameter)

    def searchEntity(self, name):
        for scope in reversed(self.scope_list):
            for entity in reversed(scope.entity_list):
                if entity.name == name:
                    return [entity, scope.level]
        print("Error 77: entity", name, "not found")
        exit(4)
    

    def __str__(self):
        str_ret = ""
        for scope in self.scope_list:
            str_ret += str(scope) + "\n"
        str_ret += "-------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        return str_ret


##########################################################      final code     ##########################################################


class FinalCode:

    def __init__(self, sym, inter, assembly_file):
        self.sym = sym
        self.inter = inter
        self.assembly_file = assembly_file
        self.quad_counter = 0
        self.produce(".data \n\tstr_nl: .asciz \"\\n\" \n\t.text\n")
        self.produce("j Lmain")


    def produce(self, to_produce):

        self.assembly_file.write("\t" + to_produce + "\n")


    def gnlvcode(self, v):

        var_info = self.sym.searchEntity(v)

        if isinstance(var_info[0],Procedure):
            print("Error 78: variable", v, "has the same name as a procedure or function")
            exit(5)

        current_level = self.sym.scope_list[-1].level


        if var_info[1] == current_level:

            self.produce("addi t0, sp, -" + str(var_info[0].offset))
        else:
            self.produce("lw t0, -4(sp)")
            current_level -= 1
            while var_info[1] != current_level:
                self.produce("lw t0, -4(t0)")
                current_level -= 1
            self.produce("addi t0, t0, -" + str(var_info[0].offset))



    def loadvr(self, v, reg):

        if v.isnumeric() or v[0] == "-":                                                                   # if v is an Integer
            self.produce("li " + str(reg) + ", " + str(v))
        else:
            v_info = self.sym.searchEntity(v)                                                   # search in the symbol table for the variable v
            if (v_info[1] == 1) and (not isinstance(v_info[0], TemporaryVariable)):             # if v is a global variable                                                      # if v in the first scope
                self.produce("lw " + str(reg) + ", -" + str(v_info[0].offset) + "(gp)")

            elif v_info[1] == self.sym.scope_list[-1].level:                                    # if v is in the current scope
                self.produce("lw " + str(reg) + ", -" + str(v_info[0].offset) + "(sp)")

            else:                                                                               # if v is a parent's variable
                self.gnlvcode(v)
                self.produce("lw " + str(reg) + ", " + "(t0)")



    def storerv(self, reg, v):
        if reg.isnumeric():                                                                 # if v is an Integer
            self.loadvr(str(reg), "t0")
            self.storerv("t0", str(v))

        else:
            v_info = self.sym.searchEntity(v)                                                   # search in the symbol table for the variable v
            if (v_info[1] == 1) and (not isinstance(v_info[0], TemporaryVariable)):             # if v is a global variable
                self.produce("sw " + str(reg) + ", -" + str(v_info[0].offset) + "(gp)")
            elif v_info[1] == self.sym.scope_list[-1].level:                                    # if v is in the current scope
                self.produce("sw " + str(reg) + ", -" + str(v_info[0].offset) + "(sp)")
            else:                                                                               # if v is a parent's variable
                self.gnlvcode(v)
                self.produce("sw " + str(reg) + ", " + "(t0)")

    def inter_to_final(self):

        par_counter = 8

        for qd in self.inter.quad_list[self.quad_counter:]:

            self.assembly_file.write("L" + str(self.quad_counter) + ":\n")
            self.quad_counter += 1

            qd_operator = qd.operator
            if qd_operator == "jump":
                self.produce("j L" + str(qd.op3))

            elif qd_operator == "ret":
                self.loadvr(qd.op1, "t1")
                self.produce("lw t0, -8(sp)")
                self.produce("sw t1, (t0)")

                self.produce("lw ra,(sp)")
                self.produce("jr ra")

            elif qd_operator == "par":
                par_counter += 4
                temp_count = self.quad_counter

                while self.inter.quad_list[temp_count].operator != "call":
                    temp_count += 1
                func_name = self.inter.quad_list[temp_count].op1

                func_info = self.sym.searchEntity(func_name)
                frame_length = func_info[0].frame_length

                if par_counter == 12:                                   # changes the fp only the first time (at the first par)
                    self.produce("addi fp, sp, " + str(frame_length))

                if qd.op2 == "ret":
                    v_info = self.sym.searchEntity(qd.op1)
                    self.produce("addi t0, sp, -" + str(v_info[0].offset))
                    self.produce("sw t0, -8(fp)")
                else:
                    self.loadvr(qd.op1, "t0")
                    self.produce("sw t0, -" + str(par_counter) + "(fp)")




            elif qd_operator == "call":

                par_counter = 8
                func_info = self.sym.searchEntity(qd.op1)

                if self.inter.quad_list[self.quad_counter-1].operator != "par":         # if the fuction has no parameters or a return value,
                    self.produce("addi fp, sp, " + str(func_info[0].frame_length))      # then we set the fp as it would not have been set before

                self.produce("sw sp,-4(fp)")
                self.produce("addi sp, sp, " + str(func_info[0].frame_length))
                self.produce("jal L" + str(func_info[0].starting_quad-1))
                self.produce("addi sp, sp, -" + str(func_info[0].frame_length))



            elif qd_operator == "halt":
                self.produce("li a0, 0")
                self.produce("li a7, 93")
                self.produce("ecall")

            elif qd_operator == "begin_block":
                if qd.op1 == "main_program":
                    self.assembly_file.write("Lmain:\n")
                    self.produce("addi sp, sp, 12")
                    self.produce("mv gp, sp")
                else:
                    self.produce("sw ra,(sp)")

            elif qd_operator == "end_block":
                if qd.op1 != "main_program":
                    self.produce("lw ra,(sp)")
                    self.produce("jr ra")


            elif qd_operator == "inp":
                self.produce("li a7, 5")
                self.produce("ecall")
                self.storerv("a0", qd.op1)

            elif qd_operator == "out":

                self.loadvr(qd.op1, "a0")
                self.produce("li a7, 1")
                self.produce("ecall")

                self.produce("la a0, str_nl")
                self.produce("li a7, 4")
                self.produce("ecall")




            elif qd_operator == "=":
                self.loadvr(qd.op1, "t1")
                self.storerv("t1", qd.op3)




            elif qd_operator == "+":

                if qd.op1.isnumeric():                              # if op1 is numeric
                    self.loadvr(qd.op2, "t0")
                    self.produce("addi t1, t0, " + str(qd.op1))
                    self.storerv("t1", qd.op3)

                elif qd.op2.isnumeric():                            # if op2 is numeric
                    self.loadvr(qd.op1, "t0")
                    self.produce("addi t1, t0, " + str(qd.op2))
                    self.storerv("t1", qd.op3)

                else:
                    self.loadvr(qd.op1, "t0")
                    self.loadvr(qd.op2, "t1")
                    self.produce("add t2, t0, t1")
                    self.storerv("t2", qd.op3)

            elif qd_operator == "-":

                if qd.op2.isnumeric():                            # if op2 is numeric
                    self.loadvr(qd.op1, "t0")
                    self.produce("addi t1, t0, -" + str(qd.op2))
                    self.storerv("t1", qd.op3)

                else:
                    self.loadvr(qd.op1, "t0")
                    self.loadvr(qd.op2, "t1")
                    self.produce("sub t2, t0, t1")
                    self.storerv("t2", qd.op3)

            elif qd_operator == "*":

                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("mul t2, t0, t1")
                self.storerv("t2", qd.op3)

            elif qd_operator == "//":

                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("div t2, t0, t1")
                self.storerv("t2", qd.op3)


            elif qd_operator == "<":
                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("blt " + "t0" + ", " + "t1" + ", " + "L" + str(qd.op3))

            elif qd_operator == ">":
                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("bgt " + "t0" + ", " + "t1" + ", " + "L" + str(qd.op3))

            elif qd_operator == "!=":
                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("bne " + "t0" + ", " + "t1" + ", " + "L" + str(qd.op3))

            elif qd_operator == "==":
                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("beq " + "t0" + ", " + "t1" + ", " + "L" + str(qd.op3))

            elif qd_operator == "<=":
                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("ble " + "t0" + ", " + "t1" + ", " + "L" + str(qd.op3))

            elif qd_operator == ">=":
                self.loadvr(qd.op1, "t0")
                self.loadvr(qd.op2, "t1")
                self.produce("bge " + "t0" + ", " + "t1" + ", " + "L" + str(qd.op3))

            else:
                print("Error  0:  Unknown operator in intermediate code")
                self.produce("Error  0:  Unknown operator in intermediate code")
                exit(5)

            self.produce("")





##########################################################      syntax      ##########################################################




class syntax:

    def __init__(self,file_name):
        self.file_name = file_name
        self.lex = Lex(file_name)
        self.inter = IntermediateCode()
        self.sym = SymbolTable()
        self.assembly_file = open("a.asm", "w")
        self.final = FinalCode(self.sym, self.inter, self.assembly_file)



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
        self.assembly_file.close()                          #closing the assembly file



    def def_main_part(self, tkn):                   

        print("\n############################################################\nSymbol Table (prints at the end of every function/procedure)\n############################################################\n")
        self.sym.addScope()                                 #adding a new scope to the symbol table
        if not self.def_main_function(tkn):                 #making sure that the program has at least one main function
           return None

        tkn = self.lex.next_token()

        while(self.def_main_function(tkn)):
            tkn = self.lex.next_token()

        self.final.inter_to_final()                         #calling the inter_to_final function
        return tkn




    def def_main_function(self,tkn):

        if tkn.recognized_string == "def":                      #checking if the token's string is def
            tkn_func = self.lex.next_token()
            if tkn_func.family == "id":                             #checking if the token's family is id
                tkn = self.lex.next_token()
                if tkn.recognized_string == "(":                        #checking if the token's string is (
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == ")":                        #checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":                        #checking if the token's string is :
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "#{":                       #checking if the token's string is #{

                                self.sym.addEntity(Procedure(tkn_func.recognized_string))               #adding the procedure to the symbol table

                                self.sym.addScope()                                                     #adding a new scope to the symbol table
                                tkn = self.lex.next_token()



                                decl_lines = self.declarations(tkn)                                     # calling declarations
                                tkn = decl_lines[0]

                                offset_count = 12
                                for var_ in decl_lines[1]:                                              # for every variable in the list of declarations
                                    self.sym.addEntity(Variable(var_, "int", offset_count))             # adding the variable to the symbol table
                                    offset_count += 4



                                
                                while self.def_function(tkn):                                           #calling def_function
                                    tkn = self.lex.next_token()

                                self.inter.genQuad("begin_block", tkn_func.recognized_string, "_", "_") #generating the intermediate code for the begin block
                                self.sym.updateField(self.inter.nextQuad())                       # updating the field of the main function in the symbol table
                                maybe_tkn = self.statements(tkn)                                        #calling statements



                                if maybe_tkn:
                                    tkn = maybe_tkn
                                    if tkn.recognized_string == "#}":                                       #checking if the token's string is #}
                                        self.inter.genQuad("end_block", tkn_func.recognized_string, "_", "_")   #generating the intermediate code for the end block

                                        print(self.sym)                                                         #printing the symbol table

                                        self.sym.updateField(None)                                       # updating the field of the procedure in the symbol table
                                        self.final.inter_to_final()                                             # calling the inter_to_final function
                                        self.sym.removeScope()                                                  #removing the scope from the symbol table

                                        print(self.sym)                                                         #printing the symbol table

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
        
        if tkn.recognized_string == "def":                                  #checking if the token's string is def
            tkn_func = self.lex.next_token()
            if tkn_func.family =="id":                                          #checking if the token's family is id
                tkn = self.lex.next_token()
                if tkn.recognized_string == "(":                                    #checking if the token's string is (
                    tkn = self.lex.next_token()

                    self.sym.addEntity(Function(tkn_func.recognized_string, "int")) #adding the function to the symbol table
                    self.sym.addScope()                                             #creating a new scope

                    ret_id_list = self.id_list(tkn)                                 #calling id_list
                    tkn = ret_id_list[0]

                    offset_count = 12
                    for parameter in ret_id_list[1]:                               #for every element in the list of id_list
                        form_par = FormalParameter(parameter, "int", "cv")              #creating a new FormalParameter
                        self.sym.addFormalParameter(form_par)                           #adding the FormalParameter to the FormalParameter list of the function/procedure
                        actual_par = Parameter(parameter, "int", "cv", offset_count)    #creating a new Parameter
                        offset_count += 4
                        self.sym.addEntity(actual_par)                                  #adding the FormalParameter to the symbol table
                        
                    if tkn.recognized_string == ")":                        #checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":                        #checking if the token's string is :
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "#{":                       #checking if the token's string is #{
                                tkn = self.lex.next_token()
                                

                                decl_lines = self.declarations(tkn)                         #calling declarations
                                tkn = decl_lines[0]

                                for var_ in decl_lines[1]:                                  #for every variable in the list of declarations

                                    self.sym.addEntity(Variable(var_, "int", offset_count)) #adding the variable to the symbol table
                                    offset_count += 4

                                while self.def_function(tkn):                               #calling def_function

                                    tkn = self.lex.next_token()

                                self.inter.genQuad("begin_block", tkn_func.recognized_string, "_", "_") #generating the intermediate code for the begin block
                                self.sym.updateField(self.inter.nextQuad())                       # updating the starting quad field of the main function in the symbol table
                                maybe_tkn = self.statements(tkn)                                        #calling statements

                                if maybe_tkn:                                                           #if maybe_tkn is not None
                                    tkn = maybe_tkn
                                

                                    if tkn.recognized_string == "#}":                    #checking if the token's string is #}
                                        self.inter.genQuad("end_block", tkn_func.recognized_string, "_", "_")   #generating the intermediate code for the end block

                                        print(self.sym)

                                        self.sym.updateField(None)               # updating the framelength field of the procedure in the symbol table
                                        self.final.inter_to_final()                     # calling the inter_to_final function
                                        self.sym.removeScope()                          #removing the scope

                                        print(self.sym)                                 #printing the symbol table
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
            
    





    def declarations(self,tkn):             #returns [token, [id_lists]]

        decl_ret = []
        while True:

            decl_lst = self.declaration_line(tkn)                  #calling declaration_line

            maybe_tkn = decl_lst[0]
            decl_ret += decl_lst[1]

            if maybe_tkn:                                           #if maybe_tkn is not None
                tkn = maybe_tkn
            else:                                                   #if maybe_tkn is None
                return [tkn, decl_ret]                              #returning the token and the list of id_list




    def declaration_line(self,tkn):             #returns [token, [id_list]]

        if tkn.recognized_string == "#declare":                     #checking if the token's string is #declare
            tkn = self.lex.next_token()
            ret_id_list = self.id_list(tkn)                         #calling id_list
            maybe_tkn = ret_id_list[0]

            if maybe_tkn:
                return [maybe_tkn, ret_id_list[1]]
            else:                                                       #if maybe_tkn is None
                return [tkn, []]

        else:
            return [None, []]                                           #returning None if the token's string is not #declare




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



    def assignment_stat(self, tkn):

        target = tkn.recognized_string
        if tkn.family == "id":                                      # checking if the token's family is id
            tkn = self.lex.next_token()
            if tkn.recognized_string == "=":                            # checking if the token's string is =
                tkn = self.lex.next_token()
                maybe_expression = self.expression(tkn)                     # calling expression
                maybe_tkn = maybe_expression[0]
                if maybe_tkn:                                               # checking if it's an expression and reads it
                    tkn = maybe_tkn
                    if tkn.recognized_string == ";":                            # checking if the token's string is ;

                        self.inter.genQuad("=", maybe_expression[1], "_", target)   # generating the intermediate code for the assignment statement
                        return True
                    else:
                        print("Error 17: expected ; at line", tkn.line_number)
                        exit(2)
                elif tkn.recognized_string == "int":                        # checking if the token's string is int
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == "(":                            # checking if the token's string is (
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == "input":                        # checking if the token's string is input
                            tkn = self.lex.next_token()
                            if tkn.recognized_string == "(":                            # checking if the token's string is (
                                tkn = self.lex.next_token()
                                if tkn.recognized_string == ")":                            # checking if the token's string is )
                                    tkn = self.lex.next_token()
                                    if tkn.recognized_string == ")":                            # checking if the token's string is )
                                        tkn = self.lex.next_token()
                                        if tkn.recognized_string == ";":                            # checking if the token's string is ;

                                            self.inter.genQuad("inp", target, "_", "_")                 #generating the quad

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
            if tkn.recognized_string == "(":                            # checking if the token's string is (
                tkn = self.lex.next_token()
                maybe_expression = self.expression(tkn)                     # calling expression
                maybe_tkn = maybe_expression[0]
                if maybe_tkn:                                               # checking if it's an expression
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":                            # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ";":                            # checking if the token's string is ;

                            self.inter.genQuad("out", maybe_expression[1], "_", "_")    # generating the intermediate code for the print statement
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
            if tkn.recognized_string == "(":                            # checking if the token's string is (
                tkn = self.lex.next_token()
                maybe_expression = self.expression(tkn)                     # calling expression
                maybe_tkn = maybe_expression[0]
                if maybe_tkn:                                               # checking if it's an expression
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":                            # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ";":                            # checking if the token's string is ;
                            self.inter.genQuad("ret",maybe_expression[1],"_","_")   # generating the intermediate code for the return statement
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
                maybe_condition = self.condition(tkn)   # calling condition
                maybe_tkn = maybe_condition[0]

                if maybe_tkn:                           # checking if it's a condition
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":        # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":        # checking if the token's string is :

                            self.inter.backpatch(maybe_condition[1], self.inter.nextQuad())  # backpatching the true list with the next quad

                            tkn = self.lex.next_token()             # calling next token before going inside any methods
                            maybe_tkn = self.statement(tkn)         # calling statement
                            if maybe_tkn:                           # checking if it's a statement
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

                            ifList = self.inter.makeList(self.inter.nextQuad())                 # making a list for the next quad

                            if tkn.recognized_string == "else":                                 # checking if the token's string is else

                                self.inter.genQuad("jump", "_", "_", "_")                           # generating quad for jump
                                self.inter.backpatch(maybe_condition[2], self.inter.nextQuad())     # backpatching the false list with the next quad

                                tkn = self.lex.next_token()

                                if tkn.recognized_string == ":":                                    # checking if the token's string is :
                                    tkn = self.lex.next_token()                                     # calling next token before going inside any methods
                                    maybe_tkn = self.statement(tkn)                                     # calling statement

                                    if maybe_tkn:                                                       # checking if it's a statement
                                        self.inter.backpatch(ifList, self.inter.nextQuad())                 # backpatching the if list with the next quad
                                        return maybe_tkn

                                    elif tkn.recognized_string == "#{":                                 # checking if the token's string is #{
                                        tkn = self.lex.next_token()                                         # calling next token before going inside any methods
                                        maybe_tkn = self.statements(tkn)                                    # calling statements

                                        if maybe_tkn:                                                       # checking if there are statements
                                            tkn = maybe_tkn

                                            if tkn.recognized_string == "#}":                                   # checking if the token's string is #}

                                                self.inter.backpatch(ifList, self.inter.nextQuad())                 # backpatching the if list with the next quad

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
                                self.inter.backpatch(maybe_condition[2], self.inter.nextQuad())  # backpatching the false list with the next quad
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

                condQuad = self.inter.nextQuad()            # getting the next quad

                maybe_condition = self.condition(tkn)       # calling condition
                maybe_tkn = maybe_condition[0]

                if maybe_tkn:                               # checking if it's a condition
                    tkn = maybe_tkn
                    if tkn.recognized_string == ")":            # checking if the token's string is )
                        tkn = self.lex.next_token()
                        if tkn.recognized_string == ":":            # checking if the token's string is :

                            self.inter.backpatch(maybe_condition[1], self.inter.nextQuad()) # backpatching the true list
                            
                            tkn = self.lex.next_token()                             # calling next token before going inside any methods
                            maybe_tkn = self.statement(tkn)                         # calling statement

                            if maybe_tkn:                                           # checking if it's a statement

                                self.inter.genQuad("jump", "_", "_", condQuad)      # generating quad for jump
                                self.inter.backpatch(maybe_condition[2], self.inter.nextQuad()) # backpatching the false list

                                return maybe_tkn
                            elif tkn.recognized_string == "#{":                     # checking if the token's string is #{
                                
                                tkn = self.lex.next_token()                             # calling next token before going inside any methods
                                maybe_tkn = self.statements(tkn)                        # calling statements
                                if maybe_tkn:                                           # checking if there are statements

                                    tkn = maybe_tkn
                                    if tkn.recognized_string == "#}":                       # checking if the token's string is #}

                                        self.inter.genQuad("jump", "_", "_", condQuad)          # generating quad for jump
                                        self.inter.backpatch(maybe_condition[2], self.inter.nextQuad()) # backpatching the false list

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

        if tkn.family == "id":                                  # checking if the token's family is id
            ret_id_list = []                                        # creating the list with the ids that will be returned
            ret_id_list.append(tkn.recognized_string)               # adding the token's string to the list
            tkn = self.lex.next_token()
            while tkn.recognized_string == ",":                     # checking if the token's string is ,
                tkn = self.lex.next_token()                             # calling next token before going inside any methods
                if tkn.family == "id":                                  # checking if the token's family is id
                    ret_id_list.append(tkn.recognized_string)               # adding the token's string to the list
                    tkn = self.lex.next_token()
                else:
                    print("Error 52: expected an id at line", tkn.line_number)
                    exit(2)
            return [tkn, ret_id_list]
        else:
            return [tkn, []]








    def expression(self, tkn):                                           #NOTE: done here
       
        op1 = ""

        if tkn.recognized_string == "-":
            op1 = "-"
        
        tkn = self.optional_sign(tkn)                                   # checking if it's an optional_sign
        
        maybe_term = self.term(tkn)                                     # calling term
        maybe_tkn = maybe_term[0]

        if maybe_tkn:                                                   # checking if it's a term
            tkn = maybe_tkn

            op1 += maybe_term[1]                                            # storing the term



            while tkn.family == "addOperator":                          # checking if the token's family is addOperator

                temp_op = tkn.recognized_string                             # storing the addOperator

                tkn = self.lex.next_token()                                 # calling next token before going inside any methods
                maybe_term = self.term(tkn)                                 # calling term
                maybe_tkn = maybe_term[0]

                if maybe_tkn:                                               # checking if it's a term

                    target = self.inter.newTemp()
                    self.inter.genQuad(temp_op, op1, maybe_term[1], target) # generating quad
                    op1 = target


                    offset_ = 12
                    for element in reversed(self.sym.scope_list[-1].entity_list):  # finding the offset of the last variable in the scope
                        if not isinstance(element, Procedure):                          # if it's not a procedure
                            offset_ = element.offset + 4                                    # then add 4 to that offset
                            break
                    tmp = TemporaryVariable(target, "int", offset_)                     # creating a temporary variable
                    self.sym.addEntity(tmp)                                             # adding the temp_var to the symbol table


                    tkn = maybe_tkn
                else:
                    print("Error 53: expected a term at line", tkn.line_number)
                    exit(2)



            return [tkn,op1]
        else:
            return [None,None]

    




    def term(self,tkn):                                         #NOTE: done here

                                                      
        maybe_factor = self.factor(tkn)                         # calling factor
        maybe_tkn = maybe_factor[0]
             

        if maybe_tkn:                                           # checking if it's a factor 

            op1 = maybe_factor[1] 

            tkn = maybe_tkn
            while tkn.family == "mulOperator":                      # checking if the token's family is mulOperator
                
                temp_op = tkn.recognized_string                         # storing the mulOperator

                tkn = self.lex.next_token()                             # calling next token before going inside any methods
                maybe_factor = self.factor(tkn)                         # calling factor
                maybe_tkn = maybe_factor[0]

                if maybe_tkn:                                           # checking if it's a factor

                    target = self.inter.newTemp()                                   # creating a temporary variable
                    self.inter.genQuad(temp_op, op1, maybe_factor[1], target)       # generating quad
                    op1 = target


                    offset_ = 12
                    for element in reversed(self.sym.scope_list[-1].entity_list):   # finding the offset of the last variable in the scope
                        if not isinstance(element, Procedure):                          # if it's not a procedure
                            offset_ = element.offset + 4                                # then add 4 to that offset
                            break
                    tmp = TemporaryVariable(target, "int", offset_)                 # creating a temporary variable
                    self.sym.addEntity(tmp)                                         # adding the temp_var to the symbol table


                    tkn = maybe_tkn
                else:
                    print("Error 54: expected a factor at line", tkn.line_number)
                    exit(2)
            return [tkn,op1]
        else:
            return [None,None]




    def factor(self,tkn):       #returns list of [the next tkn, variable/number/temp_var]
        
        if tkn.family == "number":                                  # checking if the token's family is number
            
            return [self.lex.next_token(),tkn.recognized_string]        # returning the next token and the number

        elif tkn.recognized_string == "(":                          # checking if the token's string is (
            tkn = self.lex.next_token()
            maybe_expression = self.expression(tkn)                        # calling expression
            maybe_tkn = maybe_expression[0]

            if maybe_tkn:
                tkn = maybe_tkn
                if tkn.recognized_string == ")":                                # checking if the token's string is )
                    return [self.lex.next_token(),maybe_expression[1]]
                else:
                    print("Error 55: expected ) at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 56: expected expression at line", tkn.line_number)
                exit(2)
            
        elif tkn.family == "id":                                    # checking if the token's family is id
            
            the_id = tkn.recognized_string
            tkn = self.lex.next_token()

            maybe_idtail= self.idtail(tkn)                          # calling idtail
            if maybe_idtail[1] == None:
                return [maybe_idtail[0],the_id]
            

            self.inter.genQuad("call",the_id,"_","_")               # generating quad
            return maybe_idtail
        else:                                                       # if none of the above           
            return [None,None] 




    def idtail(self,tkn):                                           #NOTE: done here

        if tkn.recognized_string == "(":                            # checking if the token's string is (
            tkn = self.lex.next_token()                                 # calling next token before going inside any methods
            maybe_par_list = self.actual_par_list(tkn)                  # calling actual_par_list
            maybe_tkn = maybe_par_list[0]

            if maybe_tkn:                                               # if maybe_tkn is not None
                tkn = maybe_tkn
                if tkn.recognized_string == ")":                            # checking if the token's string is )
                    return [self.lex.next_token(),maybe_par_list[1]]
                else:
                    print("Error 57: expected ) at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 58: expected actual_par_list at line", tkn.line_number)
                exit(2)
        else:
            return [tkn,None]
        





    def actual_par_list(self,tkn):


        maybe_expression = self.expression(tkn)                             #calling expression
        maybe_tkn = maybe_expression[0]

        if maybe_tkn:
            self.inter.genQuad("par",maybe_expression[1],"cv","_")              # generating quad
            tkn = maybe_tkn
            while tkn.recognized_string == ",":     
                tkn = self.lex.next_token()    

                maybe_expression = self.expression(tkn)                             #calling expression
                maybe_tkn = maybe_expression[0] 

                if maybe_tkn:              
                    tkn = maybe_tkn
                    self.inter.genQuad("par",maybe_expression[1],"cv","_")              # generating quad
                else:
                    print("Error 59: expected an expression at line", tkn.line_number)
                    exit(2)
            
            temp_var = self.inter.newTemp()                                     # creating a temporary variable
            self.inter.genQuad("par", temp_var, "ret", "_")                     # generating quad with return value


            offset_ = 12
            for element in reversed(self.sym.scope_list[-1].entity_list):           # finding the offset of the last variable in the scope
                if not isinstance(element, Procedure):                                  # if it's not a procedure
                    offset_ = element.offset + 4                                            # then add 4 to that offset
                    break
            tmp = TemporaryVariable(temp_var, "int", offset_)                       # creating a temporary variable
            self.sym.addEntity(tmp)                                                 # adding the temp_var to the symbol table


            return [tkn,temp_var]
        else:

            temp_var = self.inter.newTemp()                     # creating a temporary variable
            self.inter.genQuad("par", temp_var, "ret", "_")     # generating quad with return value


            offset_ = 12
            for element in reversed(self.sym.scope_list[-1].entity_list):   # finding the offset of the last variable in the scope
                if not isinstance(element, Procedure):                          # if it's not a procedure
                    offset_ = element.offset + 4                                    # then add 4 to that offset
                    break
            tmp = TemporaryVariable(temp_var, "int", offset_)               # creating a temporary variable
            self.sym.addEntity(tmp)                                         # adding the temp_var to the symbol table


            return [tkn,temp_var]





    def optional_sign(self,tkn):
        
        if tkn.family == "addOperator":
            return self.lex.next_token()
        else:
            return tkn
        
    


    def condition(self,tkn):            #returns list of [the next tkn, condition_true, condition_false]
        
        maybe_bool_term = self.bool_term(tkn)                             #calling bool_term
        maybe_tkn = maybe_bool_term[0]

        if maybe_tkn:
            condition_true = maybe_bool_term[1]
            condition_false = maybe_bool_term[2]

            tkn = maybe_tkn
            while tkn.recognized_string == "or":                                # checking if the token's string is or

                self.inter.backpatch(condition_false,self.inter.nextQuad())         # backpatching

                tkn = self.lex.next_token()
                maybe_bool_term = self.bool_term(tkn)                               #calling bool_term
                maybe_tkn = maybe_bool_term[0]

                if maybe_tkn:
                    condition_true = self.inter.mergeList(condition_true,maybe_bool_term[1])
                    condition_false = maybe_bool_term[2]
                    tkn = maybe_tkn

                else:
                    print("Error 60: expected a bool_factor at line", tkn.line_number)
                    exit(2)
            return [tkn, condition_true, condition_false]
        else:
            return [None,None,None]





    def bool_term(self,tkn):    #return [tkn, true_list, false_list]
        
        maybe_bool_factor = self.bool_factor(tkn)                             #calling bool_factor
        maybe_tkn = maybe_bool_factor[0]

        if maybe_tkn:

            bool_term_true = maybe_bool_factor[1]
            bool_term_false = maybe_bool_factor[2]

            tkn = maybe_tkn
            while tkn.recognized_string == "and":                   # checking if the token's string is and

                self.inter.backpatch(bool_term_true,self.inter.nextQuad())     # backpatching

                tkn = self.lex.next_token()
                maybe_bool_factor = self.bool_factor(tkn)                       #calling bool_factor
                maybe_tkn = maybe_bool_factor[0]
                if maybe_tkn:
                    bool_term_false = self.inter.mergeList(bool_term_false, maybe_bool_factor[2])
                    bool_term_true = maybe_bool_factor[1]
                    tkn = maybe_tkn
                else:
                    print("Error 61: expected a bool_factor at line", tkn.line_number)
                    exit(2)
            return [tkn, bool_term_true, bool_term_false]
        else:
            return [None,None,None]



    def bool_factor(self,tkn):  #returns [tkn, true_list, false_list]


        if tkn.recognized_string == "not":
            tkn = self.lex.next_token()
            if tkn.recognized_string == "[":
                tkn = self.lex.next_token()
                maybe_condition = self.condition(tkn)                   #calling condition
                maybe_tkn = maybe_condition[0]

                if maybe_tkn:

                    tkn = maybe_tkn
                    if tkn.recognized_string == "]":

                        return [self.lex.next_token(),maybe_condition[2],maybe_condition[1]]

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
            tkn = self.lex.next_token()
            maybe_condition = self.condition(tkn)                       #calling condition
            maybe_tkn = maybe_condition[0]
            if maybe_tkn:
                tkn = maybe_tkn
                if tkn.recognized_string == "]":
                    return [self.lex.next_token(), maybe_condition[1], maybe_condition[2]]
                else:
                    print("Error 65: expected ] at line", tkn.line_number)
                    exit(2)
            else:
                print("Error 66: expected a condition at line", tkn.line_number)
                exit(2)
        else:
            maybe_expression1 = self.expression(tkn)                    #calling expression
            maybe_tkn = maybe_expression1[0]
            if maybe_tkn:
                rel_op_tkn = maybe_tkn
                if rel_op_tkn.family == "relOperator":                      #checking if the token's family is relOperator
                    tkn = self.lex.next_token()
                    maybe_expression2 = self.expression(tkn)                    #calling expression
                    maybe_tkn = maybe_expression2[0]

                    if maybe_tkn:

                        bool_factor_true = self.inter.makeList(self.inter.nextQuad())
                        self.inter.genQuad(rel_op_tkn.recognized_string,maybe_expression1[1],maybe_expression2[1],"_")  #generating quad
                        bool_factor_false = self.inter.makeList(self.inter.nextQuad())
                        self.inter.genQuad("jump", "_", "_", "_")                                                       #generating quad

                        return [maybe_tkn, bool_factor_true, bool_factor_false]
                    else:
                        print("Error 67: expected an expression at line", tkn.line_number)
                        exit(2)
                else:
                    print("Error 68: expected a relOperator at line", tkn.line_number)
                    exit(2)
            else:
                return [None,None,None]





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

                            self.inter.genQuad("begin_block", "main_program", "_", "_")     #generating quad
                            if not self.main_function_call(tkn):                            #making sure that the program has at least one main function
                                print("Error 69: no main function call found at line", tkn.line_number)
                                exit(2)

                            tkn = self.lex.next_token()

                            while self.main_function_call(tkn):                             #checking if there are more main  function calls
                                tkn = self.lex.next_token()

                            self.inter.genQuad("halt", "_", "_", "_")                       #generating quad
                            self.inter.genQuad("end_block", "main_program", "_", "_")       #generating quad
                            self.final.inter_to_final()                                     #calling inter_to_final
                            self.sym.removeScope()  # removing the scope from the symbol table
                            print(self.sym)
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

        if tkn_func.family == "id":                             # checking if the token's family is id
            tkn = self.lex.next_token()
            if tkn.recognized_string == "(":                        # checking if the token's string is (
                tkn = self.lex.next_token()
                if tkn.recognized_string == ")":                        # checking if the token's string is )
                    tkn = self.lex.next_token()
                    if tkn.recognized_string == ";":
                        self.inter.genQuad("call", tkn_func.recognized_string, "_", "_")    #generating quad
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

    f = open("quads.int", "w")

    for i,q in enumerate(syn.inter.quad_list):
        print(i,":",q)
        f.write(q.__str__() + "\n")
    f.close()



    #--------------------for testing the lex--------------------#
    #lex = Lex("test1.txt")
    #for i in range(100):

        #tnk=lex.next_token()
        #print("token:",tnk.family,tnk.recognized_string,tnk.line_number)
    #syn=syntax("test.txt")


  