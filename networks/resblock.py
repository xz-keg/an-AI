from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math

__all__ = ['ResNet']

global_progress = 0.0

class _ResBlock(nn.Module):
    def __init__(self,input_channel,res1_channel):
        #input=output, since this is a resnet structure
        super(_ResBlock,self).__init__()
        self.in_channels=input_channel
        self.conv1=nn.Conv2d(input_channel,res1_channel,[3,3],stride=1)
        self.conv2=nn.Conv2d(res1_channel,input_channel,[3,3],stride=1)
        self.norm1=nn.BatchNorm2d(input_channel)
        self.norm2=nn.BatchNorm2d(res1_channel)
        self.relu=nn.ReLU(inplace=True)
    
    def forward(self,x):
        x1=self.conv1(x)
        x1=self.norm2(x1)
        x1=self.relu(x1)
        x1=self.conv2(x1)
        x=x+x1
        x=self.norm1(x)
        x=self.relu(x)
        return x

class _ConvBlock(nn.Module):
    def __init__(self,input_channel,output_channel):
        super(_ConvBlock,self).__init__()
        self.in_channels=input_channel
        self.conv=nn.Conv2d(input_channel,output_channel,[3,3],stride=1)
        self.norm=nn.BatchNorm2d(output_channel)
        self.relu=nn.ReLU(inplace=True)
    def forward(self,x):
        x=self.conv(x)
        x=self.norm(x)
        x=self.relu(x)
        return x

class _Policy(nn.Module):
    def __init__(self,input_channel,output_channel):
        super(_Policy,self).__init__()
        self.conv=nn.Conv2d(input_channel,output_channel,[1,1],stride=1)
        self.norm=nn.BatchNorm2d(output_channel)
        self.relu=nn.ReLU(inplace=True)
        
        self.out=nn.Linear(361*output_channel,362)
    def forward(self,x):
        x=self.conv(x)
        x=self.norm(x)
        x=self.relu(x)
        x=x.view(x.size(0),-1)
        x=self.out(x)
        return x

class _Value(nn.Module):
    def __init__(self,input_channel,output_channel,komi_type=1):
        super(_Value,self).__init__()
        self.conv=nn.Conv2d(input_channel,output_channel,[1,1],stride=1)
        self.norm=nn.BatchNorm2d(output_channel)
        self.relu=nn.ReLU(inplace=True)
        
        self.hidden=nn.Linear(361*output_channel,256)
        self.scale=nn.Linear(256,komi_type=1)
    
    def forward(self,x):
        x=self.conv(x)
        x=self.norm(x)
        x=self.relu(x)
        x=x.view(x.size(0),-1)
        x=self.hidden(x)
        x=self.relu(x)
        x=self.scale(x)
        x=nn.Tanh(x)
        return x

class GoNetWork(nn.Module):
    def __init__(self,input_channel,block_num,komi_type=1):
        super(GoNetWork,self).__init__()
        self.DenseTower=nn.Sequential()
        self.relu=nn.ReLU(inplace=True)
        conv=_ConvBlock(input_channel,256)
        self.DenseTower.add_module('initial_conv',conv)
        for i in range(block_num):
           block=_ResBlock(256,256)
           self.DenseTower.add_module('denseblock_%d' % (i + 1), block)
        self.policyhead=_Policy(256,2)
        self.valuehead=_Value(256,1,komi_type)
           
    def forward(self,x):
        x=self.DenseTower(x)
        poli=self.policyhead(x)
        val=self.valuehead(x)
        return poli,val


