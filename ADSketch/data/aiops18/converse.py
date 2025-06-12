# import pickle
# import pandas as pd
# import numpy as np

# def convert_signal_dict_to_csv(pkl_file, csv_file):
#     with open(pkl_file, 'rb') as f:
#         data = pickle.load(f)

#     rows = []
#     for sample_id, value in data.items():
#         if isinstance(value, list) and len(value) == 2:
#             signal, label = value
#             # 确保都是 NumPy 数组，然后转为列表和字符串
#             signal_list = signal.tolist() if isinstance(signal, np.ndarray) else signal
#             label_list = label.tolist() if isinstance(label, np.ndarray) else label

#             rows.append({
#                 "id": sample_id,
#                 "signal": str(signal_list),
#                 "label": str(label_list)
#             })
#         else:
#             print(f"跳过无效结构: {sample_id}")

#     df = pd.DataFrame(rows)
#     df.to_csv(csv_file, index=False)
#     print(f"已保存到 {csv_file}")

# # 示例用法
# convert_signal_dict_to_csv("./test_data_dict.pkl", "output.csv")

import csv
import sys

def add_last_column_with_zero(input_file, output_file=None, new_column_name="new_column"):
    """
    在 CSV 文件最后一列添加全为 0 的数据项
    
    参数:
    input_file (str): 输入 CSV 文件路径
    output_file (str, optional): 输出 CSV 文件路径。若为 None，则覆盖原文件
    new_column_name (str): 新列的表头名称（默认为 "new_column"）
    """
    # 读取 CSV 文件内容
    with open(input_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # 获取表头
        rows = list(reader)    # 获取数据行
    
    # 添加新列名到表头
    header.append(new_column_name)
    # 为所有行添加值为 0 的新列
    for row in rows:
        row.append('0')  # 字符串形式，兼容 CSV 格式
    
    # 写入修改后的内容
    output_path = output_file or input_file
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # 写入表头
        writer.writerows(rows)   # 写入数据行
    
    print(f"已成功在最后一列添加全为 0 的字段，并保存到 {output_path}")

if __name__ == "__main__":
    
    input_file = './data.csv'
    output_file ='./data1.csv'
    new_column_name = sys.argv[3] if len(sys.argv) > 3 else "is_anomaly"  # 默认列名为 "is_anomaly"
    
    add_last_column_with_zero(input_file, output_file, new_column_name)