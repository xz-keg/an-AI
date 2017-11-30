#tromp--tayler scoring
import torch
import numpy as np

def scoring(state,komi):
    
    issearched=np.zeros(19,19)
    def checkstate(i,j,w):
        if issearched[i][j]>0:
            return -1
        issearched[i][j]=w
        current=0
        #0 , no #1, only 0, #2, only 1, #3, both
        for i1 in [-1,1]:
            for i2 in [-1,1]:
                newx=i+i1
                newy=i+i2
                if current==3:
                    return 3
                if (newx>=0) and (newx<=18) and (newy>=0) and (newy<=18):
                    if state[0][newx][newy]+state[1][newx][newy]==0:
                        k=checkstate(newx,newy)
                        if (k==3):
                            return 3
                        if (k==1) and (current in [0,2]):
                            current=current+1
                        if (k==2) and (current in [0,1]):
                            current=current+2

                    #0,
                    if state[0][newx][newy]==1:
                        # same as k==1
                        if (current in [0,2]):
                            current=current+1
                    if state[1][newx][newy]==1:
                        if (current in [0,1]):
                            current=current+2
                                
        return current
    w=0
    lis=[0]
    for i in range(19):
        for j in range(19):
            if issearched[i][j]==0:
                if state[0][i][j]+state[1][i][j]==0:
                    w=w+1
                    now=checkstate(i,j,w)
                    lis.append(now)
    score=[0,0]
    for i in range(19):
        for j in range(19):
            if state[0][i][j]==1:
                score[0]+=1
            if state[1][i][j]==1:
                score[1]+=1
            if state[0][i][j]+state[1][i][j]==0:
                sc=lis[int(issearched[i][j])]
                if sc==1:
                    score[0]+=1
                if sc==2:
                    score[1]+=1

    if state[16][0][0]==1:
        return score[0]-score[1]-komi
    else:
        return score[0]-score[1]+komi

    return 0



