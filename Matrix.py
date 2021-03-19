import numpy as np
import matplotlib.pyplot as plt
import struct
import os, sys
import re
import copy
import math
from scipy.ndimage import label

class Matrix:
    """
    Class to Read and Hangle Matrix files
    """
    def __init__(self, Path, Head): # Give the Path of the folder containing all the mtrx files and head file
        # Read PATH and open file
        self.Path = Path
        #self.Head = Path + '/' + Head

        self.Head = os.path.join(Path, Head)
        self.fp = None # file variable
        #for x in os.listdir(Path): # List the folder and look for the _0001.mtrx file
        #    if x[-10:] == "_0001.mtrx":
        #        self.fp = open(self.Path+"/"+x, "rb")
        self.fp = open(self.Head, 'rb')
        if self.fp == None:
            print("Matrix file not found!")
            sys.exit(1)
        if self.fp.read(8) != b"ONTMATRX": # header of the file
            print("Unknown header! Wrong Matrix file format")
            sys.exit(2)
        self.version = self.fp.read(4) # should be 0101
        self.IDs = {}
        self.params = {} # dictionary to list all the parameters
        self.images = {} # images[x] are the parameters used during the record for file named x

        # Parse the file and read the block
        while True: # While not EOF scan files and read block
            r = self.read_block()
            if r == False:
                break

    def read_string(self):
        """
        Strings are stored as UTF-16. First 32-bits is the string length
        """
        N = struct.unpack("<L", self.fp.read(4))[0] # string length
        if N == 0:
            return ""
        s = self.fp.read(N*2).decode('utf-16')
        return s

    def plotSTS(self, ID, num=1): # plot STS file called xxx--ID_num.I(V)_mtrx
        x, y = self.getSTS(ID, num)
        plt.plot(x, y)
        plt.show()

    def getUpDown(self, X, Y, NPTS):
        """
        Split data in Up and Down measurement, pad them with NaN if necessary and return them in increasing order.
        The returned value are X,Yup, Ydown
        If Up/Down data are missing an empty array will be returned
        """
        if len(Y) < NPTS: # Missing data
            Y = np.pad(Y, NPTS, 'constant', constant_values=np.nan)
        elif len(Y) > NPTS: # Forward and backward scans
            if len(Y) < 2*NPTS: # Missing data
                Y = np.pad(Y, 2*NPTS, 'constant', constant_values=np.nan)
            if X[NPTS-1] < X[0]:
                return X[NPTS:], [Y[NPTS:], Y[NPTS-1::-1]]
            else:
                return X[:NPTS], [Y[:NPTS], Y[-1:NPTS-1:-1]]
        if X[-1] < X[0]:
            return X[::-1], [np.empty(NPTS), Y[::-1], np.empty(NPTS)]
        return X, [Y, np.empty(NPTS)]



    def getSTSData(self, ID, nums=[1]):
        if not ID in self.IDs or len(nums) < 1:
            return None
        # retrieve the spectroscopy data (V, I and an object IM containing the parameters)
        V, I, IM = self.getSTS(ID, nums[0], params=True)
        NPTS = int(IM['Spectroscopy']['Device_1_Points']['value'])
        hasDI = self.IDs[ID]['hasDI']
        # Call the function to split and flip data if it's UP/Down measurements
        V, I = self.getUpDown(V, I, NPTS)
        for num in nums[1:]: # Skip first num as it's already parsed above
            X, Y = self.getUpDown(*self.getSTS(ID, num), NPTS=NPTS)
            if not np.array_equal(V, X):
                raise Exception("Bias axis differs between measurements?!?")
            for i in range(2): # i=0: Up scan, i=1: Down scan
                I[i] = np.vstack((I[i], Y[i]))
        Im = [np.nan]*2   # Store the mean of I
        Ims = [np.nan]*2  # Store StDev of I
        for i in range(2): # i=0: Up scan, i=1: Down scan
            Im[i] = I[i].mean(axis=0)
            Ims[i] = I[i].std(axis=0)
        if hasDI:
            X, dI = self.getUpDown(*self.getDIDV(ID, nums[0]), NPTS=NPTS)
            for num in nums[1:]:
                X, Y = self.getUpDown(*self.getDIDV(ID, num), NPTS=NPTS)
                if not np.array_equal(V, X):
                    raise Exception("Bias axis differs between measurements?!?")
                for i in range(2): # i=0: Up scan, i=1: Down scan
                    dI[i] = np.vstack((dI[i], Y[i]))
            dIm = [np.nan]*2   # Store the mean of dI/dV
            dIms = [np.nan]*2  # Store the StdDev of dI/dV
            for i in range(2): # i=0: Up scan, i=1: Down scan
                dIm[i] = dI[i].mean(axis=0)
                dIms[i] = dI[i].std(axis=0)
            return {'nums':nums, 'V':V, 'I':I, 'dI':dI, 'Imean':Im, 'Istd':Ims, 'dImean':dIm, 'dIstd':dIms}

    def getDIDV(self, ID, num=1):
        """
        The dI/dV measurements are stored the same way as the I(V), but with file extension Aux2(V).
        """
        return self.getSTS(ID, num, ext='Aux2')

    def getSTSparams(self, ID, num=1, ext='I'):
        if not ID in self.IDs:
            return None, None
        I = u"%s--%i_%i.%s(V)_mtrx"%(self.IDs[ID]['root'], ID, num, ext)
        if not I in self.images:
            return None
        return self.images[I]

    def openTopo(self, ID, num = 1, ext = 'Z'):
        """
        Open file xxxx-ID_num.Z_mtrx
        """
        if ID not in self.IDs:
            return None
        I = u"%s--%i_%i.%s_mtrx"%(self.IDs[ID]['root'], ID, num, ext)
        if not I in self.images:
            return None
        #print(self.images[I]['Z_t'])
        #ImagePath = self.Path + '/' + I

        ImagePath = os.path.join(self.Path, I)
        if not os.path.exists(ImagePath):
            return None
        with open(ImagePath, 'rb') as ff:
            if ff.read(8) != b"ONTMATRX":
                print("ERROR: Invalid STS format")
                sys.exit(1)
            if ff.read(4) != b"0101":
                print("ERROR: Invalid STS version")
                sys.exit(2)
            t = ff.read(4) # TLKB header
            ff.read(8) # timestamp
            ff.read(8) # Skip 8bytes (??? unknown data. Usualy it's = 00 00 00 00 00 00 00 00)
            t = ff.read(4) # CSED header
            ss = struct.unpack('<15L', ff.read(60)) # 15 uint32. ss[6] and ss[7] store the size of the points. ([6] is what was planned and [7] what was actually recorded)
            # ss[6] should be used to reconstruct the X-axis and ss[7] to read the binary data
            if ff.read(4) != b'ATAD':
                print("ERROR: Data should be here, but aren't. Please debug script")
                sys.exit(3)
            ff.read(4)
            #print(ss)
            data = list(struct.unpack("<%il"%(ss[7]), ff.read(ss[7]*4)))
            # The data are stored as unsigned LONG
            points = self.images[I]['XYScanner']['Points']['value']
            lines = self.images[I]['XYScanner']['Lines']['value']
            if not len(data)%points == 0:
                data.extend(np.ones(points-len(data)%points)*data[-1])
                #add supplemental zeros to make sure the data can be converted to matrix
            image_total = np.array(data).reshape((-1, points))
            image_up = []
            if image_total.shape[0] >= 2*lines:
                for i in range(0, 2*lines, 2):
                    temp = list(image_total[i,:])
                    image_up.append(temp)
                    #get every other line in image_total
                    #since forward and backward data were saved consectively
                    #get only the forward scan up image
            else:
                for i in range(0, image_total.shape[0], 2):
                    temp = list(image_total[i,:])
                    image_up.append(temp)
            image_up = np.array(image_up)
            #image_up = image_up*(6.33*10**(-8))
            image_up = np.flipud(image_up)
            #plt.ion()
            #plt.matshow(image_up)
            #plt.pause(0.1)
            #plt.colorbar()
            #plt.show()
            #plt.pause(3)
            #plt.close()
            return image_up

    def flattenImage(self, Y):
        """
        Flatten STM image using Normal Equation
        Y is the matrix of the image
        """
        #m = 256 #size of the matrix
        #X1, X2 = np.mgrid[:m, :m]
        m1 = Y.shape[0]
        m2 = Y.shape[1]
        X1, X2 = np.mgrid[:m1, :m2]
        X = np.hstack(   ( np.reshape(X1, (m1*m2, 1)) , np.reshape(X2, (m1*m2, 1)) ) )
        X = np.hstack(   ( np.ones((m1*m2, 1)) , X ))
        YY = np.reshape(Y, (m1*m2, 1))

        theta = np.dot(np.dot( np.linalg.pinv(np.dot(X.transpose(), X)), X.transpose()), YY)
        #using normal equation to get the best fit plane
        plane = np.reshape(np.dot(X, theta), (m1, m2))

        Y_sub = Y - plane
        Y_sub = Y_sub - np.amin(Y_sub)
        for i in range(1, Y_sub.shape[0]):
            differences = Y_sub[i,:]-Y_sub[i-1,:]
            Y_sub[i,:] = Y_sub[i,:]-np.median(differences)
        Y_sub = Y_sub - np.amin(Y_sub)
        #plt.ion()
        #plt.matshow(Y_sub)
        #plt.colorbar()
        #plt.pause(0.1)
        #plt.show()
        #plt.pause(3)
        #plt.close()
        #plt.ioff()
        return Y_sub

    def labelTopo(self, Y):
        """
        Differentiate Au from nanoribbon in STM topological images
        topo is the matrix of image
        """
        topo = np.copy(Y)
        height, binedge = np.histogram(topo, 100)
        peak = []
        points = topo.shape[1]
        lines = topo.shape[0]
        for number in range(1, len(height)-1):
            if height[number+1]<height[number] \
               and height[number-1]<height[number] \
               and height[number]>900/(256*256)*points*lines:
                peak.append(binedge[number])
        print(peak)
        plt.plot(height, binedge[:-1])
        plt.xlabel('Count')
        plt.ylabel('Apparent Height')
        plt.show()
        with np.nditer(topo, op_flags=['readwrite']) as matrix:
            for point in matrix:
                if point<peak[0]+700000:
                    point[...] = 1
                elif point>peak[-1]-400000 and point<peak[-1]+400000:
                    point[...] = 2
                else:
                    point[...] = 0
        s = np.ones((3,3), dtype = int)
        labeled_topo, features = label(topo, s)
        print(features)
        plt.matshow(topo)
        plt.colorbar()
        plt.show()

    def findAu(self, Y, ID, num = 1, ext = 'Z'):
        """
        Find area to conduct ZRamp or STS
        topo is the matrix of image
        """
        topo = np.copy(Y)
        height, binedge = np.histogram(topo, 100)
        peak = []
        I = u"%s--%i_%i.%s_mtrx"%(self.IDs[ID]['root'], ID, num, ext)
        width = self.images[I]['XYScanner']['Width']['value']*10**9
        points = topo.shape[1]
        lines = topo.shape[0]
        for number in range(1, len(height)-1):
            if height[number+1]<height[number] \
               and height[number-1]<height[number] \
               and height[number]>900/(256*256)*points*lines:
                peak.append(binedge[number])
        if not peak:
            peak.append(0)

        for j in range(lines):
            for i in range(points):
                peak_index = 0
                area_index = 1
                while peak_index < len(peak):
                    if peak_index > 0:
                        if peak[peak_index] < peak[peak_index - 1] + 700000:
                            peak[peak_index] = peak[peak_index - 1]
                            peak_index += 1
                            continue
                    if topo[j, i] < peak[peak_index] + 700000 \
                       and topo[j, i] > peak[peak_index] - 700000:
                        topo[j, i] = area_index
                        break
                    area_index += 1
                    peak_index += 1
                if not topo[j, i] == int(topo[j, i]):
                    topo[j, i] = 0

