import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Riazi-Daubert方程
def RiaziDaubert(T,rho):
# 转换成NumPy数组
    t_b = np.array(T)
    rho = np.array(rho)
# 计算临界温度
    c_1 = np.array(18.2934)
    c_2 = np.array(0.595251)
    c_3 = np.array(0.347420)
    part_a = np.power(t_b, c_2)
    part_b = np.power(rho, c_3)
    part_c = np.multiply(part_a, part_b)
    Tpc = np.multiply(c_1, part_c)
# 计算临界压力
    c_4 = np.array(0.295152e7)
    c_5 = np.array(-2.20820)
    c_6 = np.array(2.22086)
    part_1 = np.power(t_b, c_5)
    part_2 = np.power(rho, c_6)
    part_3 = np.multiply(part_1, part_2)
    Ppc = np.multiply(c_4, part_3)
# 计算临界体积
    c_7 = np.array(0.822382e-4)
    c_8 = np.array(2.51217)
    c_9 = np.array(-1.62214)
    v_part_a = np.power(t_b, c_8)
    v_part_b = np.power(rho, c_9)
    v_part_c = np.multiply(v_part_a, v_part_b)
    vc = np.multiply(c_7, v_part_c)
    return Tpc, Ppc, vc
# 从输入中读入自变量
df = pd.read_csv('test_data.csv')
temp = df['Temperature'].values
rho = df['rho'].values
with ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(RiaziDaubert, temp, rho)
results = list(results)
# 将计算完毕的结果保存为csv文件
Tpc_list, Ppc_list, vc_list = [], [], []
for i in results:
    Tpc_list.append(i[0])
    Ppc_list.append(i[1])
    vc_list.append(i[2])
data = {'temperature': temp, 'Tpc': Tpc_list, 'Ppc': Ppc_list, 'vc': vc_list}
df2 = pd.DataFrame(data)
df2.to_csv('result_data.csv', index=False)