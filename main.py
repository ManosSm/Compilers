import string


class Token:import string


class Token:

    def __init__(self, family, recognized_string, line_number):
        self.family = family
        self.recognized_string = recognized_string
        self.line_number = line_number


class Lex:

    def __init__(self, file_name):
        self.file_name = file_name
        self.current_line = 0
        self.current_char = 0
        self.keyword_set={"def","not","and","or","declare","print","return","if","else","while"}                   #TODO
        self.final_state_set=   {  
                                    2:"number",
                                    4:"id/keyword",         #==================HERE+++++++======                   #TODO
                                    5:"addOparator",
                                    6:"mulOp",
                                    8:"groupSymbol",
                                    12:"delimitor",
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
        eof_offset = 0

        while 1:
            in_read = file.read(1)
            in_id = 99

            if in_read.isalpha():                           # if letter
                in_id = 0
                rec_string+=in_read                         # adding character to the recognised string
            elif in_read.isnumeric():                       # if number
                in_id = 1
                rec_string+=in_read                         # adding character to the recognised string
            elif in_read in string.whitespace:              # if a white character
                if in_read == "\n":                         # if changed line
                    self.current_line += 1

                print("current line:", self.current_line)

                if in_read == "":                           # if eof
                    in_id = 23
                    eof_offset = 1
                else:
                    in_id = 22                              # if white character except eof
            elif in_read in self.symbol_dict:
                in_id = self.symbol_dict[in_read]
                rec_string+=in_read                         # adding character to the recognised string
            else:
                print("Error: unknown character", in_read, "at line", self.current_line)
                file.close()
                exit(1)

            state = self.state_list[state][in_id]                        
            
            print(in_read)
            print(state)

            if state == 0:                                        #NOTE: maybe improveivanb;ele
                rec_string = ""

            if state in self.final_state_set:                   # if state is final
                rec_string = rec_string[0:(len(rec_string) + self.state_list[state][0] + eof_offset)]  # black box
                self.current_char = file.tell() + self.state_list[state][0] + eof_offset
                file.close()
                return Token(self.final_state_set[state], rec_string, self.current_line)
           

if __name__ == '__main__':
    lex = Lex("test.txt")

    for i in range(10):

        tnk=lex.next_token()
        print("token:",tnk.family,tnk.recognized_string,tnk.line_number)