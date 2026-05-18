import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# NEDOL方程
def NEDOL(T,SG):
# 转换成NumPy数组
    t_b = np.array(T)
    SG = np.array(SG)
# 计算临界温度
    term1 = 1.1569
    term2 = 0.3882 * np.log10(SG)
    term3 = 0.66709 * np.log10(1.8 * t_b)
    log_18Tc = term1 + term2 + term3
    Tc = (10 ** log_18Tc) / 1.8
# 计算Watson因子WK
    WK = ((1.8 * t_b) ** (1/3)) / SG
# 对比沸点Trb
    Trb = t_b / Tc
# 计算临界压力
    log_147Pc = 2.22066 - 0.05445 * WK + 3.12579 * (1 - Trb)
    Pc_bar = (10 ** log_147Pc) / 14.7
    Pc = Pc_bar * 0.1
    return Tc, Pc
# 从输入中读入自变量
df = pd.read_csv('test_data.csv')
temp = df['Temperature'].values
SG = df['SG'].values
with ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(NEDOL, temp, SG)
results = list(results)
# 将计算完毕的结果保存为csv文件
Tc_list, Pc_list = [], []
for i in results:
    Tc_list.append(i[0])
    Pc_list.append(i[1])
data = {'temperature': temp, 'Tc': Tc_list, 'Pc': Pc_list}
df2 = pd.DataFrame(data)
df2.to_csv('result_data.csv', index=False)