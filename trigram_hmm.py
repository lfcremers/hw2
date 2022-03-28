#!/usr/bin/python

"""
Implement a trigrm HMM and viterbi here. 
You model should output the final tags similar to `viterbi.pl`.

Usage:  python train_trigram_hmm.py tags text > tags

"""
import sys,re,collections

def train_trigram_hmm():
    hmm=collections.defaultdict(int)
    for line in open(sys.argv[1]):
        for term in line:
            print(term)



def viterbi_trigram():
    pass


if __name__ == "__main__":
    train_trigram_hmm()
    viterbi_trigram()
    
