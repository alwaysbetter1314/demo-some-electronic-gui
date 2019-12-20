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
'''
function_map:
-  draw_ui :    绘制ui
-  load_data:   载入xyz数据
-  paint :      在图1上画点
-  draw_lines : 画出长方体区域
-  draw:        更新图1
'''

class Demo:
    def __init__(self):
        # 图1
        self.canvas = None
        # 图2： 极坐标
        self.canvas_polar = None
        # 图1 子图
        self.axc = None
        # 所有点的xyz坐标 [ [x1,y1,z1],... ]
        self.all_data = None
        # 框框条件 [x1,x2,y1,y2,z1,z2]
        self.condition = None
        # 选定后的数组
        self.selected_points = None

        self.draw_ui()
    # 绘制UI
    def draw_ui(self):
        root = Tk()
        root.title('电流三维')
        ################## Field1 :  label frame
        label_frame = LabelFrame(root,width=1400,height=1000,text=' ')
        label_frame.grid(row=1,column=0,columnspan=4)
        label_frame.grid_propagate(0) 
        # 2. button_load_data
        button_dk=Button(label_frame,text='导入电流数据',command=self.paint)
        button_dk.grid(row=1,column=0)
        # input_fields
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
        # paint lines
        button_hx=Button(label_frame,text='画线',command=self.draw_lines)
        button_hx.grid(row=10,column=0)
        ################# Field 2 -- 画布1
        image = tkinter.PhotoImage()
        # 画布的大小和分别率figsize 设置图形的大小，a 为图形的宽， b 为图形的高，单位为英寸
        fig = Figure(figsize=(8, 5), dpi=100)
        # 利用子图画图
        axc = fig.add_subplot(111)
        axc=Axes3D(fig)
        self.axc =axc
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        canvas = FigureCanvasTkAgg(fig, master=label_frame)
        #canvas.draw()  
        canvas.get_tk_widget().grid(row=1,column=2, columnspan=3,rowspan=10)
        self.canvas =canvas

        ################ Field3 : 极坐标
        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        x = np.arange(-10, 10, 1)
        y = 1 / (1 + np.exp(-x))
        t = np.arctan2(x, y)
        # 绘制图形
        a.scatter(x, y, s=75, c=t)
        # 把绘制的图形显示到tkinter窗口上
        canvas_polar = FigureCanvasTkAgg(f, master=label_frame)
        canvas_polar.get_tk_widget().grid(row=20,column=2, columnspan=3,rowspan=10)
        self.canvas_polar = canvas_polar

        root.mainloop()
    #  载入数据
    def load_data(self, path=''):
        data_List = []
        file_path = tkinter.filedialog.askopenfilename(title=u'选择文件', initialdir=(''))
        with open(file_path,'r') as f:
            for line in f.readlines()[2:4000]:
                # 变换前三个元素xyz 为float
                X,Y,Z= map(float,line.split()[:3])
                data_List.append([X,Y,Z])
        self.all_data = data_List
        return data_List

    def select_data(self):
        x1,x2, y1, y2, z1, z2 = map(float,self.condition)
        self.selected_points = [ item for item in self.all_data if x1<=item[0]<=x2 and y1<=item[1]<=y2 and z1<=item[2]<=z2 ]
        print(self.selected_points)
        tkinter.messagebox.showinfo('已选择',self.selected_points)

    # xyz画点
    def paint(self):
        #调整X，Y轴的方向
        axc =self.axc
        axc.view_init(45, 60)
        # item为单个[x,y,z] 
        for item in tqdm.tqdm(self.load_data() ):
            #绘制散点图https://matplotlib.org/api/markers_api.html  可以选择图形
            axc.scatter3D(*item,c='b',marker=".")
            #设置坐标轴标签
            axc.set_xlabel('x')
            axc.set_ylabel('y')
            axc.set_zlabel('z')    
        self.draw()

    # 画线并选点
    def draw_lines(self):
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
        
        self.draw()
        self.select_data()
    # 更新canvas1
    def draw(self):
        self.canvas.draw()


if __name__ == '__main__':
	Demo()
