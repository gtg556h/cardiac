import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.patches import Rectangle
import matplotlib.patches as patches


# Notes:

# Current status: Works!
# Initialize piv object
# Execute 'p1.analyze(scale, screenID0
# View resultant data via p1.screen[i]

# The skeleton of the framework below has been laid.
# Currently, we can instantiate a member of piv class
# Then: varname = pivInstance.analyzed(pivInstance, 100) generates an instance of class roi, with all required vars
# Need to restructure class layout to make it run more logically!


# Implemented ROI selection in Slider method
# Generate new routine, using Slider base, where integer selection of multiple ROIs generates a list of ROIs.
# After ROI list generation, sieve function is performed on EACH roi, generating mean ux1, uy1 etc... computations on each ROI

# Need to organize code better with multiple class additions and proper inheritence




# from io import StringIO

class piv(object):
    """Class documentation here...
    """
    def __init__(self, filename):
        print('Importing data:')

        # Import data from .npz:
        data = np.load(filename)
        self.t=data['t']; self.x=data['x']; self.y=data['y']; self.ux1=data['ux1']; self.uy1=data['uy1']; self.mag1=data['mag1']
        self.ang1=data['ang1']; self.p1=data['p1']; self.ux2=data['ux2']; self.uy2=data['uy2']; self.mag2=data['mag2']
        self.p2=data['p2']; self.ux0=data['ux0']; self.uy0=data['uy0']; self.mag0=data['mag0']; self.side=data['side']
        self.pivN=data['pivN']; self.nFrames=data['nFrames']; self.dt=data['dt']; self.dx=data['dx']


    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #  DATA PROCESSING
    #####################################################
    #####################################################
    #####################################################
    #####################################################

    def sieveByROI(self, target):
        """Take ROI data generated by manual selection in class 
        method quiver, and create new data arrays 
        """
        # Insert exception for nonexistence of ROI
        print('sieving')

        self.extracted = np.zeros_like(self.t)
        extracted = np.zeros_like(self.t)

        # Following needs repair!!!

        self.indices = np.where((self.x[:,0] < self.roi.x1) & (self.x[:,0] > self.roi.x0) & (self.y[:,0] < self.roi.y1) & (self.y[:,0] > self.roi.y0))

        for i in range(0, self.t.shape[0]):
            self.extracted[i] = (np.mean(self.ux0[self.indices, i])**2 + np.mean(self.uy0[self.indices, i])**2)**0.5
            extracted[i] = np.mean(target[self.indices, i])
            
        return extracted


    #####################################################
    #####################################################
    def analyze(self, scale=1, screenID='default'):

        try:
            self.screen
        except AttributeError:
            self.screen = []
        
        self.screen.append(self.analyzed(self, scale, screenID))



    ######################################################  

    class analyzed:

        ############################################
        class roi:
            def __init__(self, piv, x0, x1, y0, y1):
                print('processing roi')

                self.ux0 = np.zeros_like(piv.t); self.uy0 = np.zeros_like(piv.t)
                self.ux1 = np.zeros_like(piv.t); self.uy1 = np.zeros_like(piv.t)
                self.ux2 = np.zeros_like(piv.t); self.uy2 = np.zeros_like(piv.t)
                
                self.indices = np.where((self.x[:,0] < x1) & (self.x[:,0] > x0) & (self.y[:,0] < y1) & (self.y[:,0] > y0))
                
                for i in range(0, piv.t.shape[0]):
                    self.ux0[i] = np.mean(piv.ux0[self.indices, i])
                    self.uy0[i] = np.mean(piv.uy0[self.indices, i])
                    self.ux1[i] = np.mean(piv.ux1[self.indices, i])
                    self.uy1[i] = np.mean(piv.uy1[self.indices, i])
                    self.ux2[i] = np.mean(piv.ux2[self.indices, i])
                    self.uy2[i] = np.mean(piv.uy2[self.indices, i])
 


        ###########################################
        class RectangleBuilder2:
            def __init__(self, ax):
                print('Select roi')
                self.fig = ax.get_figure()
                self.ax = ax
                self.x0 = []
                self.y0 = []
                self.x1 = []
                self.y1 = []

            def connect(self):
                self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
                self.cidpress = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

            def on_press(self, event):
                print('click', event)
                if event.inaxes!=self.ax: return
                self.x0_ = event.xdata
                self.y0_ = -event.ydata

            def on_release(self, event):
                print('release', event)
                if event.inaxes!=self.ax: return
                self.x1_ = event.xdata
                self.y1_ = -event.ydata
                self.x0.append(np.min([self.x0_, self.x1_]))
                self.y0.append(np.min([self.y0_, self.y1_]))
                self.x1.append(np.max([self.x0_, self.x1_]))
                self.y1.append(np.max([self.y0_, self.y1_]))
                del [self.x0_, self.x1_, self.y0_, self.y1_]
                self.draw_rectangle()

            def draw_rectangle(self):
                print(self.x0[-1],self.y0[-1])
                rect = self.ax.add_patch(patches.Rectangle((self.x0[-1], -self.y0[-1]), (self.x1[-1] - self.x0[-1]), (-self.y1[-1] + self.y0[-1])))
                self.fig.canvas.draw()

        ################################################
        def __init__(self, piv, scale=1, screenID='default'):

            print('analysis loop')
            self.analysisID = screenID
            fig, ax = plt.subplots()
            plt.subplots_adjust(left=0.12, bottom=0.2)

            Q = ax.quiver(piv.x[:,0], -piv.y[:,0], piv.ux1[:,0], -piv.uy1[:,0], pivot='mid', color='r', units='inches', scale=scale)

            axcolor = 'lightgoldenrodyellow'
            axframe = plt.axes([0.12, 0.1, 0.78, 0.03], axisbg=axcolor)
            sframe = Slider(axframe, 'Frame', 0, piv.nFrames, valinit=0)

            def update(val):
                n = np.round(sframe.val)
                U = piv.ux1[:,n]
                V = -piv.uy1[:,n]
                Q.set_UVC(U,V)
                fig.canvas.draw_idle()

            sframe.on_changed(update)

            resetAx = plt.axes([0.8, 0.025, 0.1, 0.04])
            roiAx = plt.axes([0.6, 0.025, 0.1, 0.04])
            button2 = Button(resetAx, 'Reset', color=axcolor, hovercolor='0.975')
            button1 = Button(roiAx, 'ROI', color=axcolor, hovercolor='0.975')

            def reset(event):
                sframe.reset()
            def roiSelect(event):
                print('Select ROI')
                self.roi = self.RectangleBuilder2(ax)
                self.roi.connect()

            button2.on_clicked(reset)
            button1.on_clicked(roiSelect)

            plt.show()



           





    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #####################################################
    #  DATA VISUALIZATION
    #####################################################
    #####################################################
    #####################################################
    #####################################################

    def slider(self, scale=1):
        """Generates quiver plot with slider control
           of current frame
        """
    
        class RectangleBuilder:
            def __init__(self, ax):
                print('rectangle builder time')
                self.fig = ax.get_figure()
                self.ax = ax

            def connect(self):
                self.cidpress = fig.canvas.mpl_connect('button_press_event', self.on_press)
                self.cidpress = fig.canvas.mpl_connect('button_release_event', self.on_release)

            def on_press(self, event):
                print('click', event)
                if event.inaxes!=self.ax: return
                self.x0_ = event.xdata    
                self.y0_ = -event.ydata

            def on_release(self, event):
                print('release', event)
                if event.inaxes!=self.ax: return
                self.x1_ = event.xdata
                self.y1_ = -event.ydata
                self.x0 = np.min([self.x0_, self.x1_])
                self.x1 = np.max([self.x0_, self.x1_])
                self.y0 = np.min([self.y0_, self.y1_]) 
                self.y1 = np.max([self.y0_, self.y1_])
                del [self.x0_, self.x1_, self.y0_, self.y1_]
                self.draw_rectangle()

            def draw_rectangle(self):
                rect = ax.add_patch(patches.Rectangle((self.x0,-self.y0),(self.x1-self.x0),(-self.y1 + self.y0)))
                self.fig.canvas.draw()


        
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.12, bottom=0.2)

        Q = ax.quiver( self.x[:,0], -self.y[:,0], self.ux1[:,0], -self.uy1[:,0], pivot='mid', color='r', units='inches', scale=scale)

        axcolor = 'lightgoldenrodyellow'
        axframe  = plt.axes([0.12, 0.1, 0.78, 0.03], axisbg=axcolor)

        sframe = Slider(axframe, 'Frame', 0, self.nFrames, valinit=0)

        def update(val):
            n = np.round(sframe.val)

            U = self.ux1[:,n]
            V = -self.uy1[:,n]
            Q.set_UVC(U,V)
            fig.canvas.draw_idle()

        sframe.on_changed(update)

        resetAx = plt.axes([0.8, 0.025, 0.1, 0.04])
        roiAx = plt.axes([0.6, 0.025, 0.1, 0.04])
        button2 = Button(resetAx, 'Reset', color=axcolor, hovercolor='0.975')
        button1 = Button(roiAx, 'ROI', color=axcolor, hovercolor='0.975')
        def reset(event):
            sframe.reset()

        def roiSelect(event):
            print('Select ROI')
            self.roi = RectangleBuilder(ax)
            self.roi.connect()

        button2.on_clicked(reset)
        button1.on_clicked(roiSelect)

        plt.show()


    #####################################################
    #####################################################


    #####################################################
    #####################################################

    def quiver(self, scale=1):
        # Animation of quiver
        fig,ax = plt.subplots(1,1)
        Q = ax.quiver( self.x[:,0], -self.y[:,0], self.ux1[:,0], -self.uy1[:,0], pivot='mid', color='r', units='inches', scale=scale)

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

    def quiverPlusContour(self, scale=1):
        # Coplot animation of quiver and contourf
        # Initiate figure and quiver
        fig = plt.figure(figsize=(10,5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        Q = ax1.quiver( self.x[:,0], -self.y[:,0], self.ux1[:,0], -self.uy1[:,0], pivot='mid', color='r', units='inches', scale=scale)

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



