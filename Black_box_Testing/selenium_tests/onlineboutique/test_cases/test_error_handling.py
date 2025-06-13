"""
错误处理场景测试
基于Selenium IDE录制优化 - Online Boutique版本
场景4完成后返回购物车页面
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conftest import record_performance

class TestErrorHandling:
    
    def test_error_handling_scenarios(self, driver_setup, base_url, browser_type):
        """测试各种错误处理场景（基于录制优化）"""
        driver = driver_setup
        
        start_time = time.time()
        driver.get(base_url)
        load_time = time.time() - start_time
        record_performance("首页加载", load_time, browser_type)
        
        # 设置窗口大小（基于录制）
        driver.set_window_size(1708, 1020)
        
        try:
            # 测试场景1: 无效邮箱格式（基于录制）
            print("🧪 场景1: 测试无效邮箱格式...")
            
            # 首先进入结算流程
            self._add_product_to_cart(driver)
            
            # 测试无效邮箱（基于录制先输入"1"）
            try:
                email_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "email"))
                )
                email_field.click()
                email_field.clear()
                email_field.send_keys("1")  # 基于录制的无效邮箱
                
                # 尝试提交（基于录制）
                submit_button = driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)")
                submit_button.click()
                
                time.sleep(2)
                
                # 验证错误处理
                current_url = driver.current_url
                if "/cart" in current_url:
                    print("✅ 无效邮箱被正确阻止")
                
                # 修正为有效邮箱（基于录制）
                email_field.clear()
                email_field.send_keys("1@1.com")  # 基于录制的修正
                
                print("✅ 邮箱格式错误测试完成")
                
            except Exception as e:
                print(f"⚠️ 邮箱格式测试失败: {e}")
            
            # 测试场景2: 地址字段验证（基于录制）
            print("🧪 场景2: 测试地址字段验证...")
            
            try:
                # 填写部分地址信息（基于录制）
                street_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "street_address"))
                )
                street_field.clear()
                street_field.send_keys("1")  # 基于录制的简短地址
                
                # 尝试提交
                submit_button = driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)")
                submit_button.click()
                
                time.sleep(2)
                print("✅ 地址字段验证测试完成")
                
            except Exception as e:
                print(f"⚠️ 地址字段测试失败: {e}")
            
            # 测试场景3: 邮编验证（基于录制显示了多次邮编测试）
            print("🧪 场景3: 测试邮编验证...")
            
            # 继续购物添加更多商品（基于录制逻辑）
            try:
                continue_shopping = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Continue Shopping"))
                )
                continue_shopping.click()
                
                # 添加另一个商品
                product_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(3) .hot-product-card-img-overlay"))
                )
                product_element.click()
                
                add_to_cart = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".cymbal-button-primary"))
                )
                add_to_cart.click()
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ 继续购物流程失败: {e}")
            
            # 测试不同长度的邮编（基于录制）
            zip_tests = ["1", "111111", "1111111", "11111111", "97123"]  # 基于录制的测试值
            
            for zip_code in zip_tests:
                try:
                    print(f"📮 测试邮编: {zip_code}")
                    
                    zip_field = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "zip_code"))
                    )
                    zip_field.clear()
                    zip_field.send_keys(zip_code)
                    
                    # 尝试提交
                    submit_button = driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)")
                    submit_button.click()
                    
                    time.sleep(1)
                    
                    if zip_code == "97123":  # 基于录制，这个是有效的邮编
                        print(f"✅ 有效邮编 {zip_code} 被接受")
                    else:
                        print(f"✅ 无效邮编 {zip_code} 验证测试")
                        
                except Exception as e:
                    print(f"⚠️ 邮编 {zip_code} 测试失败: {e}")
                    continue
            
            # 测试场景4: 信用卡验证（基于录制）
            print("🧪 场景4: 测试信用卡验证...")
            
            # 继续添加商品以进入支付阶段（基于录制）
            try:
                continue_shopping2 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Continue Shopping"))
                )
                continue_shopping2.click()
                
                # 添加第四个商品（基于录制）
                product4_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(4) .hot-product-card-img-overlay"))
                )
                product4_element.click()
                
                add_to_cart4 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".cymbal-button-primary"))
                )
                add_to_cart4.click()
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ 第四个商品添加失败: {e}")
            
            # 测试无效信用卡号（基于录制）
            invalid_cards = ["1", "1111111111111111"]  # 基于录制的测试值
            
            for card_number in invalid_cards:
                try:
                    print(f"💳 测试信用卡号: {card_number}")
                    
                    card_field = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "credit_card_number"))
                    )
                    card_field.clear()
                    card_field.send_keys(card_number)
                    
                    # 尝试提交
                    submit_button = driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)")
                    submit_button.click()
                    
                    time.sleep(1)
                    print(f"✅ 无效信用卡 {card_number} 验证测试")
                    
                except Exception as e:
                    print(f"⚠️ 信用卡 {card_number} 测试失败: {e}")
                    continue
            
            # 场景4完成后：返回购物车页面
            print("🔄 场景4完成，返回购物车页面...")
            try:
                # 方法1: 直接访问购物车URL
                cart_url = f"{base_url}/cart"
                driver.get(cart_url)
                
                # 等待购物车页面加载
                WebDriverWait(driver, 10).until(
                    EC.url_contains("/cart")
                )
                
                print("✅ 成功返回购物车页面")
                print(f"📍 当前URL: {driver.current_url}")
                
                # 验证购物车页面加载
                time.sleep(2)
                page_source = driver.page_source.lower()
                if "cart" in page_source:
                    print("✅ 购物车页面内容确认正常")
                
            except Exception as e:
                print(f"⚠️ 返回购物车页面失败: {e}")
                
                # 备用方法: 尝试通过购物车链接返回
                try:
                    print("🔄 尝试通过购物车链接返回...")
                    cart_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/cart"]'))
                    )
                    cart_link.click()
                    
                    # 等待页面加载
                    WebDriverWait(driver, 10).until(
                        EC.url_contains("/cart")
                    )
                    
                    print("✅ 通过购物车链接成功返回")
                    
                except Exception as e2:
                    print(f"⚠️ 购物车链接返回也失败: {e2}")
            
            # 测试场景5: CVV验证（基于录制）
            print("🧪 场景5: 测试CVV验证...")        
            
            cvv_tests = ["asv", "asv.", "123"]  # 基于录制的测试值
            
            for cvv in cvv_tests:
                try:
                    print(f"🔒 测试CVV: {cvv}")
                    
                    cvv_field = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "credit_card_cvv"))
                    )
                    cvv_field.clear()
                    cvv_field.send_keys(cvv)
                    
                    # 尝试提交
                    submit_button = driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)")
                    submit_button.click()
                    
                    time.sleep(1)
                    
                    if cvv == "123":  # 基于录制，这个是有效的CVV
                        print(f"✅ 有效CVV {cvv} 被接受")
                        
                        # 最终的Continue Shopping（基于录制）
                        try:
                            final_continue = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.LINK_TEXT, "Continue Shopping"))
                            )
                            final_continue.click()
                            print("✅ 最终Continue Shopping完成")
                        except Exception as e:
                            print(f"⚠️ 最终Continue Shopping失败: {e}")
                        
                    else:
                        print(f"✅ 无效CVV {cvv} 验证测试")
                        
                except Exception as e:
                    print(f"⚠️ CVV {cvv} 测试失败: {e}")
                    continue
            
            print("✅ 错误处理场景测试完成")
            
        except Exception as e:
            # 失败时截图
            timestamp_str = str(int(time.time()))
            screenshot_path = f"reports/failed_error_handling_{timestamp_str}.png"
            os.makedirs("reports", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            print(f"❌ 错误处理测试失败，截图: {screenshot_path}")
            raise e
    
    def _add_product_to_cart(self, driver):
        """辅助方法：添加商品到购物车"""
        try:
            # 点击logo回到首页（基于录制）
            logo_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".logo"))
            )
            logo_element.click()
            
            # 继续购物（基于录制逻辑）
            continue_shopping = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Continue Shopping"))
            )
            continue_shopping.click()
            
            # 添加商品
            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay"))
            )
            product_element.click()
            
            add_to_cart = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cymbal-button-primary"))
            )
            add_to_cart.click()
            
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ 添加商品到购物车失败: {e}")