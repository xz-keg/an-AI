# make moves
import torch
import numpy as np

def makemove(state,move,type=0):
#type-- board information type, we shall support 48 channel version, 18 channel and 17 channel version.
# 48 channel version need some further modification functions to be done.
#move-- an integer 0~362
    newstate=torch.zeros(17,19,19)
    for i in range(7):
        newstate[2+i*2]=state[1+i*2]
        newstate[3+i*2]=state[0+i*2]
    newstate[16]=1-state[16]
    newstate[0]=newstate[2]
    newstate[1]=newstate[3]
    mvx=move/19
    mvy=move%19
    if (move!=361):
        if newstate[0][mvx][mvy]==1:
            return newstate,1 #error!illegal move
        newstate[0][mvx][mvy]=1

    issearched=np.zeros(19,19)
    def checkstate(i,j,w,color):
        if issearched[i][j]>0:
            return -1
        issearched[i][j]=w
        for i1 in [-1,1]:
            for i2 in [-1,1]:
                newx=i+i1
                newy=i+i2
                if (newx>=0) and (newx<=18) and (newy>=0) and (newy<=18):
                    if newstate[color][newx][newy]+newstate[1-color][newx][newy]==0:
                        return 0
                    if newstate[1-color][newx][newy]==1:
                        k=checkstate(newx,newy)
                        if k==0:
                            return 0
        return 1

    w=0
    if (move!=361):
        for i1 in [-1,1]:
            for i2 in [-1,1]:
                newx=mvx+i1
                newy=mvy+i2
                if (newx>=0) and (newx<=18) and (newy>=0) and (newy<=18) and (newstate[1][newx][newy]==1):
                    w=w+1
                    stat=checkstate(newx,newy,w,0)
                    if stat==1:
                        for i in range (19):
                            for j in range(19):
                                if issearched[i][j]==w:
                                    newstate[1][newx][newy]=0
        if checkstate(mvx,mvy,w+1,1)==1:
            return state,1 #error!illegal move

#compare against previous stages to make sure there's no repetition
    err=0
    for ii in range(1,4):
        suc=0
        for i in range(2):
            for j in range(19):
                for k in range(19):
                    if newstate[ii*4+i][j][k]!=newstate[i][j][k]:
                        suc=1
        if suc==0:
            if (move!=361) or (ii!=1):
                return newstate,1  #error!illegal move!
            else
                return newstate,2  #double pass

    return newstate,0  #legal move





