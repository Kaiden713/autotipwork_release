"""
Module: open_last

Author: Shenkai Wang, Junmian Zhu, Raymond Blackwell, and Felix R. Fischer

Description: Open and process the last collected topographic image and STS spectrum

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

from Matrix import Matrix
import os
import matplotlib.pyplot as plt


def open_last_sts(data_path, head):
    #here data_path should be the Lucile folder
    mtrx_path = data_path
    head = head + "_0001.mtrx"
    my_matrix = Matrix(mtrx_path, head)
    #here mtrx_path should be the folder with the head file
    keys = list(my_matrix.IDs.keys())
    last_ID = keys[-1]
    while last_ID:
        if not last_ID in my_matrix.IDs.keys():
            last_ID -= 1
            continue
        if my_matrix.IDs[last_ID]['hasDI']:
            last_num = my_matrix.IDs[last_ID]['nums'][-1]
            while last_num:
                try:
                    V, didv = my_matrix.getDIDV(last_ID, last_num)
                    break
                except TypeError:
                    last_num -= 1
            #plt.ion()
            #plt.plot(V, didv)
            #plt.pause(0.1)
            #plt.show()
            #plt.pause(3)
            #plt.close()
            #plt.ioff()
            return V, didv
            break
        else:
            last_ID -= 1
    return None, None

def analyse_last_topo(data_path, head):
    mtrx_path = data_path
    head = head + "_0001.mtrx"
    my_matrix = Matrix(mtrx_path, head)
    keys = list(my_matrix.IDs.keys())
    keys.sort()
    last_ID = keys[-1]
    while last_ID:
        if not last_ID in my_matrix.IDs.keys():
            last_ID -= 1
            continue
        if my_matrix.IDs[last_ID]['hasZ']:
            last_num = my_matrix.IDs[last_ID]['nums'][-1]
            while last_num:
                try:
                    image = my_matrix.openTopo(last_ID, last_num)
                    image = my_matrix.flattenImage(image)
                    image = my_matrix.three_point_flatten(image, last_ID, last_num)
                    execute_positions = my_matrix.findAu(image, last_ID, last_num)
                    return execute_positions
                    break
                except TypeError:
                    last_num -= 1
            break
        else:
            last_ID -= 1

def convert_execute_positions(execute_positions, points, lines):
    for execute_position in execute_positions:
        execute_position[0] = (execute_position[0]-lines/2)*2/lines
        execute_position[1] = (execute_position[1]-points/2)*2/points
        temp = execute_position[0]
        execute_position[0] = execute_position[1]
        execute_position[1] = temp
    #print(execute_positions)
    return execute_positions



"""

Junmian Modified: Change the directory

"""
#path = 'D:/LUCILE_rawdata/Dropbox/LUCILE_rawdata'
#execute_positions = analyse_last_topo('D:/LUCILE_rawdata/Dropbox/LUCILE_rawdata',
#                                      'Au_Pos3--STM_Spectroscopy')

#execute_positions = analyse_last_topo('D:/LUCILE_rawdata/Dropbox/LUCILE_rawdata',
#                                     'Clean_Au(111)_Pos2--STM_Spectroscopy')
#execute_positions = convert_execute_positions(execute_positions, 256, 256)
#print(execute_positions)
