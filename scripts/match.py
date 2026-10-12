import pandas as pd
import os

# ================= 配置区域 =================
# 1. 你的深圳机场数据文件名 (一定要改对！)
MY_FILE_NAME = '深圳到达大屏数据.xlsx' 

# 2. 你那列注册号的表头名字 (航旅纵横导出的通常叫 '注册号' 或 '飞机注册号'，不对就改这里)
REG_COL_NAME = '注册号' 
# 注意：通常大屏数据可能没有直接的注册号列。
# 如果你的表里有注册号(如 B1234)，填那一列的名字。
# 如果你的表里只有航班号(ZH9101)，这招是用不了的！
# ===> 关键确认：你之前说你有注册号，请把这里改成那一列的表头文字！
# 例如：REG_COL_NAME = '飞机注册号'

# ===========================================

def main():
    print("🚀 正在读取你的 Excel 文件...")
    try:
        # 读取所有 Sheet
        my_data = pd.read_excel(MY_FILE_NAME, sheet_name=None)
        # 合并成一张大表
        df_my = pd.concat(my_data.values(), ignore_index=True)
    except Exception as e:
        print(f"❌ 读取 Excel 失败: {e}")
        return

    # 检查列名是否存在
    # 如果你不知道列名，这行会把所有列名打出来给你看
    if REG_COL_NAME not in df_my.columns:
        print(f"❌ 没找到列名 '{REG_COL_NAME}'！")
        print(f"你的表格里只有这些列: {list(df_my.columns)}")
        print("请修改代码里的 REG_COL_NAME 配置。")
        return

    print("🚀 正在加载全球飞机数据库 (约几百兆，稍等)...")
    try:
        df_db = pd.read_csv('aircraftDatabase.csv', 
                            usecols=['registration', 'typecode', 'model'],
                            dtype=str)
    except Exception as e:
        print(f"❌ 读取数据库失败: {e}")
        print("请确认 aircraftDatabase.csv 在当前文件夹里！")
        return

    print("🔄 正在清洗数据 (双向去杠)...")
    
    # 1. 清洗你的数据：转大写，去空格，去横杠
    df_my['clean_key'] = df_my[REG_COL_NAME].astype(str).str.upper().str.strip().str.replace('-', '', regex=False)
    
    # 2. 清洗数据库：同上
    df_db['clean_key'] = df_db['registration'].astype(str).str.upper().str.strip().str.replace('-', '', regex=False)

    print(f"⚡ 正在极速匹配 {len(df_my)} 条航班...")
    
    # 3. 合并 (Left Join)
    result = pd.merge(df_my, df_db[['clean_key', 'typecode', 'model']], on='clean_key', how='left')

    # 删除辅助列
    result.drop(columns=['clean_key'], inplace=True)
    
    # 统计成功率
    success_count = result['model'].notnull().sum()
    print(f"✅ 匹配完成！成功匹配: {success_count} 条 ({success_count/len(result):.1%})")

    # 4. 导出
    out_file = '匹配结果_带机型.xlsx'
    result.to_excel(out_file, index=False)
    print(f"📂 文件已保存为: {out_file}")

if __name__ == "__main__":
    main()