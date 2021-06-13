#NOTE: self.image_cube is a non-numpy array implementation at the moment!


import sys, traceback
from os import listdir
from os.path import isfile, join
from astropy.io import fits
import numpy as np
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from progress import Progress

class selector(QRubberBand):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 4))
        color = QColor(Qt.green)
        painter.drawRect(event.rect())


##ImageCubeLoadSignal and ImageCubeLoader is a class that assists in dumping all the data into the image cube without having to terminate the MainWindow
##Done via multi-threading
class ImageCubeLoadSignal(QObject):
    #Class to monitor the progress of loading the fits files into the image cube
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class ImageCubeLoader(QRunnable):
    #Separate Thread to handle mutliprocesses 
    #This one, in particular, deals with opening each fits file and inserting them into the image cube
    def __init__(self, fn, *args, **kwargs):
        super(ImageCubeLoader, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.signals = ImageCubeLoadSignal()
        self.kwargs['progress_callback'] = self.signals.progress

    

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except: 
            #Handles exception if there's an issue with loading data
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


##Image_viewer is the actual image GUI we see on the top left of the screen
class image_viewer(QGraphicsView):
    rect_sig = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.empty = True
        self.zoom = 0
        self.max_zoom = 7
        self.scene = QGraphicsScene(self)
        self.photo = QGraphicsPixmapItem()
        self.scene.addItem(self.photo)
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))

        self.rect = selector(QRubberBand.Rectangle, self)

        #Stores the rectangle geometry relative to scene
        self.rect_scene = QRect()
        self.rect_change = False
        self.rect_exists = False

    def show_photo(self):
        rect = QtCore.QRectF(self.photo.pixmap().rect())
        self.setSceneRect(rect)

    def set_photo(self, pixmap=None):
        self.zoom = 0
        if self.rect_exists:
            self.update_rect()
        if pixmap and not pixmap.isNull():
            self.empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.photo.setPixmap(pixmap)
            self.show_photo()

    def update_rect(self):
        top_left = self.mapFromScene(self.rect_scene.topLeft())
        bottom_right = self.mapFromScene(self.rect_scene.bottomRight())
        self.rect.setGeometry(QRect(top_left, bottom_right))

    def fit_to_window(self):
        self.zoom = 0
        viewrect = self.viewport().rect()
        imagerect = self.transform().mapRect(self.photo.pixmap().rect())
        factor = min(viewrect.width() / imagerect.width(), viewrect.height() / imagerect.height())
        self.scale(factor, factor)

    def wheelEvent(self, event):
        if (not self.rect_change):
            if event.angleDelta().y() > 0:
                self.zoom += 1
                if (abs(self.zoom) < self.max_zoom):
                    self.scale(1.25, 1.25)
                else:
                    self.zoom = self.max_zoom
            else:
                self.zoom -= 1
                if (abs(self.zoom) < self.max_zoom):
                    self.scale(0.75, 0.75)
                else:
                    self.zoom = -self.max_zoom

            if (self.zoom == 0):
                self.fit_to_window()

            self.update_rect()

    def mousePressEvent(self, event):
        if (self.photo.isUnderMouse()):
            self.origin = event.pos()
            self.rect.setGeometry(QRect(self.origin, QSize()))
            self.rect.show()
            self.rect_sig.emit(self.rect.geometry())
            self.rect_change = True
        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if (self.photo.isUnderMouse()):
            if self.rect_change == True:
                self.rect.setGeometry(QRect(self.origin, event.pos()).normalized())
                self.rect_sig.emit(self.rect.geometry())
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.rect_change = False
        self.rect_exists = True
        top_left = self.mapToScene(self.rect.geometry().topLeft())
        bottom_right = self.mapToScene(self.rect.geometry().bottomRight())
        self.rect_scene = QRect(QPoint(top_left.x(), top_left.y()), QPoint(bottom_right.x(), bottom_right.y()))
        QGraphicsView.mouseReleaseEvent(self, event)

    def resizeEvent(self, event):
        self.update_rect()
        QGraphicsView.resizeEvent(self, event)

