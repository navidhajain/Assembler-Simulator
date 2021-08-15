codetable = {
    "add": ["00000", "A"],
    "sub": ["00001", "A"],
    "ld": ["00100", "D"],
    "st": ["00101", "D"],
    "mul": ["00110", "A"],
    "div": ["00111", "C"],
    "rs": ["01000", "B"],
    "ls": ["01001", "B"],
    "xor": ["01010", "A"],
    "or": ["01011", "A"],
    "and": ["01100", "A"],
    "not": ["01101", "C"],
    "cmp": ["01110", "C"],
    "jmp": ["01111", "E"],
    "jlt": ["10000", "E"],
    "jgt": ["10001", "E"],
    "je": ["10010", "E"],
    "hlt": ["10011", "F"]
}

regs = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
}

labels = {}
variable = {}
progc = 0
actualc = 0
hltnotthere = True
output = []
flagerror = True


def haslabel(line):
    if line.find(":") != -1:
        index = line.find(":")
        l = line[index + 2:]
        if l == "hlt":
            hltnotthere = False
        if l.strip() == "":
            return "0" * 8
        process(l)
        return True
    else:
        return False


def getbin(value):
    v = int(value)
    if v not in range(0, 256):
        print("Illegal Immediate values (less than 0 or more than 255) at line number ", progc)
        exit()
    x = bin(v).replace("0b", "")
    if len(x) < 8:
        x = "0" * (8 - len(x)) + str(x)
    return str(x)


def gettypea(line2):  # add r1 r2 r3, ans = 0000000
    line = str(line2)
    arr = line.split()
    if len(arr) != 4 or ":" in line or "$" in line:
        print("Wrong syntax used for instructions at line number ", progc)
        exit()
    if "FLAGS" in line:
        print("illegal use of flags at line number ", progc)
        exit()

    ans = codetable[arr[0]][0]

    if arr[1] not in regs or arr[2] not in regs or arr[3] not in regs:
        print("Typos in instruction name or register name at line number ", progc)
        exit()
    else:
        ans = ans + "00" + regs[arr[1]] + regs[arr[2]] + regs[arr[3]]

    return ans


def gettypeb(line2):
    line = str(line2)
    if ":" in line:
        print("misuse of labels at line number ", progc)
        exit()
    if "FLAGS" in line:
        print("illegal use of flags at line number ", progc)
        exit()

    arr = line.split()
    if "$" not in line or len(arr) != 3:
        print("Wrong syntax used for instructions at line number ", progc)
        exit()

    ans = codetable[arr[0]][0]
    if arr[1] not in regs:
        print("Typos in instruction name or register name at line number ", progc)
        exit()
    else:
        ans = ans + regs[arr[1]]

    ans = ans + getbin(arr[2][1:])

    return ans


def gettypec(line2):
    line = str(line2)
    arr = line.split()
    if ":" in line:
        print("misuse of labels at line number ", progc)
        exit()
    if "FLAGS" in line:
        print("illegal use of flags at line number ", progc)
        exit()
    if len(arr) != 3 or "$" in line:
        print("Wrong syntax used for instructions at line number ", progc)
        exit()

    ans = codetable[arr[0]][0]
    ans = ans + "0" * 5

    if arr[1] not in regs or arr[2] not in regs:
        print("Typos in instruction name or register name at line number ", progc)
        exit()
    else:
        ans = ans + regs[arr[1]] + regs[arr[2]]

    return ans


def mov(line2):
    line = str(line2)
    arr = line.split()
    if ":" in line:
        print("misuse of labels at line number ", progc)
        exit()
    if arr[1] == "FLAGS":
        print("illegal use of flags at line number ", progc)
        exit()
    if (len(arr) == 3):
        if arr[2][0] == "$":
            ans = "00010" + regs[arr[1]] + getbin(arr[2][1:])
        else:
            if arr[2] not in regs or arr[1] not in regs:
                print("Typos in instruction name or register name at line number ", progc)
                exit()
            ans = "00011" + "0" * 5 + regs[arr[1]] + regs[arr[2]]
    else:
        print(" general syntax error at line number ", progc)
        exit()

    return ans


def gettyped(line2):
    line = str(line2)
    arr = line.split()

    if ":" in line:
        print("misuse of labels at line number ", progc)
        exit()

    if "FLAGS" in line:
        print("illegal use of flags at line number ", progc)
        exit()

    if len(arr) != 3 or "$" in line:
        print("Wrong syntax used for instructions at line number ", progc)
        exit()

    ans = codetable[arr[0]][0]
    if arr[1] not in regs:
        print("Typos in instruction name or register name at line number ", progc)
        exit()
    else:
        ans = ans + regs[arr[1]]
    if arr[2] not in variable:
        print("Use of undefined variablesat line number ", progc)
        exit()

    ans = ans + variable[arr[2]]

    return ans


