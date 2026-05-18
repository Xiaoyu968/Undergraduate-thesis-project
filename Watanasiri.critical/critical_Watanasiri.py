import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Watanasiri方程
def Watanasiri(T,MW,SG):
# 转换成NumPy数组
    t_b = np.array(T)
    MW = np.array(MW)
    SG = np.array(SG)
# 计算临界温度
    c_1 = np.array(-0.00093906)
    c_2 = np.array(0.030905)
    c_3 = np.array(1.11067)
    c_4 = np.array(0.078154)
    c_5 = np.array(-0.061061)
    c_6 = np.array(-0.016943)
    term1 = c_1 * t_b
    term2 = c_2 * np.log(MW)
    term3 = c_3 * np.log(t_b)
    sg_sqrt = np.power(SG, 1/2)
    sg_cbrt = np.power(SG, 1/3)
    term4 = np.multiply(c_4,sg_sqrt)
    term5 = np.multiply(c_5,sg_cbrt)
    term6 = np.multiply(c_6,SG)
    term7 = term4 + term5 + term6
    term8 = np.multiply(MW,term7)
    ln_Tpc = term1 + term2 + term3 + term8
    Tpc = np.exp(ln_Tpc)
# 计算临界体积
    c_7 = np.array(80.4479)
    c_8 = np.array(-129.8083)
    c_9 = np.array(63.1750)
    c_10 = np.array(-13.1750)
    c_11 = np.array(1.10108)
    c_12 = np.array(42.1958)
    part_1 = np.multiply(c_8, SG)
    part_2 = np.power(SG, 2)
    part_3 = np.multiply(c_9, part_2)
    part_4 = np.power(SG, 3)
    part_5 = np.multiply(c_10, part_4)
    part_6 = np.log(MW)
    part_7 = np.multiply(c_11, part_6)
    part_8 = np.log(SG)
    part_9 = np.multiply(c_12, part_8)
    ln_vc = c_7 + part_1 + part_3 + part_5 + part_7 + part_9
    vc_cm3mol = np.exp(ln_vc)
# 计算临界压力
    c_13 = np.array(3.95431)
    c_14 = np.array(0.70682)
    c_15 = np.array(-4.8400)
    c_16 = np.array(-0.15919)
    term_p1 = Tpc / vc_cm3mol
    term_p2 = np.power(term_p1, 0.8)
    term_p3 = np.multiply(c_14, term_p2)
    term_p4 = MW / Tpc
    term_p5 = np.multiply(c_15, term_p4)
    term_p6 = t_b / MW
    term_p7 = np.multiply(c_16, term_p6)
    ln_Ppc = c_13 + term_p3 + term_p5 + term_p7
    Ppc_bar = np.exp(ln_Ppc)
    Ppc = Ppc_bar * 0.1
    return Tpc, vc_cm3mol, Ppc
# 从输入中读入自变量
df = pd.read_csv('test_data.csv')
temp = df['Temperature'].values
MW = df['MW'].values
SG = df['SG'].values
with ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(Watanasiri, temp, MW, SG)
results = list(results)
# 将计算完毕的结果保存为csv文件
Tpc_list, vc_list, Ppc_list = [], [], []
for i in results:
    Tpc_list.append(i[0])
    vc_list.append(i[1])
    Ppc_list.append(i[2])
data = {'temperature': temp, 'Tpc': Tpc_list, 'vc':vc_list, 'Ppc':Ppc_list}
df2 = pd.DataFrame(data)
df2.to_csv('result_data.csv', index=False)