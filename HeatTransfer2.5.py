import math
import matplotlib.pyplot as plt
import os
import numpy as np
import imageio
import time
L=1####
Alpha=0.01
T1=273####
T2=300####
x1=1####
x2=2####
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
mkpath="C:\\Users\\你的用户名\\Desktop\\HeatTransfer\\2.5\\"+str(nowtime)+"\\"
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
    y=T1-(T1-T2)*(math.log(x/x1))/(math.log(x2/x1))
    return y


def initialize(T1,T2,dx):
    global A
    global T
    global Theoretical
    global x1
    global x2
    n=int((x2-x1)/dx)
    print(n)
    for i in range(n+1):
        A.append(point(T1,x1+i*dx))
        Theoretical.append(Tfun(x1+i*dx))
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
            A[i].dT=dt*Alpha*((A[i+1].T-A[i-1].T)/(2*A[i].x*dx)+(A[i-1].T+A[i+1].T-2*A[i].T)/(dx**2))

def fun2(a,b,X,Y):
    global x1
    global x2
    r=(a**2+b**2)**0.5
    left=0
    right=0
    y=0
    if r<x1 or r>=x2:
        return 0
    else:
        for i in range(len(X)):
            if r<X[i]:
                left=i-1
                right=i
                break
        #y=Y[right]
        y=Y[left]+((Y[right]-Y[left])/(X[right]-X[left]))*(r-X[left])
        return y

    



def DrawAndJudge(tick,dt,T1,T2,dx):
    global A
    global T
    global judge
    global pause
    global Theoretical
    global filenames
    global mkpath
    global x1
    global x2
    X=[]
    Y=[]
    n=int((x2-x1)/dx)
    dT=[]
    if tick==0 or tick%500==0:
        for i in range(len(A)):
            X.append(A[i].x)
            Y.append(A[i].T)
            dT.append(abs(T[i]-A[i].T))
            T[i]=A[i].T
        dT.sort(reverse = True)
        plt.clf()
        plt.xlim(x1,x2)
        plt.ylim(min(T1,T2)-5,max(T1,T2)+5)
        plt.xlabel("r/m")
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
            plt.xlim(0,x2)
            plt.ylim(0,x2)
            plt.xlabel("r/m")
            x=np.linspace(0,x2,500)
            y=np.linspace(0,x2,500)
            z=np.zeros((500,500))
            for i,a in enumerate(x):
                for j,b in enumerate(y):
                    z[i,j]=fun2(a,b,X,Y)
            z=np.ma.masked_array(z,z==0)
            xx,yy=np.meshgrid(x,y)
            c = plt.pcolormesh(xx,yy,z.T, cmap ="jet", vmin = min(Y), vmax = max(Y)) 
            plt.colorbar(c)
            plt.savefig(mkpath+"数值解"+".jpg")

            plt.clf()
            plt.xlim(0,x2)
            plt.ylim(0,x2)
            plt.xlabel("r/m")
            x=np.linspace(0,x2,500)
            y=np.linspace(0,x2,500)
            z=np.zeros((500,500))
            for i,a in enumerate(x):
                for j,b in enumerate(y):
                    z[i,j]=fun2(a,b,X,Theoretical)
            z=np.ma.masked_array(z,z==0)
            xx,yy=np.meshgrid(x,y)
            c = plt.pcolormesh(xx,yy,z.T, cmap ="jet", vmin = min(Theoretical), vmax = max(Theoretical)) 
            plt.colorbar(c)
            plt.savefig(mkpath+"解析解"+".jpg")

            return(0)

f=open(mkpath+"数据.txt",'a')
f.write("x1:"+str(x1))
f.write("\n")
f.write("x2:"+str(x2))
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


initialize(T1,T2,dx)
print(Theoretical)
for tick in range(80001):
    if DrawAndJudge(tick,dt,T1,T2,dx)==0:
        break
    update(Alpha,dt,dx)


frames = []
for image_name in filenames:                # 索引各自目录
    frames.append(imageio.imread(image_name))

imageio.mimsave(mkpath+"动画.gif", frames, 'GIF', duration = 0.01)

print("gif动画生成完毕")




