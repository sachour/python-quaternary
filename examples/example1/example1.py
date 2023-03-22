import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from collections.abc import Mapping, Sequence
from quaternary import quaternary
from copy import deepcopy as copy
mpl.rcParams['axes.linewidth']  = 1.
mpl.rcParams['axes.edgecolor']  = 'gray'
mpl.rcParams['font.size']       = 15
mpl.rcParams['font.family']     = 'Arial'

fig=plt.figure()

quat=quaternary(fig)
quat.set_grid()
quat.set_label1('C$_1$')
quat.set_label2('C$_4$')
quat.set_label3('C$_{10}$')
quat.set_label4('CO$_2$',pad=0.05)
dfL=pd.read_excel('phenvC1.xlsx',sheet_name='L')*100.
dfV=pd.read_excel('phenvC1.xlsx',sheet_name='V')*100.

CP=[[c] for c in dfL.iloc[-1,:].tolist()]

quat.plot(dfL['C1'],dfL['C4'],dfL['C10'],'k-',lw=1.0)
quat.plot(dfV['C1'],dfV['C4'],dfV['C10'],'k-',lw=1.0)
quat.scatter(CP[1],CP[2],CP[3],facecolor='r',marker='o')
CPlocus=[c for c in CP]

dfL=pd.read_excel('phenvCO2.xlsx',sheet_name='L')*100.
dfV=pd.read_excel('phenvCO2.xlsx',sheet_name='V')*100.

CP=[[c] for c in dfL.iloc[-1,:].tolist()]
quat.plot(dfL['C1'],dfL['C4'],dfL['C10'],'k-',lw=1.0)
quat.plot(dfV['C1'],dfV['C4'],dfV['C10'],'k-',lw=1.0)
quat.scatter(CP[1],CP[2],CP[3],facecolor='r',marker='o')
CPCO2=CP

df=pd.read_excel('phenvCrossS1.xlsx')*100.

CP=[[c] for c in df.iloc[0,:].tolist()]
quat.plot(df['C1'],df['C4'],df['C10'],'k-',lw=1.0)
quat.scatter(CP[1],CP[2],CP[3],facecolor='r',marker='o')
CPlocus[0]+=CP[0]
CPlocus[1]+=CP[1]
CPlocus[2]+=CP[2]
CPlocus[3]+=CP[3]

df=pd.read_excel('phenvCrossS2.xlsx')*100.

CP=[[c] for c in df.iloc[0,:].tolist()]
quat.plot(df['C1'],df['C4'],df['C10'],'k-',lw=1.0)
quat.scatter(CP[1],CP[2],CP[3],facecolor='r',marker='o')
CPlocus[0]+=CP[0]
CPlocus[1]+=CP[1]
CPlocus[2]+=CP[2]
CPlocus[3]+=CP[3]

CPlocus[0]+=CPCO2[0]
CPlocus[1]+=CPCO2[1]
CPlocus[2]+=CPCO2[2]
CPlocus[3]+=CPCO2[3]
quat.plot(CPlocus[1],CPlocus[2],CPlocus[3],'r--',label='Critical locus\ncurve')

Cdf=pd.read_excel('RouteCentral.xlsx')*100.

Sg=copy(Cdf['Sg'])
Sg[Sg==0.]=np.nan
Sg[Sg==100.]=np.nan
bblindx=np.nanargmin(Sg)
dewindx=np.nanargmax(Sg)
#
quat.scatter(Cdf['C1'][[bblindx,dewindx]],Cdf['C4'][[bblindx,dewindx]],Cdf['C10'][[bblindx,dewindx]],
    marker='o',facecolor='b',edgecolor='b',depthshade=False)


Sg=copy(Cdf['Sg'])
quat.plot(Cdf['C1'][Sg==0],Cdf['C4'][Sg==0],Cdf['C10'][Sg==0],'k-',label='Central L')
msk=np.logical_and(Sg!=0.,Sg!=1.)
quat.plot(Cdf['C1'][msk],Cdf['C4'][msk],Cdf['C10'][msk],'b-',label='Central LV')
quat.plot(Cdf['C1'][Sg==100.],Cdf['C4'][Sg==100.],Cdf['C10'][Sg==100.],'r-',label='Central V')


Sdf=pd.read_excel('RouteSorbed.xlsx')*100.

quat.plot(Sdf['C1'],Sdf['C4'],Sdf['C10'],'k--',label='Sorbed')

l=4
for i in range(l):
    indx=int(len(Sdf)*i/l)
    lz1=[Cdf['C1'][indx],Sdf['C1'][indx]]
    lz2=[Cdf['C4'][indx],Sdf['C4'][indx]]
    lz3=[Cdf['C10'][indx],Sdf['C10'][indx]]
    quat.plot(lz1,lz2,lz3,'k--',lw=0.7,marker='o',markerfacecolor='None',markeredgecolor='k')
#
quat.plot(lz1,lz2,lz3,'k--',lw=0.7,marker='o',markerfacecolor='None',
    markeredgecolor='k',label='Sorption line')

#
i=0;indx=int(len(Sdf)*i/l)
lz1=[Cdf['C1'][indx],Sdf['C1'][indx]]
lz2=[Cdf['C4'][indx],Sdf['C4'][indx]]
lz3=[Cdf['C10'][indx],Sdf['C10'][indx]]
quat.text(lz1[1]-7,lz2[1],lz3[1],'0%',fontsize=12)

i=1;indx=int(len(Sdf)*i/l)
lz1=[Cdf['C1'][indx],Sdf['C1'][indx]]
lz2=[Cdf['C4'][indx],Sdf['C4'][indx]]
lz3=[Cdf['C10'][indx],Sdf['C10'][indx]]
quat.text(lz1[1]-7,lz2[1],lz3[1],'25%',fontsize=12)

i=2;indx=int(len(Sdf)*i/l)
lz1=[Cdf['C1'][indx],Sdf['C1'][indx]]
lz2=[Cdf['C4'][indx],Sdf['C4'][indx]]
lz3=[Cdf['C10'][indx],Sdf['C10'][indx]]
quat.text(lz1[1]-7,lz2[1],lz3[1],'50%',fontsize=12)

i=3;indx=int(len(Sdf)*i/l)
lz1=[Cdf['C1'][indx],Sdf['C1'][indx]]
lz2=[Cdf['C4'][indx],Sdf['C4'][indx]]
lz3=[Cdf['C10'][indx],Sdf['C10'][indx]]
quat.text(lz1[1]-7,lz2[1],lz3[1],'75%',fontsize=12)


fig.legend(fancybox=False,bbox_to_anchor=(0.98,0.85))
plt.tight_layout(rect=(0.,-0.03,1.0,1.03))
plt.savefig('ex1.png',dpi=400)
plt.savefig('../../readme_images/ex1.png',dpi=400)
plt.close()
