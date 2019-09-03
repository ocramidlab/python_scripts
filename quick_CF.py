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
ptypes   = map(int,sys.argv[4].split(","))
MAS      = 'CIC'
do_RSD   = False
axis     = 0
threads  = 1

## First do the total Power Spectrum
delta = MASL.density_field_gadget(snapshot, ptypes, grid, MAS, do_RSD, axis)
delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0

# compute the correlation function
CF     = PKL.Xi(delta, BoxSize, MAS, threads)
r      = CF.r3D #radii in Mpc/h
xi0    = CF.xi  #correlation function (monopole)
#xi2    = CF.xi[:,1]  #correlation function (quadrupole)
#xi4    = CF.xi[:,2]  #correlation function (hexadecapole)
Nmodes = CF.Nmodes3D #number of modes

plt.plot(r, xi0)
plt.yscale('log')
plt.xscale('log')
plt.title('Correlation Function')

#plt.show()

plt.savefig(snapshot+'_CF_all.png')
#### Writing ######                                                                                             

f_out=snapshot+'_CF_all.dat'

f1=open(f_out,'w')
for i in range(len(r)):
    f1.write(str(r[i])+' '+str(xi0[i])+' '+str(Nmodes[i])+'\n')

f1.close()

## Then do the individual species type by type
if len(ptypes) > 1: 
    for type in ptypes:
        delta = MASL.density_field_gadget(snapshot, [type], grid, MAS, do_RSD, axis)
        delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0

        # compute the correlation function
        CF     = PKL.Xi(delta, BoxSize, MAS, threads)
        r      = CF.r3D #radii in Mpc/h
        xi0    = CF.xi  #correlation function (monopole)
        #xi2    = CF.xi[:,1]  #correlation function (quadrupole)
        #xi4    = CF.xi[:,2]  #correlation function (hexadecapole)
        Nmodes = CF.Nmodes3D #number of modes

        #### Writing ######                                           
        f_out=snapshot+'_CF_type'+str(type)+'.dat'
        
        f1=open(f_out,'w')
        for i in range(len(r)):
            f1.write(str(r[i])+' '+str(xi0[i])+' '+str(Nmodes[i])+'\n')

        f1.close()
            
