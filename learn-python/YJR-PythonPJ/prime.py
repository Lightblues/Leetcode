import math
import time

def primes1(n):
    """return all primes less then n"""
    primes = [2]
    # Method 1
    for k in range(2, n+1):
        if is_prime(k):
            primes.append(k)
    return primes

def primes2(n):
    primes = [2]
    # Method 2
    """assert n>1"""
    if n == 2:
        return primes
    for k in range(3, n+1):
        flag = True
        for p in primes:

            if k % p == 0:
                flag = False
                break
            # Method 2.2
            if p > math.sqrt(k):
                break
        if flag:
            primes.append(k)
    return primes

def is_prime(k):
    """Test if k in prime"""
    # Method 2: falg
    flag = True
    for i in range(2, int(math.sqrt(k))+1):
        if k % i == 0:
            # Method 1: return
    #         return False
    # return True
            flag = False
            break
    return flag


if __name__ == '__main__':
    start = time.time()
    ps = primes2(1000)
    print(ps)
    print('Time: ', time.time()-start)
    # [Method 1] Time:  0.0011110305786132812
    # [Method 2] Time:  0.0008418560028076172
    # [Method 2.2] Time:  0.0006282329559326172
