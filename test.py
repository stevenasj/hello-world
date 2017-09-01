import math
import numpy as np
import matplotlib as mplot
import sys

class Data:
    """Data class that stores frequency and [S]"""
    def __init__(self):
        self.s_mag = [] #unit in numerical (20LOG)
        self.s_phase= [] #unit in degrees
        self.s_real=[]
        self.s_imag=[]
    def add_sparam(self, mag, phase, real, imag):
        self.s_mag.append(mag)
        self.s_phase.append(phase)
        self.s_real.append(real)
        self.s_imag.append(imag)
    def print_Data(self):
        print("Freq:" + str(self.frequency)+"\n")
        print("mag:" + str(self.s_mag)+"\n")
        print("phase:"+str(self.s_phase)+"\n")
        print("real:" + str(self.s_real)+"\n")
        print("imag:"+str(self.s_imag)+"\n")
    def get(self,option):
        if option == "freq":
            return self.frequency
        elif option =="mag":
            return np.array(self.s_mag)
        elif option =="phase":
            return np.array(self.s_phase)
        elif option =="real":
            return np.array(self.s_real)
        elif option =="imag":
            return np.array(self.s_imag)
        else: raise ValueError
def polar2real(mag,phase):
    return mag*math.cos(math.radians(phase))
def polar2imag(mag,phase):
    return mag*math.sin(math.radians(phase))
def magnitude(real, imag):
    return (real**2+imag**2)**0.5
def mag_matrix(real,imag):
    return (real*real+imag*imag)**.5
def num2dB(num):
    return 20*math.log10(num)
def dB2num(num):
    return 10**(num/20)
def readData(fileName):
    """Read from fileName and return a data list with frequency and [S]"""
    line_lst = []
    data_lst = []
    num_of_pts = 0
    with open(fileName, 'r') as f:
        for line in f:
            if line[0] != "!" and line[0] != "#" \
            and line.strip():#strip checks empty line
                line_lst = line.split()
                mag_lst = []
                phase_lst = []
                real_lst=[]
                imag_lst=[]
                if len(line_lst) == 9:
                    num_of_pts = num_of_pts+1
                    entry = Data()
                    data_lst.append(entry)
                    data_lst[num_of_pts-1].frequency = float(line_lst[0])
                    for i in range(4):
                        mag=dB2num(float(line_lst[i*2+1]))
                        phase=float(line_lst[i*2+2])
                        mag_lst.append(mag)
                        phase_lst.append(phase)
                        real_lst.append(polar2real(mag,phase))
                        imag_lst.append(polar2imag(mag,phase))
                else:
                    for i in range(4):
                        mag=dB2num(float(line_lst[i*2]))
                        phase=float(line_lst[i*2+1])
                        mag_lst.append(mag)
                        phase_lst.append(phase)
                        real_lst.append(polar2real(mag,phase))
                        imag_lst.append(polar2imag(mag,phase))
                data_lst[num_of_pts-1].add_sparam(mag_lst,phase_lst,real_lst,imag_lst)
    return data_lst
def s2mixedS(s_param):
    """ [S_mm] = [M][S][M]^-1 """
    conv_M = [[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]]
    conv_M = np.array([[(0.5**0.5)*x[i] for i in range(4)] for x in conv_M])
    inv_M = np.linalg.inv(conv_M)
    return np.linalg.multi_dot([conv_M, s_param, inv_M])
def s2t_2pts(s_param):
    """[S] to [T]"""
    s11,s12= s_param[0][0],s_param[0][1]
    s21,s22= s_param[1][0],s_param[1][1]
    t11 = 1/s21
    t12 = -s22/s21
    t21 = s11/s21
    t22 = -(s11*s22-s12*s21)/s21
    return np.array([[t11,t12],[t21,t22]])
def t2s_2pts(t_param):
    """[T] to [S]"""
    t11 = t_param[0][0]
    t21 = t_param[1][0]
    t12 = t_param[0][1]
    t22 = t_param[1][1]
    s11 = t21/t11
    s12 = (t11*t22-t12*t21)/t11
    s21 = 1/t11
    s22 = -t12/t11
    return np.array([[s11,s12],[s21,s22]])
def s2t_4pts(s_param):
    """[S] to [T]"""
    s11,s12,s13,s14 = s_param[0][0],s_param[0][1],s_param[0][2],s_param[0][3]
    s21,s22,s23,s24 = s_param[1][0],s_param[1][1],s_param[1][2],s_param[1][3]
    s31,s32,s33,s34 = s_param[2][0],s_param[2][1],s_param[2][2],s_param[2][3]
    s41,s42,s43,s44 = s_param[3][0],s_param[3][1],s_param[3][2],s_param[3][3]
    t11 = -s42/(s32*s41-s42*s31)
    t12 = s32/(s32*s41-s42*s31)
    t21 = s41/(s32*s41-s42*s31)
    t22 = -s31/(s32*s41-s42*s31)
    t32 = (s11*s32-s12*s31)/(s32*s41-s31*s42)
    t31 = (s11-t32*s41)/s31
    t42 = (s32*s21-s22*s31)/(s32*s41-s31*s42)
    t41 = (s21-t42*s41)/s31
    t13 = -t11*s33-t12*s43
    t23 = -t21*s33-t22*s43
    t33 = s13-t31*s33-t32*s43
    t43 = s23-t41*s33-t42*s43
    t14 = -t11*s34-t12*s44
    t24 = -t21*s34-t22*s44
    t34 = s14-t31*s34-t32*s44
    t44 = s24-t41*s34-t42*s44
    return np.array([[t11,t12,t13,t14],[t21,t22,t23,t24], \
                     [t31,t32,t33,t34],[t41,t42,t43,t44]])
