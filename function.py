import matplotlib.pyplot as plt
import math
import numpy as np

class Line:
    def __init__(self, in_x=90.0, in_y=0, in_ang=90.0, in_velo_ang=0.0, in_slip=0.0,in_velo = 400.0,in_K=10000.0):
        self.ang = in_ang
        self.ang_de = in_ang *1000
        self.velo_ang = in_velo_ang
        self.slip = in_slip
        self.x = []
        self.y = []
        self.dt = 0.001
        self.velo = in_velo
        self.x.append(in_x)
        self.y.append(in_y)
        self.K = in_K

    
    def update_point(self, accel_ang=0.0,slip_flag=0.0):
        if slip_flag == True:
            self.slip = (self.slip*1000.0-self.velo_ang)/(1000.0+self.K/self.velo)
        
        self.ang = self.ang_de/1000
        self.velo_ang += accel_ang * self.dt
        self.ang_de += self.velo_ang

        print('ang:',self.ang,'v_ang:',self.velo_ang)

        self.x.append(self.x[-1] + self.velo * np.cos(np.radians(self.ang + self.slip)) * self.dt)
        self.y.append(self.y[-1] + self.velo * np.sin(np.radians(self.ang + self.slip)) * self.dt)

    def plot_line(self):
        plt.figure(figsize=(8, 8), dpi=100)
        plt.xlim(0, 180)
        plt.ylim(0, 180)
        plt.title("sulalome")
        plt.grid(color='gray', linestyle=":")
        
        plt.plot(self.x, self.y)
        plt.show()


class Control:
    def __init__(self):
        self.ang_fst = 0.0
        self.ang_mid = 0.0
        self.ang_end = 0.0

    def calc_angle(self,accel_ang,ang,velo_ang_fst,velo_ang_mid,velo_ang_end):
        self.ang_fst = (velo_ang_mid**2.0 - velo_ang_fst**2.0) / 2.0 / accel_ang
        self.ang_mid = ang - (velo_ang_mid**2.0 - velo_ang_end**2.0) / 2.0 / accel_ang
        self.ang_end = ang
        print('fst:',self.ang_fst,'mid',self.ang_mid,'end',self.ang_end)