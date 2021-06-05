import random
import numpy as np
import math
import sys


def Key_Generation(k: int, n: int) -> (list, int, list, list, list, list):
    """
    k と n を引数として，以下を返す関数
     ・ ランダムに生成された k * n の生成行列 G
     ・ G から生成される符号語の誤り訂正能力 t
     ・ ランダムに生成された k * k の正則行列 S
     ・ ランダムに生成された n * n の置換行列 P
     ・ G_pub = S * G * P
     ・符号語全体 code
    """
    # k と n を元にランダムに生成行列Gを作る
    G = np.random.randint(0, 2, size=(k, n))

    # Gから生成される符号語を列挙する
    code = []
    for i in range(2 ** k):
        code_word = []        
        for l in range(n):  # 各行に対してループ
            lth_ele = 0  # l列目と各 bit 列との演算結果を格納
            for j in range(k):
                if((i >> j) & 1):
                    lth_ele = lth_ele + G[j][l]
            lth_ele %= 2
            code_word.append(lth_ele)
        not_exists = True
        for lis in code:
            if(lis == code_word):
                not_exists = False
        if(not_exists == True):
            code.append(code_word)

    # 符号語全体から最小距離 d を算出する
    d = n
    for lis in code:
        weight = 0  # 各符号語のHamming重みを格納
        for num in lis:
            weight = weight + lis[num]
        if(d > weight and weight > 0):
            d = weight

    # d から誤り訂正能力 t を算出する
    t = math.floor(d / 2) + 1

    # k * k の正則行列 S をランダムに生成する
    exists = False
    while(exists == False):
        S = np.random.randint(0, 2, size=(k, k))
        if(np.linalg.det(S) != 0):
            exists = True

    # n * n の置換行列 P をランダムに生成する
    perm = list(range(n))
    random.shuffle(perm)
    P = []
    for i in range(n):  # 各行に対してループ
        p = []
        for j in range(n): # perm[i] = j なら1, それ以外なら0を格納する
            if (perm[i] == j):
                p.append(1)
            else:
                p.append(0)
        P.append(p)

    # G_pub = S * G * P を算出する
    G_pub = np.dot(S, G)
    G_pub = np.dot(G_pub, P)

    return G, t, S, P, G_pub, code


def Encryption(G_pub: list, t: int, m: int) -> list:
    """
    G_pub と t と m を引数として，暗号文 c を返す関数
    """
    arr_G_pub = np.array(G_pub)
    n = arr_G_pub.shape[1]
    
    # Hamming 重みが t なる n 次元エラーベクトル e をランダムに生成する
    exists = False
    while(exists == False):
        e = np.random.randint(0, 2, size=(n, 1))
        weight = 0
        for ele in e:
            weight += ele
        if(weight == t):
            exists = True

    # 暗号文 c を c = m * G_pub + e で生成する
    c = np.dot(m.T, G_pub)
    c += e.T

    return c


def Decryption(G: list, S: list, P: list, c: list, t:int, code: list) -> list:
    """
    諸々の行列と暗号文を引数として，暗号文の復号結果を返す関数
    """
    arr_G = np.array(G)
    k = arr_G.shape[0]
    n = arr_G.shape[1]
    
    # S の逆行列 S^{-1} を算出する
    S_inv = np.linalg.inv(S)
    for i in range(k):
        for j in range(k):
            S_inv[i][j] %= 2

    # P の逆行列 P^{-1} を算出する
    P_inv = []
    for i in range(n):
        p_inv = []
        for j in range(n):
            if(P[j][i] == 1):
                p_inv.append(1)
            else:
                p_inv.append(0)
        P_inv.append(p_inv)

    # c * P^{-1} = m * S * G + z * P^{-1} を算出する
    c_P_inv = np.dot(c, P_inv)
    c_P_inv_list = c_P_inv.tolist()

    # 誤り訂正能力の範囲で訂正できる符号を特定する
    for code_word in code:
        match = 0
        for num in range(n):
            if(c_P_inv_list[0][num] == code_word[num]):
                match += 1
        if (match == n - t):
            error_correct = code_word

    # G の形から m * S を特定する（ビット全探索）
    m_S = []
    for i in range(2 ** k):
        m_S_G = [0 for i in range(n)]
        for j in range(k):
            if ((i >> j) & 1):
                for l in range(n):
                    m_S_G[l] += G[j][l]
                    m_S_G[l] %= 2
        if (m_S_G == error_correct):
            m_s = []
            for j in range(k):
                if ((i >> j) & 1):
                    m_s.append(1)
                else:
                    m_s.append(0)
            m_S.append(m_s)

    # m * S に S^{-1} を掛けて平文を出力する
    decode_m = []
    for m_S_ele in m_S:
        decode_m_ele = np.dot(m_S_ele, S_inv)
        decode_m_ele = decode_m_ele.tolist()
        for i in range(k):
            decode_m_ele[i] %= 2
        decode_m.append(decode_m_ele)
    
    return decode_m


def McEliece(k: str, n: str) -> None:
    k = int(k)
    n = int(n)
    G, t, S, P, G_pub, code = Key_Generation(k, n)
    m = np.random.randint(0, 2, size=(k, 1))
    print(m)
    c = Encryption(G_pub, t, m)
    decode_m = Decryption(G, S, P, c, t, code)
    print(decode_m)
    success = False
    for decode_m_ele in decode_m:
        exist = True
        for i in range(k):
            if(m[i][0] != decode_m_ele[i]):
                exist = False
        if(exist == True):
            success = True
    if(success == True):
        print("success")
    else:
        print("failure")


def main() -> None:
    args = sys.argv
    if 3 == len(args):
        McEliece(args[1], args[2])
    elif 2 >= len(args):
        print('Arguments are too short')
    else:
        print('Arguments are too long')


if __name__ == "__main__":
    main()
