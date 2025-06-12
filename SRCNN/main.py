import os
import pandas as pd
from msanomalydetector import SpectralResidual, THRESHOLD, MAG_WINDOW, SCORE_WINDOW, DetectMode

def detect_anomaly(series, threshold, mag_window, score_window, sensitivity, detect_mode):
    batch_size = 1  # 这里假设用1，视你的数据量和模型需求调整
    detector = SpectralResidual(series=series, threshold=threshold, mag_window=mag_window, score_window=score_window,
                                sensitivity=sensitivity, detect_mode=detect_mode, batch_size=batch_size)
    result_df = detector.detect()
    print(result_df)
    # 保存结果到 CSV 文件，比如保存到当前目录
    result_df.to_csv('anomaly_result.csv', index=False)

if __name__ == '__main__':
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "yahoo/A1Benchmark"))
    for sample_file in os.listdir(sample_dir):
        # 读取csv时加上engine='python'
        sample = pd.read_csv(os.path.join(sample_dir, sample_file), engine='python')
        detect_anomaly(sample, THRESHOLD, MAG_WINDOW, SCORE_WINDOW, 99, DetectMode.anomaly_only)
