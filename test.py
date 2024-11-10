import numpy as np
import pywt
import matplotlib.pyplot as plt

# 示例时间序列，包含0-1-0的结构
time_series = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

# 1. 进行小波变换（DWT）
# 使用 'db1'（Daubechies 1）小波，适合二值序列的简单特征分析
coeffs = pywt.wavedec(time_series, 'db1', level=3)

# 提取不同尺度下的小波系数
cA3, cD3, cD2, cD1 = coeffs
for i in coeffs:
    print(i.shape)
# 2. 查看不同尺度下的系数，识别长时间保持1的结构
plt.figure(figsize=(12, 8))

plt.subplot(5, 1, 1)
plt.scatter(range(len(time_series)),time_series, label='Original Time Series')
plt.legend()

plt.subplot(5, 1, 2)
plt.scatter(range(len(cA3)),cA3, label='Approximation Coefficients (cA3)')
plt.legend()

plt.subplot(5, 1, 3)
plt.scatter(range(len(cD3)),cD3, label='Detail Coefficients (cD3)')
plt.legend()

plt.subplot(5, 1, 4)
plt.scatter(range(len(cD2)),cD2, label='Detail Coefficients (cD2)')
plt.legend()

plt.subplot(5, 1, 5)
plt.scatter(range(len(cD1)),cD1, label='Detail Coefficients (cD1)')
plt.legend()

plt.tight_layout()
plt.show()

# 3. 通过系数分析，筛选出符合“长时间保持1”的段落
# cA3中较大值的区域往往对应着稳定的1区域
threshold = 0.5  # 可调整的阈值
long_ones_sections = np.where(cA3 > threshold)[0]  # 获取高于阈值的区域

print("符合条件的长时间1段位于:", long_ones_sections)