#!/usr/bin/env python3

import cmd
from termcolor import colored
from math import *
from convertor import Convertor

# TODO:
# better graphics
# add more units (including temperature!)
# number base operations
# check speedcrunch for more features
# allow some configurations - default angle units etc.
# make order in default()
# support units with more than 1 word like "us gallon"(re)
# maybe add option to translate word e.g. lemon in hebrew?? (probably bad idea)

class Calculator(cmd.Cmd):
    intro = "I'm Lyca the lyte calculator. I can also convert units and currencies!"
    prompt = colored('~ ', 'green')
    convertor = Convertor()
    precision = 5

    def do_EOF(self, arg):
        return self.do_exit(arg)

    def do_q(self, arg):
        return self.do_exit(arg)

    def do_exit(self, arg):
        return True

    def default(self, arg):
        output = None
        # normal python
        try:
            output = eval(arg)
        except:
            pass

        # try fixing trailing parenthesses if missing
        try:
            output = eval(arg + ")")
        except:
            try:
                if arg[-1] == "(":
                    output = eval(arg[:-1] + ")")
            except:
                pass

        # try conversion
        try:
            if self.convertor.is_conversion_like(arg):
                val, src_unit, target_unit = self.convertor.parse_arg(arg)
                try:
                    output = self.convertor.convert_unit(val, src_unit, target_unit)
                except:
                    output = self.convertor.convert_currency(val, src_unit, target_unit)

        except Exception as e:
            print(e)

        if output:
            output = str(round(output, self.precision))
            print(output, end="\n\n")
        else:
            print("input error")
        
        return False

            
if __name__ == '__main__':
    Calculator().cmdloop()
