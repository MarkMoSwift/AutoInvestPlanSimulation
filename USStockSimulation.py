import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import random
from datetime import datetime, timedelta

def random_date(start, end):
    """在 start 和 end 之间生成一个随机时间点"""
    # 计算两个日期之间的总秒数
    delta_seconds = int((end - start).total_seconds())
    # 生成随机的秒数
    random_seconds = random.randrange(delta_seconds)
    return start + timedelta(seconds=random_seconds)

# 指定起始日期和结束日期
start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2025-04-07', '%Y-%m-%d')

# 获取随机时间点并去掉时间部分
rand_time = random_date(start_date, end_date).date()


# 设置字体为 SimHei（黑体），以支持中文
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置参数
ticker = 'QQQ'  # 纳斯达克100 ETF

start_date = rand_time
end_date = '2025-2-28'

monthly_invest = 500  # 每月投入金额

# 下载数据
data = yf.download(ticker, start=start_date, end=end_date)

# 确保 'Close' 是一维的 Series
if isinstance(data['Close'], pd.DataFrame):
    data = data['Close'].squeeze()  # 将二维数据转换为一维
else:
    data = data['Close']

# 重新采样为每月第一个交易日的价格
data = data.resample('BMS').first()

print(data.head())  # 检查数据内容

# 模拟定投
shares_bought = monthly_invest / data  # 每月买入份额
total_shares = shares_bought.cumsum()
total_invested = monthly_invest * pd.Series(range(1, len(data)+1), index=data.index)
portfolio_value = total_shares * data

# 汇总结果
result = pd.DataFrame({
    'Price': data,
    'Shares Bought': shares_bought,
    'Total Shares': total_shares,
    'Total Invested': total_invested,
    'Portfolio Value': portfolio_value,
})

# 打印最终结果
final_value = portfolio_value.iloc[-1]
total_cost = total_invested[-1]
return_rate = (final_value - total_cost) / total_cost * 100
years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365
annualized = ((final_value / total_cost) ** (1/years) - 1) * 100

print(f"入场时间：{start_date}")
print(f"总投入: ${total_cost:.2f}")
print(f"投资市值: ${final_value:.2f}")
print(f"总收益率: {return_rate:.2f}%")
print(f"年化收益率: {annualized:.2f}%")

# 可视化
ax = result[['Total Invested', 'Portfolio Value']].plot(figsize=(12,6), title='定投' + ticker + '模拟结果')
# 在左上角添加文本
ax.text(0.05, 0.85, f"入场时间：  {start_date}", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.8, f"总投入：    ${total_cost:.2f}", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.75, f"投资市值：  ${final_value:.2f}", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.7, f"总收益率：  {return_rate:.2f}%", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.65, f"年化收益率：{annualized:.2f}%", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
plt.ylabel('USD')
plt.grid(True)

plt.show()

