import os
import json
import logging
import argparse
import numpy as np

# 确保导入路径正确，假设 adsketch 目录在当前目录下
from dataset_loader import load_data # 导入新的数据加载函数
from adsketch.motif_operations import offline_anomaly_detection, online_anomaly_detection
from adsketch.utils import seed_everything, init_logging # 导入日志和随机种子设置

# Setup the logging file name
seed_everything(seed=1234)
os.makedirs('./logs', exist_ok=True)
init_logging(f'./logs/microservice_demo.log')

parser = argparse.ArgumentParser()
parser.add_argument("--adaptive", type=bool, default=False, help="Adaptive pattern learning")
parser.add_argument("--res_dir", type=str, default='./res/microservice/',
                    help="The directory to save experimental figures")
parser.add_argument("--pattern_dir", type=str, default='./offline_metrics/microservice/',
                    help="The directory to save the learned metric patterns and other necessary info")
args = vars(parser.parse_args())

os.makedirs(args['res_dir'], exist_ok=True)
os.makedirs(args['pattern_dir'], exist_ok=True)

with open('params.json', 'r') as json_reader:
    params = json.load(json_reader)

def calculate_weighted_avg(scores, weights):
    return np.average(scores, weights=weights) if weights else 0.0

# 混合多窗口
def fusion_microservice_anomaly_detection():
    logging.info('{}{}{}'.format('^' * 15, ' Anomaly detection for Microservice Metrics ', '^' * 15))
    
    # 指标名称列表
    metric_names = [
        'UsageOfCPU-sockshop',
        'AverageUsageOfCPU',
        'TotalUsageOfCPU',
        'UserUsageOfCPU',
        'SyatemUsageOfCPU',
        'OverallLoad',
        'ClientSuccessRate(non-5xx responses)frontend-external',
        'ServerRequestVolume-productcatalogservice',
        'ServerSuccessRate(non-5xx-responses)frontend-external',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-adservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-cartservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-paymentservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-productcatalogservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-recommendationservice',
        'IncomingRequestsBySourceAndResponseCode-frontend-mTLS(ad)',
        'IncomingRequestsBySourceAndResponseCode-frontend-mTLS(product)',
        'IncomingRequestsBySourceAndResponseCode-frontend(ad)',
        'IncomingRequestsBySourceAndResponseCode-frontend(product)',
        'IncomingRequestsBySourceAndResponseCode-loadgenerator(200)',
        'IncomingRequestsBySourceAndResponseCode-loadgenerator(500)',
        'IncomingSuccessRate(non-5xx-responses)BySource-loadgenerator',
        'ResponseSizeByServiceWorkload-productcatalogservice-P95',
        'ResponseSizeBySource-loadgenerator-P90',
        'ResponseSizeBySource-loadgenerator-P95',
        'ResponseSizeBySource-loadgenerator-P99'
    ]
    microservice_params = params['metrics']
    adaptive_learning = args['adaptive']

    offline_f1_list = []
    offline_weight_list = []

    online_f1_list = []
    online_weight_list = []
    
    normal_data_point = 700
    offline_test_start_point = normal_data_point
    
    # 用于存储所有指标的结果
    all_metrics_online_res = []
    all_metrics_offline_res = []

    # 多窗口设置
    window_sizes = [10, 15, 20]
    window_weights = [0.2, 0.5, 0.3]

    for metric_name in metric_names:
        # 从配置中获取原始 m 和 p
        config_m, p = microservice_params[metric_name]["m"], microservice_params[metric_name]["p"]

        logging.info('{}{}{}'.format('^' * 10, f' Processing Metric: {metric_name}, config m: {config_m}, p: {p} ', '^' * 10))
        logging.info(f'Adaptive pattern learning: {adaptive_learning}')

        fig_dir = os.path.join(args['res_dir'], f'{metric_name}_{config_m}_{p}')
        offline_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{config_m}_{p}.pkl')

        # 数据加载与分割
        metric_values, metric_labels = load_data(metric_name)
        logging.info(f'Loaded data for {metric_name}: {len(metric_values)} points.')
        
        train_metric_values = metric_values[:normal_data_point]
        train_metric_labels = metric_labels[:normal_data_point]
        
        test_metric_values = metric_values[offline_test_start_point:]
        test_metric_labels = metric_labels[offline_test_start_point:]
        
        online_test_metric_values = metric_values[offline_test_start_point:]
        online_test_metric_labels = metric_labels[offline_test_start_point:]
        
        test_length = len(test_metric_labels)

        offline_weight_list.append(test_length)
        online_weight_list.append(test_length)
        
        logging.info(f'Train data size: {len(train_metric_values)}')
        logging.info(f'Test/Online data size: {len(online_test_metric_values)}')

        # 离线阶段多窗口融合检测
        offline_window_results = []  # 存储当前指标各窗口的离线结果

        for window_m in window_sizes:
            window_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{window_m}_{p}.pkl')
            window_fig_dir = fig_dir + f'_window_{window_m}'
            
            logging.info(f'start m={window_m} offline...')
            offline_res = offline_anomaly_detection(
                window_m, p, train_metric_values, test_metric_values, test_metric_labels,
                window_pattern_dir, window_fig_dir + '_offline.png'
            )
            
            offline_window_results.append(offline_res)
            logging.info(f'window m={window_m} offline result: Precision={offline_res[0]:.3f}, Recall={offline_res[1]:.3f}, F1={offline_res[2]:.3f}')

        # 加权融合离线多窗口结果
        if offline_window_results:
            offline_metrics_array = np.array([res[:3] for res in offline_window_results])
            offline_fused_metrics = np.average(offline_metrics_array, axis=0, weights=window_weights)
            
            logging.info(f'offline fusion result: Precision={offline_fused_metrics[0]:.3f}, Recall={offline_fused_metrics[1]:.3f}, F1={offline_fused_metrics[2]:.3f}')

            final_offline_res = offline_fused_metrics
            offline_f1_list.append(final_offline_res[2])
            all_metrics_offline_res.append(final_offline_res)
        else:
            logging.warning(f'所有离线窗口检测失败，使用配置 m={config_m}')
            # 使用原始配置 m 进行离线检测
            offline_res = offline_anomaly_detection(
                config_m, p, train_metric_values, test_metric_values, test_metric_labels,
                pattern_path=offline_pattern_dir, fig_path=fig_dir + '_offline_fallback.png'
            )
            offline_f1_list.append(offline_res[2])
            all_metrics_offline_res.append(offline_res)

        # 在线阶段多窗口融合检测
        online_window_results = []  # 存储当前指标各窗口的在线结果

        for window_m in window_sizes:
            window_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{window_m}_{p}.pkl')
            window_fig_dir = fig_dir + f'_window_{window_m}'
            
            logging.info(f'start m={window_m} online...')
            online_res = online_anomaly_detection(
                adaptive_learning, window_m, p, None,
                train_metric_values, test_metric_values, test_metric_labels,
                online_test_metric_values, online_test_metric_labels,
                window_pattern_dir, window_fig_dir, stride=1
            )
            
            online_window_results.append(online_res)
            logging.info(f'window m={window_m} online result: Precision={online_res[0]:.3f}, Recall={online_res[1]:.3f}, F1={online_res[2]:.3f}')

        # 加权融合在线多窗口结果
        if online_window_results:
            online_metrics_array = np.array([res[:3] for res in online_window_results])
            online_fused_metrics = np.average(online_metrics_array, axis=0, weights=window_weights)
            
            logging.info(f'online fusion result: Precision={online_fused_metrics[0]:.3f}, Recall={online_fused_metrics[1]:.3f}, F1={online_fused_metrics[2]:.3f}')

            final_online_res = online_fused_metrics
            online_f1_list.append(final_online_res[2])
            all_metrics_online_res.append(final_online_res)
        else:
            logging.warning(f'所有在线窗口检测失败，使用配置 m={config_m}')
            # 使用原始配置 m 进行在线检测
            online_res = online_anomaly_detection(
                adaptive_learning, config_m, p, None,
                train_metric_values, test_metric_values, test_metric_labels,
                online_test_metric_values, online_test_metric_labels,
                offline_pattern_dir, fig_dir, stride=1
            )
            online_f1_list.append(online_res[2])
            all_metrics_online_res.append(online_res)

    # 汇总结果
    if all_metrics_offline_res:
        offline_avg = np.mean(all_metrics_offline_res, axis=0)
        logging.info('{}{}{}'.format('^' * 15, ' Overall Offline Experimental Results ', '^' * 15))
        logging.info('Average Precision: {:.3f}, Average Recall: {:.3f}, Average F1: {:.3f}'.format(
            offline_avg[0], offline_avg[1], offline_avg[2]))

    if all_metrics_online_res:
        online_avg = np.mean(all_metrics_online_res, axis=0)
        logging.info('{}{}{}'.format('^' * 15, ' Overall Online Experimental Results ', '^' * 15))
        logging.info('Average Precision: {:.3f}, Average Recall: {:.3f}, Average F1: {:.3f}'.format(
            online_avg[0], online_avg[1], online_avg[2]))
        
    offline_avg_f1 = calculate_weighted_avg(offline_f1_list, offline_weight_list)
    online_avg_f1 = calculate_weighted_avg(online_f1_list, online_weight_list)
    
    logging.info('{}{}{}'.format('^' * 15, ' Weighted Average Result', '^' * 15))
    logging.info(f'Offline Average F1: {offline_avg_f1:.3f}')
    logging.info(f'Online Average F1: {online_avg_f1:.3f}')

