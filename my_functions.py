import numpy as np
import matplotlib.pyplot as plt


def WM(cover, payload, i, j, nm_qz):
    A_bef = ((np.angle(cover) + np.pi) / np.pi)
    plt.hist(A_bef.flatten(), ec='black', rwidth=0.8)
    plt.savefig("histgram_before_quantization.png")
    plt.close()
    A = A_bef*pow(2, nm_qz-1)
    A = A.astype("int64")
    L = A.shape[0]
    K = A.shape[1]
    N = len(payload)
    n_sb = j - i + 1

    A_fl = A.flatten()
    plt.hist(A_fl, ec='black', rwidth=0.8)
    plt.savefig("histgram_after_quantization.png")
    plt.close()

    B_fl = payload
    n = (L*K // N)  # 繰り返しの回数
    zeros = np.zeros((L*K) % N, dtype="int64")

    wm_tile = np.tile(B_fl, n)
    steg_stack = np.hstack((wm_tile, zeros))

    for k in range(n_sb):
        A_fl = A_fl & ~pow(2, i) | (steg_stack*pow(2, i))
        i += 1

    plt.hist(A_fl, ec='black', rwidth=0.8)
    plt.savefig("histgram_after_embedding")
    plt.close()

    A_fl_copy = A_fl
    steg_adj = np.where(A_fl < pow(2, nm_qz), A_fl+0.5, A_fl)
    plt.hist(steg_adj, ec='black', rwidth=0.8)
    plt.savefig("histgram_adjusting")
    plt.close()

    steg_spec = ((steg_adj.reshape((L, K))/pow(2, nm_qz-1))*np.pi) - np.pi
    steg_spec = np.array(steg_spec)
    steg_exp = np.e**(1j*steg_spec)
    return[steg_exp, steg_spec, N, A_fl_copy]


def EX(steg_spec, i, j, len_wm, nm_qz):
    steg_exp = np.e**(1j*steg_spec)
    L = steg_exp.shape[0]
    K = steg_exp.shape[1]
    N = len_wm
    n_sb = j-i+1
    n = (L*K*n_sb) // N

    steg_phase = np.angle(steg_exp)
    steg = ((steg_phase.flatten() + np.pi) / np.pi) * pow(2, nm_qz - 1)
    steg = steg.astype("int64")
    steg_tr = steg[:int(N * n / n_sb)]
    cp = np.zeros(N * n)
    for k in range(n_sb):
        cp[int(N * n / n_sb)*k:int(N * n / n_sb)*(k+1)] = steg_tr & pow(2, i)
        i += 1
    cp_ex = np.where(cp != 0, 1, cp)
    cp_split = np.split(cp_ex, n_sb)
    cp_sum = np.sum(cp_split, axis=0)
    th = n_sb/2
    extract_data = (cp_sum > th) * 1
    return[extract_data, steg, cp, cp_ex, cp_split, cp_sum, th]


def getNearestValue(list, num):
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return[idx, list[idx]]


def WMQS(div, num_data, num_bin):
    # 量子化幅
    qs_bin = (2 * np.pi) / div
    # 少子化幅に基づいて[-pi, pi]を等分割したリストを作成
    qs_list = np.arange((-np.pi)+(qs_bin/2), np.pi -
                        (qs_bin / 2) + qs_bin, qs_bin)
    #  入力データに最も近い量子化代表値を抽出
    nv = getNearestValue(qs_list, num_data)
    qs_list_sub = np.delete(qs_list, nv[0])
    # 二番目に近い代表値を取得
    nv_sub = getNearestValue(qs_list_sub, num_data)

    if (nv[0] % 2 == 0) and num_bin == 1:
        if nv[0] == 0:
            if nv[1] <= num_data:
                num_data = qs_list[1]
            if nv[1] > num_data:
                num_data = qs_list[div - 1]
        else:
            num_data = nv_sub[1]

    if (nv[0] % 2 == 1) and num_bin == 0:
        if nv[0] == div - 1:
            if nv[1] < num_data:
                num_data = qs_list[0]
            if nv[1] >= num_data:
                num_data = qs_list[div - 2]
        else:
            num_data = nv_sub[1]

    if ((nv[0] % 2 == 0) and num_bin == 0) or ((nv[0] % 2 == 1) and num_bin == 1):
        num_data = nv[1]
    return[num_data, nv[0], nv[1]]


def ERQS(div, num_data):
    qs_bin = (2*np.pi) / div
    qs_list = np.arange((-np.pi)+(qs_bin/2), np.pi -
                        (qs_bin/2) + qs_bin, qs_bin)
    nv = getNearestValue(qs_list, num_data)
    if nv[0] % 2 == 0:
        extract_data = 0
    else:
        extract_data = 1
    return[extract_data]
