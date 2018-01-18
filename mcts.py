import torch
import numpy as np
from makemove import makemove
class edge():
    state=torch.zeros(17,19,19)
    p=
    q=
    nvisit=

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




def mcts(state,times)
{
    allsituation=[]
    
    state_count=[]
    state_next=[]
    def deepen(state,makemove,getnetpred,id)
        state_hash=hash(state)
        #if not at leaf, move on
        if state_hash in allsituation:
            ind=allsituation.index(state_hash)
            policy,value=netpred[ind]
            state_count+=1
            
            move=get_move()
            makemove(state,move)
        #if already at leaf, terminates
        else:
            allsituation.append(state_hash)
            ind=len(allsituation)-1
            policy,value=getnetpred(state)
            state_count.append(1)
            policy_count,value_actual=[]
        
        return value

#policy, 362 vector
#value predicted value
#ncount-- 362 array of each visiting
#
# calculate
#check for all 362 possible cases.
#
}
