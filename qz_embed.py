import my_functions
import numpy as np
import sys

args = sys.argv

cover = np.load(args[1])
payload = np.load(args[2])
bit_wm = np.shape(payload)[0]
div = int(args[3])

N = cover.size
K = cover.shape[0]
L = cover.shape[1]
n_wm = N // bit_wm

cover = np.round(np.angle(cover).flatten(), 2)

wmqs = np.zeros(bit_wm*n_wm)
cover_data_remains = cover[bit_wm*n_wm:]

for w in range(n_wm):
    for n in range(bit_wm):
        wmqs[bit_wm*w+n] = my_functions.WMQS(div=div, num_data=cover[bit_wm *
                                                                     w+n], num_bin=payload[n])[0]
    #　現在の状況の表示
    if (w/n_wm)*100 % 10 == 0:
        print("現在" + str(int((w/n_wm)*100) + 10) + "％完了")
wmqs = np.hstack((wmqs, cover_data_remains))
wmqs = wmqs.reshape(K, L)
steg_exp = np.e**(1j*wmqs)
np.save("steg_data_qz.npy", steg_exp)
