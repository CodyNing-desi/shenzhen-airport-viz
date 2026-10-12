import matplotlib.pyplot as plt
import numpy as np

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据准备
labels = ['波音', '空客', 'Others']
counts = [6279, 6717, 1379]  # 原始次数
percentages = [42.1, 45.1, 9.3]  # 计算好的百分比
# 组合标签（显示“名称+次数+百分比”）
display_labels = [f'{label}\n{count}次\n({pct}%)' for label, count, pct in zip(labels, counts, percentages)]

# 配色（区分度高的专业配色）
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
explode = (0.05, 0.05, 0)  # 突出波音、空客

# 创建画布
fig, ax = plt.subplots(figsize=(10, 8), dpi=120)

# 绘制饼状图
wedges, texts, autotexts = ax.pie(
    counts,  # 按原始次数占比绘制
    explode=explode,
    labels=display_labels,
    colors=colors,
    autopct='',  # 关闭默认百分比（已整合到标签）
    shadow=True,
    startangle=90,
    textprops={'fontsize': 14, 'fontweight': 'bold'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}  # 白色边框更清晰
)

# 设置标题
ax.set_title('深圳机场机型品牌分布', fontsize=22, fontweight='bold', pad=30)

# 保证饼图为正圆形
ax.axis('equal')

# 调整布局，避免标签重叠
plt.tight_layout()

# 保存图片（也可直接plt.show()弹窗显示）
plt.savefig('深圳机场机型品牌分布.png', dpi=150, bbox_inches='tight')
plt.show()