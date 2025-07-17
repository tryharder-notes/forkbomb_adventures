#Source: https://rev-kids20.forkbomb.ru/tasks/RE8_angryopaq
#Description: "Make Angry Opaq less angry and more transparent. He'll give you the flag."

import angr, claripy

def main():
    
    find_addr = 0x401550
    avoid_addr = 0x4015d6
    
    project = angr.Project('./angryopaq.elf')
    integer = claripy.BVS('integer', 32)
    
    state = project.factory.entry_state()
    state.solver.add(integer > 0x0)
    state.solver.add(integer < 0xFFFFFFFF)

    @project.hook(0x401191, length = 5) #I decided to emulate scanf because it was just easier for me to debug the program, in short, I do it myself and I advise you to do the same, because with scanf you can catch a lot of stupidities out of the blue
    def hook(state):
        state.memory.store(state.solver.eval(state.regs.rbp - 0x24), integer, 4)
        print(state.memory.load(state.solver.eval(state.regs.rbp - 0x24), 4))
    
    
    def skip_block(state, offset): #Here, the rip is simply shifted in order to bypass unwanted program blocks, on which the solver starts to get stuck and slow, so the solution is found instantly. I also added the output of executable blocks, so that it is clear along which chain the number entered by the user passes
        
        print(f'Block at {hex(state.solver.eval(state.regs.rip))} has been executed')
        state.regs.rip += offset
        block = project.factory.block(state.solver.eval(state.regs.rip))
        print('-----------------------------------------------------------------------')
        print(block.pp())
        print('-----------------------------------------------------------------------')
    
    #Here the execution of the hooked instruction is preserved in its original form, the rip is simply shifted by a specified number of bytes.
    project.hook(0x4011b1, lambda state: skip_block(state, 0x30), length = 3)
    project.hook(0x4011e7, lambda state: skip_block(state, 0x12), length = 3)
    project.hook(0x4011ff, lambda state: skip_block(state, 0x1b), length = 3)
    project.hook(0x401220, lambda state: skip_block(state, 0x12), length = 3)
    project.hook(0x401238, lambda state: skip_block(state, 0x15), length = 3)
    project.hook(0x401253, lambda state: skip_block(state, 0x7c), length = 3)
    project.hook(0x4012d7, lambda state: skip_block(state, 0x4c), length = 3)
    project.hook(0x40132b, lambda state: skip_block(state, 0x35), length = 3)
    project.hook(0x401368, lambda state: skip_block(state, 0x3e), length = 3)
    project.hook(0x4013ae, lambda state: skip_block(state, 0x2f), length = 3)
    project.hook(0x4013e5, lambda state: skip_block(state, 0x55), length = 3)
    project.hook(0x401442, lambda state: skip_block(state, 0x1b), length = 3)
    project.hook(0x401465, lambda state: skip_block(state, 0x2c), length = 3)
    project.hook(0x401499, lambda state: skip_block(state, 0x7e), length = 3)
    project.hook(0x40151f, lambda state: skip_block(state, 0x15), length = 3)
    
    simulation = project.factory.simgr(state)
    
    simulation.explore(find = find_addr)
    
    if simulation.found:

        result = simulation.found[0]
        
        rev_flag = result.solver.eval(integer, cast_to = int)
        
        flag = int.from_bytes(rev_flag.to_bytes(4, 'little'), 'big') #It is necessary to reverse the code, because endianness is not taken into account - the solver will spit out the number exactly as it will be in memory
        
        print(f'Code is: {flag}')
        
    else:
        
        print('Nope :(')
        print(simulation.errored)
        print(hex(state.addr))
    
if __name__ == "__main__":
    main()
