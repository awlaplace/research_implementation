"""
k と n を引数にとって，k × n のLDPC符号の生成行列をランダムに生成し，
符号語を列挙するスクリプト
"""

import random
import numpy as np
import sys


def list_weight(lis: list) -> int:
    w = 0
    for ele in lis:
        w += ele 
    return w


def LDPC_encode(k: str, n: str) -> None:
    k = int(k)
    n = int(n)
    
    ## LDPC符号のHamming重みは O(1) で，ランダムに生成する
    exists = False
    while exists == False:
        weight = random.randrange(10)
        if(weight > 0):
            if(weight <= k and weight <= n):
                exists = True
    
    print("Hamming重みは", weight)

    ## 各列が weight のHamming重みの生成行列をランダムに生成する
    matrix_trans = []
    for column in range(n):
        column_vec = [0 for i in range(k)]
        while list_weight(column_vec) < weight:
            parity = random.randrange(k)
            if column_vec[parity] == 0:
                column_vec[parity] += 1
        matrix_trans.append(column_vec)

    matrix_trans = np.array(matrix_trans)
    matrix = matrix_trans.T

    ## 生成行列 matrix を表示する
    matrix_list = matrix.tolist()
    print("生成行列を表示します")
    print(matrix_list)

    ## matrix によって生成される符号語全体を表示する
    code = []
    for i in range(2 ** k):
        code_word = []        
        for l in range(n):  # 各行に対してループ
            lth_ele = 0  # l列目と各 bit 列との演算結果を格納
            for j in range(k):
                if((i >> j) & 1):
                    lth_ele = lth_ele + matrix[j][l]
            lth_ele %= 2
            code_word.append(lth_ele)
        not_exists = True
        for lis in code:
            if(lis == code_word):
                not_exists = False
        if(not_exists == True):
            code.append(code_word)
    print("上記の生成行列によって生成される各符号語を表示します")
    for code_word in code:
        print(code_word)
    

def main() -> None:
    args = sys.argv
    if 3 == len(args):
        LDPC_encode(args[1], args[2])
    elif 2 >= len(args):
        print('Arguments are too short')
    else:
        print('Arguments are too long')


if __name__ == "__main__":
    main()