"""
   cross.py
   COMP9444, CSE, UNSW
"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

class Full3Net(torch.nn.Module):
    def __init__(self, hid):
        super(Full3Net, self).__init__()

        self.linear1 = nn.Linear(2, hid)
        self.linear2 = nn.Linear(hid, hid)
        self.output = nn.Linear(hid, 1)

    def forward(self, input):
        i = self.linear1(input)
        self.hid1 = torch.tanh(i)

        j = self.linear2(self.hid1)
        self.hid2 = torch.tanh(j)

        k = self.output(self.hid2)
        output = torch.sigmoid(k)
        return output

class Full4Net(torch.nn.Module):
    def __init__(self, hid):
        super(Full4Net, self).__init__()

        self.linear1 = nn.Linear(2, hid)

        self.linear2 = nn.Linear(hid, hid)

        self.linear3 = nn.Linear(hid, hid)

        self.output = nn.Linear(hid, 1)

    def forward(self, input):
        i = self.linear1(input)
        self.hid1 = torch.tanh(i)

        j = self.linear2(self.hid1)
        self.hid2 = torch.tanh(j)

        k = self.linear3(self.hid2)
        self.hid3 = torch.tanh(k)

        l = self.output(self.hid2)
        output = torch.sigmoid(l)
        return output

class DenseNet(torch.nn.Module):
    def __init__(self, num_hid):
        super(DenseNet, self).__init__()

        self.linear1 = nn.Linear(2, num_hid)

        self.linear2 = nn.Linear(num_hid + 2, num_hid)

        self.linear3 = nn.Linear(num_hid + num_hid + 2, 1)

    def forward(self, input):
        i = self.linear1(input)

        self.hid1 = torch.tanh(i)

        j = torch.cat([input, self.hid1], dim=1)
        k = self.linear2(j)
        self.hid2 = torch.tanh(k)

        l = torch.cat([self.hid2, self.hid1, input], dim=1)
        m = self.linear3(l)

        output = torch.sigmoid(m)

        return output
