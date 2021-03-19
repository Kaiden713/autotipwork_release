#Shenkai Wang, Junmian Zhu, and Raymond Blackwell started this project in Oct. 2019

#Shenkai Wang last edited on 11/26/2019

#I would recommend adding new functions instead of changing existing ones

#Include comments for any change!!!

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
