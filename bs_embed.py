import my_functions
import numpy as np
import sys

args = sys.argv

cover = np.load(args[1])
payload = np.load(args[2])
len_wm = np.shape(payload)[0]
i = int(args[3])
j = int(args[4])
nm_qz = int(args[5])

steg_exp, steg_spec, N, A_fl_copy = my_functions.WM(
    cover, payload, i, j, nm_qz)

np.save("steg_data_bs.npy", steg_spec)
