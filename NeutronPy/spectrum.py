import sys
from PyQt5 import QtWidgets
import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from beamline import Beamline
from image_viewer import ImageViewerWindow
from materials import Materials

class Spectrum(QtWidgets.QWidget):
    def __init__(self, beamline, materials, imageviewer):
        '''
        The Spectrum takes in the instances of beamline, materials, and 
        imageviewer created in main.py. This is to track the variables of inputs
        to be reflected to the spectrum
        '''
        self.beamline = beamline
        self.materials = materials
        self.imageviewer = imageviewer


        super(Spectrum, self).__init__()
        self.initUI()

    def initUI(self):
        '''
        The UI initialization
        '''
        self.setGeometry(100, 100, 800, 600)
        self.center()

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        '''
        Creating buttons to generate the plots.
        We connect the pressing of the buttons to crossSectionalData 
        and AntonCode function for plotting
        '''
        btn1 = QtWidgets.QPushButton('Plot 1: Cross Section (MeV vs Barns) ', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(self.crossSectionalData)
        grid.addWidget(btn1, 5, 0)

        btn2 = QtWidgets.QPushButton('Plot 2: Spectra (Transmission vs Energy)', self)
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.AntonCode)
        grid.addWidget(btn2, 5, 1)

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 3, 0, 1, 2)

        #self.show() - UNCOMMENT THIS LINE FOR SELF DEBUGGING

    def crossSectionalData(self):
        '''
        Obtaining the updated parameter inputs from beamline, materials, 
        and imageviewer
        '''
        fullParameters = self.getUpdatedParameters()

        self.figure.clf()
        ax3 = self.figure.add_subplot(111)
        
        '''
        The plotting function itself
        '''
        x = [i for i in range(100)]
        y = [i**(fullParameters[0] + fullParameters[1]) for i in x]
        
        
        ax3.plot(x, y, 'r.-')
        ax3.set_title('Cross Section (MeV vs Barns)')
        self.canvas.draw_idle()

    def AntonCode(self):
        '''
        Obtaining the updated parameter inputs from beamline, materials, 
        and imageviewer
        '''
        fullParameters = self.getUpdatedParameters()

        self.figure.clf()
        ax1 = self.figure.add_subplot(211)

        '''
        The plotting function(s) itself (QuickFit)
        As we are plotting multiple functions in one graph
        '''    
        x1 = [i for i in range(200)]
        y1 = [x1[0]*x1[1]*x1[2]*x1[3]*x1[6]*x1[7]*x1[8]*x1[9] for i in x1]

        ax1.plot(x1, y1, 'b.-')
        ax1.set_title("Experimental Spectrum") #obtained from Diether's experimental data
        ax1.set_xlabel("Energy / Time") #Energy, Time, or Wavelength - depending on how the user picks it
        ax1.set_ylabel("Transmission")
        ax2 = self.figure.add_subplot(212)


        x2 = [i for i in range(100)] #pass the x1, y1 values to here for Anton's method

        #pass anton's method using the global variable fullParameters
        y2 = [fullParameters[1] for i in x2]

        ax2.plot(x2, y2, 'b.-')
        self.canvas.draw_idle()
        ax2.set_title('Fitting')
        ax2.set_xlabel("Energy / Time")
        ax2.set_ylabel("Transmission")


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def getUpdatedParameters(self):
        '''
        Function that obtains the updated inputs from beamline, materials,
        and image viewer. We call the saveInput functions for all these instances
        and that is converted into an array called fullParameters above
        '''
        
        beamlineInput = self.beamline.saveInput()
        #beamlineInput = [flightPath, delayOnTrigger, [minimumEnergyRange, maximumEnergyRange]]

        self.flightPath =  beamlineInput[0] #1 Flight Path: L (meters)
        self.delayOnTrigger = beamlineInput[1] #2 Delay on trigger: dT (miliseconds)
        self.energyRange = beamlineInput[2] #3 Minimum and Maximum Energy Range (eV)
        """
        elementName = ""
        isotopicAbundance = float(self.isotopicAbundance.text()) #value between 0 and 1 (for Ag it is 0.52 and 0.48 for Ag-107 and Ag-109 isotopes)
        atomicFraction = float(self.atomicFraction.text()) #number of 0-1. (e.g. Gd2O3 it is 0.4 for Gd and 0.6 for O)
        density = float(self.density.text()) #Rho (g/cm^3)
        thickness = float(self.density.text()) #d (um)
        component = int(self.component.text())# integer number starting from 1 (in case there are several different samples in the beam behind each other)


        #number of assert statements to make sure user input is as desired
        assert flightPath >= 0
        assert delayOnTrigger >= 0
        assert minimumEnergyRange >= 0
        assert maximumEnergyRange > minimumEnergyRange
        assert 0 <= isotopicAbundance and isotopicAbundance <= 1
        assert 0 <= atomicFraction and atomicFraction <= 1
        assert density > 0
        assert thickness > 0
        assert component >= 1

        energyRange = pd.array([minimumEnergyRange, maximumEnergyRange]) #size: 2
        
        #IsotopeName	Abundance	AtomicFraction	Density	AtomicMass	"Thickness,um"	GrupN
        materialParameters = pd.DataFrame([elementName, isotopicAbundance, atomicFraction, density, thickness, component]) #size: 6
        cross_sectional_data = pd.array([]) #size: 2 - DIETHER

        
        return flightPath, delayOnTrigger, energyRange, materialParameters, [cross_sectional_data]
        """
        return [self.flightPath, self.delayOnTrigger, self.energyRange]

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Spectrum()
    sys.exit(app.exec_())
