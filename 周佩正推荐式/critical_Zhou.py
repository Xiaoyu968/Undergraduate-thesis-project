import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# 周佩正推荐式
def Zhoupeizheng(T,SG,slope):
# 转成NumPy数组
    t_b = np.array(T)
    SG = np.array(SG)
    slope = np.array(slope)
# 计算临界温度
    if slope > 0.5:
        c_1 = np.array([3.85254])
        c_2 = np.array([0.82944])
        c_3 = np.array([0.42928])
        term_1 = np.log(SG)
        term_2 = np.log(t_b)
        term_3 = np.multiply(term_2, c_3)
        term_4 = np.multiply(c_2, term_1)
        ln_tpc = c_1 + term_3 + term_4
    else:
        c_4 = np.array([4.05209])
        c_5 = np.array([0.40122])
        c_6 = np.array([0.37899])
        term_5 = np.log(SG)
        term_6 = np.log(t_b)
        term_7 = np.multiply(c_5, term_5)
        term_8 = np.multiply(c_6, term_6)
        ln_tpc = c_4 + term_7 + term_8
    tpc_C = np.exp(ln_tpc)
    Tpc = tpc_C + 273.15
# 计算临界压力
    if slope > 0.5:
        c_7 = np.array([8.18024])
        c_8 = np.array([1.93053])
        c_9 = np.array([-0.87273])
        part_1 = np.log(SG)
        part_2 = np.multiply(c_8, part_1)
        part_3 = np.log(t_b)
        part_4 = np.multiply(c_9, part_3)
        ln_Ppc = c_7 + part_2 + part_4
    else:
        c_10 = np.array([7.74174])
        c_11 = np.array([2.80203])
        c_12 = np.array([-0.75393])
        part_5 = np.log(SG)
        part_6 = np.log(t_b)
        part_7 = np.multiply(c_11, part_5)
        part_8 = np.multiply(c_12, part_6)
        ln_Ppc = c_10 + part_7 + part_8
    Ppc_bar = np.exp(ln_Ppc)
    Ppc = Ppc_bar * 0.1
    return Tpc, Ppc
# 从输入中读入自变量
df = pd.read_csv('test_data.csv')
temp = df['Temperature'].values
SG = df['SG'].values
slope = df['slope'].values
with ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(Zhoupeizheng, temp, SG, slope)
results = list(results)
# 将计算完毕的结果保存为csv文件
Tpc_list, Ppc_list = [], []
for i in results:
    Tpc_list.append(*i[0])
    Ppc_list.append(*i[1])
data = {'Temperature': temp, 'Tpc': Tpc_list, 'Ppc': Ppc_list}
df2 = pd.DataFrame(data)
df2.to_csv('result_data.csv', index=False)