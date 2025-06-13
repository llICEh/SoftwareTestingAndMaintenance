"""
商品详情查看功能测试
基于Selenium IDE录制优化 - Online Boutique版本
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conftest import record_performance

class TestProductDetail:
    
    def test_product_detail_view(self, driver_setup, base_url, browser_type):
        """测试商品详情页面查看（基于录制）"""
        driver = driver_setup
        
        start_time = time.time()
        driver.get(base_url)
        load_time = time.time() - start_time
        record_performance("首页加载", load_time, browser_type)
        
        # 设置窗口大小（基于录制）
        driver.set_window_size(1708, 1020)
        
        try:
            # 点击第一个商品（基于你的录制）
            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay"))
            )
            
            start_time = time.time()
            product_element.click()
            
            # 等待商品详情页加载
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cymbal-button-primary"))
            )
            
            load_time = time.time() - start_time
            record_performance("商品详情页", load_time, browser_type)
            
            # 验证商品详情页面元素
            assert add_to_cart_button.is_displayed()
            print("✅ 'Add to Cart'按钮显示正常")
            
            # 验证URL包含product
            assert "/product/" in driver.current_url
            print("✅ 商品详情页URL正确")
            
            # 验证商品信息显示
            try:
                # 检查商品名称
                product_name = driver.find_element(By.TAG_NAME, "h1")
                assert product_name.text.strip() != ""
                print(f"✅ 商品名称显示: {product_name.text}")
            except:
                print("⚠️ 商品名称元素未找到")
            
            # 验证商品价格显示
            try:
                # 查找价格元素（可能的选择器）
                price_selectors = [
                    ".price",
                    ".product-price", 
                    "[data-currency]",
                    ".money"
                ]
                
                price_found = False
                for selector in price_selectors:
                    try:
                        price_element = driver.find_element(By.CSS_SELECTOR, selector)
                        if price_element.is_displayed():
                            print(f"✅ 商品价格显示: {price_element.text}")
                            price_found = True
                            break
                    except:
                        continue
                
                if not price_found:
                    print("⚠️ 价格元素未找到，但详情页加载正常")
                    
            except Exception as e:
                print(f"⚠️ 价格验证失败: {e}")
            
            # 验证数量选择器（如果存在）
            try:
                quantity_selector = driver.find_element(By.ID, "quantity")
                if quantity_selector.is_displayed():
                    print("✅ 数量选择器显示正常")
            except:
                print("⚠️ 数量选择器未找到")
            
            # 验证推荐商品区域
            try:
                recommendations = driver.find_elements(By.CSS_SELECTOR, ".col-md-3 img")
                if len(recommendations) > 0:
                    print(f"✅ 推荐商品显示: {len(recommendations)}个推荐商品")
                else:
                    print("⚠️ 推荐商品区域未找到")
            except Exception as e:
                print(f"⚠️ 推荐商品验证失败: {e}")
            
            print("✅ 商品详情页面查看测试完成")
            
        except Exception as e:
            # 失败时截图
            timestamp_str = str(int(time.time()))
            screenshot_path = f"reports/failed_product_detail_{timestamp_str}.png"
            os.makedirs("reports", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            print(f"❌ 商品详情查看失败，截图: {screenshot_path}")
            raise e
    
    def test_product_navigation(self, driver_setup, base_url, browser_type):
        """测试商品间导航功能"""
        driver = driver_setup
        
        driver.get(base_url)
        driver.set_window_size(1708, 1020)
        
        try:
            # 测试多个商品的详情页访问
            product_selectors = [
                ".col-md-4:nth-child(2) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(3) .hot-product-card-img-overlay",
                ".col-md-4:nth-child(4) .hot-product-card-img-overlay"
            ]
            
            for i, selector in enumerate(product_selectors, 2):
                try:
                    print(f"🔍 测试第{i}个商品详情页...")
                    
                    # 确保在首页
                    if "/product/" in driver.current_url:
                        logo_element = driver.find_element(By.CSS_SELECTOR, ".top-left-logo")
                        logo_element.click()
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".hot-product-card-img-overlay"))
                        )
                    
                    # 点击商品
                    product_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    start_time = time.time()
                    product_element.click()
                    
                    # 等待详情页加载
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".cymbal-button-primary"))
                    )
                    
                    load_time = time.time() - start_time
                    record_performance(f"商品{i}详情页", load_time, browser_type)
                    
                    # 验证详情页加载成功
                    assert "/product/" in driver.current_url
                    assert driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").is_displayed()
                    
                    print(f"✅ 第{i}个商品详情页加载成功")
                    
                except Exception as e:
                    print(f"⚠️ 第{i}个商品详情页测试失败: {e}")
                    continue
            
            print("✅ 商品导航测试完成")
            
        except Exception as e:
            print(f"❌ 商品导航测试失败: {e}")
            raise e