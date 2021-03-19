from STM import STM
from open_last import analyse_last_topo
from Matrix import Matrix

my_stm = STM()
my_stm.init()
head = my_stm.get_head_file()
rawdata_path = my_stm.get_file_path()
head = head + "_0001.mtrx"
my_matrix = Matrix(rawdata_path, head)
image = my_matrix.openTopo(4, 2)
image = my_matrix.flattenImage(image)
image = my_matrix.three_point_flatten(image, 4, 2)
execute_positions = my_matrix.findAu(image, 4, 2)

