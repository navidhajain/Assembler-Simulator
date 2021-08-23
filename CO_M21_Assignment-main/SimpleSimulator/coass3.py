import matplotlib.pyplot as plt

regs= {"000": "0000000000000000",
       "001": "0000000000000000",
       "010": "0000000000000000",
       "011": "0000000000000000",
       "100": "0000000000000000",
       "101": "0000000000000000",
       "110": "0000000000000000",
       "111": "0000000000000000"}

memory_address = []

def getbin(value):
    v = int(value)
    if value>=0:
        x = bin(v).replace("0b", "")
    else:
        x=bin(v).replace("-0b", "")
    if len(x) < 16:
        x = "0" * (16 - len(x)) + str(x)
    return str(x)

def getpc(value):
    v = int(value)
    x = bin(v).replace("0b", "")
    if len(x) < 8:
        x = "0" * (8 - len(x)) + str(x)
    return str(x)

def getint(string):
    return int(string, 2)

def add(line): #INCOMPLETE
    global program_counter
    reg1 = line[7:10]
    reg2 = getint(regs[line[10:13]])
    reg3 = getint(regs[line[13:]])
    reg4 = reg2+reg3

    if reg4>256 or reg4<0:
        regs["111"] = "0000000000001000"        
    else:        
        regs["111"] = "0000000000000000"

    regs[reg1]=getbin(reg4)    
    printline(line)
    program_counter += 1    

def sub(line): #INCOMPLETE
    global program_counter
    reg1 = line[7:10]
    reg2 = getint(regs[line[10:13]])
    reg3 = getint(regs[line[13:]])
    reg4 = reg2 - reg3

    if reg4 > 256 or reg4< 0:
        regs["111"] = "0000000000001000"       
    else:        
        regs["111"] = "0000000000000000"

    regs[reg1] = getbin(reg4)    
    printline(line)
    program_counter += 1

def movimm(line):
    global program_counter
    regs[line[5:8]] = "00000000" + line[8:]
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def movreg(line):
    global program_counter
    regs[line[10:13]] = regs[line[13:]]
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def load(line):
    global program_counter
    value = getint(line[8:])
    regs[line[5:8]] = memory_address[value]
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def store(line):
    global program_counter
    value = getint(line[8:])
    memory_address[value] = regs[line[5:8]]
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def multiply(line): #INOMPLETE
    global program_counter
    reg1 = line[7:10]
    reg2 = getint(regs[line[10:13]])
    reg3 = getint(regs[line[13:]])
    reg4 = reg2 * reg3

    if reg4 > 256 or reg4 < -256:
        regs["111"] = "0000000000001000"        
    else:     
        regs["111"] = "0000000000000000"

    regs[reg1] = getbin(reg4)            
    printline(line)
    program_counter += 1    

#nwkna
#nsakv

def divide(line):
    global program_counter
    reg1=getint(line[10:13])
    reg2=getint(line[13:])
    regs["000"]=getbin(reg1/reg2)
    regs["001"]=getbin(reg1%reg2)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def rightshift(line):
    global program_counter
    regused=line[5:8]
    a=getint(regs[regused])
    imm= getint(line[8:])
    regs[regused]=getbin(a>>imm)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def leftshift(line):
    global program_counter
    regused=line[5:8]
    a=getint(regs[regused])
    imm= getint(line[8:])
    regs[regused]=getbin(a<<imm)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def xor(line):
    global program_counter
    reg1=line[7:10]
    reg2=getint(line[10:13])
    reg3 =getint(line[13:])
    regs[reg1]=getbin(reg2^reg3)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def or1(line):
    global program_counter
    reg1=line[7:10]
    reg2=getint(line[10:13])
    reg3 =getint(line[13:])
    regs[reg1]=getbin(reg2|reg3)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def and1(line):
    global program_counter
    reg1=line[7:10]
    reg2=getint(line[10:13])
    reg3 =getint(line[13:])
    regs[reg1]=getbin(reg2 & reg3)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1


def invert(line):
    global program_counter
    reg1=line[10:13]
    reg2 =getint(line[13:])
    regs[reg1]=getbin(~reg2)
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def compare(line):
    global program_counter
    reg1 = getint(regs[line[10:13]])
    reg2 = getint(regs[line[13:]])
    if reg1 < reg2:
        regs["111"] = "0000000000000100"
    if reg1 > reg2:
        regs["111"] = "0000000000000010"
    if reg1 == reg2:
        regs["111"] = "0000000000000001"
    printline(line)
    program_counter += 1

def unconjump(line):
    global program_counter
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter = getint(line[8:])

def jlt(line):
    global program_counter
    if regs["111"] == "0000000000000100" :
        printline(line)
        program_counter = getint(line[8:])
        return
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def jgt(line):
    global program_counter
    if regs["111"] == "0000000000000010":
        printline(line)
        program_counter = getint(line[8:])
        return
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def je(line):
    global program_counter
    if regs["111"] == "0000000000000001":
        printline(line)
        program_counter = getint(line[8:])
        return
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

def hlt(line):
    global program_counter
    regs["111"] = "0000000000000000"
    printline(line)
    program_counter += 1

program_counter=0
#isko yahan pe likhne se kuch nhi hoga isse acha upar hi likh dete top pe
def printline(line):
    print(getpc(program_counter), end=' ')
    for i in regs:
        print(regs[i], end=' ')
    print()

def process(line):
    global program_counter

    code = line[:5]
    if code == "00000":
        add(line)
        #printline(line)
    if code == "00001":
        sub(line)
        #printline(line)
    if code == "00010":
        movimm(line)
        #printline(line)
    if code == "00011":
        movreg(line)
        #printline(line)
    if code=="00100":
        load(line)        
        #printline(line)
    if code=="00101":
        store(line)
        #printline(line)
    if code == "00111":
        multiply(line)
        #printline(line)
    if code=="00111":
        divide(line)
        #printline(line)
    if code=="01000":
        rightshift(line)
        #printline(line)
    if code=="01001":
        leftshift(line)
        #printline(line)
    if code=="01010":
        xor(line)
        #printline(line)
    if code=="01011":
        or1(line)
       # printline(line)
    if code=="01100":
        and1(line)
        #printline(line)
    if code=="01101":
        invert(line)
        #printline(line)
    if code=="01110":
        compare(line)
        #printline(line)
    if code=="01111":
        unconjump(line)
       # printline(line)
    if code=="10000":
        jlt(line)
        #printline(line)
    if code=="10001":
        jgt(line)
        #printline(line)
    if code=="10010":
        je(line)
        #printline(line)
    if code=="10011":
        hlt(line)
        #printline(line)

x = []
y = []

def main():
    global memory_address
    cycle_number=0
    global program_counter
    arr = []
    
    while True:
        try:
            line = input()
            if line == "ss":
                break
            arr.append(line)
        except EOFError:
            break
    len_arr = len(arr)
    for i in range(0,256):
        if i < len_arr:
            memory_address.append(arr[i])
        if i >= len_arr:
            memory_address.append("0000000000000000")


    while program_counter >=0 and program_counter < len(arr):
        x.append(cycle_number)
        y.append(program_counter)
        process(arr[program_counter])
        cycle_number+=1
        
    # print("yash is god")
    # print(x)
    # print(y)
    plt.plot(x,y,'o')
    plt.savefig("abc.png")
    #if plt.show doesnt work use plt.savefig(specify path wjere pu want to store the png)
    #for load and store 2 points aane chahiye cuz we are accenss from 2 sides


    for i in range(len(memory_address)):
        print(memory_address[i], end = '\n')

if __name__== "__main__":
    #print("yash is god")
    main()