import numpy as np
import math
import datetime


def q_t_exp(qi, a, t):
    return qi * math.exp(a * t * -1)

def q_t_exp_range(qi, a, l):
    output_arr = []
    for i in range(l):
        output_arr.append(q_t_exp(qi, a, i + 1))
    return output_arr


def q_t_har(qi, a, t):
    return qi / (a + (a * t))

def q_t_har_range(qi, a, l):
    output_arr = []
    for i in range(l):
        output_arr.append(q_t_har(qi, a, i + 1))
    return output_arr


def q_t_hyp(qi, a, t, n):
    return qi / math.pow((1 + (a * t / n)), n)

def q_t_hyp_range(qi, a, n, l):
    output_arr = []
    for i in range(l):
        output_arr.append(q_t_hyp(qi, a, i + 1, n))
    return output_arr


def r2(xArr, yArr):
    return np.corrcoef(xArr, yArr)[1, 0]


def cumulative(inputArr):
    cumulative = 0.0
    output_arr = []
    for i in range(len(inputArr)):
        cumulative += inputArr[i]
        output_arr.append(cumulative)
    return output_arr


def calc(qi, length, mode, **kwargs):
    a = kwargs.get('a', None)
    
    if(a is None):
        raise ValueError("required parameter a is not supplied")

    if(qi is None):
        raise ValueError("required parameter qi is not supplied")

    if(length is None):
        raise ValueError("required parameter length is not supplied")

    if(length < 1):
        raise ValueError("value of length must be greater than 0")

    if(mode is None):
        raise ValueError("required parameter mode is not supplied")

    if(mode == 'exponential'):
        return q_t_exp_range(qi, a, length)

    if(mode == 'harmonic'):
        return q_t_har_range(qi, a, length)

    if(mode == 'hyperbolic'):
        n = kwargs.get('n', None)
        if(n is None):
            raise ValueError("required parameter n is not supplied")
        if(n < 0 or n > 1):
            raise ValueError("value of n must be in range 0 and 1")
        return q_t_hyp_range(qi, a, n, length)

    raise ValueError("parameter mode is invalid")
