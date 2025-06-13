import pytest
import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption("--browser", action="store", default="chrome", help="浏览器类型: chrome, firefox, edge")
    parser.addoption("--base-url", action="store", default="http://127.0.0.1:8080", help="测试基础URL")

@pytest.fixture(scope="session")
def browser_type(request):
    """获取浏览器类型"""
    return request.config.getoption("--browser").lower()

@pytest.fixture(scope="session")
def base_url(request):
    """获取基础URL"""
    return request.config.getoption("--base-url")

@pytest.fixture(scope="function")
def driver_setup(browser_type):
    """设置和清理WebDriver"""
    driver = None
    
    try:
        if browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            # 无头模式可选（如果需要看到浏览器操作可以注释掉）
            # options.add_argument('--headless')
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            # 无头模式可选
            # options.add_argument('--headless')
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
        elif browser_type == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            # 无头模式可选
            # options.add_argument('--headless')
            
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_type}")
        
        # 设置窗口大小和等待时间
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        yield driver
        
    except Exception as e:
        print(f"WebDriver设置失败: {e}")
        raise e
    finally:
        if driver:
            driver.quit()

def record_performance(page_name, load_time, browser_type):
    """
    记录性能数据到JSON文件
    修复版本：正确处理数据累积，避免覆盖
    """
    # 确保reports目录存在
    os.makedirs("reports", exist_ok=True)
    
    perf_file = "reports/performance_metrics.json"
    
    # 创建新的性能数据记录
    perf_data = {
        'timestamp': time.time(),
        'page': page_name,
        'load_time': round(load_time, 3),  # 保留3位小数
        'browser': browser_type,
        'datetime': datetime.now().isoformat(),
        'test_session': datetime.now().strftime('%Y%m%d_%H%M%S')  # 添加测试会话标识
    }
    
    # 读取现有数据
    existing_data = []
    if os.path.exists(perf_file):
        try:
            with open(perf_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # 检查文件是否为空
                    existing_data = json.loads(content)
                    if not isinstance(existing_data, list):
                        existing_data = []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️ 性能数据文件读取警告: {e}")
            existing_data = []
    
    # 添加新数据
    existing_data.append(perf_data)
    
    # 写入文件（使用原子写入方式避免并发问题）
    temp_file = f"{perf_file}.tmp"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        # 原子性替换文件
        if os.path.exists(perf_file):
            os.replace(temp_file, perf_file)
        else:
            os.rename(temp_file, perf_file)
            
        print(f"📊 性能数据已记录: {page_name} - {load_time:.3f}s ({browser_type})")
        
    except Exception as e:
        print(f"❌ 性能数据保存失败: {e}")
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)

def get_performance_summary():
    """获取性能数据摘要"""
    perf_file = "reports/performance_metrics.json"
    
    if not os.path.exists(perf_file):
        return {"total_records": 0, "message": "无性能数据"}
    
    try:
        with open(perf_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            return {"total_records": 0, "message": "性能数据为空"}
        
        # 基本统计
        total_records = len(data)
        browsers = set(record.get('browser', 'unknown') for record in data)
        pages = set(record.get('page', 'unknown') for record in data)
        avg_time = sum(record.get('load_time', 0) for record in data) / total_records
        
        return {
            "total_records": total_records,
            "browsers": list(browsers),
            "pages": len(pages),
            "avg_load_time": round(avg_time, 3),
            "message": f"已记录 {total_records} 条性能数据"
        }
        
    except Exception as e:
        return {"total_records": 0, "message": f"数据读取失败: {e}"}

# 测试会话钩子
def pytest_sessionstart(session):
    """测试会话开始时的钩子"""
    print(f"\n🚀 Selenium测试会话开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示当前性能数据状态
    summary = get_performance_summary()
    print(f"📊 当前性能数据状态: {summary['message']}")

def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时的钩子"""
    print(f"\n✅ Selenium测试会话结束: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示最终性能数据统计
    summary = get_performance_summary()
    print(f"📊 最终性能数据统计:")
    print(f"   总记录数: {summary['total_records']}")
    if summary['total_records'] > 0:
        print(f"   浏览器: {', '.join(summary.get('browsers', []))}")
        print(f"   页面数: {summary.get('pages', 0)}")
        print(f"   平均加载时间: {summary.get('avg_load_time', 0)}s")

# 测试失败时的钩子
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告时的钩子，用于处理失败截图"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # 测试失败时记录额外信息
        test_name = item.name
        timestamp = str(int(time.time()))
        
        # 如果可以访问driver，保存截图
        if hasattr(item, 'funcargs') and 'driver_setup' in item.funcargs:
            driver = item.funcargs['driver_setup']
            try:
                screenshot_path = f"reports/failed_{test_name}_{timestamp}.png"
                driver.save_screenshot(screenshot_path)
                print(f"📸 失败截图已保存: {screenshot_path}")
            except Exception as e:
                print(f"⚠️ 截图保存失败: {e}")

# 自定义标记
def pytest_configure(config):
    """配置自定义标记"""
    config.addinivalue_line(
        "markers", "slow: 标记测试为慢速测试"
    )
    config.addinivalue_line(
        "markers", "smoke: 标记测试为冒烟测试"
    )
    config.addinivalue_line(
        "markers", "regression: 标记测试为回归测试"
    )