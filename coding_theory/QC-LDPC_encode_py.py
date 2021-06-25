"""
n を引数にとって，n × 2n のQC-LDPC符号の生成行列をランダムに生成し，
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


def LDPC_encode(n: str) -> None:
    n = int(n)
    
    ## LDPC符号のHamming重みは O(1) で，ランダムに生成する
    exists = False
    while exists == False:
        left_weight = random.randrange(10)
        if(left_weight > 0):
            if(left_weight <= n and left_weight <= n):
                exists = True
    exists = False
    while exists == False:
        right_weight = random.randrange(10)
        if(right_weight > 0):
            if(right_weight <= n and right_weight <= n):
                exists = True
    
    print("Hamming重みは", left_weight, "と", right_weight)

    ## 各列が weight のHamming重みの生成行列をランダムに生成する
    ## 各行列は巡回行列なので，１行目を決めると他の行も決まる
    left_matrix_trans = []
    ## Hamming 重みが left_weight で要素が n なるリストをランダムに作る
    column_vec = [0 for i in range(n)]
    exists = False
    while exists == False:
        for index in range(n):
            column_vec[index] = random.randrange(2)
        if list_weight(column_vec) == left_weight:
            exists = True
        else:
            column_vec = [0 for i in range(n)]
    left_column_vec = column_vec

    right_matrix_trans = []
    ## Hamming 重みが right_weight で要素が n なるリストをランダムに作る
    column_vec = [0 for i in range(n)]
    exists = False
    while exists == False:
        for index in range(n):
            column_vec[index] = random.randrange(2)
        if list_weight(column_vec) == right_weight:
            exists = True
        else:
            column_vec = [0 for i in range(n)]
    right_column_vec = column_vec
    
    matrix_trans = []
    for row in range(n):
        column_vec = []
        for column in range(n):
            column_vec.append(left_column_vec[(row + column) % n])
        for column in range(n):
            column_vec.append(right_column_vec[(row + column) % n])
        matrix_trans.append(column_vec)

    matrix_trans = np.array(matrix_trans)
    matrix = matrix_trans.T

    ## 生成行列 matrix を表示する
    matrix_list = matrix.tolist()
    print("生成行列を表示します")
    print(matrix_list)

    ## matrix によって生成される符号語全体を表示する
    code = []
    for i in range(2 ** (2 * n)):
        code_word = []        
        for l in range(n):  # 各行に対してループ
            lth_ele = 0  # l列目と各 bit 列との演算結果を格納
            for j in range(n):
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
    if 2 == len(args):
        LDPC_encode(args[1])
    elif 1 >= len(args):
        print('Arguments are too short')
    else:
        print('Arguments are too long')


if __name__ == "__main__":
    main()