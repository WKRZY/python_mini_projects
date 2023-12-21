# 读取excel 数据
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('gold_day_price.xlsx')
# 取出第一列（时间）和第二列（价格）
time = data.iloc[:, 0]
price = data.iloc[:, 1]
# 求五日均线
data['MA5'] = price.rolling(window=5).mean()
# 求六十日均线
data['MA60'] = price.rolling(window=60).mean()
plt.plot(time, data['MA5'])
# 绘制六十日均线
plt.plot(time, data['MA60'])
plt.legend(['5_days', '60_days'])
plt.show()
