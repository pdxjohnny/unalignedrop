#!/usr/bin/python3
import sys

for l in sys.stdin:
    l = l.split()
    if len(l) < 1 or l[0][-1] != ':' or not l[0][:-1].isdigit():
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
    l = l[:i]
    l = '%-20s%s\n' % (addr, ' '.join(l))
    sys.stdout.write(l)
