/*
  * 位数rと F_2[X] / (X^r - 1) の元 f を入力したら f^{-1} を返すプログラム
  * r については，Z/rZ で 2 が原始元の必要がある
  * f については，そのHamming重みが奇数の必要がある
*/
#include <iostream>
#include <cmath>
using namespace std;

bool is_primitive(int r){
    bool flag = true;
    int num = 1;
    for(int index = 0; index < r - 2; index++){
        num *= 2;
        num %= r;
        if(num == 1) flag = false;
    }

    return flag;
}

int main(){
    // 入力
    int r;
    cout << "標数rを入力してください。Z/rZ で 2 が原始元である必要があります。" << endl;
    cin >> r;
    if(is_primitive(r) == false){
        cout << "rは原始元ではありません" << endl;
        cout << "プログラムを強制終了します" << endl;
        exit(0);
    }

    int f[r];
    int weight = 0;
    cout << "F_2係数r次元ベクトルfを降順で入力してください。Hamming重みが奇数である必要があります。" << endl;
    for(int index = r - 1; index >= 0; index--){
        cin >> f[index];
        weight += f[index];
    }
    if(weight % 2 == 0){
        cout << "fのHamming重みが奇数ではありません" << endl;
        cout << "プログラムを強制終了します" << endl;
        exit(0);
    }

    // f を一旦出力する
    cout << "fを降順で出力します。" << endl;
    int cnt = 0;
    for(int index = r - 1; index >= 0; index--){
        if(index > 1 && f[index] == 1 && cnt == 0){
            cout << "X^" << index;
            cnt++;
        }
        else if(index > 1 && f[index] == 1 && cnt > 0){
            cout << " + " << "X^" << index;
        }
        else if(index == 1 && f[index] == 1 && cnt == 0){
            cout << "X";
            cnt++;
        }
        else if(index == 1 && f[index] == 1 && cnt > 0){
            cout << " + X";
        }
        else if(index == 0 && f[index] == 1 && cnt == 0){
            cout << "1";
            cnt++;
        }
        else if(index == 0 && f[index] == 1 && cnt > 0){
            cout << " + 1";
        }
    }
    cout << endl;

    // 0 ~ 2^r-1 の範囲でbit全探索をして，f^-1 を特定する
    int ans[(1 << r)];
    for(int i = 0; i < (1 << r); i++) ans[i] = 0;
    int target_number = -1;
    for(int bit = 0; bit < (1 << r); bit++){
        int Hamming_sum[r] = {0};
        for(int index = 0; index < r; index++){
            if((bit & (1 << index))){
                for(int f_index = 0; f_index < r; f_index++){
                    if(f[f_index] == 1) Hamming_sum[(index + f_index) % r]++;
                }
            }
        }
        bool exists = true;
        for(int index = 0; index < r; index++){
            if(1 <= index && index <= r - 1 && Hamming_sum[index] % 2 == 1) exists = false;
            if(index == 0 && Hamming_sum[index] % 2 == 0) exists = false;
        }
        if(exists == true) target_number = bit;
    }

    // f^{-1} を出力する
    cout << "fの逆元を降順で出力します。" << endl;
    cnt = 0;
    for(int i = r - 1; i >= 0; i--){
        int power = pow(2, i);

        if(i > 1 && (target_number / power) == 1 && cnt == 0){
            cout << "X^" << i;
            cnt++;
        }
        else if(i > 1 && (target_number / power) == 1 && cnt > 0){
            cout << " + " << "X^" << i;
        }
        else if(i == 1 && (target_number / power) == 1 && cnt == 0){
            cout << "X";
            cnt++;
        }
        else if(i == 1 && (target_number / power) == 1 && cnt > 0){
            cout << " + X";
        }
        else if(i == 0 && (target_number / power) == 1 && cnt == 0){
            cout << "1";
            cnt++;
        }
        else if(i == 0 && (target_number / power) == 1 && cnt > 0){
            cout << " + 1";
        }
        target_number %= power;
    }
    cout << endl;
}