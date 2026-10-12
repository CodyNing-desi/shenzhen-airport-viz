# 第一步：安装依赖库（首次运行需执行，已安装则跳过）
# 打开命令提示符（Windows）或终端（Mac/Linux），输入：
# pip install pandas matplotlib openpyxl

# 第二步：完整代码
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 基础配置（解决中文显示、图表样式）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']  # 适配不同系统中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['figure.facecolor'] = 'white'  # 图表背景色为白色

# 2. 读取Excel数据（需替换为你的Excel文件路径）
# 示例：如果文件在桌面，Windows路径可能是 r'C:\Users\你的用户名\Desktop\新建 Microsoft Excel 工作表 (2).xlsx'
#       Mac路径可能是 '/Users/你的用户名/Desktop/新建 Microsoft Excel 工作表 (2).xlsx'
file_path = '你的Excel文件完整路径.xlsx'  # ！！！此处必须替换为你的文件实际路径
df = pd.read_excel(file_path, engine='openpyxl')  # 兼容.xlsx格式

# 3. 数据处理（提取月份和客流数据，添加单位格式）
months = df['月份'].astype(str) + '月'  # 月份格式化为“1月、2月”
daily_flow = df['日均客流（万人次）']  # 客流数据（已明确单位为万人次）

# 4. 创建图表画布
fig, ax = plt.subplots(figsize=(12, 8), dpi=120)  # 画布大小12*8英寸，分辨率120

# 5. 绘制柱状图
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(months)))  # 渐变蓝色系
bars = ax.bar(
    x=months,
    height=daily_flow,
    color=colors,
    width=0.6,
    edgecolor='#1f77b4',  # 柱子边框色
    linewidth=1.2,
    alpha=0.9  # 柱子透明度
)

# 6. 添加数值标签（显示“X.X万人次”）
for bar, value in zip(bars, daily_flow):
    ax.text(
        x=bar.get_x() + bar.get_width()/2,  # 水平居中
        y=bar.get_height() + 0.2,  # 垂直在柱子顶部+0.2处
        s=f'{value:.1f}万人次',  # 数值+单位
        ha='center', va='bottom',
        fontsize=11,
        fontweight='bold',
        color='#2c3e50'
    )

# 7. 设置图表标题和轴标签
ax.set_title(
    label='2024年深圳机场各月日均客流数据',
    fontsize=20,
    fontweight='bold',
    pad=30,
    color='#2c3e50'
)
ax.set_xlabel(
    xlabel='月份',
    fontsize=14,
    fontweight='bold',
    labelpad=15,
    color='#34495e'
)
ax.set_ylabel(
    ylabel='日均客流（万人次）',
    fontsize=14,
    fontweight='bold',
    labelpad=15,
    color='#34495e'
)

# 8. 优化图表细节
ax.set_ylim(0, max(daily_flow) * 1.15)  # Y轴从0开始，顶部留15%空间
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1)  # 仅显示水平网格
ax.set_axisbelow(True)  # 网格置于柱子下方
ax.tick_params(axis='x', labelsize=12)  # X轴刻度字体大小
ax.tick_params(axis='y', labelsize=12, labelformat='%.1f')  # Y轴刻度显示1位小数
# 隐藏顶部和右侧边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#bdc3c7')
ax.spines['bottom'].set_color('#bdc3c7')

# 9. 保存/显示图表
plt.tight_layout()  # 自动调整布局，避免标签被截断
# 保存图表（路径可自定义，示例保存在桌面）
plt.savefig(
    fname='2024年深圳机场各月日均客流数据柱状图.png',
    dpi=150,
    bbox_inches='tight'
)
plt.show()  # 弹出窗口显示图表

print("图表已生成并保存！")