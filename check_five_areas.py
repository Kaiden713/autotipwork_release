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
