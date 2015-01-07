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


@memoize
def cmpfunc(a, b):
    result = None
    s = 'Which is greater, {a} or {b} (<, =, or >)? '.format(a=a, b=b)
    while result is None or result not in '<=>':
        result = input(s).strip()
    return '<=>'.index(result) - 1
keyfunc = cmp_to_key(cmpfunc)


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

class SortableWithHeuristic:

    def __init__(self, val, heur):
        self.val = val
        self.heur = heur

    def __str__(self):
	    return '{val}: {heur}'.format(val=self.val, heur=self.heur)

def get_heuristic_func(val):
    result = None
    s = 'Give an approximate numeric score to item {}: '.format(val)
    while result is None:
        try:
            result = float(input(s).strip())
        except ValueError:
            pass
    return result

def heuristic_sort(seq, get_heuristic_func, cmpfunc):
    def swap(a, b):
        seq[a], seq[b] = seq[b], seq[a]

    idx = 0
    while idx < len(seq):
        val = seq[idx]
        heur = get_heuristic_func(val)
        seq[idx] = SortableWithHeuristic(val, heur)

        # find the current location
        j = idx
        while j > 0 and seq[j].heur < seq[j-1].heur:
            swap(j, j-1)
            j -= 1

        moved = False
        while j < idx and cmpfunc(seq[j].val, seq[j+1].val) == 1:
            swap(j, j+1)
            j += 1
            moved = True

        if not moved:
            while j > 0 and cmpfunc(seq[j].val, seq[j-1].val) == -1:
                swap(j, j-1)
                j -= 1

        if 0 < j < idx:
            seq[j].heur = (seq[j-1].heur + seq[j+1].heur) / 2
        elif idx > 0:
	        if j == 0 and seq[j].heur > seq[j+1].heur:
		        seq[j].heur = seq[j+1].heur - 1
	        elif j == idx and seq[j].heur < seq[j-1].heur:
		        seq[j].heur = seq[j-1].heur + 1

        idx += 1


def main():
    import sys
    seq = []
    if len(sys.argv) > 1:
        seq.extend(sys.argv[1:])
    if not seq:
        seq.extend(x.strip() for x in sys.stdin.readlines())
    heuristic_sort(seq, get_heuristic_func, cmpfunc)
    print('\n'.join('* {}'.format(item) for item in reversed(seq)))

if __name__ == '__main__':
    main()
