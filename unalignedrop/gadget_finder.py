#!/usr/bin/env python3.5
import sys
import subprocess

import unalignedrop.asm_compiler

def gadget(look_for_asm, look_in_file):
    look_for = unalignedrop.asm_compiler.find_hex(look_for_asm)
    print('Looking for: \'' + look_for_asm + '\'' + ' -> ' + str(look_for))

    o = subprocess.check_output(['objdump', '-d', '-j', '.text', look_in_file])
    look_in = unalignedrop.asm_compiler.instructions_from_objdump(o.decode('utf-8'))
    look_in = [i for l in look_in for i in l]

    look_for = ''.join(look_for)
    look_in = ''.join(look_in)

    i = look_in.find(look_for)
    if i > 0:
        return int(i / 2)
    raise Exception('Could not find \'' + look_for_asm + '\' in ' + look_in_file)

def main():
    addr = hex(gadget(sys.argv[1], sys.argv[2]))
    print('Target gadget \'%s\' is at %s' % (sys.argv[1], addr))

if __name__ == '__main__':
    main()
