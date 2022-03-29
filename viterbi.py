#!/usr/bin/python

"""
Implement the Viterbi algorithm in Python (no tricks other than logmath!), given an
HMM, on sentences, and outputs the best state path.
Please check `viterbi.pl` for reference.

Usage:  python viterbi.py hmm-file < text > tags

special keywords:
 $init_state   (an HMM state) is the single, silent start state
 $final_state  (an HMM state) is the single, silent stop state
 $OOV_symbol   (an HMM symbol) is the out-of-vocabulary word
"""
from email.policy import default
import sys, re
from collections import defaultdict

hmm_file = sys.argv[1]

hmm=defaultdict(int)
freqs=defaultdict(int)
 
for line in open(hmm_file):
    terms=re.split("\s+", line.rstrip())
    if terms[0]=='trans':
        if terms[1] not in hmm:
            hmm[terms[1]]=defaultdict(int)

        hmm[terms[1]][terms[2]]=terms[3]

    if terms[0]=='emit':
        if terms[2] not in freqs:
            freqs[terms[2]]=defaultdict(int)

        freqs[terms[2]][terms[1]]=terms[3]

#words=['This', 'time', ',', 'the', 'firms', 'were', 'ready', '.']
#words=['Influential', 'members', 'of', 'the', 'House', 'Ways', 'and', 'Means', 'Committee', 'introduced', 'legislation', 'that', 'would', 'restrict', 'how', 'the', 'new', 'savings-and-loan', 'bailout', 'agency', 'can', 'raise', 'capital', ',', 'creating', 'another', 'potential', 'obstacle', 'to', 'the', 'government', "'s", 'sale', 'of', 'sick', 'thrifts', '.']

for line in sys.stdin:
    words=re.split("\s+", line.rstrip())
    threads=[]
    newthreads=[]
    paths=[]
    newpaths=[]
    for word in words[0:1]:
        if word in freqs: 
            active_pos=freqs[word]
            for pos in active_pos:

                if pos in hmm['init']:
                    #multiply the POS frequency of the word by the transition probability 
                    #of that POS at the start of the sentence
                    threads.append(float(hmm['init'][pos])*float(active_pos[pos]))
                    paths.append(['init',pos])
                else:
                    # print("ERROR: unknown POS")
                    # raise ValueError()
                    #what to do with unknown tag like 'RP'?
                    continue

        elif str.lower(word) in freqs:
            active_pos=freqs[str.lower(word)]
            for pos in active_pos:

                if pos in hmm['init']:
                    #multiply the POS frequency of the word by the transition probability 
                    #of that POS at the start of the sentence
                    threads.append(float(hmm['init'][pos])*float(active_pos[pos]))
                    paths.append(['init',pos])
                else:
                    # print("ERROR: unknown POS")
                    # raise ValueError()
                    continue
                    #what to do with tag like 'RP' when it follows 'init'?
        
        else:
            word="OOV"
            active_pos=freqs[word]

            for pos in active_pos:

                if pos in hmm['init']:
                    #multiply the POS frequency of the word by the transition probability 
                    #of that POS at the start of the sentence
                    threads.append(float(hmm['init'][pos])*float(active_pos[pos]))
                    paths.append(['init',pos])
                else:
                    #what to do with the 'POS' tag?s
                    # print("ERROR: unknown POS")
                    # raise ValueError()
                    continue


    for word in words[1:]:
        if word in freqs:
            active_pos = freqs[word]
            #for each pos in active_pos, 
            #take each value in threads, multiply it by the transition of the POS of the respective
            #value in threads to the pos in active pos
            #find the max of all those values, multiply it by the frequency of that word-pos, and then
            #it becomes one of the new threads/new paths, both of which must replace the lists of the previous word

            for pos in active_pos:
                if pos in hmm:
                    #take each value in threads:
                    values=[]
                    parts=[] #to track all the paths
                    for val,path in zip(threads,paths):
                        values.append(val*float(hmm[path[-1]][pos]))
                        parts.append(path)
                    #get the maximum value in values:
                    maxval=max(values)
                    maxpath=parts[values.index(maxval)] + [pos]
                    
                    #add them to the newthreads and newpaths:
                    newthreads.append(maxval*float(freqs[word][pos]))
                    newpaths.append(maxpath)
                else:
                    print("ERROR: unknown POS")
                    raise ValueError()

        elif str.lower(word) in freqs:
            active_pos=freqs[str.lower(word)]
            for pos in active_pos:
                
                if pos in hmm:
                    values=[]
                    parts=[]        
                    for val,path in zip(threads,paths):
                        values.append(val*float(hmm[path[-1]][pos]))
                        parts.append(path)
                    maxval=max(values)
                    maxpath=parts[values.index(maxval)] + [pos]

                    newthreads.append(maxval*float(freqs[str.lower(word)][pos]))
                    newpaths.append(maxpath)
                else:
                    print("ERROR: unknown POS")
                    raise ValueError()
                
        else:
            active_pos=freqs["OOV"]

            for pos in active_pos:

                if pos in hmm:
                    values=[]
                    parts=[]        
                    for val,path in zip(threads,paths):
                        values.append(val*float(hmm[path[-1]][pos]))
                        parts.append(path)
                    maxval=max(values)
                    maxpath=parts[values.index(maxval)] + [pos]

                    newthreads.append(maxval*float(freqs["OOV"][pos]))
                    newpaths.append(maxpath)
                else:
                    print("ERROR: unknown POS")
                    raise ValueError()

        threads=newthreads
        newthreads=[]
        paths=newpaths
        newpaths=[]
    
    #add the ending character:
    #active_pos=freqs[word]


    #print(threads)
    [print(i, end=" ") for i in paths[0][1:]]
    #print(paths)
    print()


        