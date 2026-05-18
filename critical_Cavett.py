import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Cavett方程
def Cavett(T_k,SG):
# 沸点转成℃
    T = T_k - 273.15
# 计算API重度
    API = 141.5/SG - 131.5
# 计算T_1
    if T <= 704.4:
        c_1 = np.array([1.67909873])
        c_2 = np.array([-0.001905318587])
        c_3 = np.array([1.260054922e-6])
        t_b = np.array(T)
        T_1 = c_1 + np.multiply(c_2, t_b) + np.multiply(c_3, np.square(t_b))
    else:
        c_1 = np.array([0.9622])
        c_2 = np.array([-0.000130041])
        t_b = np.array((T-704.4))
        T_1 = c_1 + np.multiply(c_2, t_b)
# 计算临界温度
    part_a = np.multiply(5.888088e-8, API) + 9.5570856e-6
    part_b = np.multiply(part_a, T)
    part_c = part_b - 0.00892021122
    part_d = np.multiply(part_c, API)
    term_Tpc = part_d + 0.30582674e-3 + T_1
    Tpc = np.multiply(term_Tpc, (T + 17.7778)) + 426.745
# 计算T_1p
    if T <= 537.8:
        c_1 = np.array([9.4120109e-4])
        c_2 = np.array([-3.0474749e-6])
        c_3 = np.array([1.5184103e-9])
        t_b = np.array(T)
        T_1p = np.multiply(c_1, t_b) + np.multiply(c_2, np.square(t_b)) + np.multiply(c_3, np.power(t_b, 3))
    else:
        c_1 = np.array([-0.587864])
        c_2 = np.array([-0.0005985])
        t_b = np.array(T-1000.0)
        T_1p = np.multiply(c_2, t_b) + c_1
# 计算T_2
    term1_part_a = 1.3949619e-10 * API + 1.1047899e-8
    term1_part_b = np.multiply(term1_part_a, API)
    term1 = np.multiply(term1_part_b, T ** 2)
    term2_part_a = -4.8271599e-8 * API - 2.087611e-5
    term2_part_b = np.multiply(term2_part_a, API)
    term2 = np.multiply(term2_part_b, T)
    T_2 = term1 + term2 + 2.8290406 + T_1p
# 计算临界压力
    Ppc_psia = 6.8947*(10**T_2)
    Ppc = Ppc_psia*0.001
    return Tpc, Ppc
# 从输入中读入自变量
df = pd.read_csv('test_data.csv')
temp = df['Temperature'].values
SG = df['SG'].values
with ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(Cavett, temp, SG)
results = list(results)
# 将计算完毕的结果保存为csv文件
Tpc_list, Ppc_list = [], []
for i in results:
    Tpc_list.append(*i[0])
    Ppc_list.append(*i[1])
data = {'temperature': temp, 'Cavett_Tpc': Tpc_list, 'Cavett_Ppc':Ppc_list}
df2 = pd.DataFrame(data)
df2.to_csv('result_data.csv', index=False)
