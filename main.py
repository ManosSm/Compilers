import string


class Token:

    def __init__(self, family, recognized_string, line_number):
        self.family = family
        self.recognized_string = recognized_string
        self.line_number = line_number


class Lex:
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(self.file_name)
        self.token = None
        self.current_Line = 0
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

                            #0 are letters   1 are digits    22 are blank chars    23 eof   99 error
        self.state_list=[   [3,1,99,5,5,6,7,16,17,18,13,12,12,12,8,8,8,8,9,99,99,99,0,99],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            []
                        ]

    def next_token(self):
        
        while 1:
            token = self.file.read(1)

            if not token:
                break
            print(token in string.whitespace)


if __name__ == '__main__':
    lex = Lex("test.txt")
    lex.next_token()