class ImageViewerWindow(QWidget):
    def __init__(self):
        super().__init__()
        #For multi-threading data loadout
        self.threadpool = QThreadPool()

        self.viewer = image_viewer()
        self.files = None
        self.dir = "."

        #Load button: Opens directory selection
        self.load_button = QToolButton(self)
        self.load_button.setText('Select File/Directory')
        self.load_button.clicked.connect(self.load_dir)

        #Coordinates of the selection rectangle and their labels
        self.x_min_label = QLabel("X Min")
        self.x_min = QSpinBox()

        self.x_max_label = QLabel("X Max")
        self.x_max = QSpinBox()

        self.y_min_label = QLabel("Y Min")
        self.y_min = QSpinBox()

        self.y_max_label = QLabel("Y Max")
        self.y_max = QSpinBox()

        self.z_label = QLabel("Z")
        self.z = QSpinBox() #TODO: The spinbox for the z value does not seem to update; the z-scrollbar works though
        self.z.setMinimum(0)
        self.z.valueChanged.connect(self.load_new_image_z)

        #Update values based on changes in both the viewer and the spinboxes
        self.viewer.rect_sig.connect(self.update_xy)
        self.x_min.valueChanged.connect(self.update_rect)
        self.y_min.valueChanged.connect(self.update_rect)
        self.x_max.valueChanged.connect(self.update_rect)
        self.y_max.valueChanged.connect(self.update_rect)

        #Contrast Slider
        self.slider_label = QLabel("Contrast")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(255)

        #Update on Contrast Change
        self.slider.valueChanged.connect(self.load_new_image_scroll_bar)

        #Scroll bar
        self.scroll_bar = QSlider(Qt.Horizontal)
        self.scroll_bar.setOrientation(Qt.Horizontal)
        self.scroll_bar.setMinimum(0)
        self.scroll_bar.setMaximum(0)
        self.scroll_bar.valueChanged.connect(self.load_new_image_scroll_bar)

        #Add the image viewer and scroll bar
        layout = QVBoxLayout(self)
        VB = QVBoxLayout(self)
        VB.addWidget(self.viewer)
        VB.addWidget(self.scroll_bar)
 
        #Add the coordinates and the get file button
        HB = QVBoxLayout(self)
        HB.setAlignment(Qt.AlignLeft)
        HB.addWidget(self.load_button)
        HB.addWidget(self.x_min_label)
        HB.addWidget(self.x_min)
        HB.addWidget(self.x_max_label)
        HB.addWidget(self.x_max)
        HB.addWidget(self.y_min_label)
        HB.addWidget(self.y_min)
        HB.addWidget(self.y_max_label)
        HB.addWidget(self.y_max)
        HB.addWidget(self.z_label)
        HB.addWidget(self.z)
        HB.addWidget(self.slider_label)
        HB.addWidget(self.slider)
        layout.addLayout(VB)
        layout.addLayout(HB)
    
    def load_dir(self):
        self.dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        #TODO Fix the FileNotFoundError when clicking cancel
        if dir != '': 
            self.files = listdir(self.dir)

            self.scroll_bar.setMaximum(len(self.files) - 1)
            self.z.setMaximum(len(self.files) - 1)
            self.load_new_image(0)

            #loads every image file in the directory into an image cube containing information
            #on each pixel of each slice of data
            #For debugging, looking at the load_new_images method will be helpful as abstractions
            #are omitted for this list comprehension to maintain fastest runtime
            def load_image_cube(progress_callback):
            
                #Take the data from all the fits files and dump them into an array
                self.image_cube = []
                startTimer1 = time.perf_counter()
                fileLen = len(self.files)
                for fileNum in range(0, fileLen):
                    with fits.open(self.dir + '/' + self.files[fileNum], memmap = True) as hdul:
                        self.image_cube.append(hdul[0].data)
                        del hdul[0].data
                        if (fileNum - 1) * 100 // fileLen  != fileNum * 100 // fileLen:
                            progress_callback.emit(fileNum / fileLen * 100)
                endTimer1 = time.perf_counter()
                progress_callback.emit(100)
                self.loadingBar.finishFits2Array(endTimer1 - startTimer1)
                time.sleep(2)


                '''
                #Initializing Image Cube into a Numpy Array
                startTimer2 = time.perf_counter()
                self.loadingBar.startLoadImageCube()
                '''
                #TODO: uncomment these blocks for other needed operations other than sum
                #self.image_cube = np.array(self.image_cube) #this apparently takes a long time ~7.6 s for 2600 fits files
                '''
                endTimer2 = time.perf_counter()
                self.loadingBar.finishLoadImageCube(endTimer2 - startTimer2)
                time.sleep(2)
                '''

                #Close the loading window
                self.loadingBar.close()
            
            def progress_fn(n):
                #   print("%d%% done" % n)
                self.loadingBar.setValue(n)

            #Naive Approach: This method literally takes in all the pixel arrays found on the fits file and shoves them into an image_cube
                #Pros: This method is great as the runtime of you selecting a region and computing the sum becomes way faster beacause it took everything in from the beginning
                #Cons: This method might suffer from some poor runtime to dump all the fits file into an image cube but doesn't seem too much of a problem at the moment
            def naive_load_data():
                #loading bar
                self.loadingBar = Progress()
                cubeThread = ImageCubeLoader(load_image_cube)
                cubeThread.signals.progress.connect(progress_fn)
                self.threadpool.start(cubeThread)
            
            naive_load_data() #In the case runtime becomes an issue, take a look at the compressed_load_data function and implementation
                              #Similar to naive_load_data(), it has its pros and cons - personally in my opinion, naive_load_data() does better

            #Compressed Approach: 
                #We create a image cube 3D array with NaN values and instantiate them
            """
            def compressed_load_data():
                oneSlice = fits.open(self.dir + '/' + self.files[0])[0].data
                length = len(oneSlice)
                width = len(oneSlice[0])
                self.image_cube = np.empty((len(self.files), length, width))
                self.image_cube[:] = np.NaN

            tic = time.perf_counter()
            compressed_load_data()
            toc = time.perf_counter()
            print(f"Instantiated image_cube in {toc - tic:0.4f} seconds")
            """

    # Loads a new image from the image library
    #   This load_new_image is only for the image viewing purposes - it only loads and 
    #   shows one slice each for optimizing runtime while scrolling the z-bar
    def load_new_image(self, value):
        if self.files != None:
            filename = self.dir + '/' + self.files[value]

            hdul = fits.open(filename)

            image_data = hdul[0].data
            image_data = image_data / image_data.max()
            image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data)) * (255 - self.slider.value())
            image_data = image_data.astype(np.uint8)

            hdul.close()

            h,w = image_data.shape
            qimage = QImage(image_data.data, h, w, QImage.Format_Grayscale8)

            self.viewer.set_photo(QPixmap(qimage))

            self.viewer.fit_to_window()

            bottom_right = self.viewer.mapToScene(self.viewer.viewport().rect().bottomRight())
            self.x_min.setMaximum(bottom_right.x())
            self.y_min.setMaximum(bottom_right.y())
            self.x_max.setMaximum(bottom_right.x())
            self.y_max.setMaximum(bottom_right.y())

    # Changed the value of  z to obtain next image
    def load_new_image_z(self):
        value = self.z.value()
        self.scroll_bar.setValue(value)
        self.load_new_image(value)

    # Changed the value of the scroll_bar to obtain next image
    def load_new_image_scroll_bar(self):
        value = self.scroll_bar.value()
        self.z.setValue(value)
        self.load_new_image(value)


    # Update the values of the x and y coordinates based on the scene  (aka the image)
    def update_xy(self, rect):
        top_left = self.viewer.mapToScene(rect.topLeft())
        bottom_right = self.viewer.mapToScene(rect.bottomRight())
        self.x_min.setValue(top_left.x())
        self.y_min.setValue(top_left.y())
        self.x_max.setValue(bottom_right.x())
        self.y_max.setValue(bottom_right.y())

    def update_rect(self):
        rect_new = QRect(QPoint(self.x_min.value(), self.y_min.value()), QPoint(self.x_max.value(), self.y_max.value()))
        top_left = self.viewer.mapFromScene(rect_new.topLeft())
        bottom_right = self.viewer.mapFromScene(rect_new.bottomRight())
        self.viewer.rect_scene = rect_new
        self.viewer.update_rect()
        return [self.x_min.value(), self.x_max.value(), self.y_min.value(), self.y_max.value()]


    #Save Input function for main.py integration
    def saveInput(self):

        try:
            #z : SliceNum
            z = float(self.scroll_bar.value())
            
            #xmin, xmax are the x coordinates of the rectangle user selected; same goes for y
            xmin, xmax, ymin, ymax = self.update_rect()

            def naive_sum_data(): 
                #sumImageCube is the sum of all the pixel values of the rectangle you selected for all the slices in the image_cube you created when selecting the directory
                self.sumImageCube = [np.sum((self.image_cube[sliceNum])[ymin:ymax, xmin:xmax]) for sliceNum in range(0, len(self.image_cube))]
                #TODO: uncomment these blocks for other needed operations other than sum
                #self.sumImageCube = np.array([np.sum((self.image_cube[sliceNum])[ymin:ymax, xmin:xmax]) for sliceNum in range(0, len(self.image_cube))])
            
            naive_sum_data()
            
            #These print statements are here for whenever you want to see if the inputs are actually updating when you click on the plots in spectrum
            #Can comment out if needed
            print("xmin: " + str(xmin) + " xmax: " + str(xmax))
            print("ymin: " + str(ymin) + " ymax: " + str(ymax))
            print("z: " + str(z))
            return [[xmin, xmax], [ymin, ymax], z, self.sumImageCube]
        except ValueError:
            print('One of your inputs is not a number')




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ImageViewerWindow()
    w.setGeometry(0, 0, 800, 600)
    w.show()
    sys.exit(app.exec_())
