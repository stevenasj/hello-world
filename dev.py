import math
import numpy as np
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

#       [0 0] [0 1] [0 2] [0 3]
# [0 0] SDD11 SDD12 SDC11 SDC12
# [1 0] SDD21 SDD22 SDC21 SDC22
# [2 0] SCD11 SCD12 SCC11 SCC12
# [3 0] SCD21 SCD22 SCC21 SCC22

def cascadedS(sParam1, sParam2,port_num):
    if port_num == 2:
        return (t2s_2pts(s2t_2pts(sParam1).dot(s2t_2pts(sParam2))))
    elif port_num ==4:
        return (t2s_4pts(s2t_4pts(sParam1).dot(s2t_4pts(sParam2))))
    else:
        raise ValueError("Bad Number of Ports :(")

s = np.array([[0.0267153,0.925283,0.0148643,-0.00693513], \
              [0.921372,0.026048,-0.00693885,0.0149818], \
              [0.0148526,-0.0070081,0.0251593,0.922917], \
              [-0.00701927,0.0149899,0.925373,0.0259384]])
print(s)
t = s2t_4pts(s)
print(cascadedS(s,s,4))
print(t2s_4pts(t))
