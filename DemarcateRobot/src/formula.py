from math import * 

PI=3.1415926

def calc_circle_modle_compensation(delta,S,Base):
    delta=abs(float(delta))
    S=abs(float(S))
    Base=abs(float(Base))

    p=(float)(delta/S)
    th=atan(p)
    th2=180.0*th/PI
    R=0.5*(delta+pow(S,2)/delta)
    k=R/(R-Base)    
    return [k,th,R]

def calc_motor_control_compensation(delta,S,Base):
    [k,th,R] = calc_circle_modle_compensation(delta,S,Base)
    k = (k-1)*24.5 + 1    
    return [k,th,R]

def calc_DeadReckoning_compensation(delta,S,Base):
    [k,th,R] = calc_circle_modle_compensation(delta,S,Base)
    k = (k-1)*1 + 1  
    return [k,th,R]


if __name__ == '__main__':
    delta = raw_input('delta:')
    S = raw_input('S:')
    Base = raw_input('Base:')

    [k,th,R] = calc_motor_control_compensation(delta,S,447)
    print k
