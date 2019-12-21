from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.filedialog
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from functools import reduce
import numpy as np
import tqdm
import math
import operator

'''
function_map:
-  draw_ui :    绘制ui
-  load_data:   载入xyz数据
-  paint :      在图1上画点
-  draw_lines : 画出长方体区域
-  draw:        更新图1
-  calulator:   计算微分
'''

class Demo:
    def __init__(self):
        # 图1
        self.canvas = None
        # 图2： 极坐标
        self.canvas_polar = None
        # 图1 子图
        self.axc = None
        # 所有点的xyz坐标一直到area [ [x1,y1,z1... area],... ]
        self.all_data = None
        # 框框条件 [x1,x2,y1,y2,z1,z2]
        self.condition = None
        # 选定后的数组
        self.selected_points = None
        # 极坐标子图
        self.axc_polar = None 

        self.draw_ui()
    # 绘制UI
    def draw_ui(self):
        root = Tk()
        root.title('电流三维')
        ################## Field1 :  label frame
        label_frame = LabelFrame(root,width=1400,height=1000,text=' ')
        label_frame.grid(row=1,column=0,columnspan=4)
        label_frame.grid_propagate(0) 
        self.label_frame = label_frame
        # 2. button_load_data
        button_dk=Button(label_frame,text='导入电流数据',command=self.paint)
        button_dk.grid(row=1,column=0)
        ## 输入框
        self.L1 = Label(label_frame, text="X1")
        self.L1.grid(row=2,column=0)
        self.E1 = Entry(label_frame,)
        self.E1.grid(row=2,column=1,padx=10)

        self.L2 = Label(label_frame, text="X2")
        self.L2.grid(row=3,column=0)
        self.E2 = Entry(label_frame,)
        self.E2.grid(row=3,column=1)

        self.L3 = Label(label_frame, text="Y1")
        self.L3.grid(row=4,column=0)
        self.E3 = Entry(label_frame,)
        self.E3.grid(row=4,column=1)

        self.L4 = Label(label_frame, text="Y2")
        self.L4.grid(row=5,column=0)
        self.E4 = Entry(label_frame,)
        self.E4.grid(row=5,column=1)

        self.L5 = Label(label_frame, text="Z1")
        self.L5.grid(row=6,column=0)
        self.E5 = Entry(label_frame,)
        self.E5.grid(row=6,column=1)

        self.L6 = Label(label_frame, text="Z2")
        self.L6.grid(row=7,column=0)
        self.E6 = Entry(label_frame,)
        self.E6.grid(row=7,column=1)
        ## paint lines
        button_hx=Button(label_frame,text='画线',command=self.draw_lines)
        button_hx.grid(row=10,column=0)
        ## 画极坐标
        button_hx=Button(label_frame,text='画极坐标',command=self.draw_polar)
        button_hx.grid(row=11,column=0)

        ################# Field 2 -- 画布1
        image = tkinter.PhotoImage()
        # 画布的大小和分别率figsize 设置图形的大小，a 为图形的宽， b 为图形的高，单位为英寸
        self.fig = Figure(figsize=(8, 5), dpi=100)
        # 利用子图画图
        self.axc = self.fig.add_subplot(111)
        self.axc = Axes3D(self.fig)
        # 将绘制的图形显示到tkinter:创建属于label_frame的canvas画布,并将图f置于画布上
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.label_frame)
        self.canvas.get_tk_widget().grid(row=1,column=2, columnspan=3,rowspan=10)

        ################ Field3 : 极坐标
        self.fig_polar = Figure(figsize=(5,4), dpi=100)
        self.axc_polar = self.fig_polar.add_subplot(111,projection='polar')
        # 把绘制的图形显示到窗口上
        self.canvas_polar = FigureCanvasTkAgg(self.fig_polar, master=self.label_frame)
        self.canvas_polar.get_tk_widget().grid(row=20,column=2, columnspan=3,rowspan=10)

        root.mainloop()
    #  载入数据
    def load_data(self, path=''):
        data_List = []
        file_path = tkinter.filedialog.askopenfilename(title=u'选择文件', initialdir=(''))
        with open(file_path,'r') as f:
            for line in f.readlines()[2:]:
                # 变换10个元素为float
                X,Y,Z,KxRe,KyRe,KzRe,KxIm, KyIm, KzIm, Area= map(float,line.split())
                data_List.append([X,Y,Z,KxRe,KyRe,KzRe,KxIm, KyIm, KzIm, Area])
        self.all_data = data_List
        return data_List

    # 选择数据
    def select_data(self):
        x1,x2, y1, y2, z1, z2 = map(float,self.condition)
        self.selected_points = [ item for item in self.all_data if x1<=item[0]<=x2 and y1<=item[1]<=y2 and z1<=item[2]<=z2 ]

    # xyz画点
    def paint(self):
        if self.all_data == None:
            self.all_data = self.load_data()
        #调整X，Y轴的方向
        axc =self.axc
        # axc.view_init(45, 60)
        # 分离xyz列， 然后一次绘图。
        x= []
        y= []
        z= []
        other_except_last = []
        for item in tqdm.tqdm(self.all_data):
            x.append(item[0])
            y.append(item[1])
            z.append(item[2])
            other_except_last.append(item[3:9])
        #绘制散点图https://matplotlib.org/api/markers_api.html 
        # last_error : c 如何与电流结合实现渐变色
        axc.scatter3D(x,y,z,c=reduce(operator.add,self.cal_current(other_except_last) ), marker=".",alpha=0.5)
        #设置坐标轴标签
        axc.set_xlabel('x')
        axc.set_ylabel('y')
        axc.set_zlabel('z')    
        self.canvas.draw()

    # 画线并选点
    def draw_lines(self):
        # 清除之前的子图
        self.fig.clf()
        # 重新上图，打点，画框
        self.axc = self.fig.add_subplot(111)
        self.axc = Axes3D(self.fig)
        self.paint()

        self.condition = [self.E1.get(),self.E2.get(),self.E3.get(),self.E4.get(),self.E5.get(),self.E6.get()]
        x1,x2, y1, y2, z1, z2 = map(float,self.condition)
        #画线；r表示红色
        self.axc.plot([x1,x1],[y1,y2],[z1,z1],c='r')
        self.axc.plot([x1,x2],[y1,y1],[z1,z1],c='r')
        self.axc.plot([x2,x2],[y2,y1],[z1,z1],c='r')
        self.axc.plot([x2,x1],[y2,y2],[z1,z1],c='r')
        
        self.axc.plot([x1,x1],[y1,y2],[z2,z2],c='r')
        self.axc.plot([x1,x2],[y1,y1],[z2,z2],c='r')
        self.axc.plot([x2,x2],[y2,y1],[z2,z2],c='r')
        self.axc.plot([x2,x1],[y2,y2],[z2,z2],c='r')
        
        self.axc.plot([x1,x1],[y1,y1],[z2,z1],c='r')
        self.axc.plot([x1,x1],[y2,y2],[z2,z1],c='r')
        self.axc.plot([x2,x2],[y2,y2],[z2,z1],c='r')
        self.axc.plot([x2,x2],[y1,y1],[z2,z1],c='r')
        
        self.canvas.draw()
        # update 区域内的点
        self.select_data()

    def draw_polar(self):
        # 先清除画出的极坐标
        self.fig_polar.clf()
        x = [i for i in range(0,361)]
        y_all = list(np.array([len(self.all_data)]*361,dtype=np.float))
        y_selected = list(np.array([len(self.selected_points)]*361,dtype=np.float))
        # 绘制图形
        self.axc_polar = self.fig_polar.add_subplot(111,projection='polar')
        self.axc_polar.scatter(x, y_all, c='b')
        self.axc_polar.scatter(x, y_selected, c='r')
        self.canvas_polar.draw()
    # 计算电流
    def cal_current(self,data_List):
        result_list = []
        for item in data_List:
            n4,n5,n6,n7,n8,n9 = item
            complex45 = complex(n4,n5)
            complex67 = complex(n6,n7)
            complex89 = complex(n8,n9)
            I = math.sqrt(abs(complex45)**2 + abs(complex67)**2 + abs(complex89)**2 )
            result_list.append([I])
        return result_list

    # 计算积分
    def cal_jifen(self, selected_points, freq = 5e9, plane = 0 ):
        return np.array([len(selected_points)]*361,dtype=np.float)

if __name__ == '__main__':
    Demo()
