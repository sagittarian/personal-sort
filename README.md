personal-sort
=============

Sort a list by your own subjective criteria

A simple implementation of a sorting algorithm, meant to allow
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