def t2s_4pts(t_param):
    t11,t12,t13,t14 = t_param[0][0],t_param[0][1],t_param[0][2],t_param[0][3]
    t21,t22,t23,t24 = t_param[1][0],t_param[1][1],t_param[1][2],t_param[1][3]
    t31,t32,t33,t34 = t_param[2][0],t_param[2][1],t_param[2][2],t_param[2][3]
    t41,t42,t43,t44 = t_param[3][0],t_param[3][1],t_param[3][2],t_param[3][3]
    s41 = -t21/(t11*t22-t12*t21)
    s42 = t11/(t11*t22-t12*t21)
    s31 = t22/(t11*t22-t12*t21)
    s32 = -t12/(t11*t22-t12*t21)
    s22 = (t11*t42-t12*t41)/(t11*t22-t12*t21)
    s21 = (t42-s22*t22)/t12
    s12 = (t11*t32-t12*t31)/(t11*t22-t12*t21)
    s11 = (t32-s12*t22)/t12
    s13 = t33-s11*t13-s12*t23
    s23 = t43-s21*t13-s22*t23
    s33 = -s31*t13-s32*t23
    s43 = -s41*t13-s42*t23
    s14 = t34-s11*t14-s12*t24
    s24 = t44-s21*t14-s22*t24
    s34 = -s31*t14-s32*t24
    s44 = -s41*t14-s42*t24
    return np.array([[s11,s12,s13,s14],[s21,s22,s23,s24], \
                     [s31,s32,s33,s34],[s41,s42,s43,s44]])
def cascadedS(sParam1, sParam2,port_num = 4):
    if port_num == 2:
        return (t2s_2pts(s2t_2pts(sParam1).dot(s2t_2pts(sParam2))))
    elif port_num ==4:
        return (t2s_4pts(s2t_4pts(sParam1).dot(s2t_4pts(sParam2))))
    else:
        raise ValueError("Bad Number of Ports :(")
def writeMixedS(filename,data,data_type):
    mixedS = dict(SDD11=(0,0),SDD12=(0,1),SDD21=(1,0),SDD22=(1,1), \
             SDC11=(0,2),SDC12=(0,3),SDC21=(1,2),SDC22=(1,3), \
             SCD11=(2,0),SCD12=(2,1),SCD21=(3,0),SCD22=(3,1), \
             SCC11=(2,2),SCC12=(2,3),SCC21=(3,2),SCC22=(3,3))
    with open(filename,'w') as f:
        f.write("Freq\t"+"\t".join(data_type[:])+"\n")
        for i in range(len(data)):
            f.write(str(10*(i+1))+"\t")
            for d in data_type:
                f.write(str(num2dB(data[i][mixedS[d]]))+"\t")
            f.write("\n")


if len(sys.argv)<2:
    raise ValueError("No read file :(")
for i in range(len(sys.argv)-1):
    data_l = readData(str(sys.argv[i+1]))
    num_of_pts = len(data_l)
    mm_S_mag=[]
    cascade_mag=[]
    for f in range(num_of_pts):
        mm_S_real = s2mixedS(data_l[f].get("real"))
        mm_S_imag = s2mixedS(data_l[f].get("imag"))
        mm_S_mag.append(mag_matrix(mm_S_real,mm_S_imag))
        cascade_real = cascadedS(data_l[f].get("real"),data_l[f].get("real"))
        cascade_imag = cascadedS(data_l[f].get("imag"),data_l[f].get("imag"))
        c_mm_S_real = s2mixedS(cascade_real)
        c_mm_S_imag = s2mixedS(cascade_imag)
        cascade_mag.append(mag_matrix(c_mm_S_real,c_mm_S_imag))
    fileName_out = str(sys.argv[i+1])[:-4]+"_out"+".txt"
    istr = input("Enter parameters needed, separated by space:\n")
    data_type = istr.split(" ")
    writeMixedS(fileName_out,mm_S_mag,data_type)


#       [0 0] [0 1] [0 2] [0 3]
# [0 0] SDD11 SDD12 SDC11 SDC12
# [1 0] SDD21 SDD22 SDC21 SDC22
# [2 0] SCD11 SCD12 SCC11 SCC12
# [3 0] SCD21 SCD22 SCC21 SCC22
