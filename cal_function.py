import numpy as np

def cal_function(X,Y,Z,KxRe,KyRe,KzRe,KxIm, KyIm, KzIm, Area,freq= 0.5,plane= 3):
    #前面10个为已经读取的数
    #f为输入文件的文件名，一个浮点数，如0.5
    #plane先默认为3
    f = freq*1e9
    jx = [complex(i,j) for i,j in zip(KxRe,KxIm)]
    jy = [complex(i,j) for i,j in zip(KyRe,KyIm)]
    jz = [complex(i,j) for i,j in zip(KzRe,KzIm)]
    j = np.array([jx,jy,jz])

    R = np.array([X,Y,Z],dtype=np.float) * 1e-3
    S = np.array(Area)*1e-6
    #带入公式前的预处理，记得单位的归一化
    c = 3e8
    w = 2*np.pi*f
    k = w/c
    u0 = 4e-7*np.pi
    ################################################################
    E_theta = []
    thetas = np.arange(0,360,1)
    for theta in thetas:

        k0 = [np.sin(j*np.pi/180.), 0, np.cos(j*np.pi/180.)]
        E=0

        for i in range(0,len(S)):
            dE = ( j[i]-( j[i]*k0)*k0 ) * np.exp(j*k*k0*R[i])  *[S[i],S[i],S[i] ]
            E = dE + E
        

            E = (j*w*u0)/(4*np.pi)*E 
            E_abs = (4*np.pi) * np.sqrt(abs(E[1][1])**2 + abs(E[1][2])**2 + abs(E[1][3])**2 )
            E_abs = 10*log10(E_abs)
        
        E_theta[theta] = E_abs

#################################################################

    return E_theta

if __name__ == '__main__':
    # test
    data =  np.array([  [49.3464,-49.6732         ,  0.15   ,  0.00375367 ,  9.49386e-007     ,         0    , -0.0012466 ,  -0.000673359   ,    0    ,   0.480584],[49.3464,-49.6732         ,  0.15   ,  0.00375367 ,  9.49386e-007     ,         0    , -0.0012466 ,  -0.000673359   ,    0    ,   0.480584]],dtype=np.float)
    print(data.shape)
    reshape = data.reshape([10,2])
    print(reshape.shape)

    a = cal_function( *reshape.tolist() )
    print(a)
