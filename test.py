import math
import numpy as np
import matplotlib as mplot

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
            if line[0] != "!" and line[0] != "#":
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

data_l = readData("test_input.s4p")
num_of_pts = len(data_l)
mm_S_mag=[]
for i in range(num_of_pts):
    mm_S_real = s2mixedS(data_l[i].get("real"))
    mm_S_imag = s2mixedS(data_l[i].get("imag"))
    mm_S_mag.append(mag_matrix(mm_S_real,mm_S_imag))

#       [0 0] [0 1] [0 2] [0 3]
# [0 0] SDD11 SDD12 SDC11 SDC12
# [1 0] SDD21 SDD22 SDC21 SDC22
# [2 0] SCD11 SCD12 SCC11 SCC12
# [3 0] SCD21 SCD22 SCC21 SCC22

with open('test_output.txt','w') as f:
    f.write("Freq\tSDD11\tSDD21\tSCD21\n")
    for i in range(num_of_pts):
        f.write(str(10*(i+1))+"\t"
                + str(num2dB(mm_S_mag[i][0,0]))+"\t"
                + str(num2dB(mm_S_mag[i][1,0]))+"\t"
                + str(num2dB(mm_S_mag[i][3,0]))+"\n")
