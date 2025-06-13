#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正版JMeter测试数据准备脚本
基于前端页面分析结果，确保数据格式与实际API匹配
"""

import csv
import json
import requests
import random
import os
import re
from typing import List, Dict

def create_test_users_csv():
    """创建测试用户数据 - 字段名与HTML表单完全匹配"""
    users_data = []
    
    # 真实的测试城市和州
    cities_states = [
        ('New York', 'NY', '10001'),
        ('Los Angeles', 'CA', '90210'), 
        ('Chicago', 'IL', '60601'),
        ('Houston', 'TX', '77001'),
        ('Phoenix', 'AZ', '85001'),
        ('Philadelphia', 'PA', '19101'),
        ('San Antonio', 'TX', '78201'),
        ('San Diego', 'CA', '92101'),
        ('Dallas', 'TX', '75201'),
        ('San Jose', 'CA', '95101')
    ]
    
    countries = ['United States', 'Canada', 'United Kingdom']
    
    for i in range(1, 101):  # 创建100个测试用户
        city, state, base_zip = random.choice(cities_states)
        zip_code = str(int(base_zip) + i)
        
        user = {
            'user_id': f'user_{i:03d}',
            'email': f'testuser{i}@example.com',
            'first_name': f'Test{i}',
            'last_name': f'User{i}',
            'street_address': f'{i} {random.choice(["Main", "Oak", "Pine", "Elm", "Maple"])} Street',
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'country': random.choice(countries),
            # 使用有效的测试信用卡号
            'credit_card': random.choice([
                '4111111111111111',  # Visa测试卡
                '4000000000000002',  # Visa测试卡
                '5555555555554444',  # MasterCard测试卡
                '4012888888881881'   # Visa测试卡
            ]),
            'exp_month': random.choice([f'{i:02d}' for i in range(1, 13)]),
            'exp_year': random.choice(['2025', '2026', '2027', '2028']),
            'cvv': f'{random.randint(100, 999)}'
        }
        users_data.append(user)
    
    # 保存为CSV
    os.makedirs('data', exist_ok=True)
    with open('data/test_users.csv', 'w', newline='', encoding='utf-8') as f:
        if users_data:
            writer = csv.DictWriter(f, fieldnames=users_data[0].keys())
            writer.writeheader()
            writer.writerows(users_data)
    
    print("✅ 测试用户数据已生成: data/test_users.csv")
    return len(users_data)

def create_products_csv():
    """创建产品数据 - 基于实际Online Boutique产品"""
    
    # 基于前端页面分析的真实产品数据
    real_products = [
        {
            'product_id': 'OLJCESPC7Z',
            'product_name': 'Sunglasses', 
            'price': '19.99',
            'image_file': 'sunglasses.jpg',
            'category': 'accessories'
        },
        {
            'product_id': '66VCHSJNUP',
            'product_name': 'Tank Top',
            'price': '18.99', 
            'image_file': 'tank-top.jpg',
            'category': 'clothing'
        },
        {
            'product_id': '1YMWWN1N4O',
            'product_name': 'Watch',
            'price': '109.99',
            'image_file': 'watch.jpg',
            'category': 'accessories'
        },
        {
            'product_id': 'L9ECAV7KIM',
            'product_name': 'Loafers',
            'price': '89.00',
            'image_file': 'loafers.jpg',
            'category': 'footwear'
        },
        {
            'product_id': '2ZYFJ3GM2N',
            'product_name': 'Hairdryer',
            'price': '24.99',
            'image_file': 'hairdryer.jpg',
            'category': 'electronics'
        },
        {
            'product_id': '0PUK6V6EV0',
            'product_name': 'Candle Holder',
            'price': '18.99',
            'image_file': 'candle-holder.jpg',
            'category': 'home'
        },
        {
            'product_id': 'LS4PSXUNUM',
            'product_name': 'Salt & Pepper Shakers',
            'price': '18.49',
            'image_file': 'salt-and-pepper-shakers.jpg',
            'category': 'kitchen'
        },
        {
            'product_id': '9SIQT8TOJO',
            'product_name': 'Bamboo Glass Jar',
            'price': '5.49',
            'image_file': 'bamboo-glass-jar.jpg',
            'category': 'kitchen'
        },
        {
            'product_id': '6E92ZMYYFZ',
            'product_name': 'Mug',
            'price': '8.99',
            'image_file': 'mug.jpg',
            'category': 'kitchen'
        }
    ]
    
    # 生成测试数据，包含不同数量选项
    products_data = []
    for product in real_products:
        for quantity in [1, 2, 3, 4, 5]:
            products_data.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'price': product['price'],
                'quantity': quantity,
                'category': product['category'],
                'image_file': product['image_file']
            })
    
    # 保存为CSV
    with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
        if products_data:
            writer = csv.DictWriter(f, fieldnames=products_data[0].keys())
            writer.writeheader()
            writer.writerows(products_data)
    
    print(f"✅ 商品数据已生成: data/products.csv ({len(products_data)} 条记录)")
    return len(products_data)

def verify_online_boutique_service(base_url="http://127.0.0.1:8080"):
    """验证Online Boutique服务状态"""
    try:
        print(f"🔍 检查Online Boutique服务: {base_url}")
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Online Boutique服务正常运行")
            
            # 检查是否包含预期的元素
            if 'Online Boutique' in response.text:
                print("✅ 页面内容正常")
                return True
            else:
                print("⚠️ 页面内容可能不正确")
                return False
        else:
            print(f"❌ 服务响应异常: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ 无法连接到服务: {e}")
        print("📋 请确保:")
        print("  1. Online Boutique应用正在运行")
        print("  2. 服务地址为 http://127.0.0.1:8080")
        print("  3. 防火墙没有阻止连接")
        return False

def create_jmx_config_data():
    """创建JMX配置数据"""
    config_data = {
        "test_config": {
            "base_url": "127.0.0.1",
            "port": "8080",
            "protocol": "http"
        },
        "load_profiles": {
            "microservice_comparison": {
                "threads": 20,
                "ramp_time": 60,
                "loop_count": 3,
                "description": "微服务对比测试 - 统一配置"
            },
            "low_load": {
                "threads": 20,
                "ramp_time": 60,
                "duration": 300,
                "description": "低负载基准测试"
            },
            "medium_load": {
                "threads": 50,
                "ramp_time": 120,
                "duration": 600,
                "description": "中负载标准测试"
            },
            "high_load": {
                "threads": 100,
                "ramp_time": 180,
                "duration": 900,
                "description": "高负载压力测试"
            }
        },
        "user_behavior_weights": {
            "browse_only": 70,
            "cart_operations": 20,
            "complete_purchase": 10
        },
        "api_endpoints": {
            "homepage": "/",
            "product_detail": "/product/{product_id}",
            "add_to_cart": "/cart",
            "view_cart": "/cart",
            "checkout": "/cart/checkout",
            "static_css": "/static/styles/styles.css",
            "product_image": "/static/img/products/{image_file}"
        }
    }
    
    # 保存为JSON
    with open('data/jmeter_config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    print("✅ JMeter配置数据已生成: data/jmeter_config.json")

def create_troubleshooting_guide():
    """创建问题排查指南"""
    guide = """# JMeter测试问题排查指南

