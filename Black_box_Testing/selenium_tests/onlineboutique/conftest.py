# conftest.py
import pytest
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="选择浏览器: chrome, firefox, edge"
    )
    parser.addoption(
        "--base-url",
        action="store", 
        default="http://127.0.0.1:8080",
        help="Online Boutique系统的基础URL"
    )

@pytest.fixture(scope="session")
def browser_type(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session") 
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(scope="function")
def driver_setup(browser_type):
    """为每个测试函数提供独立的driver实例"""
    
    driver = None
    
    if browser_type.lower() == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")  # 如需无头模式
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
    elif browser_type.lower() == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument("--headless")  # 如需无头模式
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
    elif browser_type.lower() == "edge":
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
    
    else:
        raise ValueError(f"不支持的浏览器类型: {browser_type}")
    
    # 通用配置
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    yield driver
    
    # 清理
    driver.quit()

# 全局性能数据收集
performance_data = []

@pytest.fixture(scope="session", autouse=True)
def performance_reporter():
    """自动收集和报告性能数据"""
    yield
    
    # 测试结束后保存性能数据
    if performance_data:
        os.makedirs("reports", exist_ok=True)
        
        with open("reports/performance_metrics.json", "w") as f:
            json.dump(performance_data, f, indent=2)
        
        print(f"\n性能数据已保存到 reports/performance_metrics.json")
        print(f"共收集 {len(performance_data)} 条性能记录")

def record_performance(page_name, load_time, browser):
    """记录性能数据的辅助函数"""
    performance_record = {
        "page": page_name,
        "load_time": round(load_time, 2),
        "browser": browser,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "fast" if load_time < 3 else "slow"
    }
    performance_data.append(performance_record)
    return performance_record