##        with np.nditer(topo, op_flags=['readwrite']) as matrix:
##            for point in matrix:
##                peak_index = 0
##                while peak_index < len(peak):
##                    if point < peak[peak_index] + 700000 \
##                       and point > peak[peak_index] - 700000 \
##                       and point > len(peak) + 1:
##                        point[...] = peak_index + 1
##                    peak_index += 1
##                if point > len(peak) + 1:
##                    point[...] = 0

        fivenm = int(5/width*points)
        fifteennm = int(30/width*points)
        s = np.ones((fivenm,fivenm), dtype = int)
        possible_positions = []
        execute_positions = []
        for j in range(lines - fivenm):
            for i in range(points - fivenm):
                marker = topo[j, i]
                if marker == 0:
                    continue
                #peak_index = 0
                #while peak_index < len(peak):
                if np.array_equal(topo[j:j+fivenm, i:i+fivenm], s*marker):
                    possible_positions.append([j+int(fivenm/2), i+int(fivenm/2)])
                    topo[j:j+fivenm, i:i+fivenm] = np.zeros((fivenm,fivenm), dtype = int)
                    #peak_index += 1
        #print(possible_positions)
        for position in possible_positions:
            good_position = True
            s = np.ones((3,3), dtype = int)
            if not execute_positions:
                execute_positions.append(position)
                topo[position[0]:position[0]+3, position[1]:position[1]+3] = s + 0.5
            for new_position in execute_positions:
                distance = math.sqrt((position[0]-new_position[0])**2+(position[1]-new_position[1])**2)
                if distance<fifteennm:
                    good_position = False
                    break
            if good_position:
                execute_positions.append(position)
                topo[position[0]:position[0]+3, position[1]:position[1]+3] = s + 0.5
            else:
                pass
        for execute_position in execute_positions:
            execute_position[0] = lines - execute_position[0]
        #print(execute_positions)
        #plt.ion()
        #plt.matshow(topo)
        #plt.colorbar()
        #plt.pause(0.1)
        #plt.show()
        #plt.pause(3)
        #plt.close()
        #plt.ioff()
        return execute_positions

    def three_point_flatten(self, Y, ID, num = 1, ext = 'Z'):
        """
        Find three points in the gold region and calculate the surface to subtract
        """
        topo = np.copy(Y)
        height, binedge = np.histogram(topo, 100)
        peak = []
        flattened = False
        points = topo.shape[1]
        lines = topo.shape[0]
        I = u"%s--%i_%i.%s_mtrx"%(self.IDs[ID]['root'], ID, num, ext)
        width = self.images[I]['XYScanner']['Width']['value']*10**9
        for number in range(1, len(height)-1):
            if height[number+1]<height[number] \
               and height[number-1]<height[number] \
               and height[number]>900/(256*256)*points*lines:
                peak.append(binedge[number])
                break
        peak.append(binedge[np.argmax(height)])
        if not peak:
            peak.append(0)
        for peakn in peak:
            topo = np.copy(Y)
            with np.nditer(topo, op_flags=['readwrite']) as matrix:
                for point in matrix:
                    if point<peakn+700000 and point>peakn - 700000:
                        point[...] = 1
                    #elif point>peak[-1]-400000 and point<peak[-1]+400000:
                    #    point[...] = 2
                    else:
                        point[...] = 0
            fivenm = int(5/width*points)
            s = np.ones((fivenm,fivenm), dtype = int)
            possible_positions = []
            for j in range(lines - fivenm):
                for i in range(points - fivenm):
                    if np.array_equal(topo[j:j+fivenm, i:i+fivenm], s):
                        possible_positions.append([j+int(fivenm/2), i+int(fivenm/2)])
                        topo[j:j+fivenm, i:i+fivenm] = np.zeros((fivenm,fivenm), dtype = int)
            if len(possible_positions) < 3:
                continue
            p1 = possible_positions[0]
            p1.append(np.mean(Y[p1[0]-int(fivenm/2):p1[0]+int(fivenm/2), p1[1]-int(fivenm/2):p1[1]+int(fivenm/2)]))
            p1 = np.array(p1)
            p2 = possible_positions[-1]
            p2.append(np.mean(Y[p2[0]-int(fivenm/2):p2[0]+int(fivenm/2), p2[1]-int(fivenm/2):p2[1]+int(fivenm/2)]))
            p2 = np.array(p2)
            max_distance = 0
            p3 = []
            for position in possible_positions:
                distance = abs((p2[0]-p1[0])*(p1[1]-position[1])-
                               (p1[0]-position[0])*(p2[1]-p1[1]))/math.sqrt(
                                   (p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
                if distance > max_distance:
                    max_distance = distance
                    p3 = position
                    p3.append(np.mean(Y[p3[0]-int(fivenm/2):p3[0]+int(fivenm/2), p3[1]-int(fivenm/2):p3[1]+int(fivenm/2)]))

            if not p3:
                continue
            p3 = np.array(p3)
            v1 = p3 - p1
            v2 = p2 - p1
            cp = np.cross(v1, v2)
            a, b, c = cp
            d = np.dot(cp, p3)
            plane = np.zeros((lines, points))
            for j in range(lines):
                for i in range(points):
                    try:
                        plane[j, i] = (d - a*j - b*i)/c
                    except OverflowError:
                        continue
            Y_sub = Y - plane
            Y_sub = Y_sub - np.amin(Y_sub)
            flattened = True
            #plt.ion()
            #plt.matshow(Y_sub)
            #plt.colorbar()
            #plt.pause(0.1)
            #plt.show()
            #plt.pause(3)
            #plt.close()
            #plt.ioff()
            return Y_sub
        if not flattened:
            return Y


    def getSTS(self, ID, num=1, ext='I', params=False):
        """
        Get a spectroscopy file xxxx-ID_num.I(V)_mtrx
        """
        IM = self.getSTSparams(ID,num,ext)
        if IM == None:
            return None
        v1 = IM['Spectroscopy']['Device_1_Start']['value'] # Get the start voltage used for the scan
        v2 = IM['Spectroscopy']['Device_1_End']['value'] # Get the end voltage for the scan
        I = u"%s--%i_%i.%s(V)_mtrx"%(self.IDs[ID]['root'], ID, num, ext)
        ImagePath = self.Path+"/"+I
        if not os.path.exists(ImagePath):
            return None
        ff = open(ImagePath, "rb") # read the STS file
        if ff.read(8) != b"ONTMATRX":
            print("ERROR: Invalid STS format")
            sys.exit(1)
        if ff.read(4) != b"0101":
            print("ERROR: Invalid STS version")
            sys.exit(2)
        t = ff.read(4) # TLKB header
        ff.read(8) # timestamp
        ff.read(8) # Skip 8bytes (??? unknown data. Usualy it's = 00 00 00 00 00 00 00 00)
        t = ff.read(4) # CSED header
        ss = struct.unpack('<15L', ff.read(60)) # 15 uint32. ss[6] and ss[7] store the size of the points. ([6] is what was planned and [7] what was actually recorded)
        # ss[6] should be used to reconstruct the X-axis and ss[7] to read the binary data
        if ff.read(4) != b'ATAD':
            print("ERROR: Data should be here, but aren't. Please debug script")
            sys.exit(3)
        ff.read(4)
        data = np.array(struct.unpack("<%il"%(ss[7]), ff.read(ss[7]*4))) # The data are stored as unsigned LONG

        # Reconstruct the x-axis. Take the start and end volatege (v1,v2) with the correct number of points and pad it to the data length. Padding is in 'reflect' mode in the case of Forward/backward scans.
        X = np.linspace(v1, v2, int(IM['Spectroscopy']['Device_1_Points']['value']))
        if len(X) < ss[6]:
            X = np.concatenate((X, X[::-1]))

        if len(data) < len(X):
            data = np.concatenate((data, [np.nan]*(len(X)-len(data))))
        if params:
            return X, data, IM
        return X, data

    def read_value(self):
        """
        Values are stored with a specific header for each data type
        """
        t = self.fp.read(4)
        if t == b"BUOD":
            # double
            v = struct.unpack("<d", self.fp.read(8))[0]
        elif t == b"GNOL":
            # uint32
            v = struct.unpack("<L", self.fp.read(4))[0]
        elif t == b"LOOB":
            # bool32
            v = struct.unpack("<L", self.fp.read(4))[0] > 0
        elif t == b"GRTS":
            v = self.read_string()
        else:
            v = t
        return v

    def getUI(self):
        """
        Read an unsigned int from the file
        """
        return struct.unpack("<L", self.fp.read(4))[0]

    def read_block(self, sub=False):
        indent = self.fp.read(4) # 4bytes forming the header. Those are capital letters between A-Z
        if len(indent) < 4: # EOF reached?
            return False
        bs = struct.unpack("<L", self.fp.read(4))[0]+[8, 0][sub] # Size of the block
        r = {"ID":indent, "bs":bs} # Store the parameters found in the block
        p = self.fp.tell() # store the file position of the block
        if indent == b"DOMP": # Block storing parameters changed during an experiment
            self.fp.read(12)
            inst = self.read_string()
            prop = self.read_string()
            unit = self.read_string()
            self.fp.read(4)
            value =self.read_value()
            r.update({'inst':inst, 'prop':prop, 'unit':unit, 'value':value})
            self.params[inst][prop].update({'unit':unit, 'value':value}) # Update theparameters information stored in self.params
        elif indent == b"CORP": # Processor of scanning window. Useless in this script for the moment
            self.fp.read(12)
            a = self.read_string()
            b = self.read_string()
            r.update({'a':a, 'b':b})
        elif indent == b"FERB": # A file was stored
            self.fp.read(12)
            a = self.read_string() # Filename
            r['filename'] = a
            self.images[a] = copy.deepcopy(self.params) # Store the parameters used to record the file a            se

            # Create a catalogue to avoid to scan all images later
            res = re.search(r'^(.*?)--([0-9]*)_([0-9]*)\.([^_]+)_mtrx$', a)
            ID = int(res.group(2))
            num = int(res.group(3))
            _type = res.group(4)
            if not ID in self.IDs:
                self.IDs[ID] = {'nums':[], 'root':res.group(1), 'hasDI': False, 'hasZ': False}
            if not num in self.IDs[ID]['nums']:
                self.IDs[ID]['nums'].append(num)
            if _type in ["Aux2(V)"]:
                self.IDs[ID]['hasDI'] = True
            if _type in ["Z"]:
                self.IDs[ID]['hasZ'] = True


        elif indent == b"SPXE": # Initial configuration
            self.fp.read(12) # ??? useless 12 bytes
            r['LNEG'] = self.read_block(True)  # read subblock
            r['TSNI'] = self.read_block(True)  # read subblock
            r['SXNC'] = self.read_block(True)  # read subblock
        elif indent == b"LNEG":
            r.update({'a':self.read_string(), 'b':self.read_string(), 'c':self.read_string()})
        elif indent == b"TSNI":
            anz = self.getUI()
            rr = []
            for ai in range(anz):
                a = self.read_string()
                b = self.read_string()
                c = self.read_string()
                count = self.getUI()
                pa = []
                for i in range(count):
                    x = self.read_string()
                    y = self.read_string()
                    pa.append({'a':x, 'b':y})
                rr.append({'a':a, 'b':b, 'c':c, 'content':pa})
        elif indent == b"SXNC":
            count = self.getUI()
            r['count'] = count
            rr = []
            for i in range(count):
                a = self.read_string()
                b = self.read_string()
                k = self.getUI()
                kk = []
                for j in range(k):
                    x = self.read_string()
                    y = self.read_string()
                    kk.append((x, y))
                rr.append((a, b, i, kk))
            r['content'] = rr
        elif indent == b"APEE": # Store the configurations
            self.fp.read(12) # ??? useless 12bytes
            num = self.getUI() # Number of parameters class
            r['num'] = num
            for i in range(num):
                inst = self.read_string() # Parameter class name
                grp = self.getUI() # Number of parameters in this class
                kk = {}
                for j in range(grp): # Scan for each parameter, value and unit
                    prop = self.read_string() # parameter name
                    unit = self.read_string() # parameter unit
                    self.fp.read(4) # ???
                    value = self.read_value() # parameter value
                    kk[prop] = {"unit":unit, "value":value}
                r[inst] = kk
            self.params = r # Store this information as initial values for the parmeters
           # print(self.params['Spectroscopy'])
        self.fp.seek(p) # go back to the beginning of the block
        self.fp.read(bs) # go to the next block by skiping the block-size bytes
        return r # return the informations collected
