#!/usr/bin/env python3.5
import os
import sys
from pwn import *

basic_start = '''
int main() {
    asm("'''
basic_end = '''");
    return 0;
}
'''

def instructions_from_objdump(o):
    instructions = []
    for l in o.split('\n'):
        l = l.split()
        if len(l) < 1 or l[0][-1] != ':':
            continue
        try:
            int(l[0][:-1], 16)
        except:
            continue
        addr = l[0]
        i = 0
        l = l[1:]
        for w in l:
            try:
                w = bytes.fromhex(w)
            except:
                break
            i += 1
        instructions.append(l[:i])
    return instructions

def find_instructions(base, compare_too):
    j = 0
    k = 0
    for i in range(0, len(base)):
        # print(str(base[i]), str(compare_too[i]))
        if str(base[i]) != str(compare_too[i]):
            break
        j += 1
    for i in range(1, len(compare_too) + 1):
        # print(str(base[-i]), str(compare_too[-i]))
        if str(base[-i]) != str(compare_too[-i]):
            break
        k += 1
    return [i for l in compare_too[j:-k] for i in l]

def to_hex(instruction=""):
    c = basic_start + instruction + basic_end
    print(c)
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        with open('main.c', 'wb') as f:
            f.write(c.encode('ascii'))

        p = process(['gcc', 'main.c', '-c'])
        o = p.recvall().decode('utf-8')
        if len(o) > 0:
            raise Exception('ERROR compiling \'' + instruction + '\'\n' + o)

        p = process(['objdump', '-d', '-j', '.text', 'main.o'])
        o = p.recvall().decode('utf-8')
        p.wait()
        p.shutdown()
    # print(o)
    return o

def find_hex(instruction):
    base = instructions_from_objdump(to_hex())
    compare_too = instructions_from_objdump(to_hex(instruction))
    instructions = find_instructions(base, compare_too)
    return instructions

def main():
    print(find_hex(sys.argv[1]))

if __name__ == '__main__':
    main()
