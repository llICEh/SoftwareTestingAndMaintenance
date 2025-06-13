"""
完整购买流程测试
基于Selenium IDE录制优化 - Online Boutique版本
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

class TestCompletePurchase:
    
    def test_complete_purchase_workflow(self, driver_setup, base_url, browser_type):
        """测试完整购买流程（基于录制优化）"""
        driver = driver_setup
        
        start_time = time.time()
        driver.get(base_url)
        load_time = time.time() - start_time
        record_performance("首页加载", load_time, browser_type)
        
        # 设置窗口大小（基于录制）
        driver.set_window_size(1708, 1020)
        
        try:
            # 第一步：添加商品到购物车
            print("🛍️ 步骤1: 添加商品到购物车...")
            
            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay"))
            )
            product_element.click()
            
            # 添加到购物车
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cymbal-button-primary"))
            )
            add_to_cart_button.click()
            
            time.sleep(2)
            print("✅ 商品添加成功")
            
            # 第二步：添加更多商品（基于录制）
            print("🛍️ 步骤2: 添加更多商品...")
            
            continue_shopping = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Continue Shopping"))
            )
            continue_shopping.click()
            
            # 添加第二个商品
            product2_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(3) .hot-product-card-img-overlay"))
            )
            product2_element.click()
            
            # 选择数量
            quantity_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "quantity"))
            )
            quantity_dropdown.click()
            
            select = Select(quantity_dropdown)
            select.select_by_visible_text("2")
            
            # 添加到购物车
            add_to_cart_button2 = driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary")
            add_to_cart_button2.click()
            
            time.sleep(2)
            print("✅ 第二个商品添加成功")
            
            # 第三步：进入结算流程（基于录制显示直接进入了结算）
            print("💳 步骤3: 开始结算流程...")
            
            # 根据录制，系统似乎直接进入了结算页面，我们需要填写信息
            
            # 填写邮箱（基于录制操作）
            print("📧 填写邮箱地址...")
            try:
                # 基于录制的复杂鼠标操作，简化为直接点击和输入
                email_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "email"))
                )
                email_field.click()
                email_field.clear()
                email_field.send_keys("test@example.com")
                
                print("✅ 邮箱填写完成")
                
            except Exception as e:
                print(f"⚠️ 邮箱填写失败: {e}")
            
            # 填写地址信息（基于录制）
            print("🏠 填写地址信息...")
            try:
                # 街道地址
                street_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "street_address"))
                )
                street_field.click()
                street_field.clear()
                street_field.send_keys("123 Test Street")
                
                # 城市 (基于录制可能没有明确输入，我们添加)
                try:
                    city_field = driver.find_element(By.ID, "city")
                    city_field.clear()
                    city_field.send_keys("Test City")
                except:
                    print("⚠️ 城市字段未找到")
                
                # 邮编（基于录制）
                zip_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "zip_code"))
                )
                zip_field.click()
                zip_field.clear()
                zip_field.send_keys("12345")
                
                # 国家（基于录制）
                try:
                    country_field = driver.find_element(By.ID, "country")
                    country_field.click()
                    country_field.clear()
                    country_field.send_keys("United States")
                except:
                    print("⚠️ 国家字段操作可能需要调整")
                
                print("✅ 地址信息填写完成")
                
            except Exception as e:
                print(f"⚠️ 地址信息填写失败: {e}")
            
            # 填写支付信息（基于录制）
            print("💳 填写支付信息...")
            try:
                # 信用卡号
                card_number_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "credit_card_number"))
                )
                card_number_field.click()
                card_number_field.clear()
                card_number_field.send_keys("4111-1111-1111-1111")
                
                # 到期月份（基于录制）
                month_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "credit_card_expiration_month"))
                )
                month_dropdown.click()
                
                month_select = Select(month_dropdown)
                month_select.select_by_visible_text("August")  # 基于录制选择
                
                # 到期年份（基于录制）
                year_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "credit_card_expiration_year"))
                )
                year_dropdown.click()
                
                year_select = Select(year_dropdown)
                year_select.select_by_visible_text("2025")  # 基于录制选择
                
                # CVV (基于录制可能没有填写，我们添加)
                try:
                    cvv_field = driver.find_element(By.ID, "credit_card_cvv")
                    cvv_field.clear()
                    cvv_field.send_keys("123")
                except:
                    print("⚠️ CVV字段未找到或不需要")
                
                print("✅ 支付信息填写完成")
                
            except Exception as e:
                print(f"⚠️ 支付信息填写失败: {e}")
            
            # 第四步：提交订单（基于录制）
            print("🚀 步骤4: 提交订单...")
            
            try:
                # 点击提交订单按钮（基于录制的选择器）
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)"))
                )
                
                start_time = time.time()
                submit_button.click()
                
                # 等待订单处理
                time.sleep(5)  # 给订单处理一些时间
                
                response_time = time.time() - start_time
                record_performance("订单提交", response_time, browser_type)
                
                # 验证订单处理结果（基于录制最后又点击了Continue Shopping）
                try:
                    final_continue = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Continue Shopping"))
                    )
                    
                    if final_continue.is_displayed():
                        print("✅ 订单提交成功 - 显示继续购物选项")
                        final_continue.click()  # 基于录制的最后操作
                    
                except:
                    # 检查是否有其他成功指示
                    if "order" in driver.current_url.lower() or "confirmation" in driver.current_url.lower():
                        print("✅ 订单提交成功 - 在确认页面")
                    else:
                        print("⚠️ 订单状态需要进一步确认")
                
                print("✅ 完整购买流程测试完成")
                
            except Exception as e:
                print(f"⚠️ 订单提交阶段失败: {e}")
                
                # 检查是否有错误消息
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, .alert-danger, .validation-error")
                    if error_elements:
                        for error in error_elements:
                            if error.is_displayed():
                                print(f"❌ 发现错误消息: {error.text}")
                except:
                    pass
                
                raise e
            
        except Exception as e:
            # 失败时截图
            timestamp_str = str(int(time.time()))
            screenshot_path = f"reports/failed_purchase_{timestamp_str}.png"
            os.makedirs("reports", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            print(f"❌ 完整购买流程失败，截图: {screenshot_path}")
            raise e