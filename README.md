# Python unaligned ROP gadget finder

This is a library to help you find the addresses of gadgets in the `.text`
segment of an ELF x86 / x64 binary. There are many tools our there to find rop
gadgets but none that I have seen which find unaligned gadgets. This will of
course also find aligned gadgets.

## Installation

```log
pip3.5 install --upgrade --user \
  git+https://github.com/pdxjohnny/unalignedrop.git
```
