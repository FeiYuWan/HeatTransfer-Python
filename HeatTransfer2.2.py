import math
import matplotlib.pyplot as plt
import os
import numpy as np
import imageio
import time
L=1####
Alpha=0.01
T1=300####
T2=273####
dt=0.001
dx=0.005
A=[]
t=0
judge=0.003####
pause=0.1####
T=[]
Theoretical=[]



def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False


nowtime=time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
mkpath="C:\\Users\\你的用户名\\Desktop\\HeatTransfer\\2.2\\"+str(nowtime)+"\\"
# 调用函数
mkdir(mkpath)
filenames=[]


class point:
    def __init__(self,T0,x):
        self.T=T0
        self.dT=0
        self.x=x
        self.boundarycondition=0

def Tfun(x):
    global T1
    global T2
    global L
    y=T1+((T2-T1)/L)*x
    return y


def initialize(L,T1,T2,dx):
    global A
    global T
    global Theoretical
    n=int(L/dx)
    for i in range(n+1):
        A.append(point(T2,i*dx))
        Theoretical.append(Tfun(i*dx))
    A[0].boundarycondition=1
    A[0].T=T1
    A[-1].boundarycondition=1
    A[-1].T=T2
    for i in range(len(A)):
        T.append(A[i].T)
     

def update(Alpha,dt,dx):
    global A
    global t
    print(t)
    t+=dt
    for i in range(len(A)):
        if A[i].boundarycondition==0:
            A[i].T+=A[i].dT
            A[i].dT=dt*Alpha*((A[i-1].T+A[i+1].T-2*A[i].T)/(dx**2))




def DrawAndJudge(tick,dt,T1,T2,dx,L):
    global A
    global T
    global judge
    global pause
    global Theoretical
    global filenames
    global mkpath
    X=[]
    Y=[]
    n=int(L/dx)
    dT=[]
    if tick==0 or tick%500==0:
        for i in range(len(A)):
            X.append(A[i].x)
            Y.append(A[i].T)
            dT.append(abs(T[i]-A[i].T))
            T[i]=A[i].T
        dT.sort(reverse = True)
        plt.clf()
        plt.xlim(0,L)
        plt.ylim(min(T1,T2)-5,max(T1,T2)+5)
        plt.xlabel("x/m")
        plt.ylabel("T/K")
        plt.plot(X,Y,label="Numerical")
        plt.plot(X,Theoretical,label="Analytical")
        plt.legend(loc='best')
        #plt.text(0.8,T1,dT[0])
        filename=mkpath+str(tick)+".jpg"
        plt.savefig(filename)
        filenames.append(filename)
        if tick>500 and dT[0]>=judge:
            print(dT[0])
            return(1)
        elif tick>500 and dT[0]<judge:
            print("done")
            plt.clf()
            plt.xlim(0,L)
            plt.ylim(0,1)
            plt.xlabel("x/m")
            x,y=np.array([X,[0,1]])
            Z=np.array([Y,Y])
            c = plt.pcolormesh(x,y,Z, cmap ="jet", vmin = min(Y), vmax = max(Y)) 
            plt.colorbar(c)
            plt.savefig(mkpath+"数值解"+".jpg")

            plt.clf()
            plt.xlim(0,L)
            plt.ylim(0,1)
            plt.xlabel("x/m")
            x,y=np.array([X,[0,1]])
            Z=np.array([Theoretical,Theoretical])
            c = plt.pcolormesh(x,y,Z, cmap ="jet", vmin = min(Theoretical), vmax = max(Theoretical)) 
            plt.colorbar(c)
            plt.savefig(mkpath+"解析解"+".jpg")


            return(0)

f=open(mkpath+"数据.txt",'a')
f.write("L:"+str(L))
f.write("\n")
f.write("Alpha:"+str(Alpha))
f.write("\n")
f.write("T1:"+str(T1))
f.write("\n")
f.write("T2:"+str(T2))
f.write("\n")
f.write("dt:"+str(dt))
f.write("\n")
f.write("dx:"+str(dx))
f.write("\n")
f.write("judge:"+str(judge))
f.close()


initialize(L,T1,T2,dx)
print(Theoretical)
for tick in range(80001):
    if DrawAndJudge(tick,dt,T1,T2,dx,L)==0:
        break
    update(Alpha,dt,dx)


frames = []
for image_name in filenames:                # 索引各自目录
    frames.append(imageio.imread(image_name))

imageio.mimsave(mkpath+"动画.gif", frames, 'GIF', duration = 0.01)

print("gif动画生成完毕")



