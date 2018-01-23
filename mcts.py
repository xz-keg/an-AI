import torch
import numpy as np
from makemove import makemove
class edge():
    #state=torch.zeros(17,19,19)
    p=0
    q=0
    nvisit=0
    move=-1

class node():
    def __init__(self,state):
        self.state=state
        self.statehash=hashstate(state)
        self.policy,self.value=getnetpred(state)
        self.score=self.value
        self.visitcount=1
        self.edges=[]
        for i in range(362):
            self.edges.append(edge())
            self.edges[i].p=self.policy[i]
            self.edges[i].move=i
            self.edges[i].q=self.value

    def expand(self):
        highest=-0.01
        highind=-1
        factor=0.1
        for i in range(362):
            if self.edges[i].p/(1+self.edges[i].nvisit)*factor+self.edges[i].q>highest:
                highest=self.edges[i].p/(1+self.edges[i].nvisit)+self.edges[i].q
                highind=i
#makemove
        return highind


#state is different from edge, since it allows multiple edges to gather


def hashstate(state):
#hash a state by
#1:the top layer
#2: all forbidden move points
    nu=state[16][0][0]
    hash=str(nu)
    for i in range(19):
        for j in range(19):
            if (state[0][i][j]+state[1][i][j]==0):
                hash=hash+'0'
            if state[0][i][j]==1:
                hash=hash+'1'
            if state[1][i][j]==1:
                hash=hash+'2'
    for i in range(362):
        a,b=makemave(state,i)
        hash=hash+str(b)
    return hash





def mcts(state,times)
    allstates=[]
    start=node(state)
    allstates.append(start)
    hashlist=[]
    for i in range(times):
#start from scratch
        revstate=[]
        revstate.append(0)
        curstate=allstates[0]
        while curstate.statehash in hashlist:
            move=curstate.expand()
            newstate=makemove(curstate.state,move)
            newstatehash=hashstate(newstate)
            if newstatehash in hashlist:
#find the state which is
                jj=0
                while newstatehash!=allstates[jj].statehash:
                    jj=jj+1
                




