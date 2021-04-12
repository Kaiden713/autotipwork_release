"""
Module: normalize

Author: Shenkai Wang, Junmian Zhu, Raymond Blackwell, and Felix R. Fischer

Description: Normalize the STS spectrum for machine learning model

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

import pickle
import numpy as np
import matplotlib.pyplot as plt
import math

def didv_for_voltage(v_data, didv_data, voltage, factor):
    for i in range(len(v_data)):
        if v_data[i] == voltage:
            return didv_data[i]*factor
        elif v_data[i] < voltage:
            if i >= 1:
                return 0.5*(didv_data[i]*factor + didv_data[i-1]*factor)
            else:
                return didv_data[i]*factor

def normalize(v_data, didv_data, v_win_start = -1.5, v_win_end = 2,
              search_win_start = -0.75, search_win_end = 1, scaling_factor = 0):
    if v_data[0] < v_data[-1]:
        v_data = np.flip(v_data)
        didv_data = np.flip(didv_data)
    win_num = int(1024*(v_win_end-v_win_start)/4)
    new_v = []
    new_didv = []
    i = -1
    j = -1
    if scaling_factor == 0:
        for v in range(len(v_data)):
            if v_data[v] <= search_win_end and i == -1:
                i = v
            if v_data[v] <= search_win_start and j == -1:
                j = v
                break
        scaling_factor = 1/max(didv_data[i:j])
    #if scaling_factor > 1 or scaling_factor < 0:
    #    return v_data, didv_data, scaling_factor
    if v_win_start < v_data[-1]:
        v_win_start = v_data[-1]
    if v_win_end > v_data[0]:
        v_win_end = v_data[0]
    for v in np.linspace(v_win_start, v_win_end, win_num):
        new_v.append(v)
        didv = didv_for_voltage(v_data, didv_data, v, scaling_factor)
        try:
            if not math.isnan(didv):
                new_didv.append(didv)
            else:
                new_didv.append(0)
        except TypeError:
            print('TypeError')
            continue
    new_v_arr = np.array(new_v)
    new_didv_arr = np.array(new_didv)
    return new_v_arr, new_didv_arr, scaling_factor
