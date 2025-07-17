#Source: https://rev-kids20.forkbomb.ru/tasks/RE8_smsserver
#Description: "HELP ME REGISTER THIS SMS SERVER I DON'T HAVE 700€ TO BUY THE PAID VERSION SO YOU MUST CRACK IT FOR ME BECAUSE YOU SAY YOU CAN REVERSE"

from z3 import *

def main():
    
    x = [BitVec(f'x_{i}', 32) for i in range(30)]
    
    solver = Solver()
    
    for byte in x:
        
        solver.add(byte >= 0x21)
        solver.add(byte <= 0x7e)
    
    #XOR and byte multiplication + comparison with a constant - this is literally the entire logic of checking the serial number, the difficulty is that the check consists of 4 functions, each of which has about 10 such blocks, but it is enough to sort through a little less than half and z3 will find a valid key from the program
    solver.add((x[10] * x[28]) ^ (x[4] * x[20]) == 7996)
    solver.add((x[16] * x[3]) ^ (x[22] * x[25]) == 689)
    solver.add((x[0] * x[17]) ^ (x[9] * x[18]) == 1227)
    solver.add((x[9] * x[8]) ^ (x[9] * x[28]) == 1992)
    solver.add((x[6] * x[5]) ^ (x[18] * x[14]) == 1466)
    solver.add((x[1] * x[3]) ^ (x[17] * x[1]) == 6880)
    solver.add((x[24] * x[21]) ^ (x[12] * x[20]) == 7497)
    solver.add((x[4] * x[29]) ^ (x[12] * x[11]) == 3535)
    solver.add((x[1] * x[13]) ^ (x[12] * x[26]) == 5456)
    solver.add((x[27] * x[3]) ^ (x[2] * x[12]) == 7514)
    solver.add((x[4] * x[27]) ^ (x[16] * x[18]) == 176)
    solver.add((x[1] * x[25]) ^ (x[12] * x[2]) == 2810)
    solver.add((x[10] * x[10]) ^ (x[3] * x[0]) == 4688)
    solver.add((x[22] * x[6]) ^ (x[2] * x[22]) == 1489)
    solver.add((x[28] * x[8]) ^ (x[23] * x[23]) == 8080)
    solver.add((x[29] * x[22]) ^ (x[10] * x[15]) == 7121)
    solver.add((x[27] * x[19]) ^ (x[0] * x[20]) == 6565)
    solver.add((x[14] * x[16]) ^ (x[24] * x[21]) == 230)
    solver.add((x[2] * x[25]) ^ (x[14] * x[7]) == 1658)
    solver.add((x[4] * x[21]) ^ (x[5] * x[8]) == 2392)
    solver.add((x[29] * x[10]) ^ (x[24] * x[19]) == 882)
    solver.add((x[14] * x[7]) ^ (x[5] * x[9]) == 7654)
    solver.add((x[10] * x[26]) ^ (x[18] * x[26]) == 432)
    solver.add((x[14] * x[26]) ^ (x[4] * x[23]) == 8032)
    solver.add((x[9] * x[24]) ^ (x[9] * x[0]) == 6270)
    solver.add((x[29] * x[12]) ^ (x[15] * x[23]) == 2016)
    solver.add((x[28] * x[11]) ^ (x[21] * x[19]) == 5996)
    solver.add((x[3] * x[5]) ^ (x[11] * x[21]) == 2244)
    solver.add((x[5] * x[22]) ^ (x[0] * x[13]) == 5988)
    solver.add((x[3] * x[21]) ^ (x[1] * x[17]) == 7014)
    
    
    if solver.check() == sat:
        
        model = solver.model()
        serial_number = str()
        
        for i in range(30):
            serial_number += chr(model[x[i]].as_long())
            
        print(serial_number)
        
    else:
        
        print("Nope :(")
    
    
    
if __name__ == "__main__":
    
    main()
