#Source: https://rev-kids20.forkbomb.ru/tasks/RE8_binculator
#Description: "The server sends you 10 binaries in turn. In response, you need to send a line that will make the current binary write "You win!". Timeout 120 seconds for each binary. After the 10th correct answer the server will send a flag."

import angr, claripy, pwn, base64


#This function performs analysis of a binary file.
def find_flag(bin_number):
    
        project = angr.Project(f'./bin_{bin_number}.elf')
        
        #The length of the lines is different each time
        for i in range(4, 11):
        
            input = claripy.BVS('input', i * 8)
            
            state = project.factory.entry_state(stdin = input)
            
            for byte in input.chop(8):
                state.add_constraints(byte >= 0x41)
                state.add_constraints(byte <= 0x7F)
            
            simulation = project.factory.simgr(state)
            
            #All binaries are typical, the output is the same. By the way, the addresses of the blocks are always different, so you can only rely on what falls into stdout
            simulation.explore(find = lambda s:b"You win" in s.posix.dumps(1))
            
            if simulation.found:
                
                result = simulation.found[0]
                
                flag = result.solver.eval(input, cast_to = bytes)
                
                return flag.decode()
                
                break
                
            else:
                
                print("angr: 'Nope :('")
                

#This function decrypts the data and creates a file with the corresponding sequence number.
def create_file(data, bin_number):
    
    try:
        
        with open(f'bin_{bin_number}.elf', 'wb') as f:
            
            f.write(base64.b64decode(data))
            
        print('File has been successfully created!')
        return True
        
    except Exception as e:
        
        print(f'Error creating file: {e}')
        return False
    

def main():
    
    r = pwn.remote('109.233.56.90', 63175)
    
    print(r.recvline().decode())
    
    for binary in range(1, 11):
            
        print(r.recvline().decode())
            
        data = r.recvline().decode()
            
        if create_file(data ,binary) == True:
                
            result = find_flag(binary)
                
            r.sendline(result)
                
            if r.recvline() == 'Nope ;[':
                
                print('Wrong answer!')
                break
                    
                
        else:
                
            print("Program will stop execution, because the file hasn't been created!")
            break
    
    flag = r.recv(numb = 256)
    
    print(f'Flag is: {flag.decode()}')
    
if __name__ == '__main__':
    
    main()
