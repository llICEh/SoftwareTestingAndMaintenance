import pickle
import pandas as pd
import os

def inspect_pkl(pkl_path):
    if not os.path.isfile(pkl_path):
        print(f"文件不存在: {pkl_path}")
        return

    with open(pkl_path, 'rb') as f:
        try:
            obj = pickle.load(f)
        except Exception as e:
            print(f"无法加载pkl文件：{e}")
            return

    print("==== 基本信息 ====")
    print(f"类型: {type(obj)}")

    if isinstance(obj, pd.DataFrame):
        print("DataFrame 概况:")
        print(f"行列数: {obj.shape}")
        print(f"列名: {list(obj.columns)}")
        print("预览数据:")
        print(obj.head())
    
    elif isinstance(obj, dict):
        print(f"字典键数量: {len(obj)}")
        print(f"前5个键: {list(obj.keys())[:5]}")
    
    elif isinstance(obj, list):
        print(f"列表长度: {len(obj)}")
        print("前5个元素类型:", [type(i) for i in obj[:5]])
    
    else:
        print("对象是其他类型，尝试打印其内容（前200字符）:")
        try:
            s = str(obj)
            print(s[:200] + ("..." if len(s) > 200 else ""))
        except Exception as e:
            print(f"无法转换对象为字符串：{e}")

def inspect_dict_values(pkl_file, max_items=5):
    import pickle

    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)

    print(f"字典总共包含 {len(data)} 个键")

    for i, (key, value) in enumerate(data.items()):
        print(f"\n--- 键: {key} ---")
        print(f"类型: {type(value)}")
        try:
            if isinstance(value, dict):
                print(f"子字典键: {list(value.keys())}")
            elif hasattr(value, '__dict__'):
                print(f"对象属性: {dir(value)}")
            else:
                print(f"内容预览: {str(value)[:200]}")
        except Exception as e:
            print(f"无法显示内容: {e}")
        if i + 1 >= max_items:
            break

# 示例调用
if __name__ == "__main__":
    # 替换为你自己的文件路径
    pkl_file = "./test_data_dict.pkl"
    inspect_dict_values(pkl_file)
