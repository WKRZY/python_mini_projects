def symmetric_vector(a, b):
    """
    计算向量a 关于向量b的对称向量
    :param a:
    :param b:
    :return:
    """
    # 参考链接https://www.yulucn.com/question/4251215506
    b_mod_squared = b[0] ** 2 + b[1] ** 2

    # 计算对称向量的x和y分量
    symmetric_x = (2 * a[1] * b[0] * b[1] + (a[0] * (b[0] ** 2 - b[1] ** 2))) / b_mod_squared
    symmetric_y = (2 * a[0] * b[0] * b[1] - (a[1] * (b[0] ** 2 - b[1] ** 2))) / b_mod_squared

    symmetric = [symmetric_x, symmetric_y]

    return symmetric


import numpy as np

a = np.array([1, 1])
b = np.array([1, 0])
s = symmetric_vector(a, b)
print(s)
