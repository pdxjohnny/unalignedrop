#!/usr/bin/env python3.5
import os
import sys
import json
import hashlib
import subprocess

import unalignedrop.asm_compiler

class CacheGadget(object):

    def __init__(self, func):
        self.cache_file = os.path.join(os.path.expanduser('~'), '.unalignedrop-cache')
        self.cache = {}
        self.func = func
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except:
                pass

    def __call__(self, look_for_asm, look_in_file):
        h = look_in_file
        try:
            h = hashlib.md5()
            with open(look_in_file, 'rb') as f:
                for l in f:
                    h.update(l)
            h = h.digest().hex()
        except:
            pass
        if h in self.cache and look_for_asm in self.cache[h]:
            res = self.cache[h][look_for_asm]
            if not isinstance(res, int):
                raise Exception(res)
            return res
        else:
            try:
                res = self.func(look_for_asm, look_in_file)
            except Exception as e:
                res = str(e)
            if not h in self.cache:
                self.cache[h] = {}
            self.cache[h][look_for_asm] = res
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
            if not isinstance(res, int):
                raise Exception(res)
            return res

@CacheGadget
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
