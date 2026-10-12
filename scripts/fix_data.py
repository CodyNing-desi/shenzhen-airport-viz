import pandas as pd
import os

# ================= 配置区域 =================

# 1. 你那个“缺数据”的机型表文件名
TARGET_FILE = '匹配结果_带机型.xlsx' 

# 2. 你的原始大屏数据文件（支持模糊匹配，只要文件名包含这个关键词就会被读取）
RAW_DATA_KEYWORD = '深圳到达大屏数据' 

# 3. 机型表里“航班号”这一列的表头名字
TARGET_FLIGHT_COL = '航班号'

# 4. 机型表里“航点/城市”这一列的表头名字（我们要填补这一列）
#    如果你的表里这列叫'航点'，就填'航点'；如果叫'到达地'，就填'到达地'
TARGET_CITY_COL = '航点' 

# ===========================================

def get_city_from_row(row):
    # 尝试从原始数据的不同列名中提取城市
    if '到达地' in row and pd.notnull(row['到达地']):
        return row['到达地']
    if '出发地' in row and pd.notnull(row['出发地']):
        return row['出发地']
    if '航点' in row and pd.notnull(row['航点']):
        return row['航点']
    return None

def main():
    # --- 第一步：构建“航班号 -> 城市”的超级字典 ---
    flight_route_map = {}
    print("正在扫描原始文件构建路由字典...")
    
    files = [f for f in os.listdir('.') if RAW_DATA_KEYWORD in f and f != TARGET_FILE and not f.startswith('~$')]
    
    for f in files:
        try:
            if f.endswith('.csv'):
                df = pd.read_csv(f)
            else:
                # 读取Excel的所有sheet
                dfs = pd.read_excel(f, sheet_name=None)
                df = pd.concat(dfs.values(), ignore_index=True)
            
            # 统一列名查找
            # 找到航班号列（通常叫'航班号'）
            flight_col = None
            for col in df.columns:
                if '航班号' in col:
                    flight_col = col
                    break
            
            if flight_col:
                for _, row in df.iterrows():
                    flight_no = str(row[flight_col]).strip().upper()
                    city = get_city_from_row(row)
                    
                    # 存入字典：如果航班号存在且城市不为空
                    if flight_no and city:
                        flight_route_map[flight_no] = city
                        
        except Exception as e:
            print(f"读取原始文件 {f} 时出错: {e}")

    print(f"✅ 字典构建完成！共收录 {len(flight_route_map)} 个航班的航线信息。")

    # --- 第二步：回填目标文件 ---
    print(f"正在修复目标文件: {TARGET_FILE} ...")
    try:
        target_df = pd.read_excel(TARGET_FILE)
    except:
        print("❌ 找不到目标文件，请检查文件名！")
        return

    # 检查列是否存在，不存在则创建
    if TARGET_CITY_COL not in target_df.columns:
        print(f"⚠️ 目标表中没有 '{TARGET_CITY_COL}' 列，正在新建该列...")
        target_df[TARGET_CITY_COL] = None

    # 开始回填
    filled_count = 0
    
    def fill_city(row):
        nonlocal filled_count
        # 如果当前这一行的城市已经有了，就不动它
        current_city = row[TARGET_CITY_COL]
        if pd.notnull(current_city) and str(current_city).strip() != '':
            return current_city
        
        # 如果是空的，去字典里查
        flight_no = str(row[TARGET_FLIGHT_COL]).strip().upper()
        if flight_no in flight_route_map:
            filled_count += 1
            return flight_route_map[flight_no]
        else:
            return None # 还是查不到

    target_df[TARGET_CITY_COL] = target_df.apply(fill_city, axis=1)

    # --- 第三步：保存 ---
    output_file = '最终完整版_带机型_带航点.xlsx'
    target_df.to_excel(output_file, index=False)
    
    print(f"🎉 修复完成！")
    print(f"共补全了 {filled_count} 条缺失的航点数据。")
    print(f"文件已保存为: {output_file}")

if __name__ == "__main__":
    main()