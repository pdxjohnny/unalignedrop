#!/usr/bin/env python3.5
import os
import sys
import tempfile
import subprocess

basic_start = '''
int main() {
    asm("'''
basic_end = """");
    return 0;
}
"""


def sections_from_objdump(o):
    last_section = ""
    sections = []
    instructions = []
    for l in o.split("\n"):
        if len(l) > 0 and l.startswith("Disassembly of section"):
            if last_section != "":
                sections.append([last_section, instructions])
                instructions = []
            last_section = l.split()[-1][:-1]
        objdump_line_to_array(l, instructions)
    if last_section != "":
        sections.append([last_section, instructions])
    return sections


def instructions_from_objdump(o):
    instructions = []
    for l in o.split("\n"):
        objdump_line_to_array(l, instructions)
    return instructions


def objdump_line_to_array(l, instructions):
    l = l.split()
    if len(l) < 1:
        return
    try:
        addr = int(l[0][:-1], 16)
    except:
        return
    l = l[1:]
    for w in l:
        try:
            bytes.fromhex(w)
            if addr < len(instructions):
                instructions[addr] = w
            else:
                instructions.append(w)
            addr += 1
        except:
            break


def find_instructions(base, compare_too):
    j = 0
    k = 0
    for i in range(0, len(base)):
        # print(base[i], compare_too[i])
        if base[i] != compare_too[i]:
            break
        j += 1
    for i in range(1, len(compare_too) + 1):
        # print(base[-i], compare_too[-i])
        if base[-i] != compare_too[-i]:
            break
        k += 1
    return [i for i in compare_too[j:-k]]


def to_hex(instruction=""):
    c = basic_start + instruction + basic_end
    # print(c)
    pwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        try:
            os.chdir(d)
            with open("main.c", "wb") as f:
                f.write(c.encode("ascii"))

            o = ""
            try:
                o = subprocess.check_output(["gcc", "main.c", "-c"])
                o = o.decode("utf-8")
            except Exception as e:
                if len(o) > 0:
                    raise Exception("ERROR compiling '" + instruction + "'\n" + o)
                else:
                    raise e

            o = subprocess.check_output(["objdump", "-d", "-j", ".text", "main.o"])
            o = o.decode("utf-8")
        finally:
            os.chdir(pwd)
    # print(o)
    return o


def find_hex(instruction):
    base = instructions_from_objdump(to_hex())
    compare_too = instructions_from_objdump(to_hex(instruction))
    instructions = find_instructions(base, compare_too)
    return instructions


def main():
    print(find_hex(sys.argv[1]))


if __name__ == "__main__":
    main()
