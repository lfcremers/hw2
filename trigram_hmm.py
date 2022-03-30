#!/usr/bin/python

"""
Implement a trigrm HMM and viterbi here. 
You model should output the final tags similar to `viterbi.pl`.

Usage:  python train_trigram_hmm.py tags text > tags

"""

#python trigram_hmm.py ptb.2-21.tgs ptb.2-21.txt[train text?] [intefence text]> ptb.23.out
#python trigram_hmm.py data/ptb.2-21.tgs ptb.2-21.txt ptb.22.txt> ptb.23.out

import sys,re,collections

vocab={}

emissions = {}
transitions = {}
transitionsTotal=collections.defaultdict(int)
emissionsTotal=collections.defaultdict(int)

hmm={}
freqs={}

def train_trigram_hmm():
    
    prevtag="init"
    prevprevtag="init"
    for tags, tokens in zip(open(sys.argv[1]),open(sys.argv[2])):
        words=re.split("\s+", tokens.rstrip())
        tags=re.split("\s+", tags.rstrip())
        for tag,word in zip(tags, words):

            if word not in vocab:
                vocab[word]=1
                word="OOV"
            if tag not in emissions:
                emissions[tag] = collections.defaultdict(int)
             
            if prevprevtag not in transitions:
                transitions[prevprevtag]= collections.defaultdict(int)
                transitionsTotal[prevprevtag]=collections.defaultdict(int)
                hmm[prevprevtag]=collections.defaultdict(int)

            if prevtag not in transitions[prevprevtag]:
                transitions[prevprevtag][prevtag]=collections.defaultdict(int)
                #transitionsTotal[prevprevtag][prevtag]=collections.defaultdict(int)
                hmm[prevprevtag][prevtag]=collections.defaultdict(int)

            emissions[tag][word]+=1
            emissionsTotal[tag]+=1

            transitions[prevprevtag][prevtag][tag]+=1
            transitionsTotal[prevprevtag][prevtag]+=1

            prevprevtag=prevtag
            prevtag=tag

        if prevprevtag not in transitions:
            transitions[prevprevtag]=collections.defaultdict(int)
            transitionsTotal[prevprevtag]=collections.defaultdict(int)
            hmm[prevprevtag]=collections.defaultdict(int)
        if prevtag not in transitions[prevprevtag]:
            transitions[prevprevtag][prevtag]=collections.defaultdict(int)
            hmm[prevprevtag][prevtag]=collections.defaultdict(int)

        transitions[prevprevtag][prevtag]["final"]+=1
        transitionsTotal[prevprevtag][prevtag]+=1
        prevtag="init"
        prevprevtag="init"

    for prevprevtag in transitions:
        for prevtag in transitions[prevprevtag]:
            for tag in transitions[prevprevtag][prevtag]:
                hmm[prevprevtag][prevtag][tag]=(float(transitions[prevprevtag][prevtag][tag])/transitionsTotal[prevprevtag][prevtag])

    for tag in emissions:
        for word in emissions[tag]:
            if word not in freqs:
                freqs[word]=collections.defaultdict(int)
            freqs[word][tag]=(float(emissions[tag][word])/emissionsTotal[tag])


def viterbi_trigram():
    for line in open(sys.argv[3]):
        words=re.split("\s+", line.rstrip())
        threads,newthreads,paths,newpaths=[],[],[],[]
        prevtag="init"
        prevprevtag='init'
        for idx in range(len(words)):
            if words[idx] in freqs:
                active_pos=freqs[words[idx]]
                word=words[idx]
            elif str.lower(words[idx]) in freqs:
                active_pos=freqs[str.lower(words[idx])]
                word=str.lower(words[idx])
            else:
                word="OOV"
                active_pos=freqs[word]

            if idx==0:
                
                for pos in active_pos:
                    if pos in hmm['init']['init']:

                        threads.append(float(hmm['init']['init'][pos])*float(active_pos[pos]))
                        paths.append(['init','init',pos])
                    else:
                        #raise ValueError()
                        continue
            else:
                
                for pos in active_pos:
                    #if pos in hmm[paths[-2]][paths[-1]]:
                    values=[]
               
                    for val, path in zip(threads, paths):
                        if path[-1] in hmm[path[-2]] and pos in hmm[path[-2]][path[-1]]:

                            values.append(val*float(hmm[path[-2]][path[-1]][pos]))
                        else:
                            values.append(0)
                        
                    
                    maxval=max(values)
                    maxpath=paths[values.index(maxval)]+[pos]
                    newthreads.append(maxval* float(freqs[word][pos]))
                    newpaths.append(maxpath)
                    # else:
                    #     raise ValueError()
            
                threads=newthreads
                newthreads=[]
                paths=newpaths
                newpaths=[]
        [print(i, end=" ") for i in paths[0][2:]]
        print()


if __name__ == "__main__":
    train_trigram_hmm()
    viterbi_trigram()

