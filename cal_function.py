# -*- coding: utf-8 -*-

import numpy as np

def cal_function(X,Y,Z,KxRe,KyRe,KzRe,KxIm, KyIm, KzIm, Area,freq,plane):
#前面10个为已经读取的数
#f为输入文件的文件名，一个浮点数，如0.5
#plane先默认为3
f = freq*1e9
J = [complex(KxRe,KxIm),complex(KyRe,KyIm),complex(KzRe,KzIm)]
R = [X,Y,Z]*1e-3
S = Area*1e-6
#带入公式前的预处理，记得单位的归一化
c = 3e8
w = 2*pi*f
k = w/c
u0 = 4e-7*pi
################################################################
E_theta = []
theta = np.arange(0,360,1)
for theta in thetas

    k0 = [math.sin(j*math.pi/180), 0, math.cos(j*math.pi/180)]
    E=0

    for i = 0:lenth(S)-1  #总点数
        dE = ( J[i]-( J[i]*k0)*k0 ) * exp(j*k*k0*R[i])  *S[i]
        E = dE + E
    

        E = (j*w*u0)/(4*math.pi)*E 
        E_abs = (4*math.pi) * math.sqrt(abs(E[1][1])**2 + abs(E[1][2])**2 + abs(E[1][3])**2 )
        E_abs = 10*log10(E_abs)
    
    E_theta[theta] = E_abs

#################################################################

return E_theta
