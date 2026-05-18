import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# LeeKesler方法
def LeeKesler(T,SG):
# 转换成NumPy数组
    t_b = np.array(T)
    SG = np.array(SG)
# 计算临界温度
    c_1 = np.array(189.83)
    c_2 = np.array(450.56)
    c_3 = np.array(0.4244)
    c_4 = np.array(0.1174)
    c_5 = np.array(0.1441)
    c_6 = np.array(-1.0069)
    part_a = c_1 + np.multiply(c_2, SG)
    part_b = c_3 + np.multiply(c_4, SG)
    part_c = np.multiply(part_b, t_b)
    part_d = c_5 + np.multiply(c_6, SG)
    part_e = part_d * 1e5 / t_b
    Tpc = part_a + part_c + part_e
# 计算临界压力
    c_7 = np.array(10.294135)
    c_8 = np.array(0.0566)
    c_9 = np.array(0.436392)
    c_10 = np.array(4.12164)
    c_11 = np.array(0.213426)
    c_12 = np.array(0.475794)
    c_13 = np.array(11.81952)
    c_14 = np.array(1.5301548)
    c_15 = np.array(2.45055)
    c_16 = np.array(9.9010)
    ln_term1 = c_7 - c_8 / SG
    ln_term2 = -(c_9 + c_10 / SG + c_11 / SG) * 1e-3 * t_b
    ln_term3 = (c_12 + c_13 / SG + c_14 / np.power(SG, 2)) * 1e-7 * np.power(t_b, 2)
    ln_term4 = -(c_15 + c_16 / np.power(SG, 2)) * 1e-10 * np.power(t_b, 3)
    ln_Ppc = ln_term1 + ln_term2 + ln_term3 + ln_term4
    Ppc_psia = np.exp(ln_Ppc)
    Ppc = Ppc_psia * 0.001
    return Tpc, Ppc
# 从输入中读入自变量
df = pd.read_csv('test_data.csv')
temp = df['Temperature'].values
SG = df['SG'].values
with ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(LeeKesler, temp, SG)
results = list(results)
# 将计算完毕的结果保存为csv文件
Tpc_list, Ppc_list = [], []
for i in results:
    Tpc_list.append(i[0])
    Ppc_list.append(i[1])
data = {'temperature': temp, 'Tpc': Tpc_list, 'Ppc': Ppc_list}
df2 = pd.DataFrame(data)
df2.to_csv('result_data.csv', index=False)