def gettypee(line2):  # ask once
    line = str(line2)
    arr = line.split()
    if "FLAGS" in line:
        print("illegal use of flags at line number ", progc)
        exit()
    if arr[1] not in labels:
        print("Use of undefined labels at line number ", progc)
        exit()
    if ":" in line:
        print("misuse of labels at line number ", progc)
        exit()    
    if len(arr) != 2 or "$" in line:
        print("Wrong syntax used for instructions at line number ", progc)
        exit()

    ans = codetable[arr[0]][0]

    ans = ans + "0" * 3 + labels[arr[1]]

    return ans


def gettypef(line2):
    line = str(line2)
    arr = line.split()
    if "FLAGS" in line:
        print("illegal use of flags at line number ", progc)
        exit()
    if ":" in line:
        print("misuse of labels at line number ", progc)
        exit()    
    if len(arr) != 1 or "$" in line:
        print("Wrong syntax used for instructions at line number ", progc)
        exit()

    ans = codetable[arr[0]][0]
    ans = ans + "0" * 11
    return ans


def isvar(line):
    arr = line.split()
    if arr[0] == "var":
        return True
    return False


def process(line):
    '''if "mov" in line and FLAGS:
        print("Illegal use of FLAGS register")
        exit()'''
    if line == '':
        return
    if (haslabel(line)):
        return
    if (isvar(line)):
        return
    line2 = str(line)
    arr = line2.split()
    if arr[0] not in codetable and arr[0] != "mov":

        print("Typos in instruction name or register name at line number ", progc)
        exit()
    else:
        if (arr[0] != "mov" and codetable[arr[0]][1] == "A"):
            output.append(gettypea(line))
        elif (arr[0] != "mov" and codetable[arr[0]][1] == "B"):
            output.append(gettypeb(line))
        elif (arr[0] != "mov" and codetable[arr[0]][1] == "C"):
            output.append(gettypec(line))
        elif (arr[0] != "mov" and codetable[arr[0]][1] == "D"):
            output.append(gettyped(line))
        elif (arr[0] != "mov" and codetable[arr[0]][1] == "E"):
            output.append(gettypee(line))
        elif (arr[0] != "mov" and codetable[arr[0]][1] == "F"):
            output.append(gettypef(line))
        elif (arr[0] == "mov"):
            output.append(mov(line))
        else:
            output.append("Genral Syntax Error at line number ", progc)
            exit()
        # except:
        #   print("g")
        #  print(mov(line))

    return


if __name__ == "__main__":

    arr = []
    arr1 = []

    while True:
        try:
            line = input()
            if line.strip != '':
                arr.append(line)
            arr1.append(line)
        except EOFError:
            break

    pc = len(arr) - 1
    l = ''
    noofvariables = 0


    for i in range(len(arr1)):
        if arr1[i] == '':
            continue
        arr2 = arr1[i].split()
        if arr2[0] == "var":
            noofvariables += 1

#arr[] = arr without empty lines
#arr1[] = arr with lines
    #for i in range(len(arr)):
        # if arr[i].strip == "":
        #     continue
    i = 0
    arr2 = arr[i].split()
    while arr2[0] == "var" :
        """if i > noofvariables:
            print("Variables not declared at the beginning at line number ")
            exit()
        if arr2[0] in variable:
            print("General Syntax Error at line number ", i + 1)
            exit()"""
        variable[arr2[1]] = getbin(len(arr) - noofvariables + i)
        i += 1
        arr2 = arr[i].split()
    # print(variable)

    for i in range(len(arr)):
        if "hlt" in arr[i] and i!=len(arr)-1:            
            print("hlt not being used as the last instruction at line number ", i)
            exit()

    for i in range(i,len(arr)):
        arr2 = arr[i].split()
        if arr2[0] == "var" :
            print("Variable not declared at the begining")
            exit()

    for i in range(0, len(arr)):
        s = arr[i]
        a = s.split()
        if ":" in s:
            if a[0] in codetable:
                print("error")
            else:
                key = a[0][:-1]
                labels[key] = getbin(i - noofvariables)
        if "hlt" in s:
            hltnotthere = False
    #print("yuvi_is_god")             

    for line in arr1:
        progc += 1
        process(line)

    if hltnotthere:
        print("Missing hlt instruction")
        exit()

    for i in output:
        print(i)