#!/usr/bin/env python3.5
import sys
import subprocess

import unalignedrop.asm_compiler
import unalignedrop.cache

@unalignedrop.cache.Cache
def section(section, look_in_file):
    o = subprocess.check_output(['objdump', '-D', '-z', look_in_file])
    look_in = unalignedrop.asm_compiler.sections_from_objdump(o.decode('utf-8'))

    found = False
    offset = 0
    for i in range(0, len(look_in)):
        print(look_in[i][0], hex(len(look_in[i][1])))
        if look_in[i][0] == section:
            found = True
            break
        offset += len(look_in[i][1])

    if not found:
        raise Exception('Could not find \'' + section + '\' in ' + look_in_file)

    return offset

def main():
    addr = hex(section(sys.argv[1], sys.argv[2]))
    print('Section \'%s\' is at %s' % (sys.argv[1], addr))

if __name__ == '__main__':
    main()
