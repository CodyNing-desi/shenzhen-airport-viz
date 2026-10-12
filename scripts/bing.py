import matplotlib.pyplot as plt
import numpy as np

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据
labels = ['京沪航线', '其他航线']
sizes = [54, 46]
colors = ['#2E86AB', '#A23B72']  # 调整更醒目的配色
explode = (0.05, 0)  # 突出京沪航线

# 创建画布
fig, ax = plt.subplots(figsize=(10, 8), dpi=120)

# 绘制饼图
wedges, texts, autotexts = ax.pie(
    sizes,
    explode=explode,
    labels=labels,
    colors=colors,
    autopct='%1.0f%%',  # 整数百分比显示
    shadow=True,
    startangle=90,
    textprops={'fontsize': 16, 'fontweight': 'bold'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}  # 增加白色边框
)

# 美化百分比文字
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(18)
    autotext.set_fontweight('bold')

# 设置标题
ax.set_title('深圳机场宽体客机航线占比', fontsize=22, fontweight='bold', pad=30)

# 保证饼图为正圆形
ax.axis('equal')

# 保存图片（也可直接plt.show()显示）
plt.tight_layout()
plt.savefig('深圳机场宽体客机航线占比.png', dpi=150, bbox_inches='tight')
plt.show()