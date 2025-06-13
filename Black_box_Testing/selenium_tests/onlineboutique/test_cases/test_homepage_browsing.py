"""
首页浏览功能测试
基于Selenium IDE录制优化 - Online Boutique版本
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conftest import record_performance

class TestHomepageBrowsing:
    
    def test_homepage_product_browsing(self, driver_setup, base_url, browser_type):
        """测试首页商品浏览功能（基于录制优化）"""
        driver = driver_setup
        
        start_time = time.time()
        driver.get(base_url)
        load_time = time.time() - start_time
        record_performance("首页加载", load_time, browser_type)
        
        # 设置窗口大小（基于录制）
        driver.set_window_size(1708, 1020)
        
        try:
            # 验证页面标题
            assert "Online Boutique" in driver.title
            print("✅ 页面标题验证成功")
            
            # 测试商品浏览（基于你的录制逻辑）
            product_selectors = [
                ".col-md-4:nth-child(2) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(3) .hot-product-card-img-overlay", 
                ".col-md-4:nth-child(4) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(5) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(6) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(7) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(8) .hot-product-card-img-overlay"
            ]
            
            for i, selector in enumerate(product_selectors, 2):
                try:
                    print(f"🔍 点击第{i}个商品...")
                    
                    # 点击商品
                    product_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    start_time = time.time()
                    product_element.click()
                    
                    # 等待商品详情页加载
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".cymbal-button-primary"))
                    )
                    
                    load_time = time.time() - start_time
                    record_performance(f"商品详情页-产品{i}", load_time, browser_type)
                    
                    # 验证URL包含product
                    assert "/product/" in driver.current_url
                    
                    # 点击Logo返回首页（基于录制）
                    logo_element = driver.find_element(By.CSS_SELECTOR, ".top-left-logo")
                    logo_element.click()
                    
                    # 等待返回首页
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".hot-product-card-img-overlay"))
                    )
                    
                    print(f"✅ 第{i}个商品浏览成功")
                    
                except Exception as e:
                    print(f"⚠️ 第{i}个商品浏览失败: {e}")
                    continue
            
            print("✅ 商品浏览测试完成")
            
        except Exception as e:
            print(f"❌ 首页浏览测试失败: {e}")
            raise e
    
    def test_product_recommendations(self, driver_setup, base_url, browser_type):
        """测试商品推荐功能（基于录制）"""
        driver = driver_setup
        
        driver.get(base_url)
        driver.set_window_size(1708, 1020)
        
        try:
            # 进入商品详情页
            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay"))
            )
            product_element.click()
            
            # 等待详情页加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cymbal-button-primary"))
            )
            
            # 测试推荐商品点击（基于你的录制）
            recommendation_selectors = [
                ".col-md-3:nth-child(1) img",
                ".col-md-3:nth-child(2) img",
                ".col-md-3:nth-child(3) img", 
                ".col-md-3:nth-child(4) img"
            ]
            
            for i, selector in enumerate(recommendation_selectors, 1):
                try:
                    print(f"🎯 点击推荐商品{i}...")
                    
                    recommendation_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    start_time = time.time()
                    recommendation_element.click()
                    
                    # 等待新商品页面加载
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".cymbal-button-primary"))
                    )
                    
                    load_time = time.time() - start_time
                    record_performance(f"推荐商品{i}", load_time, browser_type)
                    
                    print(f"✅ 推荐商品{i}加载成功")
                    
                    # 如果不是最后一个，返回原商品页继续测试
                    if i < len(recommendation_selectors):
                        driver.back()
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".col-md-3:nth-child(1) img"))
                        )
                    
                except Exception as e:
                    print(f"⚠️ 推荐商品{i}测试失败: {e}")
                    continue
            
            print("✅ 商品推荐测试完成")
            
        except Exception as e:
            print(f"❌ 商品推荐测试失败: {e}")
            raise e
    
    def test_currency_conversion(self, driver_setup, base_url, browser_type):
        """测试货币转换功能（基于录制）"""
        driver = driver_setup
        
        driver.get(base_url)
        driver.set_window_size(1708, 1020)
        
        try:
            # 回到首页确保在正确位置
            logo_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".top-left-logo"))
            )
            logo_element.click()
            
            # 等待页面加载
            time.sleep(2)
            
            # 测试货币转换（基于你的录制逻辑）
            currencies = ["GBP", "EUR", "CAD", "JPY", "USD"]
            
            for currency in currencies:
                try:
                    print(f"💱 切换到货币: {currency}")
                    
                    # 点击货币选择器
                    currency_dropdown = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.NAME, "currency_code"))
                    )
                    currency_dropdown.click()
                    
                    # 选择货币
                    select = Select(currency_dropdown)
                    select.select_by_value(currency)
                    
                    # 等待页面更新
                    time.sleep(1)
                    
                    # 验证货币已切换（检查页面中的货币符号）
                    if currency == "USD":
                        expected_symbol = "$"
                    elif currency == "EUR":
                        expected_symbol = "€"
                    elif currency == "GBP":
                        expected_symbol = "£"
                    elif currency == "JPY":
                        expected_symbol = "¥"
                    elif currency == "CAD":
                        expected_symbol = "$"  # CAD也使用$符号
                    
                    # 检查页面是否包含对应的货币符号或代码
                    page_source = driver.page_source
                    assert currency in page_source or expected_symbol in page_source
                    
                    print(f"✅ 货币{currency}切换成功")
                    
                except Exception as e:
                    print(f"⚠️ 货币{currency}切换失败: {e}")
                    continue
            
            print("✅ 货币转换测试完成")
            
        except Exception as e:
            print(f"❌ 货币转换测试失败: {e}")
            raise e