"""
Module: check five areas

Author: Shenkai Wang, Junmian Zhu, Raymond Blackwell, and Felix R. Fischer

Description: Obtain topographic images at five different areas. Can be run to see if everything works.

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

def operate(operation, record_file):
    operation_time = str(datetime.datetime.now().time())
    print(operation_time)
    print(operation)
    with open(record_file, 'a') as file:
        file.write(operation_time + '\n' + operation + '\n')
today = datetime.date.today()
path = 'D:/auto_matrix/operation_record'
filename = path + '/' + str(today) + '.txt'
if not os.path.isfile(filename):
    with open(filename, 'w') as file:
        pass

my_stm = STM()
operate(my_stm.init(), filename)
positions = [[0, 0], [400, 400], [400, -400], [-400, -400], [-400, 400]]
for position in positions:
    operate(my_stm.set_xy_offset(position[0], position[1]), filename)
    time.sleep(70)
    operate(my_stm.start(), filename)
    operate(my_stm.monitor_zout(), filename)
    operate(my_stm.stop(), filename)
operate(my_stm.set_xy_offset(0, 0), filename)
operate(my_stm.pull_tip_back(), filename)
operate(my_stm.rundown(), filename)
