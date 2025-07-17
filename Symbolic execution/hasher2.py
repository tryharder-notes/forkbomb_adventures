#Source: https://rev-kids20.forkbomb.ru/tasks/RE8_hasher2
#Description: Also crack that (harder).
#Estimated script running time - 9 minutes

import hashlib, claripy, angr

def main():

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUWVXYZ1234567890'
    
    find_addr = 0x409a14
    avoid_addr = 0x400e32

    def find_chars():   #angr can't impose md5 encryption on symbolic execution, so it's better to bruteforce 6 symbols in a separate function, approximate running time is 4-5 minutes           
        for char_1 in alphabet:
            for char_2 in alphabet:
                for char_3 in alphabet:
                    for char_4 in alphabet:
                        for char_5 in alphabet:
                            for char_6 in alphabet:
                                
                                string = char_1 + char_2 + char_3 + char_4 + char_5 + char_6
                                
                                if hashlib.md5(string.encode()).hexdigest() == '17f2289b1cfbec5b56871c15f84e5887':
                                    
                                    print(f'?????{char_1}-?????{char_2}-?????{char_3}-?????{char_4}-?????{char_5}-?????{char_6}')
                                    
                                    return string
                                    
    hash_chars = find_chars()
    
    project = angr.Project('./hasher2.elf')
    
    char_1 = claripy.BVV(hash_chars[0], 8)
    char_2 = claripy.BVV(hash_chars[1], 8)
    char_3 = claripy.BVV(hash_chars[2], 8)
    char_4 = claripy.BVV(hash_chars[3], 8)
    char_5 = claripy.BVV(hash_chars[4], 8)
    char_6 = claripy.BVV(hash_chars[5], 8)

    delim = claripy.BVV(b'-', 8)
    
    symbolic_data = [claripy.BVS(f'sym_data_{i}', 5 * 8) for i in range(6)]
    junk = claripy.BVV(b'AAAAAA-AAAAAA-AAAAAA-AAAAAA-AAAAAA-AAAAAA', 8 * 41) #This is a dummy serial number that matches the expected format.
    
    serial_number = claripy.Concat(symbolic_data[0], char_1, delim, symbolic_data[1], char_2, delim, symbolic_data[2], char_3, delim, symbolic_data[3], char_4, delim, symbolic_data[4], char_5, delim, symbolic_data[5], char_6) #Here we stick the serial number
    
    state = project.factory.entry_state(args = ['./hasher2.elf', serial_number])
    
    for data in symbolic_data:
        for byte in data.chop(8):
            state.add_constraints((byte >= 0x30) & (byte <= 0x5a))
            
    @project.hook(0x400ef3) #The check_format function is called at address 0xef3, which checks the format of the entered key. It greatly delays the work of angr if a symbolic variable flies into it, so we hook the address where the key is thrown into rdi for transfer to the function and spoof it, we give the address to which we write a dummy key that will pass this check
    def hook(state):
        state.memory.store(0x300000, junk, 41)
        state.regs.rax = 0x300000
    
    simulation = project.factory.simgr(state)
    
    simulation.explore(find = find_addr, avoid = avoid_addr)
    
    if simulation.found:

        result = simulation.found[0]
        
        flag = result.solver.eval(serial_number, cast_to = bytes)
        
        print(f'Flag is: {flag.decode('ascii')}')
        
    else:
        
        print('Nope :(')
        print(simulation.errored)
        print(hex(state.addr))
    
if __name__ == '__main__': 
    main()
