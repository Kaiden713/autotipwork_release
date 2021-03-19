"""

Module: STM.py

Author: Shenkai Wang, Junmian Zhu and Raymond Blackwell started this project
        on Oct. 2019.

Description: Contains an entire class for the operation on STM.



Change:
1. Shenkai Wang last edited on 11/26/2019


WARNING:
#If you want to add any function, try to program in the Script Manager first to made sure it works
#If parameters are of the wrong type or with out of range values, matrix will crash and you have to
#restart the whole unit
#I would recommend adding new functions instead of changing existing ones

#Include comments for any change!!!
"""

from ctypes import *
import time
import datetime
import numpy as np


class STM:
    """
    Operate Omicron STM through RemoteAccess_API
    """

    def __init__(self):
        #path to RemoteAccess_API.dll
        #self.remotepath = r"C:\Program Files (x86)\Omicron NanoScience\MATRIX\V3.2\SDK\RemoteAccess\RemoteAccess_API.dll"
        self.remotepath = r"C:\Program Files (x86)\Scienta Omicron\MATRIX\V3.3.1\SDK\RemoteAccess\RemoteAccess_API.dll"
        #matrix installation path
        #self.installpath = c_char_p(b'C:\\Program Files (x86)\\Omicron NanoScience\\MATRIX\\V3.2')
        self.installpath = c_char_p(b'C:\Program Files (x86)\Scienta Omicron\MATRIX\V3.3.1')
        #open RemoteAccess_API.dll using CDLL function in ctypes package
        self.matrix_lib = CDLL(self.remotepath)

    def init(self):
        """
        Initialize the connection to Matrix
        """
        #call the init function in RemoteAccess_API.dll
        #make sure Matrix is open and Experiment is open
        rc = self.matrix_lib.init(self.installpath)
        #rc should equals to 1 if connection established
        if rc == 1:
            return "Successfully connected to Matrix"
        else:
            return "Connection failed. Please make sure matrix is open"

    def rundown(self):
        rc = self.matrix_lib.rundown()
        if rc == 1:
            return "Disconnected from Matrix"
        else:
            return "Something when wrong. This should never happen"

    def start_origin(self):
        """
        Starts scanning. Same result as clicking the start button
        """
        #matrix intrinsic function
        #check MATE Help for more information
        start_exp = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.start')
        #preturn gets the value returned from the matrix intrinsic function
        #no value returned from the start function
        #check MATE Help for more information
        preturn = c_uint(0)
        #argcount indicates the amount of argument the matrix intrinsic function uses
        #start does not take any argument
        argcount = c_uint(0)
        #uses the callFunction function in RemoteAccess_API.dll
        started = self.matrix_lib.callFunction(start_exp, preturn, argcount)
        #started should equals to 1 if Matrix successfully started scanning
        if started == 1:
            return "Started scanning..."
        else:
            return "Can't start scanning. Please check connection"

    def start(self):
        """
        Starts scanning. Same result as clicking the start button
        """
        #the following steps are to initialize numpy linear regression so that
        #it won't take too long in the monitor_zout function
        line_scan = []
        count = 0
        x = np.linspace(1, 256, 256)
        for i in range(256):
            count += 2
            line_scan.append(count)
            time.sleep(0.002)
        line_scan = np.array(line_scan)
        para = np.polyfit(x, line_scan, 1)
        fx = np.poly1d(para)
        fit_line = fx(x)
        line_scan = line_scan - fit_line
        #matrix intrinsic function
        #check MATE Help for more information
        start_exp = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.start')
        #preturn gets the value returned from the matrix intrinsic function
        #no value returned from the start function
        #check MATE Help for more information
        preturn = c_uint(0)
        #argcount indicates the amount of argument the matrix intrinsic function uses
        #start does not take any argument
        argcount = c_uint(0)
        #uses the callFunction function in RemoteAccess_API.dll
        started = self.matrix_lib.callFunction(start_exp, preturn, argcount)
        #started should equals to 1 if Matrix successfully started scanning
        if started == 1:
            return "Started scanning..."
        else:
            return "Can't start scanning. Please check connection"

    def stop(self):
        """
        Stops scanning. Same result as clicking the stop button
        """
        #matrix intrinsic function
        #check the comments for start
        stop_exp = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.stop')
        preturn = c_uint(0)
        argcount = c_uint(0)
        stopped = self.matrix_lib.callFunction(stop_exp, preturn, argcount)
        #stopped should equals to 1 if Matrix successfully stopped scanning
        if stopped == 1:
            return "Stopped Scanning"
        else:
            return "Can't stop scanning. Please check connection"

    def pause(self):
        """
        Pauses scanning. Same result as clicking the pause button
        """
        #matrix intrinsic function
        #check the comments for start
        pause_exp = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.pause')
        preturn = c_uint(0)
        argcount = c_uint(0)
        paused = self.matrix_lib.callFunction(pause_exp, preturn, argcount)
        #paused should equals to 1 if Matrix successfully paused scanning
        if paused == 1:
            return "Paused scanning"
        else:
            return "Can't pause scanning. Please check connection"

    def resume(self):
        """
        Resumes scanning after paused.
        Same result as clicking the start button after scanning has been paused
        """
        #matrix intrinsic function
        #check the comments for start
        resume_exp = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.resume')
        preturn = c_uint(0)
        argcount = c_uint(0)
        resumed = self.matrix_lib.callFunction(resume_exp, preturn, argcount)
        #paused should equals to 1 if Matrix successfully paused scanning
        if resumed == 1:
            return "Resume Scanning..."
        else:
            return "Can't resume scanning. Please check connection"

    def restart(self):
        """
        Restarts scanning.
        Same effect as clicking the restart button.
        """
        #matrix intrinsic function
        #check the comments for start
        restart_exp = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.restart')
        preturn = c_uint(0)
        argcount = c_uint(0)
        restarted = self.matrix_lib.callFunction(restart_exp, preturn, argcount)
        #paused should equals to 1 if Matrix successfully paused scanning
        if restarted == 1:
            return "Restarted Scanning..."
        else:
            return "Can't restart scanning. Please check connection"

    def enable_VExt(self):
        """
        Enable V-Ext. Same effect as checking the V-Ext box
        """
        #By changing the VGap_Select value you can toggle the V-Ext on the off at your will
        #The Modulation_VExt_T1T2 value under Spectroscopy catagory only works during the acquisition of dI/dV
        vgap_select = c_char_p(b'STM_Spectroscopy::STMSCBService.VGap_Select')
        #index value determines the element index if the property is of array type
        #and must be set to '-1' if the property referred to is not an array
        index = c_uint(-1)
        #the value here is a boolean in c type
        value = c_bool(True)
        #call the setBooleanProperty function from the dll
        enabled = self.matrix_lib.setBooleanProperty(vgap_select, index, value)
        #enabled should equals to 1 if operation succeeded
        if enabled == 1:
            return "V-Ext has been turned on"
        else:
            return "Can't turn on V-Ext. Please check connection"

    def disable_VExt(self):
        """
        Disable V-Ext. Same effect as unchecking the V-Ext box
        """
        #see comments for enable_VExt
        vgap_select = c_char_p(b'STM_Spectroscopy::STMSCBService.VGap_Select')
        index = c_uint(-1)
        value = c_bool(False)
        disabled = self.matrix_lib.setBooleanProperty(vgap_select, index, value)
        if disabled == 1:
            return "V-Ext has been turned off"
        else:
            return "Can't turn off V-Ext. Please check connection"

    def set_target_position(self, positionx = 0, positiony = 0):
        """
        Set the target position for tip relocation
        """
        #positionx and positiony must be doubles between -1 to 1
        #otherwise you can set target_position but matrix will
        #crash when you move
        if positionx < -1 or positionx > 1 or positiony < -1 or positiony > 1:
            return "x and y position must be floats between -1 and 1."
        target_position = c_char_p(b'STM_Spectroscopy::XYScanner.Target_Position')
        #Target_Position is an array with two items so you need to set the two
        #values separately
        x_index = c_uint(0)
        y_index = c_uint(1)
        valuex = c_double(positionx)
        valuey = c_double(positiony)
        #there's a setDoubleArrayProperty function
        #but it's harder to use with python
        rcx = self.matrix_lib.setDoubleProperty(target_position, x_index, valuex)
        rcy = self.matrix_lib.setDoubleProperty(target_position, y_index, valuey)
        if rcx == 1 and rcy == 1:
            return f"Successfully set x, y position to {positionx}, {positiony}"
        else:
            return "Setting failed. Please check connection"

    def move_tip(self):
        """
        Move the STM tip to target position and execute the current port colour
        """
        #if Trigger_Execute_At_Target_Position is set to true
        #it will execute the Execute_Port_Colour
        xy_move = c_char_p(b'STM_Spectroscopy::XYScanner.move')
        trigger_execute = c_char_p(b'STM_Spectroscopy::XYScanner.Trigger_Execute_At_Target_Position')
        store_current_position = c_char_p(b'STM_Spectroscopy::XYScanner.Store_Current_Position')
        return_to_stored_position = c_char_p(b'STM_Spectroscopy::XYScanner.Return_To_Stored_Position')
        index = c_uint(-1)
        value = c_bool(True)
        preturn = c_uint(0)
        argcount = c_uint(0)
        triggered = self.matrix_lib.setBooleanProperty(trigger_execute, index, value)
        stored = self.matrix_lib.setBooleanProperty(store_current_position, index, value)
        returned = self.matrix_lib.setBooleanProperty(return_to_stored_position, index, value)
        moved = self.matrix_lib.callFunction(xy_move, preturn, argcount)
        if moved == 1:
            return "Tip relocated to target position"
        else:
            return "Tip relocation failed. Please check connection"

    def set_execute_port_colour(self, colour = b''):
        """
        Set the Execute_Port_Colour to colour
        """
        #if colour is empty stm will do spectroscopy by defult
        execute_port_colour = c_char_p(b'STM_Spectroscopy::XYScanner.Execute_Port_Colour')
        index = c_uint(-1)
        value = c_char_p(colour)
        setted = self.matrix_lib.setStringProperty(execute_port_colour, index, value)
        if setted == 1:
            return f"Execute_Port_Colour has been set to {colour}"

    def set_zramp(self):
        """
        Set the Execute_Port_Colour to ZRamp
        """
        zramp_setted = self.set_execute_port_colour(b'ZRamp')
        return zramp_setted

    def set_xy_offset(self, xoffset, yoffset):
        """
        Set the center of the scan window to xoffset, yoffset
        """
        x_offset = c_char_p(b'STM_Spectroscopy::XYScanner.X_Offset')
        y_offset = c_char_p(b'STM_Spectroscopy::XYScanner.Y_Offset')
        index = c_uint(-1)
        #x, y offsets must have a unit of nm
        xvalue = c_double(xoffset*(10**(-9)))
        yvalue = c_double(yoffset*(10**(-9)))
        rcx = self.matrix_lib.setDoubleProperty(x_offset, index, xvalue)
        rcy = self.matrix_lib.setDoubleProperty(y_offset, index, yvalue)
        if rcx == 1 and rcy == 1:
            return f"Successfully set x, y offset to {xoffset}, {yoffset}"
        else:
            return "Setting x, y offset failed. Please check connection"

    def get_xy_offset(self):
        """
        Set the center of the scan window to xoffset, yoffset
        """
        x_offset = c_char_p(b'STM_Spectroscopy::XYScanner.X_Offset')
        y_offset = c_char_p(b'STM_Spectroscopy::XYScanner.Y_Offset')
        index = c_uint(-1)
        #x, y offsets must have a unit of nm
        xvalue = c_double()
        yvalue = c_double()
        rcx = self.matrix_lib.getDoubleProperty(x_offset, index, byref(xvalue))
        rcy = self.matrix_lib.getDoubleProperty(y_offset, index, byref(yvalue))
        if rcx == 1 and rcy == 1:
            return xvalue.value*(10**9), yvalue.value*(10**9)
        else:
            return "Getting x, y offset failed. Please check connection"

    def scan_time(self):
        """
        Calculate the time needed to finish scanning 1 up image
        """
        raster_time = c_char_p(b'STM_Spectroscopy::XYScanner.Raster_Time')
        index = c_uint(-1)
        raster_time_value = c_double()
        #raster time has a unit of second
        rc = self.matrix_lib.getDoubleProperty(raster_time, index, byref(raster_time_value))
        xy_points = c_char_p(b'STM_Spectroscopy::XYScanner.Points')
        points = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_points, index, byref(points))
        xy_lines = c_char_p(b'STM_Spectroscopy::XYScanner.Lines')
        lines = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_lines, index, byref(lines))
        scan_time = points.value*(lines.value+1)*2*raster_time_value.value
        return scan_time

    def get_points_lines(self):
        """
        Get the current XYScanner Points and Lines
        """
        xy_points = c_char_p(b'STM_Spectroscopy::XYScanner.Points')
        index = c_uint(-1)
        points = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_points, index, byref(points))
        xy_lines = c_char_p(b'STM_Spectroscopy::XYScanner.Lines')
        lines = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_lines, index, byref(lines))
        return points.value, lines.value

    def turn_on_feedback_loop(self, turnon):
        """
        Turn on or turn off feedback loop
        turnon is a boolean
        """
        feedback_loop = c_char_p(b'STM_Spectroscopy::Regulator.Feedback_Loop_Enabled')
        index = c_uint(-1)
        value = c_bool(turnon)
        enabled = self.matrix_lib.setBooleanProperty(feedback_loop, index, value)
        return enabled

    def get_zout(self):
        """
        Get current Z position
        """
        z_out = c_char_p(b'STM_Spectroscopy::Regulator.Z_Out')
        index = c_uint(-1)
        zout = c_double()
        get_zout = self.matrix_lib.getDoubleProperty(z_out, index, byref(zout))
        if get_zout == 1:
            return zout.value*(10**9)
        else:
            print(f'Getting Z_Out failed with return value {get_zout}')

    def pull_tip_back(self, zoffset = 0):
        """
        Pull tip back several nanometers.
        zoffset must be an integer between 0 to 200
        If no zoffset input, pull tip back to +130 nm (Almost fully retract)
        """
        z_offset = c_char_p(b'STM_Spectroscopy::Regulator.Z_Offset')
        slew_rate = c_char_p(b'STM_Spectroscopy::Regulator.Z_Offset_Slew_Rate')
        index = c_uint(-1)
        if zoffset == 0:
            current_position = self.get_zout()
            zoffset = 130 - current_position
            if zoffset > 0:
                zvalue = c_double(zoffset*(10**(-9)))
            else:
                #tip is retracted or crashed
                zvalue = c_double(0)
        else:
            zvalue = c_double(zoffset*(10**(-9)))
        if not zvalue.value == 0:
            turnedon = self.turn_on_feedback_loop(True)
            #set zoffset slew rate to 10 nm/s just in case
            srvalue = c_double(100*(10**(-9)))
            rcz = self.matrix_lib.setDoubleProperty(z_offset, index, zvalue)
            rcsr = self.matrix_lib.setDoubleProperty(slew_rate, index, srvalue)
            time.sleep(1)
            turnedoff = self.turn_on_feedback_loop(False)
            time.sleep(2)
            current_position = self.get_zout()
            if rcz == 1 and turnedoff == 1:
                return f"Successfully pulled tip back to {current_position} nm"
            else:
                return f"Setting Z_Offset failed with return value {rcz}"
        else:
            return "Z_Offset is 0. The tip is fully retracted."

    def get_head_file(self):
        """
        Get Result_File_Name used by current experiment.
        Result_File_Name + "_0001.mtrx" is the head file for Matrix class in
        sw_pyOmicron
        """
        result_file_name = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.Result_File_Name')
        index = c_uint(-1)
        buffer_size = c_uint(100)
        head = create_string_buffer(b'', 100)
        got_head = self.matrix_lib.getStringProperty(result_file_name, index, buffer_size, byref(head))
        if got_head == 1:
            #returned string is in binary
            return head.value.decode('ascii')

    def get_file_path(self):
        """
        Get the current directory to data files.
        """
        result_file_path = c_char_p(b'STM_Spectroscopy::STM_Spectroscopy.Result_File_Path')
        index = c_uint(-1)
        buffer_size = c_uint(100)
        path = create_string_buffer(b'', 100)
        got_path = self.matrix_lib.getStringProperty(result_file_path, index, buffer_size, byref(path))
        if got_path == 1:
            #returned string is in binary
            return path.value.decode('ascii')

    def save_aux2v(self, switch):
        """
        Change Enable_Storing for Aux2(V) to True
        Same effect as checking the box on Channel List
        """
        aux2v = c_char_p(b'STM_Spectroscopy::Aux2_V.Enable_Storing')
        index = c_uint(-1)
        value = c_bool(switch)
        rc = self.matrix_lib.setBooleanProperty(aux2v, index, value)
        if rc == 1:
            return f"Aux2(V) will be saved: {switch}"
        else:
            return rc

    def monitor_zout_origin(self):
        """
        Get the value of z_out at every point and compare it with
        the start value of that line
        if z_out is 1 nm higher than the start value stop scanning
        """
        raster_time = c_char_p(b'STM_Spectroscopy::XYScanner.Raster_Time')
        index = c_uint(-1)
        raster_time_value = c_double()
        #raster time has a unit of second
        rc = self.matrix_lib.getDoubleProperty(raster_time, index, byref(raster_time_value))
        xy_points = c_char_p(b'STM_Spectroscopy::XYScanner.Points')
        points = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_points, index, byref(points))
        xy_lines = c_char_p(b'STM_Spectroscopy::XYScanner.Lines')
        lines = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_lines, index, byref(lines))
        stopped = ''
        for line in range(lines.value):
            t0 = time.time()
            start_value = self.get_zout()
            for point in range(points.value):
                #time.sleep(raster_time_value.value - 0.0009)
                zout = self.get_zout()
                #print(zout)
                if zout > (start_value + 1.2) or zout < (start_value - 1.2):
                    print(start_value)
                    print(zout)
                    stopped = self.stop()
                    break
            if stopped:
                break
            time.sleep(2*points.value*raster_time_value.value - (time.time() - t0))
            #print(2*points.value*raster_time_value.value - (time.time() - t0))
        if stopped:
            return "Bad area. Stopped scanning"
        else:
            return "Area doesn't have big protrutions"

    def monitor_zout(self):
        """
        Get the value of z_out at every point and compare it with
        the start value of that line
        if z_out is 1 nm higher than the start value stop scanning
        """
        raster_time = c_char_p(b'STM_Spectroscopy::XYScanner.Raster_Time')
        index = c_uint(-1)
        raster_time_value = c_double()
        #raster time has a unit of second
        rc = self.matrix_lib.getDoubleProperty(raster_time, index, byref(raster_time_value))
        xy_points = c_char_p(b'STM_Spectroscopy::XYScanner.Points')
        points = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_points, index, byref(points))
        xy_lines = c_char_p(b'STM_Spectroscopy::XYScanner.Lines')
        lines = c_uint()
        rc = self.matrix_lib.getIntegerProperty(xy_lines, index, byref(lines))
        stopped = ''
        x = np.linspace(1, points.value, points.value)
        #print(raster_time_value.value)
        #print(lines.value)
        for line in range(lines.value):
            t0 = time.time()
            line_scan = []
            for point in range(points.value):
                zout = self.get_zout()
                line_scan.append(zout)
                #time.sleep(raster_time_value.value - 0.0009)
                # Replace sleep
                my_sleep(raster_time_value.value - 0.0009)
            #print(time.time() - t0)
            line_scan = np.array(line_scan)
            #print(line_scan)
            para = np.polyfit(x, line_scan, 1)
            ##x_b = np.c_[np.ones((256, 1)), x_r]
            ##para = np.linalg.inv(x_b.T.dot(x_b)).dot(x_b.T).dot(line_scan)
            ##para = para.flatten()
            fx = np.poly1d(para)
            fit_line = fx(x)
            line_scan = line_scan - fit_line
            if np.amax(line_scan) - np.amin(line_scan) > 1:
                stopped = self.stop()
                break
            elif np.amax(line_scan) - np.amin(line_scan) < 0.005:
                np.savetxt("wrong_line_scan.txt", line_scan)
                np.savetxt("fit_line.txt", fit_line)
                stopped = self.stop()
                return "Scanning is manually stopped, or tip is crushed or not in tunneling"
            #try:
                #print(points.value, raster_time_value.value, time.time() - t0)
                #time.sleep(2*points.value*raster_time_value.value - (time.time() - t0))
            my_sleep( 2*points.value*raster_time_value.value - (time.time() - t0) )
            #except ValueError:
            #    pass
        if stopped:
            return "Bad area. Stopped scanning"
        else:
            return "Area doesn't have big protrutions"

    def get_gapvoltage(self):
        """ Get the V-Gap (Gap Voltage) value as shown in the Z-Regulation Window

        """
        gap_v = c_char_p(b'STM_Spectroscopy::GapVoltageControl.Voltage')
        index = c_uint(-1)
        #x, y offsets must have a unit of nm
        v_value= c_double()
        rcx = self.matrix_lib.getDoubleProperty(gap_v, index, byref(v_value))

        if rcx == 1 :
            return v_value.value
        else:
            return "Getting Gap Voltage Failed"


    def set_gapvoltage(self, gap_value):
        """ Set the V-Gap (Gap Voltage) value as shown in the Z-Regulation Window

        """
        gap_v = c_char_p(b'STM_Spectroscopy::GapVoltageControl.Voltage')
        index = c_uint(-1)
        #x, y offsets must have a unit of nm
        v_value= c_double(gap_value)
        rcx = self.matrix_lib.setDoubleProperty(gap_v, index, v_value)

        if rcx == 1 :
            return f"Successfully set Gap Voltage to {gap_value} V"
        else:
            return "Setting Gap Voltage failed. Please check connection."

    def control_z_offset_slew_rate(self, on):
        """ Control the Z-OffSet slew rate setting.

            Args:
                on (bool): whether to enable the Z-offset slew rate setting.

        """

        enable_slew_rate = c_char_p(b'STM_Spectroscopy::Regulator.Enable_Z_Offset_Slew_Rate')
        #index value determines the element index if the property is of array type
        #and must be set to '-1' if the property referred to is not an array
        index = c_uint(-1)
        #the value here is a boolean in c type
        value = c_bool(on)
        #call the setBooleanProperty function from the dll
        enabled = self.matrix_lib.setBooleanProperty(enable_slew_rate, index, value)
        #enabled should equals to 1 if operation succeeded
        if enabled == 1:
            return "Set the Z-Offset Slew Rate to be " + str(on)
        else:
            return "Can't change Z-Offset Slew Rate. Please check connection"

    def get_z_offset_slew_rate(self):
        """ Get the Z-Offset Slew Rate in nm/s
        """
        y_offset = c_char_p(b'STM_Spectroscopy::Regulator.Z_Offset_Slew_Rate')
        index = c_uint(-1)
        yvalue = c_double()
        rcx = self.matrix_lib.getDoubleProperty(y_offset, index, byref(yvalue))
        if rcx == 1:
            return yvalue.value*(10**9)
            #return xvalue.value*(10**9), yvalue.value*(10**9)
        else:
            return "Getting Z Offset Slew Rate failed. Please check connection"


    def set_z_offset_slew_rate(self, slew_rate):
        """ Set the Z-offset Slew Rate in unis of nm/s

        """
        if slew_rate >= 1*(10**-3) or slew_rate < 0.5*(10**-5):
            return "Slew Rate is too large or too small"
        y_offset = c_char_p(b'STM_Spectroscopy::Regulator.Z_Offset_Slew_Rate')
        index = c_uint(-1)
        value = c_double(slew_rate * (10**-9))   # Convert to m/s
        rcx = self.matrix_lib.setDoubleProperty(y_offset, index, value)
        if rcx == 1:
            return "Set the Z-Offset Slew Rate to be " + str(slew_rate)
        else:
            return "Change Z Offset Slew Rate failed. Please check connection."

    def get_scan_constraint(self):
        y_offset = c_char_p(b'STM_Spectroscopy::XYScanner.Scan_Constraint')
        index = c_uint(-1)
        yvalue = c_int()
        #head = create_string_buffer(b'', 100)

        #buffer_size = c_uint(10)
        #path = create_string_buffer(b'', 10)
        rcx = self.matrix_lib.getEnumProperty(y_offset, index, byref(yvalue))

        #rcx = self.matrix_lib.getDoubleProperty(y_offset, index, byref(yvalue))
        if rcx == 1:
            return yvalue.value
            #return xvalue.value*(10**9), yvalue.value*(10**9)
        else:
            return "Getting Scan Constraint Failed. Please check connection"

    def set_scan_constraint(self, cons):
        if (cons != 0 and cons != 1) and (cons != 2):
            return "Wrong Scan Constraint Enum, should only be 0(None), 1(Point) or 2(Line)"

        y_offset = c_char_p(b'STM_Spectroscopy::XYScanner.Scan_Constraint')
        index = c_uint(-1)
        yvalue = c_int(cons)
        #head = create_string_buffer(b'', 100)

        #buffer_size = c_uint(10)
        #path = create_string_buffer(b'', 10)
        rcx = self.matrix_lib.setEnumProperty(y_offset, index, yvalue)

        #rcx = self.matrix_lib.getDoubleProperty(y_offset, index, byref(yvalue))
        if rcx == 1:
            return "Set Scan Constraint to be "  + str(cons)
            #return xvalue.value*(10**9), yvalue.value*(10**9)
        else:
            return "Getting Scan Constraint Failed. Please check connection"


def my_sleep(time_s):
    timeout_tmp = time.time() + time_s
    while True:
        if time.time() > timeout_tmp:
            break
