import my_functions
import numpy as np
import sys

args = sys.argv

steg_spec = np.load(args[1])
len_wm = int(args[2])
i = int(args[3])
j = int(args[4])
nm_qz = int(args[5])

extract_data, steg, cp, cp_ex, cp_split, cp_sum, th = my_functions.EX(
    steg_spec, i, j, len_wm, nm_qz)

np.save("extracted_data_bs", extract_data)
