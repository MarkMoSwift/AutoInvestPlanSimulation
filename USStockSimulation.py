import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def randomDate(start, end):
    # 在 start 和 end 之间生成一个随机时间点
    # 计算两个日期之间的总秒数
    delta_seconds = int((end - start).total_seconds())
    # 生成随机的秒数
    random_seconds = random.randrange(delta_seconds)
    return start + timedelta(seconds=random_seconds)

# 指定起始日期和结束日期
startDate = datetime.strptime('2010-01-01', '%Y-%m-%d')
endDate = datetime.strptime('2025-02-28', '%Y-%m-%d')
# 指定最小时间跨度
spanTime = relativedelta(months = 3)

# 设置参数
ticker = 'QQQ'  # 纳斯达克100 ETF

# 设置字体为 SimHei（黑体），以支持中文
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

monthlyInvest = 500  # 每月投入金额

# 获取随机时间点并去掉时间部分
randTime = randomDate(startDate, endDate - spanTime).date()

enterDate = randTime
# endDate = '2025-2-28'

if 'tradeData' in locals():
    del tradeData
while True:
    # 下载数据
    tradeData = yf.download(ticker, start = enterDate, end = endDate)
    if not tradeData.empty:
        break

# 确保 'Close' 是一维的 Series
if isinstance(tradeData['Close'], pd.DataFrame):
    tradeData = tradeData['Close'].squeeze()  # 将二维数据转换为一维
else:
    tradeData = tradeData['Close']

# 重新采样为每月第一个交易日的价格
buyPriceData = tradeData.resample('BMS').first()

print(buyPriceData.head())  # 检查数据内容

# 模拟定投
sharesBought = monthlyInvest / buyPriceData  # 每月买入份额
totalShares = sharesBought.cumsum()
totalInvested = monthlyInvest * pd.Series(range(1, len(buyPriceData)+1), index=buyPriceData.index)
portfolioValue = totalShares * buyPriceData

# 汇总结果
result = pd.DataFrame({
    'Price': buyPriceData,
    'Shares Bought': sharesBought,
    'Total Shares': totalShares,
    'Total Invested': totalInvested,
    'Portfolio Value': portfolioValue,
})

# 打印最终结果
finalValue = portfolioValue.iloc[-1]
totalCost = totalInvested[-1]
returnRate = (finalValue - totalCost) / totalCost * 100
years = (pd.to_datetime(endDate) - pd.to_datetime(enterDate)).days / 365
annualized = ((finalValue / totalCost) ** (1/years) - 1) * 100

print(f"入场时间：{enterDate}")
print(f"总投入: ${totalCost:.2f}")
print(f"投资市值: ${finalValue:.2f}")
print(f"总收益率: {returnRate:.2f}%")
print(f"年化收益率: {annualized:.2f}%")

# 可视化
ax = result[['Total Invested', 'Portfolio Value']].plot(figsize=(12,6), title='定投' + ticker + '模拟结果')
# 在左上角添加文本
ax.text(0.05, 0.85, f"入场时间：  {enterDate}", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.8, f"总投入：    ${totalCost:.2f}", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.75, f"投资市值：  ${finalValue:.2f}", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.7, f"总收益率：  {returnRate:.2f}%", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.65, f"年化收益率：{annualized:.2f}%", transform=ax.transAxes, fontsize=12, color="black",
        verticalalignment='top', horizontalalignment='left')
plt.ylabel('USD')
plt.grid(True)
plt.savefig(ticker.replace('.','-') + '--' + str(enterDate) + '--' + str(endDate).rsplit(" ", 1)[0] + '--USD')

# plt.show()
