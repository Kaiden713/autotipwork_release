"""

Module: auto_tipwork

Author: Shenkai Wang, Junmian Zhu, Raymond Blackwell, and Felix R. Fischer

Description: Main Function for Autotipwork. This Function can be Run from here or the UI

UC Berkeley's Copyright and Disclaimer Notice

Copyright ©2021. The Regents of the University of California (Regents). All Rights Reserved.
Permission to use, copy, modify, and distribute this software and its documentation for
educational, research, and not-for-profit purposes, without fee and without a signed licensing agreement,
is hereby granted, provided that the above copyright notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue, Suite 510, Berkeley, CA 94720-1620,
(510) 643-7201, otl@berkeley.edu, http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

"""

from STM import STM
import time
import datetime
import os.path
from open_last import open_last_sts, analyse_last_topo, convert_execute_positions
from normalize import normalize
import sklearn
import joblib
import numpy as np
import matplotlib.pyplot as plt
import sys

def operate(operation, record_file):
    """
    Record each operation in the record_file for reference.
    """
    operation_time = str(datetime.datetime.now().time())
    print(operation_time)
    print(operation)
    with open(record_file, 'a') as file:
        file.write(operation_time + '\n' + operation + '\n')

def is_digit(n):
    """
    Check whether a string is a digit (including negative number)
    """
    try:
        int(n)
        return True
    except ValueError:
        return  False

def autotipwork(start_x = -800, start_y = 800):
    """
    Autotipwork main operation function
    """
    
    ml_model = joblib.load('ml_model_ada.pkl')

    # Create a new record file based on today's date
    record_file_path = './operation_record'
    today = datetime.date.today()
    record_file_name = record_file_path + '/' + str(today) + '.txt'
    if not os.path.isfile(record_file_name):
        with open(record_file_name, 'w') as file:
            pass

    my_stm = STM()
    operate(my_stm.init(), record_file_name)
    positions = []
    head = my_stm.get_head_file()
    rawdata_path = my_stm.get_file_path()
    print(head, rawdata_path)
    # Generate a list of scan window positions
    if not start_y%100 == 0:
        if start_y > 0:
            start_y = int(start_y/100)*100
        else:
            start_y = (int(start_y/100)-1)*100

    if (start_y/100)%2 == 0:
        if not start_x%100 == 0:
            if start_x > 0:
                start_x = (int(start_x/100)+1)*100
            else:
                start_x = int(start_x/100)*100

        for x in range(start_x, 800+100, 100):
            positions.append([x, start_y])

    else:
        if not start_x%100 == 0:
            if start_x > 0:
                start_x = int(start_x/100)*100
            else:
                start_x = (int(start_x/100)-1)*100
        for x in range(start_x, -800-100, -100):
            positions.append([x, start_y])

    for y in range(start_y-100, -800-100, -100):
        if (y/100)%2 == 0:
            for x in range(-800, 800+100, 100):
                positions.append([x, y])
        else:
            for x in range(800, -800-100, -100):
                positions.append([x, y])

    #print(positions)
    operate(my_stm.set_xy_offset(positions[0][0], positions[0][1]), record_file_name)
    time.sleep(10)
    last_spectra_good = False
    for position in positions:
        operate(my_stm.set_xy_offset(position[0], position[1]), record_file_name)
        time.sleep(10)
        operate(my_stm.start(), record_file_name)
        operate(my_stm.monitor_zout(), record_file_name)
        #operate(my_stm.monitor_zout_origin(), record_file_name)
        operate(my_stm.stop(), record_file_name)
        time.sleep(1)
        #execute_positions = analyse_last_topo('D:/LUCILE_rawdata/Dropbox/LUCILE_rawdata', head)
        execute_positions = analyse_last_topo(rawdata_path, head)

        points, lines = my_stm.get_points_lines()
        execute_positions = convert_execute_positions(execute_positions, points, lines)
        print(execute_positions)
        for execute_position in execute_positions:
            operate(my_stm.set_execute_port_colour(), record_file_name)
            operate(my_stm.enable_VExt(), record_file_name)
            operate(my_stm.set_target_position(execute_position[0], execute_position[1]), record_file_name)
            operate(my_stm.save_aux2v(False), record_file_name)
            operate(my_stm.move_tip(), record_file_name)
            time.sleep(120)
            operate(my_stm.save_aux2v(True), record_file_name)
            operate(my_stm.move_tip(), record_file_name)
            time.sleep(120)
            operate(my_stm.disable_VExt(), record_file_name)
            V, didv = open_last_sts(rawdata_path, head)
            V, didv, sf = normalize(V, didv)
            didv = np.reshape(didv, (1,-1))
            #result = ml_model.predict(didv)
            # WARNING: threshold is tuned for each model. Must change when change model.
            model_threshold = 0.5
            result = ml_model.decision_function(didv) >= model_threshold
            print(result)
            if result[0]:
                if last_spectra_good:
                    time.sleep(5)
                    #operate(my_stm.pull_tip_back(), record_file_name)
                    operate("Usable Tip Obtained", record_file_name)
                    operate(my_stm.rundown(), record_file_name)
                    sys.exit(0)
                else:
                    last_spectra_good = True
                    continue
            else:
                last_spectra_good = False
                operate(my_stm.disable_VExt(), record_file_name)
                operate(my_stm.set_zramp(), record_file_name)
                operate(my_stm.move_tip(), record_file_name)
                time.sleep(20)
    operate(my_stm.rundown(), record_file_name)

if __name__ == "__main__":
    start_x_offset = -800
    start_y_offset = 800
    while True:
        print("Start X, Y offsets must be integers between -800 to 800")
        try:
            start_x_offset = int(input("Please input start X offset: "))
            start_y_offset = int(input("Please input start Y offset: "))
            if start_x_offset<=800 and\
               start_x_offset>=-800 and\
               start_y_offset<=800 and\
               start_y_offset>=-800:
                break
        except ValueError:
            continue
    autotipwork(start_x_offset, start_y_offset)








































