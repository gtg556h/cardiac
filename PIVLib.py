import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# from io import StringIO

class piv(object):
    def __init__(self, filename):
        print('Importing data:')

        # Import data from .npz:
        data = np.load(filename)
        self.t=data['t']; self.x=data['x']; self.y=data['y']; self.ux1=data['ux1']; self.uy1=data['uy1']; self.mag1=data['mag1']
        self.ang1=data['ang1']; self.p1=data['p1']; self.ux2=data['ux2']; self.uy2=data['uy2']; self.mag2=data['mag2']
        self.p2=data['p2']; self.ux0=data['ux0']; self.uy0=data['uy0']; self.mag0=data['mag0']; self.side=data['side']
        self.pivN=data['pivN']; self.nFrames=data['nFrames']; self.dt=data['dt']

    #####################################################
    #####################################################


    def slider(self):
        pass


    #####################################################
    #####################################################

    def quiver(self):
        # Animation of quiver
        fig,ax = plt.subplots(1,1)
        Q = ax.quiver( self.x[:,0], -self.y[:,0], self.ux1[:,0], -self.uy1[:,0], pivot='mid', color='r', units='inches', scale=1)

        def update_quiver(n, Q, X, Y, nFrames):
            """
            updates the horizontal and vertical vector components by a
            fixed increment on each frame
            """
            nn = np.mod(n, self.nFrames)
            U = self.ux1[:,nn]
            V = -self.uy1[:,nn]

            Q.set_UVC(U,V)

            return Q,

        # you need to set blit=False, or the first set of arrows never gets
        # cleared on subsequent frames
        anim = animation.FuncAnimation(fig, update_quiver, fargs=(Q, self.ux1, self.uy1, self.nFrames), interval=10, blit=False)

        plt.show()

    ######################################################
    ######################################################

    def quiverPlusContour(self):
        # Coplot animation of quiver and contourf
        # Initiate figure and quiver
        fig = plt.figure(figsize=(10,5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        Q = ax1.quiver( self.x[:,0], -self.y[:,0], self.ux1[:,0], -self.uy1[:,0], pivot='mid', color='r', units='inches', scale=1)

        ######
        # Preprocessing for contour plot:
        XC_ = self.x[:,0]
        YC_ = self.y[:,0]
        nRow = np.where(XC_==XC_[0])[0].size
        nCol = np.where(YC_==YC_[0])[0].size

        XC = np.zeros((nRow,nCol))
        YC = np.zeros((nRow,nCol))
        YC2 = np.zeros((nRow,nCol))
        mag = np.zeros((nRow,nCol))

        minMag = np.min(self.mag1)
        maxMag = np.max(self.mag1)
        dLevel = (maxMag - minMag)/10
        levels = np.arange(minMag,maxMag + dLevel, dLevel)
        levels = np.arange(minMag, minMag + 6*dLevel, dLevel)

        for ii in range(0,nRow):
            XC[ii,:] = XC_[ii*nCol:(ii+1)*nCol]
            YC[ii,:] = YC_[ii*nCol:(ii+1)*nCol]
            mag[ii,:] = self.mag1[ii*nCol:(ii+1)*nCol,0]

        C = ax2.contourf(XC, -YC, mag, levels)

        #####
        def update_quiver(n, Q, C, X, Y, nFrames, nRow, nCol, levels):
            """
            updates the horizontal and vertical vector components by a
            fixed increment on each frame
            """
            nn = np.mod(n, self.nFrames)
            U = self.ux1[:,nn]
            V = -self.uy1[:,nn]


            for ii in range(0,nRow):
                mag[ii,:] = self.mag1[ii*nCol:(ii+1)*nCol, np.mod(n, self.nFrames)]


            Q.set_UVC(U,V)
            #C.set_cmap(mag)
            C = ax2.contourf(XC, -YC, mag, levels)

            return Q,C

        # you need to set blit=False, or the first set of arrows never gets
        # cleared on subsequent frames
        anim = animation.FuncAnimation(fig, update_quiver, fargs=(Q, C, self.ux1, self.uy1, self.nFrames, nRow, nCol, levels), interval=10, blit=False)

        plt.show()