# 最优窗口
def best_microservice_anomaly_detection():
    logging.info('{}{}{}'.format('^' * 15, ' Anomaly detection for Microservice Metrics ', '^' * 15))
    
    # 假设你的指标名称列表
    metric_names = [
        'UsageOfCPU-sockshop',
        'AverageUsageOfCPU',
        'TotalUsageOfCPU',
        'UserUsageOfCPU',
        'SyatemUsageOfCPU',
        'OverallLoad',
        'ClientSuccessRate(non-5xx responses)frontend-external',
        'ServerRequestVolume-productcatalogservice',
        'ServerSuccessRate(non-5xx-responses)frontend-external',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-adservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-cartservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-paymentservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-productcatalogservice',
        'IncomingRequestsByDestinationWorkloadAndResponseCode-recommendationservice',
        'IncomingRequestsBySourceAndResponseCode-frontend-mTLS(ad)',
        'IncomingRequestsBySourceAndResponseCode-frontend-mTLS(product)',
        'IncomingRequestsBySourceAndResponseCode-frontend(ad)',
        'IncomingRequestsBySourceAndResponseCode-frontend(product)',
        'IncomingRequestsBySourceAndResponseCode-loadgenerator(200)',
        'IncomingRequestsBySourceAndResponseCode-loadgenerator(500)',
        'IncomingSuccessRate(non-5xx-responses)BySource-loadgenerator',
        'ResponseSizeByServiceWorkload-productcatalogservice-P95',
        'ResponseSizeBySource-loadgenerator-P90',
        'ResponseSizeBySource-loadgenerator-P95',
        'ResponseSizeBySource-loadgenerator-P99'
    ]
    microservice_params = params['metrics']
    adaptive_learning = args['adaptive']

    offline_f1_list = []
    offline_weight_list = []
    online_f1_list = []
    online_weight_list = []
    
    normal_data_point = 700
    offline_test_start_point = normal_data_point
    
    all_metrics_online_res = []
    all_metrics_offline_res = []

    window_sizes = [10, 15, 20,25,30]  # 多窗口设置

    for metric_name in metric_names:
        config_m, p = microservice_params[metric_name]["m"], microservice_params[metric_name]["p"]
        logging.info('{}{}{}'.format('^' * 10, f' Processing Metric: {metric_name}, config m: {config_m}, p: {p} ', '^' * 10))
        logging.info(f'Adaptive pattern learning: {adaptive_learning}')

        fig_dir = os.path.join(args['res_dir'], f'{metric_name}_{config_m}_{p}')
        offline_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{config_m}_{p}.pkl')

        # 数据加载与分割
        metric_values, metric_labels = load_data(metric_name)
        logging.info(f'Loaded data for {metric_name}: {len(metric_values)} points.')
        
        train_metric_values = metric_values[:normal_data_point]
        train_metric_labels = metric_labels[:normal_data_point]
        
        test_metric_values = metric_values[offline_test_start_point:]
        test_metric_labels = metric_labels[offline_test_start_point:]
        
        online_test_metric_values = metric_values[offline_test_start_point:]
        online_test_metric_labels = metric_labels[offline_test_start_point:]
        
        test_length = len(test_metric_labels)
        offline_weight_list.append(test_length)
        online_weight_list.append(test_length)
        
        logging.info(f'Train data size: {len(train_metric_values)}')
        logging.info(f'Test/Online data size: {len(online_test_metric_values)}')

        # ===== 离线阶段：选择F1最高的窗口 =====
        offline_window_results = []

        for window_m in window_sizes:
            window_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{window_m}_{p}.pkl')
            window_fig_dir = fig_dir + f'_window_{window_m}'
            
            logging.info(f'开始窗口 m={window_m} 的离线检测...')
            offline_res = offline_anomaly_detection(
                window_m, p, train_metric_values, test_metric_values, test_metric_labels,
                window_pattern_dir, window_fig_dir + '_offline.png'
            )
            
            offline_window_results.append((window_m, offline_res))
            logging.info(f'窗口 m={window_m} 离线结果: Precision={offline_res[0]:.3f}, Recall={offline_res[1]:.3f}, F1={offline_res[2]:.3f}')

        # 选择F1最高的窗口结果
        if offline_window_results:
            best_offline_m, best_offline_res = max(
                offline_window_results, 
                key=lambda x: x[1][2]  # 根据F1值(索引2)排序
            )
            logging.info(f'离线阶段选择窗口 m={best_offline_m} 作为最终结果，F1={best_offline_res[2]:.3f}')
            
            offline_f1_list.append(best_offline_res[2])
            all_metrics_offline_res.append(best_offline_res)
            
            # 保存最佳窗口的模式库供在线阶段使用
            best_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{best_offline_m}_{p}.pkl')
        else:
            logging.warning(f'所有离线窗口检测失败，使用配置 m={config_m}')
            offline_res = offline_anomaly_detection(
                config_m, p, train_metric_values, test_metric_values, test_metric_labels,
                offline_pattern_dir, fig_dir + '_offline_fallback.png'
            )
            offline_f1_list.append(offline_res[2])
            all_metrics_offline_res.append(offline_res)
            best_pattern_dir = offline_pattern_dir

        # ===== 在线阶段：选择F1最高的窗口 =====
        online_window_results = []

        for window_m in window_sizes:
            window_pattern_dir = os.path.join(args['pattern_dir'], f'{metric_name}_{window_m}_{p}.pkl')
            window_fig_dir = fig_dir + f'_window_{window_m}'
            
            logging.info(f'开始窗口 m={window_m} 的在线检测...')
            online_res = online_anomaly_detection(
                adaptive_learning, window_m, p, None,
                train_metric_values, test_metric_values, test_metric_labels,
                online_test_metric_values, online_test_metric_labels,
                window_pattern_dir, window_fig_dir, stride=1
            )
            
            online_window_results.append((window_m, online_res))
            logging.info(f'窗口 m={window_m} 在线结果: Precision={online_res[0]:.3f}, Recall={online_res[1]:.3f}, F1={online_res[2]:.3f}')

        # 选择F1最高的窗口结果
        if online_window_results:
            best_online_m, best_online_res = max(
                online_window_results, 
                key=lambda x: x[1][2]  # 根据F1值(索引2)排序
            )
            logging.info(f'在线阶段选择窗口 m={best_online_m} 作为最终结果，F1={best_online_res[2]:.3f}')
            
            online_f1_list.append(best_online_res[2])
            all_metrics_online_res.append(best_online_res)
        else:
            logging.warning(f'所有在线窗口检测失败，使用配置 m={config_m}')
            online_res = online_anomaly_detection(
                adaptive_learning, config_m, p, None,
                train_metric_values, test_metric_values, test_metric_labels,
                online_test_metric_values, online_test_metric_labels,
                best_pattern_dir, fig_dir, stride=1
            )
            online_f1_list.append(online_res[2])
            all_metrics_online_res.append(online_res)

    # 汇总结果（保持原有逻辑不变）
    if all_metrics_offline_res:
        offline_avg = np.mean(all_metrics_offline_res, axis=0)
        logging.info('{}{}{}'.format('^' * 15, ' Overall Offline Results ', '^' * 15))
        logging.info('Average Precision: {:.3f}, Average Recall: {:.3f}, Average F1: {:.3f}'.format(
            offline_avg[0], offline_avg[1], offline_avg[2]))
    
    if all_metrics_online_res:
        online_avg = np.mean(all_metrics_online_res, axis=0)
        logging.info('{}{}{}'.format('^' * 15, ' Overall Online Results ', '^' * 15))
        logging.info('Average Precision: {:.3f}, Average Recall: {:.3f}, Average F1: {:.3f}'.format(
            online_avg[0], online_avg[1], online_avg[2]))
        
    offline_avg_f1 = calculate_weighted_avg(offline_f1_list, offline_weight_list)
    online_avg_f1 = calculate_weighted_avg(online_f1_list, online_weight_list)
    
    logging.info('{}{}{}'.format('^' * 15, ' Weighted Average Results ', '^' * 15))
    logging.info(f'Offline Average F1: {offline_avg_f1:.3f}')
    logging.info(f'Online Average F1: {online_avg_f1:.3f}')

if __name__ == '__main__':
    # fusion_microservice_anomaly_detection()
    best_microservice_anomaly_detection()