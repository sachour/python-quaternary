import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from collections.abc import Mapping, Sequence
from ResSimPostProc import SimOutput
import ternary
mpl.rcParams['axes.linewidth'] = 1.
mpl.rcParams['axes.edgecolor'] = 'gray'
mpl.rcParams['font.size'] = 15
mpl.rcParams['font.family'] = 'Arial'

class quaternary(object):
    def __init__(self,fig:mpl.figure.Figure,scale = 100):
        self.ax=fig.add_subplot(projection='3d')
        self.scale=scale
        if type(scale)is not float and type(scale) is not int:
            print('ERROR: Attempted to initialize quaternary object with')
            print('       incorrect data type for scale.')
            print('type',type(scale),' not supported.')
            exit()
        rt3=3.0**0.5
        self.map=np.array([[1.0,0.0,0.0],[0.5,rt3*0.5,0.0],[0.5,0.5/rt3,2.0**0.5/rt3]]).T
        self.mapinv=np.linalg.inv(self.map)
        zeroes=[[0.],[0.],[0.]]
        lines=np.concatenate((zeroes,self.map*scale,zeroes,
            self.map[:,1:1+1]*scale,self.map[:,0:0+1]*scale,self.map[:,2:2+1]*scale),axis=1)
        self.ax.plot(lines[0,:],lines[1,:],lines[2,:],'k-',lw=1.0)
        self.ax.set_axis_off()
        self.ax.azim = -80
        self.ax.dist = 7
        self.ax.elev = 20
        bottom_triangle=np.concatenate((zeroes,self.map[:,0:2]*scale,zeroes),axis=1)
        left_triangle=np.concatenate((zeroes,self.map[:,1:3]*scale,zeroes),axis=1)
        right_triangle=np.concatenate((zeroes,self.map[:,0:1]*scale,self.map[:,2:3]*scale,zeroes),axis=1)

        self.ax.plot_trisurf(bottom_triangle[0,:],bottom_triangle[1,:],
            bottom_triangle[2,:], color='gray',zorder=-1,alpha=0.05)
        self.ax.plot_trisurf(left_triangle[0,:],left_triangle[1,:],
            left_triangle[2,:], color='gray',zorder=-1,alpha=0.05)
        self.ax.plot_trisurf(right_triangle[0,:],right_triangle[1,:],
            right_triangle[2,:], color='gray',zorder=-1,alpha=0.05)

    def get_xyz(self,x1,x2,x3,norm=None):
        if type(x1)==list or type(x1)==tuple:
            x=[z1*self.map[0,0]+z2*self.map[0,1]+z3*self.map[0,2] for z1,z2,z3 in zip(x1,x2,x3)]
            y=[z1*self.map[1,0]+z2*self.map[1,1]+z3*self.map[1,2] for z1,z2,z3 in zip(x1,x2,x3)]
            z=[z1*self.map[2,0]+z2*self.map[2,1]+z3*self.map[2,2] for z1,z2,z3 in zip(x1,x2,x3)]
        else:
            x=x1*self.map[0,0]+x2*self.map[0,1]+x3*self.map[0,2]
            y=x1*self.map[1,0]+x2*self.map[1,1]+x3*self.map[1,2]
            z=x1*self.map[2,0]+x2*self.map[2,1]+x3*self.map[2,2]
            if norm is not None:
                length=np.sqrt(x**2+y**2+z**2)
                x,y,z=x*norm/length,y*norm/length,z*norm/length

        return x,y,z

    def plot(self,x1,x2,x3,*args,**kwargs):
        x,y,z=self.get_xyz(x1,x2,x3)
        return self.ax.plot(x,y,z,*args,**kwargs)

    def scatter(self,x1,x2,x3,**kwargs):
        x,y,z=self.get_xyz(x1,x2,x3)
        return self.ax.scatter(x,y,z,**kwargs)

    def text(self,x1,x2,x3,text:str,**kwargs):
        x,y,z=self.get_xyz(x1,x2,x3)
        self.ax.text(x,y,z,text,**kwargs)

    def set_label1(self,text:str,pad=0.0,**kwargs):
        self.text(self.scale*(1.0+pad),0.,0.,text,**kwargs)
    def set_label2(self,text:str,pad=0.0,**kwargs):
        self.text(0.,self.scale*(1.0+pad),0.,text,**kwargs)
    def set_label3(self,text:str,pad=0.0,**kwargs):
        self.text(0.,0.,self.scale*(1.0+pad),text,**kwargs)
    def set_label4(self,text:str,pad=0.0,**kwargs):
        self.text(-self.scale*pad,-self.scale*pad,-self.scale*pad,text,**kwargs)

    def set_grid(self,nmajor:int=5,lw=0.7,tick_length=0.05,ticklabelpad=[0.15,0.03,0.2]):
        if type(ticklabelpad)==list or type(ticklabelpad)==tuple or type(ticklabelpad)==np.ndarray:
            xt,yt,zt=self.get_xyz(0.,-1.,0.,norm=self.scale*ticklabelpad[0])
        elif type(ticklabelpad)==int or type(ticklabelpad)==float:
            xt,yt,zt=self.get_xyz(0.,-1.,0.,norm=self.scale*ticklabelpad)
        else:
            print('ERROR: Variable type',type(ticklabelpad),'not supported for ticklabelpad')
            print('       in quaternary.set_grid(). Please, use int float np.ndarray list or tuple.')
            exit()
        for i in range(1,nmajor): # bottom to left grid lines
            # Plot gird lines
            frac=self.scale*float(i)/nmajor
            x,y,z=self.get_xyz([self.scale-frac,0.,0.],[0.,self.scale-frac,0.],[0.,0.,self.scale-frac])
            self.ax.plot(x,y,z,linestyle='-',color='gray',linewidth=lw)
            # Plot ticks
            x,y,z=self.get_xyz([self.scale-frac,(self.scale-frac)*1.1],[0.,-0.1*(self.scale-frac)],[0.,0.])
            factor=self.scale*tick_length/((x[1]-x[0])**2.+(y[1]-y[0])**2.+(z[1]-z[0])**2.)**0.5
            x[1],y[1],z[1]=x[0]+factor*(x[1]-x[0]),y[0]+factor*(y[1]-y[0]),z[0]+factor*(z[1]-z[0])
            self.ax.plot(x,y,z,linestyle='-',color='k',linewidth=lw)
            # Add tick labels
            x[1]=x[0]+xt
            y[1]=y[0]+yt
            z[1]=z[0]+zt
            if frac==round(frac):
                self.ax.text(x[1],y[1],z[1],str(int(frac)))
            else:
                self.ax.text(x[1],y[1],z[1],str(frac))
        if type(ticklabelpad)==list or type(ticklabelpad)==tuple or type(ticklabelpad)==np.ndarray:
            xt,yt,zt=self.get_xyz(1.,1.,1.,norm=self.scale*ticklabelpad[1])
        else:
            xt,yt,zt=self.get_xyz(1.,1.,1.,norm=self.scale*ticklabelpad)
        for i in range(1,nmajor): # bottom to right grid lines
            # Plot gird lines
            frac=self.scale*float(i)/nmajor
            x,y,z=self.get_xyz([frac,frac,frac],[0.,self.scale-frac,0.],[0.,0.,self.scale-frac])
            self.ax.plot(x,y,z,linestyle='-',color='gray',linewidth=lw)
            # Plot ticks
            x,y,z=self.get_xyz([frac,frac],[0.,-0.1*(self.scale-frac)],[self.scale-frac,1.1*(self.scale-frac)])
            factor=self.scale*tick_length/((x[1]-x[0])**2.+(y[1]-y[0])**2.+(z[1]-z[0])**2.)**0.5
            x[1],y[1],z[1]=x[0]+factor*(x[1]-x[0]),y[0]+factor*(y[1]-y[0]),z[0]+factor*(z[1]-z[0])
            self.ax.plot(x,y,z,linestyle='-',color='k',linewidth=lw)
            # Add tick labels
            x[1]=x[0]+xt
            y[1]=y[0]+yt
            z[1]=z[0]+zt
            if frac==round(frac):
                self.ax.text(x[1],y[1],z[1],str(int(frac)))
            else:
                self.ax.text(x[1],y[1],z[1],str(frac))

        if type(ticklabelpad)==list or type(ticklabelpad)==tuple or type(ticklabelpad)==np.ndarray:
            xt,yt,zt=self.get_xyz(0.,-1.,0.,norm=self.scale*ticklabelpad[2])
        else:
            xt,yt,zt=self.get_xyz(0.,-1.,0.,norm=self.scale*ticklabelpad)
        for i in range(1,nmajor): # right to left grid lines
            # Plot gird lines
            frac=self.scale*float(i)/nmajor
            x,y,z=self.get_xyz([0.,0.,self.scale-frac],[0.,self.scale-frac,0.],[frac,frac,frac])
            self.ax.plot(x,y,z,linestyle='-',color='gray',linewidth=lw)
            # Plot ticks
            x,y,z=self.get_xyz([0.,0.],[0.,-0.1*(self.scale-frac),0.],[frac,frac])
            factor=self.scale*tick_length/((x[1]-x[0])**2.+(y[1]-y[0])**2.+(z[1]-z[0])**2.)**0.5
            x[1],y[1],z[1]=x[0]+factor*(x[1]-x[0]),y[0]+factor*(y[1]-y[0]),z[0]+factor*(z[1]-z[0])
            self.ax.plot(x,y,z,linestyle='-',color='k',linewidth=lw)
            # Add tick labels
            x[1]=x[0]+xt
            y[1]=y[0]+yt
            z[1]=z[0]+zt
            if frac==round(frac):
                self.ax.text(x[1],y[1],z[1],str(int(frac)))
            else:
                self.ax.text(x[1],y[1],z[1],str(frac))


    def set_view(azimuth,distance,elevation):
        self.ax.azim=azimuth
        self.ax.dist=distance
        self.ax.elev=elevation
