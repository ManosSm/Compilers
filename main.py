import string


class Token:
    family = ""
    recognized_string = ""
    line_number = 0

    def __init__(self, family, recognized_string, line_number):
        self.family = family
        self.recognized_string = recognized_string
        self.line_number = line_number


class Lex:
    current_Line = 0
    file_name = ""
    token = None

    def __init__(self, file_name):
        self.file_name = file_name

    def next_token(self):
        file = open(self.file_name)
        while 1:
            token = file.read(1)

            if not token:
                break
            print(token in string.whitespace)


if __name__ == '__main__':
    lex = Lex("test.txt")
    lex.next_token()
