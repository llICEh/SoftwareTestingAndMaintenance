
#!/usr/bin/env python3
"""
Online Boutique Chrome + Edge 双浏览器测试执行器
专门用于在Chrome和Edge上执行完整测试
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

class OnlineBoutiqueTestRunner:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8080"
        self.browsers = ["chrome", "edge"]
        self.reports_dir = "reports"
        
    def print_header(self, title):
        """打印标题"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def setup_environment(self):
        """设置环境"""
        print("🔧 准备Online Boutique测试环境...")
        
        # 创建报告目录
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # 检查Online Boutique连接
        try:
            import requests
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Online Boutique服务正常 ({self.base_url})")
                
                # 检查页面内容
                if "Online Boutique" in response.text:
                    print("✅ Online Boutique页面内容验证成功")
                else:
                    print("⚠️ 页面内容可能不是预期的Online Boutique")
                    
            else:
                print(f"⚠️ Online Boutique服务状态: {response.status_code}")
        except Exception as e:
            print(f"❌ Online Boutique连接失败: {e}")
            print("请确保Online Boutique已部署并运行在http://127.0.0.1:8080")
            return False
        
        return True
    
    def run_browser_test(self, browser):
        """执行单个浏览器的完整测试"""
        print(f"\n🌐 开始执行 {browser.upper()} 浏览器测试")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 生成报告文件名
        report_file = os.path.join(self.reports_dir, f"{browser}_online_boutique_report.html")
        
        # 构建pytest命令
        cmd = [
            sys.executable, "-m", "pytest",
            "test_cases/",
            f"--browser={browser}",
            f"--base-url={self.base_url}",
            f"--html={report_file}",
            "--self-contained-html",
            "-v", "-s", "--tb=short"
        ]
        
        print("执行命令:")
        print(" ".join(cmd))
        print("=" * 80)
        
        start_time = time.time()
        
        try:
            # 执行测试，实时显示输出
            result = subprocess.run(cmd, timeout=1800)  # 30分钟超时
            
            execution_time = time.time() - start_time
            
            print("=" * 80)
            print(f"⏰ {browser.upper()} 测试执行完成，耗时: {execution_time:.1f}秒")
            
            if result.returncode == 0:
                print(f"✅ {browser.upper()} 所有测试通过")
                status = "success"
            else:
                print(f"⚠️ {browser.upper()} 部分测试失败或有警告")
                status = "partial"
            
            print(f"📄 HTML报告: {report_file}")
            
            return {
                'browser': browser,
                'success': result.returncode == 0,
                'status': status,
                'execution_time': execution_time,
                'report_file': report_file
            }
            
        except subprocess.TimeoutExpired:
            print(f"❌ {browser.upper()} 测试执行超时")
            return {
                'browser': browser,
                'success': False,
                'status': "timeout",
                'execution_time': 0,
                'report_file': report_file
            }
        except KeyboardInterrupt:
            print(f"\n❌ 用户中断 {browser.upper()} 测试")
            return {
                'browser': browser,
                'success': False,
                'status': "interrupted",
                'execution_time': 0,
                'report_file': report_file
            }
        except Exception as e:
            print(f"❌ {browser.upper()} 测试异常: {e}")
            return {
                'browser': browser,
                'success': False,
                'status': "error",
                'execution_time': 0,
                'report_file': report_file
            }
    
    def run_all_browser_tests(self):
        """执行所有浏览器测试"""
        self.print_header("Online Boutique Chrome + Edge 双浏览器测试")
        print(f"目标浏览器: {', '.join([b.upper() for b in self.browsers])}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = []
        total_start_time = time.time()
        
        for i, browser in enumerate(self.browsers):
            result = self.run_browser_test(browser)
            results.append(result)
            
            # 浏览器间间隔
            if i < len(self.browsers) - 1:
                print(f"\n⏳ 等待5秒后继续 {self.browsers[i+1].upper()} 测试...")
                time.sleep(5)
        
        total_time = time.time() - total_start_time
        
        # 显示汇总结果
        self.print_header("测试执行汇总")
        print(f"总耗时: {total_time:.1f}秒 ({total_time/60:.1f}分钟)")
        print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n📊 详细结果:")
        print("-" * 70)
        print(f"{'浏览器':10} | {'状态':10} | {'耗时(秒)':10} | {'报告文件':30}")
        print("-" * 70)
        
        successful_count = 0
        for result in results:
            browser = result['browser'].upper()
            status = "✅ 成功" if result['success'] else "❌ 失败" if result['status'] == 'error' else "⚠️ 超时" if result['status'] == 'timeout' else "🔴 中断"
            exec_time = f"{result['execution_time']:.1f}"
            report = os.path.basename(result['report_file'])
            
            print(f"{browser:10} | {status:10} | {exec_time:10} | {report:30}")
            
            if result['success']:
                successful_count += 1
        
        print("-" * 70)
        print(f"\n📈 成功率: {successful_count}/{len(self.browsers)} ({successful_count/len(self.browsers)*100:.1f}%)")
        
        # 显示报告文件位置
        print(f"\n📁 生成的报告文件:")
        for result in results:
            if os.path.exists(result['report_file']):
                file_size = os.path.getsize(result['report_file'])
                print(f"  {result['browser'].upper()}: {result['report_file']} ({file_size} bytes)")
        
        return results, successful_count > 0
    
    def generate_analysis(self):
        """生成分析报告"""
        print(f"\n📊 生成分析报告...")
        
        analysis_scripts = [
            "utils/analyze_results.py",
            "analyze_results.py"
        ]
        
        for script in analysis_scripts:
            if os.path.exists(script):
                print(f"运行: {script}")
                print("-" * 50)
                
                try:
                    result = subprocess.run([sys.executable, script], timeout=60)
                    
                    print("-" * 50)
                    if result.returncode == 0:
                        print("✅ 分析报告生成成功")
                        
                        # 显示生成的汇总报告
                        summary_file = "reports/online_boutique_summary_report.md"
                        if os.path.exists(summary_file):
                            print(f"📄 汇总报告: {summary_file}")
                        
                        return True
                    else:
                        print("⚠️ 分析报告生成失败")
                        
                except Exception as e:
                    print(f"❌ 分析报告生成异常: {e}")
        
        print("⚠️ 未找到可用的分析脚本")
        return False
    
    def show_final_summary(self, results):
        """显示最终总结"""
        self.print_header("Online Boutique测试总结")
        
        print("🎯 测试完成情况:")
        for result in results:
            browser = result['browser'].upper()
            if result['success']:
                print(f"  ✅ {browser}: 测试完全通过")
            else:
                print(f"  ❌ {browser}: 测试失败或异常")
        
        # 查看报告命令
        print(f"\n🔍 查看测试报告:")
        for result in results:
            if os.path.exists(result['report_file']):
                print(f"  {result['browser'].upper()}: start {result['report_file']}")
        
        # 查看性能数据
        perf_file = "reports/performance_metrics.json"
        if os.path.exists(perf_file):
            try:
                with open(perf_file, 'r', encoding='utf-8') as f:
                    perf_data = json.load(f)
                print(f"\n📊 性能数据: 共收集 {len(perf_data)} 条记录")
                
                # 按浏览器统计
                browser_counts = {}
                for record in perf_data:
                    browser = record.get('browser', 'unknown')
                    browser_counts[browser] = browser_counts.get(browser, 0) + 1
                
                for browser, count in browser_counts.items():
                    print(f"  {browser.upper()}: {count} 条记录")
                    
            except Exception as e:
                print(f"⚠️ 性能数据读取失败: {e}")
        
        # 功能覆盖总结
        print(f"\n🏆 功能覆盖亮点:")
        print("  ✅ 完整的端到端购买流程测试")
        print("  ✅ 多货币转换功能验证")
        print("  ✅ 智能推荐系统测试")
        print("  ✅ 购物车完整功能验证")
        print("  ✅ 错误处理和边界情况测试")

def main():
    """主函数"""
    runner = OnlineBoutiqueTestRunner()
    
    runner.print_header("Online Boutique 双浏览器测试执行器")
    
    # 环境检查
    if not runner.setup_environment():
        print("❌ 环境设置失败")
        sys.exit(1)
    
    try:
        # 执行双浏览器测试
        results, overall_success = runner.run_all_browser_tests()
        
        # 生成分析报告
        if overall_success:
            runner.generate_analysis()
        
        # 显示最终总结
        runner.show_final_summary(results)
        
        # 退出码
        successful_browsers = sum(1 for r in results if r['success'])
        if successful_browsers == len(runner.browsers):
            print("\n🎉 所有浏览器测试都成功完成！")
            sys.exit(0)
        elif successful_browsers > 0:
            print(f"\n⚠️ 部分浏览器测试成功 ({successful_browsers}/{len(runner.browsers)})")
            sys.exit(1)
        else:
            print("\n❌ 所有浏览器测试都失败")
            sys.exit(2)
            
    except KeyboardInterrupt:
        print("\n❌ 用户中断测试执行")
        sys.exit(3)
    except Exception as e:
        print(f"\n❌ 测试执行异常: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
