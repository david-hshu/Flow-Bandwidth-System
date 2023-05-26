from __future__ import print_function, division, absolute_import
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import hiddenlayer as h
torch.nn.SmoothL1Loss


####-------------------------------------------事先定义
# # 三级平行模型（模型）
class TPCNN(nn.Module):
    def __init__(self, num_class=10, head_payload=False):
        super(TPCNN, self).__init__()
        # 上
        self.uconv1 = nn.Sequential(  #
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(16, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )
        self.uconv2 = nn.Sequential(  #
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(32, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )
        # 中
        self.mconv1 = nn.Sequential(  #
            nn.Conv2d(1, 32, kernel_size=3, stride=2, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(32, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )
        # 下
        self.dconv1 = nn.Sequential(  #
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(32, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )

        self.uconv3 = nn.Sequential(  #
            nn.Conv2d(96, 128, kernel_size=3, stride=1, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(128, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )

        self.mconv2 = nn.Sequential(  #
            nn.Conv2d(96, 128, kernel_size=3, stride=2, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(128, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )

        self.dconv2 = nn.Sequential(  #
            nn.Conv2d(96, 128, kernel_size=3, stride=1, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(128, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )

        self.uconv4 = nn.Sequential(  #
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1, dilation=1, bias=True),
            nn.BatchNorm2d(512, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU(),
        )
        self.globalconv1 = nn.Sequential(
            nn.Conv2d(896, 1024, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.9, affine=True),
            nn.ReLU()
        )

        self.dmaxpool = nn.MaxPool2d(kernel_size=2, padding=1)

        #         self.lstm1 = nn.LSTM(256,512, 2)
        #         self.lstm2 = nn.LSTM(self.i_size*2,self.i_size*2, 2)

        self.avpool = nn.AdaptiveAvgPool2d(2)
        #         self.globallstm = nn.LSTM(512, 256, 1)

        self.fc1 = nn.Linear(1024 * 2 * 2, 512)
        self.fc2 = nn.Linear(512, num_class)

    def forward(self, x, train):
        # print("x",x.shape)
        # 上
        uout = self.uconv1(x)
        uout = self.uconv2(uout)

        # 中
        mout = self.mconv1(x)

        # 下
        dout = self.dconv1(x)

        # 连接
        # print("uout", uout.shape)
        # print("mout", mout.shape)
        # print("dout", dout.shape)

        out = torch.cat((uout, mout, dout), dim=1)
        # print("out", out.shape)

        # 上
        uout = self.uconv3(out)

        # 中
        mout = self.mconv2(out)
        # 下
        dout = self.dconv2(out)

        # 连接
        # print("uout", uout.shape)
        # print("dout", dout.shape)

        out = torch.cat((uout, dout), dim=1)
        # print("out", out.shape)

        # 上
        uout = self.uconv4(out)

        # 中

        # 下
        dout = self.dmaxpool(out)

        # 连接
        # print("uout", uout.shape)
        # print("mout", mout.shape)
        # print("dout", dout.shape)

        out = torch.cat((uout, mout, dout), dim=1)
        # print("out",out.shape)
        # 最后的网络
        # print("out", out.shape)
        out = self.globalconv1(out)
        out = self.avpool(out)

        # 全连接层
        # print("out", out.shape)
        out = out.view(-1, 1024 * 2 * 2)
        out = self.fc1(out)
        out = self.fc2(out)

        return out



x1 = TPCNN()
print(x1)

vis_graph = h.build_graph(x1, (torch.zeros([64, 1, 28, 28]), True))  # 获取绘制图像的对象
vis_graph.theme = h.graph.THEMES["blue"].copy()  # 指定主题颜色
vis_graph.save("./demo1.png")  # 保存图像的路径
