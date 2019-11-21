import my_functions
import numpy as np
import sys

args = sys.argv

steg_spec = np.load(args[1])
bit_wm = int(args[2])
div = int(args[3])

N = steg_spec.size
K = steg_spec.shape[0]
L = steg_spec.shape[1]
n_wm = N // bit_wm
extract = np.zeros(bit_wm*n_wm)

steg = np.round(np.angle(steg_spec).flatten(), 2)

for w in range(n_wm):
    for n in range(bit_wm):
        extract[bit_wm*w +
                n] = my_functions.ERQS(div=div, num_data=steg[bit_wm * w + n])[0]
    if (w/n_wm)*100 % 10 == 0:
        print("現在" + str(int((w/n_wm)*100) + 10) + "％完了")

extract_tr = extract[:n_wm*bit_wm]
extract_split = np.split(extract_tr, n_wm)
extract_sum = np.sum(extract_split, axis=0)
th = n_wm//2
extract_data = (extract_sum > th) * 1

np.save("extract_data_qz.npy", extract_data)
