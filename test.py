import math

class Data:
    """Data class that stores frequency and [S]"""
    def __init__(self):
        self.s_mag = []
        self.s_phase= []
        self.s_real=[]
        self.s_imag=[]
    def add_sparam(self, mag, phase, real, imag):
        self.s_mag.append(mag)
        self.s_phase.append(phase)
        self.s_real.append(real)
        self.s_imag.append(imag)
    def

def polar2real(mag,phase):
    return mag*math.cos(phase)
def polar2imag(mag,phase):
    return mag*math.sin(phase)

line_lst = []
data_lst = []
num_of_pts = 0
with open('test_input.s4p', 'r') as f:
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
                    mag=float(line_lst[i*2+1])
                    phase=float(line_lst[i*2+2])
                    mag_lst.append(mag)
                    phase_lst.append(phase)
                    real_lst.append(polar2real(mag,phase))
                    imag_lst.append(polar2imag(mag,phase))
            else:
                for i in range(4):
                    mag=float(line_lst[i*2])
                    phase=float(line_lst[i*2+1])
                    mag_lst.append(mag)
                    phase_lst.append(phase)
                    real_lst.append(polar2real(mag,phase))
                    imag_lst.append(polar2imag(mag,phase))
            data_lst[num_of_pts-1].add_sparam(mag_lst,phase_lst,real_lst,imag_lst)

mode_conv_M = [[1,-1,0,0],[1,1,0,0],[0,0,1,-1],[0,0,1,1]]
mode_conv_M = [[(0.5**0.5)*x[i] for i in range(4)] for x in mode_conv_M]

#num_of_pts = len(data_lst) / 4
with open('test_output.txt','w') as f:
    for i in range(len(data_lst)):
        f.write("Freq:" + str(data_lst[i].frequency))
        f.write("\nmag:" + str(data_lst[i].s_mag))
        f.write("\nphase:"+str(data_lst[i].s_phase))
        f.write("\nreal:" + str(data_lst[i].s_real))
        f.write("\nimag:"+str(data_lst[i].s_imag))
