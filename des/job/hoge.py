from numba import jit
from numpy import arange
import time
#@jit(nopython=True, nogil=True)
@jit
def sum2d(arr):
    M,N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

start_time = time.time()
a = arange(100000000).reshape(10000,10000)
print(sum2d(a))
elapsed_time = time.time() - start_time
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
