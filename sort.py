#!/usr/bin/env python3
'''A simple implementation of a sorting algorithm, meant to allow
people to manually rank a list of items using whatever subjective or
objective criteria they want.

This program can be called as a script and used interactively.  You
can provide the list of things to sort as command line arguments, or
if there are no arguments provided, you can provide the list in stdin,
one item per line.

Example run:

$ ./sort.py 'ice cream' falafel hamburgers pizza
Which is greater, falafel or ice cream (<, =, or >)? <
Which is greater, hamburgers or ice cream (<, =, or >)? <
Which is greater, hamburgers or falafel (<, =, or >)? >
Which is greater, pizza or hamburgers (<, =, or >)? >
Which is greater, pizza or ice cream (<, =, or >)? <
* ice cream
* pizza
* hamburgers
* falafel

Author: Adam Mesha <adam@mesha.org>
License: MIT

'''
from functools import cmp_to_key


class memoize:
    '''We really want to be sure that we don't ask people to compare the
    same two items twice, so we cache the result.

    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        key = tuple(args)
        if key not in self.cache:
            self.cache[key] = self.func(*args)
        return self.cache[key]


@cmp_to_key
@memoize
def keyfunc(a, b):
    result = None
    s = 'Which is greater, {a} or {b} (<, =, or >)? '.format(a=a, b=b)
    while result is None or result not in '<=>':
        result = input(s).strip()
    return '<=>'.index(result) - 1


def binary_insertion_sort(seq, keyfunc):
    '''Insertion sort, using binary search to insert each element.  Runs
    in O(n**2) time, but the use case is when a human is manually
    deciding on the ordering, so the most important thing is to reduce
    the number of comparisons.

    '''
    def mv(srcidx, dstidx):
        while srcidx > dstidx:
            seq[srcidx], seq[srcidx - 1] = seq[srcidx - 1], seq[srcidx]
            srcidx -= 1

    i = 1
    while i < len(seq):
        lower = 0; upper = i
        while lower < upper:
            j = (upper + lower) // 2
            key1, key2 = keyfunc(seq[i]), keyfunc(seq[j])
            if key1 == key2:
                mv(i, j+1) # XXX this is not stable
                i += 1
                break
            if key1 < key2:
                upper = j
            else: # >
                lower = j + 1
        else:
            mv(i, upper)
            i += 1


def main():
    import sys
    seq = []
    if len(sys.argv) > 1:
        seq.extend(sys.argv[1:])
    if not seq:
        seq.extend(x.strip() for x in sys.stdin.readlines())
    binary_insertion_sort(seq, keyfunc)
    print('\n'.join('* {}'.format(item) for item in reversed(seq)))

if __name__ == '__main__':
    main()
