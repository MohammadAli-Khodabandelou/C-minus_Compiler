import FileManager.file_reader as fr
import FileManager.file_writer as fw
import re


class Scanner:
    state = ['start', 'num', 'word', 'equal', 'twoequal', 'symbol', 'slash', 'bcmt', 'bcmt*', 'lcmt', 'wspace', 'star']
    valid_tokens = '[a-zA-Z0-9;:,\[\]\(\)\{\}\+\-\*=< \n\r\t\v\f]'
    digit = '[0-9]'
    letter = '[a-zA-Z]'
    symbol = '[;:,\[\]\(\)\{\}\+\-<]'
    wspace = '[ \n\r\t\v\f]'

    keyword_reference_list = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']

    type_by_state_name = {'num': 'NUM', 'equal': 'SYMBOL', 'twoequal': 'SYMBOL', 'symbol': 'SYMBOL', 'bcmt*': 'COMMENT',
                          'lcmt': 'COMMENT', 'wspace': 'WHITESPACE', 'star': 'SYMBOL'}

    def __init__(self):
        self.read_again = False
        self.lineno = 1
        self.current_index = 0
        self.current_char = ''
        self.current_state = 'start'
        self.state_to_return = ''
        self.current_token_lexeme = ''
        self.reader = fr.Reader()
        self.error_writer = fw.ErrorWriter()
        self.symbol_writer = fw.SymbolWriter()
        self.id_list = []
        self.finished = False

    def update_start_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'num'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'word'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.symbol, self.current_char):
            self.current_state = 'symbol'
            self.current_token_lexeme += self.current_char
        elif re.search('=', self.current_char):
            self.current_state = 'equal'
            self.current_token_lexeme += self.current_char
        elif re.search('\*', self.current_char):
            self.current_state = 'star'
            self.current_token_lexeme += self.current_char
        elif re.search('/', self.current_char):
            self.current_state = 'slash'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'wspace'
            self.current_token_lexeme += self.current_char
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_num_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'num'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid number)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_word_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'word'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'word'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_equal_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.current_state = 'twoequal'
            self.current_token_lexeme += self.current_char
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_two_equal_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_slash_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.symbol, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search('=', self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search('\*', self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search('/', self.current_char):
            self.current_state = 'lcmt'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_bcmt_with_char(self):
        self.current_token_lexeme += self.current_char
        if re.search('\*', self.current_char):
            self.current_state = 'bcmt*'

    def update_bcmt_star_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.symbol, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search('=', self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search('\*', self.current_char):
            self.current_state = 'bcmt*'
            self.current_token_lexeme += self.current_char
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        else:
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char

    def update_lcmt_with_char(self):
        if re.search('\n', self.current_char):
            self.reset_state_return()
        else:
            self.current_token_lexeme += self.current_char

    def update_white_space_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'wspace'
            self.current_token_lexeme += self.current_char
        else:
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_char + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_star_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Unmatched comment)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_state(self):
        if self.current_state == 'start':
            self.update_start_with_char()
        elif self.current_state == 'num':
            self.update_num_with_char()
        elif self.current_state == 'word':
            self.update_word_with_char()
        elif self.current_state == 'equal':
            self.update_equal_with_char()
        elif self.current_state == 'twoequal':
            self.update_two_equal_with_char()
        elif self.current_state == 'slash':
            self.update_slash_with_char()
        elif self.current_state == 'bcmt':
            self.update_bcmt_with_char()
        elif self.current_state == 'bcmt*':
            self.update_bcmt_star_with_char()
        elif self.current_state == 'lcmt':
            self.update_lcmt_with_char()
        elif self.current_state == 'wspace':
            self.update_white_space_with_char()
        elif self.current_state == 'star':
            self.update_star_with_char()

    def reset_state_return(self):
        self.state_to_return = self.current_state
        self.current_state = 'start'
        self.read_again = True

    def generate_token_type(self):
        if self.state_to_return == 'word':
            if self.current_token_lexeme in self.keyword_reference_list:
                return 'KEYWORD'
            else:
                self.id_list.append(self.current_token_lexeme)
                return 'ID'
        else:
            return self.type_by_state_name[self.state_to_return]

    def get_next_token(self):
        if self.finished:
            return None
        else:
            while True:
                # Read next character
                if not self.read_again:
                    self.current_char = self.reader.read_next_char()
                    if self.current_char == '\n':
                        self.lineno += 1
                # Return the newly-found token
                else:
                    self.read_again = False
                    if self.state_to_return not in ['bcmt', 'bcmt*', 'lcmt', 'wspace']:
                        return '(' + self.generate_token_type() + ', ' + self.current_token_lexeme + ')'

                # Return none if the file has ended
                if len(self.current_char) == 0:
                    self.reader.close_file()
                    self.symbol_writer.write_symbols(self.keyword_reference_list + self.id_list)
                    self.finished = True
                    self.error_writer.close()
                    self.symbol_writer.close()
                    return None

                # Call the method to update the state and construct the token
                self.update_state()
