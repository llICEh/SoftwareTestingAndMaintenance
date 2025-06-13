# JMeter测试问题排查指南

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
