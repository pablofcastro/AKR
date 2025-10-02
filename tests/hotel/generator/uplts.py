from num2words import num2words

def preamble(doors):

    result  = "plts:\n"
    result += "    formula launch   = (s=0)\n"
    result += "                     & (c=0)"

    for door in range(1,doors+1):
        result += f"\n                     & (v{door}=0)"
    
    result += ";\n"

    return result

def init(doors):

    result  = f"\n    formula complete = (c>={doors//2});\n"
    result += "\n"
    result += "    module plts\n"
    result += f"        s  : [0..{doors}];\n"
    result += f"        c  : [0..{doors}];\n"
    
    for door in range(1,doors+1):
        result += f"        v{door} : [0..1];\n"

    return result+"\n"

def command(doors, source, target, probability):

    result  = "        "
    result += f"[{num2words(target)}] " # action
    result += f"(s={source}) -> "       # guard
    result += f"{probability:.2f}:(s'={target})&(c'=min({doors},c+(1-v{target})))&(v{target}'=1) + " # prob: update
    result += f"{(1-probability):.2f}:(s'={target})&(c'=c)&(v{target}'=1);\n" # prob: update

    return result

def epilogue():

    result  = "    endmodule\n"
    result += "endplts\n\n"

    return result

def plts(doors,probabilities):

    result  = preamble(doors)

    result += init(doors)

    result += f"{command(doors,source=0,target=1,probability=probabilities[1])}"
    result += f"{command(doors,source=0,target=2,probability=probabilities[2])}"

    result += f"{command(doors,source=1,target=2,probability=probabilities[2])}"
    result += f"{command(doors,source=1,target=3,probability=probabilities[3])}"

    result += f"{command(doors,source=2,target=1,probability=probabilities[1])}"
    result += f"{command(doors,source=2,target=4,probability=probabilities[4])}"

    for door in range(3,doors-1):

        target  = door-2
        result += f"{command(doors,source=door,target=target,probability=probabilities[target])}"

        target  = door + (1 if (door % 2) else -1)
        result += f"{command(doors,source=door,target=target,probability=probabilities[target])}"

        target  = door+2
        result += f"{command(doors,source=door,target=target,probability=probabilities[target])}"

    source, target  = doors-1, doors-3
    result += f"{command(doors,source,target,probability=probabilities[target])}"

    target  = doors
    result += f"{command(doors,source,target,probability=probabilities[target])}"

    source, target  = doors, doors-2
    result += f"{command(doors,source,target,probability=probabilities[target])}"

    target  = doors-1
    result += f"{command(doors,source,target,probability=probabilities[target])}"

    result += epilogue()

    return result

def kh(success):

    result  = f"property : Kh(launch,complete) >= {success}\n"
    result += f"endproperty\n"

    return result

def tango(doors):

    result = ""

    path  = [ num2words(door) for door in range(1,doors+1,2) ]
    path += [ num2words(door) for door in reversed(range(2,doors+1,2)) ]

    result  = "("+".".join(path)+")*+("+".".join(reversed(path))+")*"

    return result

def pericon(doors):

    result = []

    for door in range(1,doors,2):
        result += [f"(({num2words(door)}.{num2words(door+1)})*+({num2words(door+1)}.{num2words(door)})*)"]

    result  = ".".join(result)

    return result

def zamba(doors):

    result = ""

    path   = ["one"]
    flip   = 1
    room   = 1

    for cursor in range(0,doors-1):
        room += 2 if (cursor % 2) else flip
        path += [f"{num2words(room)}"]
        flip  = (-1*flip) if (cursor % 2) else flip
    
    result  = "("+".".join(path)+")+"

    path   = ["two"]
    flip   = -1
    room   = 2

    for cursor in range(0,doors-1):
        room += 2 if (cursor % 2) else flip
        path += [f"{num2words(room)}"]
        flip  = (-1*flip) if (cursor % 2) else flip

    result  += "("+".".join(path)+")"

    return result

def perception(doors, mode):

    result  = "perception :\n    "

    if mode == "tango":
        result += tango(doors)
    elif mode == "pericon":
        result += pericon(doors)
    elif mode == "zamba":
        result += zamba(doors)

    result += "\nendperception\n\n"

    return result