## 🔧 解决422错误 (Unprocessable Entity)

### 购物车添加操作错误
**问题**: POST /cart 返回422错误
**解决方案**:
1. 确保JMX中设置: postBodyRaw="false"
2. 使用正确的表单参数格式:
   - product_id: ${product_id}  
   - quantity: ${quantity}
3. 添加正确的请求头: Content-Type: application/x-www-form-urlencoded

### 订单提交操作错误  
**问题**: POST /cart/checkout 返回422错误
**解决方案**:
1. 确保所有字段名与HTML表单完全匹配:
   - email
   - street_address
   - zip_code
   - city
   - state
   - country
   - credit_card_number
   - credit_card_expiration_month (不是exp_month)
   - credit_card_expiration_year (不是exp_year)
   - credit_card_cvv

## 🔧 解决404错误 (Not Found)

### 图片文件错误
**问题**: GET /static/img/{product_id}.jpg 返回404错误
**解决方案**:
1. 使用正确的图片路径: /static/img/products/{image_file}
2. 或使用固定图片进行测试: /static/img/products/sunglasses.jpg

## 🔧 通用解决方案

### Cookie会话管理
1. 确保JMX中包含Cookie Manager
2. 设置: clearEachIteration="false"

### 请求头设置
1. 购物车和订单请求需要正确的Content-Type
2. 添加Origin和Referer头信息

### CSV数据验证
1. 确保product_id存在于实际系统中
2. 使用有效的测试信用卡号
3. 地址信息格式正确
"""

    with open('troubleshooting_guide.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ 问题排查指南已生成: troubleshooting_guide.md")

def main():
    """主函数"""
    print("🚀 开始准备修正版JMeter测试数据...")
    print("=" * 60)
    
    # 验证服务状态
    service_ok = verify_online_boutique_service()
    
    # 生成数据文件
    users_count = create_test_users_csv()
    products_count = create_products_csv()
    create_jmx_config_data()
    create_troubleshooting_guide()
    
    print("\n" + "=" * 60)
    print("✅ JMeter测试数据准备完成！")
    print(f"📊 数据统计:")
    print(f"  - 测试用户: {users_count} 个")
    print(f"  - 产品记录: {products_count} 条")
    print(f"📁 生成的文件:")
    print(f"  - data/test_users.csv - 用户测试数据")
    print(f"  - data/products.csv - 产品测试数据")
    print(f"  - data/jmeter_config.json - JMeter配置")
    print(f"  - troubleshooting_guide.md - 问题排查指南")
    
    if not service_ok:
        print(f"\n⚠️ 警告: Online Boutique服务状态异常")
        print(f"   请先启动服务再运行JMeter测试")
    
    print(f"\n💡 下一步:")
    print(f"  1. 检查生成的CSV数据文件")
    print(f"  2. 根据问题排查指南修正JMX文件")
    print(f"  3. 运行单个测试验证修复效果")

if __name__ == "__main__":
    main()