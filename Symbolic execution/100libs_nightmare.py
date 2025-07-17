#Source: https://rev-kids20.forkbomb.ru/tasks/RE8_100libs_nightmare
#Description: "Task is hard: make the binary say "YES""

import claripy, angr

def main():
    
    find_addr = 0x40219e

    #It is necessary to disable the loading of lib, because otherwise the simulation here accesses the wrong address, where, as expected, it finds nothing
    project = angr.Project('./100libs.elf', auto_load_libs = False)
    
    for i in range(0, 100):

        #And since autoloading of libs is disabled, you need to load them manually
        project.loader.dynamic_load(f"./libs/verify{i}.so")
    
    print(hex(project.loader.main_object.mapped_base))
    
    x = claripy.BVS('x', 50 * 8)
    newline = claripy.BVV(b'\n', 8)
    
    input = x.concat(newline)
    
    state = project.factory.entry_state(args = ['./100libs.elf'],stdin = input)
    
    for byte in x.chop(8):
        
        state.add_constraints(byte >= 0x21)
        state.add_constraints(byte <= 0x7e)

    #Here is where the most interesting part begins: since angr can't figure out what dlsym returns (it places some symbolic value in rax), it is necessary to tell angr at what address the function should be called. Since the libs have already been loaded, all that remains is to hook each call to the library check and throw the base address of the lib + the offset to the check function into rax, which will always be equal to 0x57a, the call occurs every 0x3f bytes
    for i in range(0, 100):
        
        lib = project.loader.shared_objects.get(f"verify{i}.so")
        
        call_addr = 0x400829 + 0x41 * i
        lib_addr = lib.mapped_base
        
        project.hook(call_addr, lambda state, lib_addr=lib_addr: setattr(state.regs, 'rax', lib_addr + 0x57a))
    
    simulation = project.factory.simgr(state)

    simulation.explore(find = find_addr)
    
    if simulation.found:

        result = simulation.found[0]
        
        flag = result.solver.eval(x, cast_to = bytes).decode('ascii')
        
        print(f'Flag is: {flag}')
        
    else:
        
        print('Nope :(')
        print(simulation.errored)
    
   
if __name__ == '__main__':
    
    main()
