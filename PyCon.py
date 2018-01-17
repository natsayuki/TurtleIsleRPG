import pygame
from string import ascii_letters
import textwrap
import re

# I dont know what this means???
re_token = re.compile(r"""[\"].*?[\"]|[\{].*?[\}]|[\(].*?[\)]|[\[].*?[\]]|\S+""")
re_is_list = re.compile(r'^[{\[(]')
re_is_number = re.compile(r"""
(?x)
[-]?[0][x][0-9a-fA-F]+[lLjJ]? | 	#  Hexadecimal
[-]?[0][0-7]+[lLjJ]? |				#  Octal
[-]?[\d]+(?:[.][\d]*)?[lLjJ]?		#  Decimal (Int or float)
""")
re_is_assign = re.compile(r'[$](?P<name>[a-zA-Z_]+\S*)\s*[=]\s*(?P<value>.+)')
re_is_comment = re.compile(r'\s*#.*')
re_is_var = re.compile(r'^[$][a-zA-Z_]+\w*\Z')


class PyCon:
    def __init__(self, screen, rect, functions=None, key_calls=None, vari=None, syntax=None):
        self.message_of_the_day = ["super sik console for super secret dev commands","*some commands do not work properly in game and will only apply to the initial turtle*","*it is better to use all stat-modifying commands in the start screen*",'*the syntax for functions that take arguments is {function} {argument} {argument}*']

        self.bg_color = (0,0,0) #(0, 25, 0)      # Blackish Green Background
        self.bg_alpha = 200             # How transparent is the Console Background
        self.txt_color_i = (0, 255, 0)  # Green bright Input Color
        self.txt_color_o = (0, 153, 0)  # Dark Green output Color

        self.changed = True
        self.active = False
        self.preserve_events = True
        self.repeat_rate = [500, 30]

        self.ps1 = "] "
        self.ps2 = ">>> "
        self.ps3 = "... "
        self.c_ps = self.ps2

        self.c_out = self.message_of_the_day
        self.c_in = ""
        self.c_hist = [""]
        self.c_hist_pos = 0
        self.c_pos = 0
        self.c_draw_pos = 0
        self.c_scroll = 0

        self.parent_screen = screen
        self.rect = pygame.Rect(rect)
        self.size = self.rect.size

        self.font = pygame.font.SysFont("Courier New", 14)
        self.font_height = self.font.get_linesize()
        self.max_lines = int((self.size[1] / self.font_height) - 1)
        self.max_chars = int(((self.size[0]) / (self.font.size(ascii_letters)[0]/len(ascii_letters))) - 1)
        self.txt_wrapper = textwrap.TextWrapper()

        self.bg_layer = pygame.Surface(self.size)
        self.bg_layer.set_alpha(self.bg_alpha)
        self.txt_layer = pygame.Surface(self.size)
        self.txt_layer.set_colorkey(self.bg_color)

        pygame.key.set_repeat(*self.repeat_rate)

        self.key_calls = {}
        self.func_calls = {}
        self.user_vars = vari
        self.user_syntax = syntax
        self.user_namespace = {}

        self.add_key_calls({"l": self.clear, "c": self.clear_input, "w": self.set_active})
        self.add_key_calls(key_calls)

        self.add_functions_calls({"help": self.help, "echo": self.output, "clear": self.clear})
        self.add_functions_calls(functions)

    def screen(self):
        return self.parent_screen

    def add_functions_calls(self, functions):
        if isinstance(functions, dict):
            self.func_calls.update(functions)

    def add_key_calls(self, functions):
        if isinstance(functions, dict):
            self.key_calls.update(functions)

    def output(self, text):
        """Print a string on the Console. Use: echo "Test Test Test" """
        self.changed = True
        if not isinstance(text, str):
            text = str(text)
        text = text.expandtabs()
        text = text.splitlines()
        self.txt_wrapper.width = self.max_chars
        for line in text:
            for w in self.txt_wrapper.wrap(line):
                self.c_out.append(w)

    def submit_input(self, text):
        self.clear_input()
        self.output(self.c_ps + text)
        self.c_scroll = 0
        self.send_pyconsole(text)

    def format_input_line(self):
        text = self.c_in[:self.c_pos] + "\v" + self.c_in[self.c_pos + 1:]
        n_max = int(self.max_chars - len(self.c_ps))
        vis_range = self.c_draw_pos, self.c_draw_pos + n_max
        return self.c_ps + text[vis_range[0]:vis_range[1]]

    def str_insert(self, text, strn):
        string = text[:self.c_pos] + strn + text[self.c_pos:]
        self.set_pos(self.c_pos + len(strn))
        return string

    def clear_input(self):
        self.c_in = ""
        self.c_pos = 0
        self.c_draw_pos = 0

    def set_pos(self, newpos):
        self.c_pos = newpos
        if (self.c_pos - self.c_draw_pos) >= int(self.max_chars - len(self.c_ps)):
            self.c_draw_pos = max(0, int(self.c_pos - (self.max_chars - len(self.c_ps))))
        elif self.c_draw_pos > self.c_pos:
            self.c_draw_pos = self.c_pos - (self.max_chars/2)
            if self.c_draw_pos < 0:
                self.c_draw_pos = 0
                self.c_pos = 0

    def set_active(self, b=None):
        if not b:
            self.active = not self.active
        else:
            self.active = b
        print("Console toggled")

    def add_to_history(self, text):
        self.c_hist.insert(-1, text)
        self.c_hist_pos = len(self.c_hist) - 1

    def draw(self):
        if not self.active:
            return

        if self.changed:
            self.changed = False
            self.txt_layer.fill(self.bg_color)
            lines = self.c_out[-(self.max_lines + self.c_scroll):len(self.c_out) - self.c_scroll]
            y_pos = self.size[1]-(self.font_height*(len(lines)+1))

            for line in lines:
                tmp_surf = self.font.render(line, True, self.txt_color_o)
                self.txt_layer.blit(tmp_surf, (1, y_pos, 0, 0))
                y_pos += self.font_height

            tmp_surf = self.font.render(self.format_input_line(), True, self.txt_color_i)
            self.txt_layer.blit(tmp_surf, (1, self.size[1]-self.font_height, 0, 0))

            self.bg_layer.fill(self.bg_color)
            self.bg_layer.blit(self.txt_layer, (0, 0, 0, 0))

        self.parent_screen.blit(self.bg_layer, self.rect)

    def process_input(self, eventlist):
        if not self.active:
            return

        for event in eventlist:
            if event.type == pygame.KEYDOWN:
                self.changed = True
                # Special Character Manipulation
                if event.key == pygame.K_TAB:
                    self.c_in = self.str_insert(self.c_in, "    ")
                elif event.key == pygame.K_BACKSPACE:
                    if self.c_pos > 0:
                        self.c_in = self.c_in[:self.c_pos - 1] + self.c_in[self.c_pos:]
                        self.set_pos(self.c_pos - 1)
                elif event.key == pygame.K_DELETE:
                    if self.c_pos < len(self.c_in):
                        self.c_in = self.c_in[:self.c_pos] + self.c_in[self.c_pos + 1:]
                elif event.key == pygame.K_RETURN or event.key == 271:
                    self.submit_input(self.c_in)
                # Changing Cursor Position
                elif event.key == pygame.K_LEFT:
                    if self.c_pos > 0:
                        self.set_pos(self.c_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    if self.c_pos < len(self.c_in):
                        self.set_pos(self.c_pos + 1)
                elif event.key == pygame.K_HOME:
                    self.set_pos(0)
                elif event.key == pygame.K_END:
                    self.set_pos(len(self.c_in))
                # History Navigation
                elif event.key == pygame.K_UP:
                    if len(self.c_out):
                        if self.c_hist_pos > 0:
                            self.c_hist_pos -= 1
                        self.c_in = self.c_hist[self.c_hist_pos]
                        self.set_pos(len(self.c_in))
                elif event.key == pygame.K_DOWN:
                    if len(self.c_out):
                        if self.c_hist_pos < len(self.c_hist) - 1:
                            self.c_hist_pos += 1
                        self.c_in = self.c_hist[self.c_hist_pos]
                        self.set_pos(len(self.c_in))
                # Scrolling
                elif event.key == pygame.K_PAGEUP:
                    if self.c_scroll < len(self.c_out) - 1:
                        self.c_scroll += 1
                elif event.key == pygame.K_PAGEDOWN:
                    if self.c_scroll > 0:
                        self.c_scroll -= 1
                # Normal character printing
                elif event.key >= 32:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        if event.key in range(256) and chr(event.key) in self.key_calls:
                            self.key_calls[chr(event.key)]()
                    else:
                        char = str(event.unicode)
                        self.c_in = self.str_insert(self.c_in, char)

    def send_pyconsole(self, text):
        if not text:  # Output a blank row if nothing is entered
            self.output("")
            return

        self.add_to_history(text)

        # Determine if the statement is an assignment
        assign = re_is_assign.match(text)

        # If it is tokenize only the "value" part of $name = value
        if assign:
            tokens = self.tokenize(assign.group('value'))
        else:
            tokens = self.tokenize(text)

        if tokens is None:
            return

        # Evaluate
        try:
            out = None
            # A variable alone on a line
            if (len(tokens) is 1) and re_is_var.match(text) and not assign:
                out = tokens[0]
            # Statement in the form $name = value
            elif (len(tokens) is 1) and assign:
                self.setvar(assign.group('name'), tokens[0])
            else:
                # Function
                out = self.func_calls[tokens[0]](*tokens[1:])
                # Assignment from function's return value
                if assign:
                    self.setvar(assign.group('name'), out)

            if out is not None:
                self.output(out)
        except (KeyError, TypeError):
            self.output("Unknown Command: " + str(tokens[0]))
            self.output(r'Type "help" for a list of commands.')

    def setvar(self, name, value):
        """Sets the value of a variable"""
        if name in self.user_vars or name not in self.__dict__:
            self.user_vars.update({name: value})
            self.user_namespace.update(self.user_vars)
        elif name in self.__dict__:
            self.__dict__.update({name: value})

    def convert_token(self, tok):
        tok = tok.strip("$")
        try:
            tmp = eval(tok, self.__dict__, self.user_namespace)
        except SyntaxError as strerror:
            self.output("SyntaxError: " + str(strerror))
            raise ParseError(tok)
        except TypeError as strerror:
            self.output("TypeError: " + str(strerror))
            raise ParseError(tok)
        except NameError as strerror:
            self.output("NameError: " + str(strerror))
        except:
            self.output("Error:")
            raise ParseError(tok)
        else:
            return tmp

    def tokenize(self, s):
        if re_is_comment.match(s):
            return [s]

        for r in self.user_syntax:
            group = r.match(s)
            if group:
                self.user_syntax[r](self, group)
                return

        tokens = re_token.findall(s)
        tokens = [i.strip("\"") for i in tokens]
        cmd = []
        i = 0
        while i < len(tokens):
            t_count = 0
            val = tokens[i]

            if re_is_number.match(val):
                cmd.append(self.convert_token(val))
            elif re_is_var.match(val):
                cmd.append(self.convert_token(val))
            elif val == "True":
                cmd.append(True)
            elif val == "False":
                cmd.append(False)
            elif re_is_list.match(val):
                while not balanced(val) and (i + t_count) < len(tokens) - 1:
                    t_count += 1
                    val += tokens[i + t_count]
                else:
                    if (i + t_count) < len(tokens):
                        cmd.append(self.convert_token(val))
                    else:
                        raise ParseError(val)
            else:
                cmd.append(val)
            i += t_count + 1
        return cmd

    def clear(self):
        """Clear the screen! Use: clear"""
        self.c_out = ["[Screen Cleared]"]
        self.c_scroll = 0

    def help(self, *args):
        if args:
            items = [(i, self.func_calls[i]) for i in args if i in self.func_calls]
            for i, v in items:
                
                if len(v.__code__.co_varnames) > 0:
                    #the line below subtracts one from argcount if one of the arguments
                    #is self (varname returns arguments as well) (v.__code__.co_varnames[0] is "self" returns True and for some reason
                    #in python subtracting a True boolean from an integer subtracts by 1
                    #if there are no variables in the function and it takes no arguments
                    #the only problem with this is it returns an index error because there are no arguments or variables
                    if v.__code__.co_varnames[0] is "self":
                        arguments = v.__code__.co_varnames[1:v.__code__.co_argcount]
                    else:
                        arguments = v.__code__.co_varnames[:v.__code__.co_argcount]
                    out = i + f": Takes {v.__code__.co_argcount - (v.__code__.co_varnames[0] is 'self')} arguments {arguments}. "
                else:
                   out = i + ": Takes %d arguments. " % (v.__code__.co_argcount) 
                doc = v.__doc__
                if doc:
                    out += textwrap.dedent(doc)
                else:
                    out += "No help is available for this function."
                tmp_indent = self.txt_wrapper.subsequent_indent
                self.txt_wrapper.subsequent_indent = " " * (len(i) + 2)
                self.output(out)
                self.txt_wrapper.subsequent_indent = tmp_indent
        else:
            out = "Available commands: " + str(self.func_calls.keys()).strip("[]")
            self.output(out)
            self.output(r'Type "help command-name" for more information on that command')

    def write_history_to_file(self):
        hist_file_text = open("History_text.txt", "w")
        for item_h in self.c_out:
            hist_file_text.write("%s\n" % item_h)
        hist_file_text.close()

        hist_file_cmd = open("History_cmd.txt", "w")
        for item_h in self.c_hist:
            hist_file_cmd.write("%s\n" % item_h)
        hist_file_cmd.close()


class ParseError(Exception):
    def __init__(self, token):
        self.token = token

    def at_token(self):
        return self.token


def balanced(t):
    stack = []
    pairs = {"\'": "\'", '\"': '\"', "{": "}", "[": "]", "(": ")"}
    for char in t:
        if stack and char == pairs[stack[-1]]:
            stack.pop()
        elif char in pairs:
            stack.append(char)
    return not bool(stack)
