#Source: https://rev-kids20.forkbomb.ru/tasks/RE8_crossword
#Description: "Here are too weird crosswords. Can you solve?"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Don't forget to install pwntools: pip3 install pwntools.
# You need to write only process_equations function, all work with sockets is already done.
# Pass DEBUG as argument to see all client-server interaction: python3 crossword_template.py DEBUG

import pwn
from z3 import *

#The function checks whether the element being checked is an arithmetic sign
def is_Sign(element):
    
    if element == '-' or element == '+' or element == '*' or element == '/' or element == '=':
           
            return True
            
    else:
        
        return False


def process_equations(text):
    
    #The size of the input data will constantly change, so it is necessary that the symbolic variables are generated based on their size.
    x = {f'x{i+1}': Real(f'x{i+1}') for i in range(len(text))}
    
    solver = Solver()
    
    space = ' '
    
    result = 0
    
    #Here the RPN is parsed and turned into a linear equation, then sent to z3
    for i in range(len(text)):
        
        text[i] = text[i].split(' ')
        
        i1 = 0
        
        while True:
            
            #Since eval() is used, unknown variables need to be put into the appropriate format so that they can be pulled from the dictionary later.
            if text[i][i1][0] == 'x':
                
                text[i][i1] = 'x[' + '"' + text[i][i1] + '"' + ']'
                
            #If an arithmetic sign was found in the string, then it is necessary to translate the expression from postfix form to infix form and an expression of the type <operand><operand><arithmetic_sign> is converted to <operand><arithmetic_sign><operand>
            if is_Sign(text[i][i1]) == True:
            
                text[i][i1] = text[i][i1 - 1] + space + text[i][i1] + space + text[i][i1 - 2]
                
                text[i].pop(i1 - 1)
                text[i].pop(i1 - 2)
                
                i1 -= 2
                
            i1 += 1
            
            #Here, what is behind the "=" sign is cut off from the resulting infix form and placed in a separate variable.
            if i1 == len(text[i]):
                
                text[i] = text[i][0]
                
                eq = text[i].find('=')
                
                result = text[i][eq + 2:]
                
                text[i] = text[i][:eq - 1]
                
                break
                
        #eval() should be used very carefully, it is not a safe function, but I just couldn't think of anything better
        solver.add(eval(text[i]) == eval(result))
        
    solver.check()
    solver.model()
        
    model = solver.model()
    word = str()
    
    #Here the received data is converted into characters, placed in the variable word and sent to main()
    for i in range(1, len(text) + 1):
        
        a = x[f'x{i}']
        
        word += chr(model[a].as_long())
    
    return word


def solve():
    r = pwn.remote('109.233.56.90', 11542)

    r.recvline()
    
    while True:
        print()

        line = r.recvline().decode().strip()
        print(line)

        if not line.startswith("Crossword"):
            return

        count = int(line.split()[4])
        
        lines = []
        for _ in range(count):
            lines.append(r.recvline().decode().strip())
        
        print("Equations:", lines)
        result = process_equations(lines)
        print("Result:", result)

        r.sendline(result)


if __name__ == "__main__":
    solve()
