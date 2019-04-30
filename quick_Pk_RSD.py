import numpy as np
import MAS_library as MASL
import Pk_library as PKL
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

snapshot = sys.argv[1] #'fR5_mnu016_DUSTGRAIN_snap_463'
BoxSize  = float(sys.argv[2]) #2000.0 #Mpc/h
grid     = long(sys.argv[3]) #1024
ptypes   = [1]
MAS      = 'CIC'
do_RSD   = True
axis     = 0
threads=1

delta = MASL.density_field_gadget(snapshot, ptypes, grid, MAS, do_RSD, axis)
delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0

Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads)
# 1D P(k)
k1D      = Pk.k1D
Pk1D     = Pk.Pk1D
Nmodes1D = Pk.Nmodes1D

# 2D P(k)
kpar     = Pk.kpar
kper     = Pk.kper
Pk2D     = Pk.Pk2D
Nmodes2D = Pk.Nmodes2D

# 3D P(k)
k      = Pk.k3D
Pk0    = Pk.Pk[:,0] #monopole
Pk2    = Pk.Pk[:,1] #quadrupole
Pk4    = Pk.Pk[:,2] #hexadecapole
Nmodes = Pk.Nmodes3D

plt.plot(k, Pk0)
plt.yscale('log')
plt.xscale('log')
plt.title('Power Spectrum')

#plt.show()

plt.savefig(snapshot+'_powerspec_RSD.png')
#### Writing ######                                                                                             

f_out=snapshot+'_powerspec_RSD.dat'

f1=open(f_out,'w')
for i in range(len(k)):
    f1.write(str(k[i])+' '+str(Pk0[i])+' '+str(Pk2[i])+' '+str(Pk4[i])+' '+str(Nmodes[i])+'\n')
f1.close()
