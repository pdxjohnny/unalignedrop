#!/usr/bin/env python3.5
import os
import json
import hashlib


class Cache(object):
    def __init__(self, func):
        cache_name = ".unalignedrop-cache-{0}".format(func.__name__)
        self.cache_file = os.path.join(os.path.expanduser("~"), cache_name)
        self.cache = {}
        self.func = func
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    self.cache = json.load(f)
            except:
                pass

    def __call__(self, file_search, look_in_file):
        h = look_in_file
        try:
            h = hashlib.md5()
            with open(look_in_file, "rb") as f:
                for l in f:
                    h.update(l)
            h = h.digest().hex()
        except:
            pass
        if h in self.cache and file_search in self.cache[h]:
            res = self.cache[h][file_search]
            if not isinstance(res, int):
                raise Exception(res)
            return res
        else:
            try:
                res = self.func(file_search, look_in_file)
            except Exception as e:
                res = str(e)
            if not h in self.cache:
                self.cache[h] = {}
            self.cache[h][file_search] = res
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f)
            if not isinstance(res, int):
                raise Exception(res)
            return res
