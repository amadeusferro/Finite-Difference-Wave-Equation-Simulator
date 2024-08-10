import matplotlib.pyplot as plt
import numpy as np

def main():
    N              = 256    # resolution
    boxsize        = 1.0    # box size
    c              = 1.     # propagation speed
    t              = 0      # time
    tStop          = 2.     # stop time
    plotRealTime   = True   # switch for plotting in real time

	# Grid
    deltaX = boxsize / N
    deltaT = (np.sqrt(2)/2) * deltaX / c
    xAxis = 0
    yAxis = 1
    right = -1
    left = 1
    fac = deltaT**2 * c**2 / deltaX**2
    
    xlin = np.linspace(0.5*deltaX, boxsize-0.5*deltaX, N)
    y, x = np.meshgrid(xlin, xlin)

	# Initial Conditions / Mask
    U = np.zeros((N, N))
    mask = np.zeros((N, N), dtype=bool)
    mask[0,:]  = True     # True, True , True , True , True , True , True, 
    mask[-1,:] = True     # True, False, False, False, False, False, True,
    mask[:,0]  = True     # True, False, False, False, False, False, True,
    mask[:,-1] = True     # True, True , True , True , True , True , True
    
	# Setting wall + double-slits
    mask[int(N/4):int(N*9/32),:N-1]     = True
    mask[1:N-1,int(N*5/16):int(N*3/8)]  = False
    mask[1:N-1,int(N*5/8):int(N*11/16)] = False
    # Setting wall + second double-slits
    # mask[int(N*3/4):int(N*25/32), :] = True
    # mask[1:N-1,int(N*5/16):int(N*3/8)]  = False
    # mask[1:N-1,int(N*5/8):int(N*11/16)] = False
	# Setting big obstacle in the middle
    #mask[int(N/4):int(N*3/4), int(N/4):int(N*3/4)] = True

    U[mask] = 0
    prevU = 1.*U
    
	# Prepare Matplotlib Figure
    fig = plt.figure(figsize=(6,6), dpi=80)
    cmap = plt.cm.seismic
    cmap.set_bad('gray')
    outputCount = 1
    
	# Simulation
    while t < tStop:

		# Calc laplacian
        ULX = np.roll(U, left, axis=xAxis)
        URX = np.roll(U, right, axis=xAxis)
        ULY = np.roll(U, left, axis=yAxis)
        URY = np.roll(U, right, axis=yAxis)

        laplacian = ( ULX + ULY - 4*U + URX + URY)
        
		# Update U
        newU  = 2*U - prevU + fac * laplacian
        prevU = 1.*U
        U     = 1.*newU
        
		# Boundary conditions (Dirichlet/inflow)
        U[mask] = 0
        U[0,:] = np.sin(20*np.pi*t) * np.sin(np.pi*xlin)**2
		
		# Update time
        t += deltaT
        print(t)
        
		# Real Time Plotting
        if (plotRealTime) or (t >= tStop):
            plt.cla()
            Uplot = 1.*U
            Uplot[mask] = np.nan
            plt.imshow(Uplot.T, cmap=cmap)
            plt.clim(-3, 3)
            ax = plt.gca()
            ax.invert_yaxis()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)    
            ax.set_aspect('equal')    
            plt.pause(0.001)
            outputCount += 1


    return 0


if __name__== "__main__":
	main()