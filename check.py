import sys
import numpy as np

args = sys.argv

payload = np.load(args[1])
extract_data = np.load(args[2])

n = payload.shape[0]

error = 0
for i in range(n):
    if payload[i] != extract_data[i]:
        error += 1

print("BER:" + str(error / n))
print("Accuracy:"+str(1-(error/n)))
