from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.filedialog
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from functools import reduce

import numpy as np
import tqdm

root = Tk()
root.title('电流三维')

a= LabelFrame(root,width=1400,height=1000,text=' ')
a.grid(row=1,column=0,columnspan=4) 
a.grid_propagate(0)


# 载入数据，10行取一个均值。
def load_data(path=''):
    data_List = []
    file_path = tkinter.filedialog.askopenfilename(title=u'选择文件', initialdir=(''))
    with open(file_path,'r') as f:
        for line in f.readlines()[2:4000]:
            X,Y,Z= map(float,line.split()[:3])
            #print(X,Y,Z)
            data_List.append([X,Y,Z])
    return data_List

# x,y,z绘图
def paint():
        #调整X，Y轴的方向
        axc.view_init(45, 60)
        for item in tqdm.tqdm(load_data() ):
            #print(item)
            #绘制散点图https://matplotlib.org/api/markers_api.html  可以选择图形
            axc.scatter3D(*item,c='b',marker=".")
            #设置坐标轴标签
            axc.set_xlabel('x')
            axc.set_ylabel('y')
            axc.set_zlabel('z')    
        huatu()

def s2f(s):
    return float(s)
    
button_dk=Button(a,text='导入电流数据',command=paint)
button_dk.grid(row=1,column=0)


L1 = Label(a, text="X1")
L1.grid(row=2,column=0)
E1 = Entry(a,)
E1.grid(row=2,column=1,padx=10)

L2 = Label(a, text="X2")
L2.grid(row=3,column=0)
E2 = Entry(a,)
E2.grid(row=3,column=1)

L3 = Label(a, text="Y1")
L3.grid(row=4,column=0)
E3 = Entry(a,)
E3.grid(row=4,column=1)

L4 = Label(a, text="Y2")
L4.grid(row=5,column=0)
E4 = Entry(a,)
E4.grid(row=5,column=1)

L5 = Label(a, text="Z1")
L5.grid(row=6,column=0)
E5 = Entry(a,)
E5.grid(row=6,column=1)

L6 = Label(a, text="Z2")
L6.grid(row=7,column=0)
E6 = Entry(a,)
E6.grid(row=7,column=1)


def hx():
    x1=s2f(E1.get())
    x2=s2f(E2.get())
    y1=s2f(E3.get())
    y2=s2f(E4.get())
    z1=s2f(E5.get())
    z2=s2f(E6.get())
    x=[x1,x2]
    y=[0,0]
    z=[0,0]
    #画一条X1到X2的线
    #axc.plot(x,y,z,c='r')
    #画线；r表示红色
    axc.plot([x1,x1],[y1,y2],[z1,z1],c='r')
    axc.plot([x1,x2],[y1,y1],[z1,z1],c='r')
    axc.plot([x2,x2],[y2,y1],[z1,z1],c='r')
    axc.plot([x2,x1],[y2,y2],[z1,z1],c='r')
    
    axc.plot([x1,x1],[y1,y2],[z2,z2],c='r')
    axc.plot([x1,x2],[y1,y1],[z2,z2],c='r')
    axc.plot([x2,x2],[y2,y1],[z2,z2],c='r')
    axc.plot([x2,x1],[y2,y2],[z2,z2],c='r')
    
    axc.plot([x1,x1],[y1,y1],[z2,z1],c='r')
    axc.plot([x1,x1],[y2,y2],[z2,z1],c='r')
    axc.plot([x2,x2],[y2,y2],[z2,z1],c='r')
    axc.plot([x2,x2],[y1,y1],[z2,z1],c='r')
    
    huatu()
    
button_hx=Button(a,text='画线',command=hx)
button_hx.grid(row=10,column=0)

#创建画布
image = tkinter.PhotoImage()
# 画布的大小和分别率figsize 设置图形的大小，a 为图形的宽， b 为图形的高，单位为英寸
fig = Figure(figsize=(10, 7), dpi=100)
# 利用子图画图
axc = fig.add_subplot(111)
axc=Axes3D(fig)
# 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
canvas = FigureCanvasTkAgg(fig, master=a)
#canvas.draw()  
canvas.get_tk_widget().grid(row=1,column=2, columnspan=4,rowspan=15)




image = tkinter.PhotoImage()
fig1 = Figure(figsize=(10, 7), dpi=100)

def huatu():
    # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas.draw()  

def main():
    root.mainloop()


if __name__ == '__main__':
    main()
