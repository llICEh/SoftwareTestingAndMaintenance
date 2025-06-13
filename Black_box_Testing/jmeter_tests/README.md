# Online Boutique 性能测试套件

基于JMeter的Online Boutique微服务应用综合性能测试方案，包含微服务对比测试和混合负载梯度测试。

## 📋 目录

- [测试概述](#测试概述)
- [环境准备](#环境准备)
- [测试架构](#测试架构)
- [实验配置详解](#实验配置详解)
- [执行指南](#执行指南)
- [结果分析](#结果分析)
- [故障排除](#故障排除)

## 🎯 测试概述

### 测试目标
- **微服务性能基准**：建立各个微服务的性能基线
- **负载能力评估**：测试系统在不同负载下的表现
- **性能瓶颈识别**：定位系统性能瓶颈和优化点
- **可扩展性验证**：验证系统的横向扩展能力

### 测试范围
- 前端静态资源加载性能
- 商品服务查询性能
- 购物车CRUD操作性能
- 订单处理业务性能
- 混合业务场景下的系统表现

## 🛠 环境准备

### 软件要求
- **JMeter 5.6.3+**：性能测试工具
- **Java 8+**：JMeter运行环境
- **Online Boutique应用**：被测试系统

### 目录结构
```
performance_testing/
├── test_plans/
│   └── online_boutique_performance_optimized.jmx
├── data/
│   ├── test_users.csv
│   └── products.csv
├── test_results/          # 测试原始数据输出
└── test_reports/          # HTML报告输出
```

### 数据文件准备

#### test_users.csv
```csv
user_id,email,first_name,last_name,street_address,city,state,zip_code,country,credit_card,exp_month,exp_year,cvv
1,john.doe@example.com,John,Doe,123 Main St,New York,NY,10001,US,4111111111111111,12,2025,123
2,jane.smith@example.com,Jane,Smith,456 Oak Ave,Los Angeles,CA,90210,US,4222222222222222,11,2024,456
```

#### products.csv
```csv
product_id,product_name,price,quantity,category
OLJCESPC7Z,Sunglasses,19.99,2,accessories
66VCHSJNUP,Tank Top,18.99,1,clothing
1YMWWN1N4O,Watch,109.99,1,accessories
```

## 🏗 测试架构

### 线程组架构
```
第一部分：微服务对比测试（统一配置对比）
├── 线程组1：首页浏览性能基准
├── 线程组2：商品服务性能测试  
├── 线程组3：购物车服务性能测试
└── 线程组4：订单服务性能测试

第二部分：混合负载梯度测试（压力测试）
├── 线程组5A：低负载基准测试
├── 线程组5B：中负载标准测试
└── 线程组5C：高负载压力测试
```

### 权重控制器设计
混合负载测试使用权重控制器模拟真实用户行为：
- **浏览行为 (70%)**：只浏览不购买
- **购物车操作 (20%)**：添加商品到购物车但不结账
- **完成购买 (10%)**：完整的购买流程

## 🔬 实验配置详解

### 第一阶段：微服务对比测试

#### 1.1 首页浏览性能基准测试
**目标**：建立前端静态资源加载的性能基线

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 20 | 并发用户数 |
| 启动时间 | 60秒 | 逐步增加负载 |
| 循环次数 | 3 | 每个用户执行3次完整流程 |
| 总时长 | ~4分钟 | 预估执行时间 |

**请求流程**：
1. 访问首页 (`/`) - 测试前端渲染性能
2. 加载CSS文件 (`/static/styles/styles.css`) - 测试静态资源服务
3. 思考时间：1-3秒随机延迟

**关键指标**：
- 首页响应时间
- 静态资源加载时间
- 页面渲染完成时间

#### 1.2 商品服务性能测试
**目标**：评估商品查询和图片加载服务的性能

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 20 | 与基准测试保持一致 |
| 启动时间 | 60秒 | 相同的负载模式 |
| 循环次数 | 3 | 相同的测试强度 |

**请求流程**：
1. 访问首页 (`/`) - 建立会话
2. 商品详情查询 (`/product/${product_id}`) - 核心业务逻辑
3. 商品图片加载 (`/static/img/${product_id}.jpg`) - 图片服务性能
4. 思考时间：1-3秒

**关键指标**：
- 商品查询响应时间
- 数据库查询性能
- 图片服务响应时间

#### 1.3 购物车服务性能测试
**目标**：测试CRUD操作和会话管理性能

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 20 | 保持测试一致性 |
| 启动时间 | 60秒 | 相同负载曲线 |
| 循环次数 | 3 | 足够的样本数据 |

**请求流程**：
1. 访问首页 (`/`) - 会话初始化
2. 浏览商品 (`/product/${product_id}`) - 选择商品
3. **添加到购物车** (`POST /cart`) - **核心测试点**
4. 查看购物车 (`GET /cart`) - 数据一致性验证
5. 思考时间：1-3秒

**关键指标**：
- 购物车添加操作响应时间
- 购物车查询性能
- 会话数据一致性

#### 1.4 订单服务性能测试
**目标**：测试最复杂的业务流程性能

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 20 | 相同基准配置 |
| 启动时间 | 60秒 | 一致的负载模式 |
| 循环次数 | 3 | 完整业务验证 |

**请求流程**：
1. 访问首页 (`/`) 
2. 浏览商品 (`/product/${product_id}`)
3. 添加到购物车 (`POST /cart`)
4. 查看购物车 (`GET /cart`)
5. **提交订单** (`POST /cart/checkout`) - **最关键测试点**

**订单数据包含**：
- 用户信息：邮箱、姓名
- 配送地址：街道、城市、州、邮编、国家
- 支付信息：信用卡号、过期时间、CVV

**关键指标**：
- 订单提交响应时间
- 支付处理性能
- 数据库事务处理时间

### 第二阶段：混合负载梯度测试

#### 2.1 低负载基准测试
**目标**：建立系统正常运行状态的性能基线

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 20 | 轻度负载 |
| 启动时间 | 60秒 | 平缓启动 |
| 持续时间 | 300秒 (5分钟) | 稳定运行时间 |
| 总时长 | ~6分钟 | 包含启动时间 |

**行为权重分配**：
- 浏览行为：70% - 模拟大部分用户只浏览
- 购物车操作：20% - 模拟用户加购物车
- 完成购买：10% - 模拟实际购买转化

**关键指标**：
- 系统基准吞吐量
- 稳定状态下的响应时间
- 资源利用率基线

#### 2.2 中负载标准测试
**目标**：测试系统在标准业务负载下的表现

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 50 | 中等负载强度 |
| 启动时间 | 120秒 | 更长的启动时间分散压力 |
| 持续时间 | 600秒 (10分钟) | 充分的稳定运行时间 |
| 总时长 | ~12分钟 | 标准测试时长 |

**负载特点**：
- 用户数提升2.5倍
- 更长的持续时间验证稳定性
- 相同的业务行为权重分配

**关键指标**：
- 负载增加后的性能衰减
- 系统稳定性验证
- 资源瓶颈初步显现

#### 2.3 高负载压力测试
**目标**：找到系统性能边界和瓶颈点

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 线程数 | 100 | 高压力测试 |
| 启动时间 | 180秒 | 最长启动时间避免冲击 |
| 持续时间 | 900秒 (15分钟) | 长时间压力测试 |
| 总时长 | ~18分钟 | 最长测试周期 |
| 思考时间 | 0.5-2秒 | 模拟急迫用户，增加压力 |

**压力特点**：
- 用户数是基准的5倍
- 思考时间缩短模拟高频访问
- 长时间持续验证系统稳定性

**关键指标**：
- 系统性能极限
- 错误率变化趋势
- 资源瓶颈识别
- 系统恢复能力

## 🚀 执行指南

### 前置准备
```cmd
# 创建必要目录
mkdir test_results test_reports data

# 确认JMeter安装
jmeter -v
```

### 分阶段执行（推荐）

#### 第一阶段：微服务对比测试

**1. 首页基准测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/homepage_baseline_test.jtl" -e -o "test_reports/homepage_baseline_report"

**2. 商品服务测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/product_service_test.jtl" -e -o "test_reports/product_service_report"
```

**3. 购物车服务测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/cart_service_test.jtl" -e -o "test_reports/cart_service_report"
```

**4. 订单服务测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/order_service_test.jtl" -e -o "test_reports/order_service_report"
```

#### 第二阶段：混合负载梯度测试

**5. 低负载基准测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/mixed_load_low_test.jtl" -e -o "test_reports/mixed_load_low_report"
```

**6. 中负载标准测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/mixed_load_medium_test.jtl" -e -o "test_reports/mixed_load_medium_report"
```

**7. 高负载压力测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/mixed_load_high_test.jtl" -e -o "test_reports/mixed_load_high_report"
```


**8. 极限压力测试**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/mixed_load_extreme_test.jtl" -e -o "test_reports/mixed_load_extreme_report"
```


### 批量执行选项

**微服务对比测试（一次性执行）**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/microservice_comparison_test.jtl" -e -o "test_reports/microservice_comparison_report"
```

**混合负载测试（一次性执行）**
```cmd
jmeter -n -t "test_plans/online_boutique_performance_optimized.jmx" -l "test_results/mixed_load_gradient_test.jtl" -e -o "test_reports/mixed_load_gradient_report"

## 📊 结果分析

### 报告位置
所有HTML报告生成在 `test_reports/` 目录下，每个测试都有独立的报告文件夹，主要查看各文件夹中的 `index.html`。

### 关键指标说明

#### 响应时间指标
- **Average**：平均响应时间 - 系统整体性能指标
- **Median**：中位数响应时间 - 大多数用户的实际体验
- **90% Line**：90%用户的响应时间 - 性能稳定性指标
- **95% Line**：95%用户的响应时间 - 极端情况处理能力
- **99% Line**：99%用户的响应时间 - 最差情况性能

#### 吞吐量指标
- **Throughput**：每秒处理请求数 - 系统处理能力
- **Received KB/sec**：每秒接收数据量 - 网络性能
- **Sent KB/sec**：每秒发送数据量 - 网络负载

#### 错误率指标
- **Error %**：错误百分比 - 系统稳定性
- **Error Count**：错误总数 - 问题严重程度

### 对比分析重点

#### 微服务性能对比
1. **首页 vs 商品服务**：静态资源 vs 动态查询性能差异
2. **商品服务 vs 购物车服务**：读操作 vs 写操作性能差异  
3. **购物车 vs 订单服务**：简单CRUD vs 复杂业务流程性能差异

#### 负载梯度分析
1. **响应时间变化趋势**：负载增加时的性能衰减曲线
2. **吞吐量饱和点**：系统最大处理能力
3. **错误率拐点**：系统开始不稳定的负载阈值

## ❓ 故障排除

### 常见问题

#### JMeter路径问题
```cmd
# 错误：'jmeter' 不是内部或外部命令
# 解决：使用完整路径
C:\apache-jmeter-5.6.3\bin\jmeter.bat -n -t ...
```

#### 数据文件缺失
```
错误：Cannot resolve file: data/test_users.csv
解决：确保CSV文件存在且路径正确
```

#### 服务连接失败
```
错误：Connection refused
解决：确认Online Boutique服务运行在127.0.0.1:8080
```

#### 内存不足
```cmd
# 增加JMeter内存
set JVM_ARGS=-Xmx4g
jmeter -n -t ...
```

### 性能调优建议

#### 系统级优化
- 增加数据库连接池大小
- 优化静态资源缓存策略
- 启用数据库查询缓存
- 考虑CDN加速图片加载

#### 应用级优化
- 优化商品查询SQL
- 购物车数据采用Redis缓存
- 订单处理采用异步队列
- 实施接口限流和熔断

## 📝 总结

这套测试方案通过系统性的实验设计，能够：

1. **建立性能基线**：通过微服务对比测试建立各组件的性能基准
2. **识别性能瓶颈**：通过梯度负载测试找到系统瓶颈点
3. **验证扩展能力**：评估系统在不同负载下的表现
4. **指导优化方向**：为系统优化提供数据支撑

建议按照分阶段执行的方式进行测试，这样能够更好地控制测试过程，及时发现和解决问题。


```
jmeter_tests
├─ data
│  ├─ jmeter_config.json
│  ├─ products.csv
│  ├─ scenarios.json
│  └─ test_users.csv
├─ jmeter.log
├─ README.md
├─ results
│  ├─ aggregate_graph.jtl
│  ├─ detailed_results.jtl
│  └─ summary_report.jtl
├─ scripts
│  └─ prepare_jmeter_data.py
├─ test_plans
│  ├─ debug_cart.jmx
│  ├─ online_boutique_performance.jmx
│  ├─ online_boutique_performance_optimized copy.jmx
│  └─ online_boutique_performance_optimized.jmx
├─ test_reports
│  ├─ cart_service_report
│  │  ├─ content
│  │  │  ├─ css
│  │  │  │  ├─ dashboard.css
│  │  │  │  ├─ jquery-ui.min.css
│  │  │  │  ├─ jquery-ui.structure.min.css
│  │  │  │  ├─ jquery-ui.theme.min.css
│  │  │  │  ├─ legends.css
│  │  │  │  └─ theme.blue.css
│  │  │  ├─ js
│  │  │  │  ├─ curvedLines.js
│  │  │  │  ├─ customGraph.js
│  │  │  │  ├─ dashboard-commons.js
│  │  │  │  ├─ dashboard.js
│  │  │  │  ├─ graph.js
│  │  │  │  ├─ hashtable.js
│  │  │  │  ├─ jquery-ui.min.js
│  │  │  │  ├─ jquery.cookie.js
│  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  ├─ jquery.numberformatter-1.2.3.min.js
│  │  │  │  └─ jquery.tablesorter.min.js
│  │  │  └─ pages
│  │  │     ├─ CustomsGraphs.html
│  │  │     ├─ icon-apache.png
│  │  │     ├─ OverTime.html
│  │  │     ├─ ResponseTimes.html
│  │  │     └─ Throughput.html
│  │  ├─ index.html
│  │  ├─ sbadmin2-1.0.7
│  │  │  ├─ bower.json
│  │  │  ├─ bower_components
│  │  │  │  ├─ bootstrap
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ dist
│  │  │  │  │  │  ├─ css
│  │  │  │  │  │  │  └─ bootstrap.min.css
│  │  │  │  │  │  ├─ fonts
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│  │  │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│  │  │  │  │  │  └─ js
│  │  │  │  │  │     └─ bootstrap.min.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .travis.yml
│  │  │  │  │  ├─ API.md
│  │  │  │  │  ├─ component.json
│  │  │  │  │  ├─ CONTRIBUTING.md
│  │  │  │  │  ├─ excanvas.js
│  │  │  │  │  ├─ excanvas.min.js
│  │  │  │  │  ├─ FAQ.md
│  │  │  │  │  ├─ flot.jquery.json
│  │  │  │  │  ├─ jquery.colorhelpers.js
│  │  │  │  │  ├─ jquery.flot.canvas.js
│  │  │  │  │  ├─ jquery.flot.categories.js
│  │  │  │  │  ├─ jquery.flot.crosshair.js
│  │  │  │  │  ├─ jquery.flot.errorbars.js
│  │  │  │  │  ├─ jquery.flot.fillbetween.js
│  │  │  │  │  ├─ jquery.flot.image.js
│  │  │  │  │  ├─ jquery.flot.js
│  │  │  │  │  ├─ jquery.flot.navigate.js
│  │  │  │  │  ├─ jquery.flot.pie.js
│  │  │  │  │  ├─ jquery.flot.resize.js
│  │  │  │  │  ├─ jquery.flot.selection.js
│  │  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  │  ├─ jquery.flot.symbol.js
│  │  │  │  │  ├─ jquery.flot.threshold.js
│  │  │  │  │  ├─ jquery.flot.time.js
│  │  │  │  │  ├─ Makefile
│  │  │  │  │  ├─ NEWS.md
│  │  │  │  │  ├─ package.json
│  │  │  │  │  ├─ PLUGINS.md
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot-axislabels
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ jquery.flot.axislabels.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot.tooltip
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ js
│  │  │  │  │     ├─ excanvas.min.js
│  │  │  │  │     ├─ jquery.flot.js
│  │  │  │  │     ├─ jquery.flot.tooltip.js
│  │  │  │  │     ├─ jquery.flot.tooltip.min.js
│  │  │  │  │     └─ jquery.flot.tooltip.source.js
│  │  │  │  ├─ font-awesome
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .npmignore
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  ├─ css
│  │  │  │  │  │  ├─ font-awesome.css
│  │  │  │  │  │  └─ font-awesome.min.css
│  │  │  │  │  ├─ fonts
│  │  │  │  │  │  ├─ fontawesome-webfont.eot
│  │  │  │  │  │  ├─ fontawesome-webfont.svg
│  │  │  │  │  │  ├─ fontawesome-webfont.ttf
│  │  │  │  │  │  ├─ fontawesome-webfont.woff
│  │  │  │  │  │  └─ FontAwesome.otf
│  │  │  │  │  ├─ less
│  │  │  │  │  │  ├─ bordered-pulled.less
│  │  │  │  │  │  ├─ core.less
│  │  │  │  │  │  ├─ extras.less
│  │  │  │  │  │  ├─ fixed-width.less
│  │  │  │  │  │  ├─ font-awesome.less
│  │  │  │  │  │  ├─ icons.less
│  │  │  │  │  │  ├─ larger.less
│  │  │  │  │  │  ├─ list.less
│  │  │  │  │  │  ├─ mixins.less
│  │  │  │  │  │  ├─ path.less
│  │  │  │  │  │  ├─ rotated-flipped.less
│  │  │  │  │  │  ├─ spinning.less
│  │  │  │  │  │  ├─ stacked.less
│  │  │  │  │  │  └─ variables.less
│  │  │  │  │  └─ scss
│  │  │  │  │     ├─ font-awesome.scss
│  │  │  │  │     ├─ _bordered-pulled.scss
│  │  │  │  │     ├─ _core.scss
│  │  │  │  │     ├─ _extras.scss
│  │  │  │  │     ├─ _fixed-width.scss
│  │  │  │  │     ├─ _icons.scss
│  │  │  │  │     ├─ _larger.scss
│  │  │  │  │     ├─ _list.scss
│  │  │  │  │     ├─ _mixins.scss
│  │  │  │  │     ├─ _path.scss
│  │  │  │  │     ├─ _rotated-flipped.scss
│  │  │  │  │     ├─ _spinning.scss
│  │  │  │  │     ├─ _stacked.scss
│  │  │  │  │     └─ _variables.scss
│  │  │  │  ├─ jquery
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ dist
│  │  │  │  │     ├─ jquery.js
│  │  │  │  │     ├─ jquery.min.js
│  │  │  │  │     └─ jquery.min.map
│  │  │  │  └─ metisMenu
│  │  │  │     ├─ .bower.json
│  │  │  │     ├─ dist
│  │  │  │     │  ├─ metisMenu.min.css
│  │  │  │     │  └─ metisMenu.min.js
│  │  │  │     └─ README.md
│  │  │  ├─ dist
│  │  │  │  ├─ css
│  │  │  │  │  └─ sb-admin-2.css
│  │  │  │  └─ js
│  │  │  │     └─ sb-admin-2.js
│  │  │  ├─ less
│  │  │  │  ├─ mixins.less
│  │  │  │  ├─ sb-admin-2.less
│  │  │  │  └─ variables.less
│  │  │  └─ README.md
│  │  └─ statistics.json
│  ├─ homepage_baseline_report
│  │  ├─ content
│  │  │  ├─ css
│  │  │  │  ├─ dashboard.css
│  │  │  │  ├─ jquery-ui.min.css
│  │  │  │  ├─ jquery-ui.structure.min.css
│  │  │  │  ├─ jquery-ui.theme.min.css
│  │  │  │  ├─ legends.css
│  │  │  │  └─ theme.blue.css
│  │  │  ├─ js
│  │  │  │  ├─ curvedLines.js
│  │  │  │  ├─ customGraph.js
│  │  │  │  ├─ dashboard-commons.js
│  │  │  │  ├─ dashboard.js
│  │  │  │  ├─ graph.js
│  │  │  │  ├─ hashtable.js
│  │  │  │  ├─ jquery-ui.min.js
│  │  │  │  ├─ jquery.cookie.js
│  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  ├─ jquery.numberformatter-1.2.3.min.js
│  │  │  │  └─ jquery.tablesorter.min.js
│  │  │  └─ pages
│  │  │     ├─ CustomsGraphs.html
│  │  │     ├─ icon-apache.png
│  │  │     ├─ OverTime.html
│  │  │     ├─ ResponseTimes.html
│  │  │     └─ Throughput.html
│  │  ├─ index.html
│  │  ├─ sbadmin2-1.0.7
│  │  │  ├─ bower.json
│  │  │  ├─ bower_components
│  │  │  │  ├─ bootstrap
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ dist
│  │  │  │  │  │  ├─ css
│  │  │  │  │  │  │  └─ bootstrap.min.css
│  │  │  │  │  │  ├─ fonts
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│  │  │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│  │  │  │  │  │  └─ js
│  │  │  │  │  │     └─ bootstrap.min.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .travis.yml
│  │  │  │  │  ├─ API.md
│  │  │  │  │  ├─ component.json
│  │  │  │  │  ├─ CONTRIBUTING.md
│  │  │  │  │  ├─ excanvas.js
│  │  │  │  │  ├─ excanvas.min.js
│  │  │  │  │  ├─ FAQ.md
│  │  │  │  │  ├─ flot.jquery.json
│  │  │  │  │  ├─ jquery.colorhelpers.js
│  │  │  │  │  ├─ jquery.flot.canvas.js
│  │  │  │  │  ├─ jquery.flot.categories.js
│  │  │  │  │  ├─ jquery.flot.crosshair.js
│  │  │  │  │  ├─ jquery.flot.errorbars.js
│  │  │  │  │  ├─ jquery.flot.fillbetween.js
│  │  │  │  │  ├─ jquery.flot.image.js
│  │  │  │  │  ├─ jquery.flot.js
│  │  │  │  │  ├─ jquery.flot.navigate.js
│  │  │  │  │  ├─ jquery.flot.pie.js
│  │  │  │  │  ├─ jquery.flot.resize.js
│  │  │  │  │  ├─ jquery.flot.selection.js
│  │  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  │  ├─ jquery.flot.symbol.js
│  │  │  │  │  ├─ jquery.flot.threshold.js
│  │  │  │  │  ├─ jquery.flot.time.js
│  │  │  │  │  ├─ Makefile
│  │  │  │  │  ├─ NEWS.md
│  │  │  │  │  ├─ package.json
│  │  │  │  │  ├─ PLUGINS.md
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot-axislabels
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ jquery.flot.axislabels.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot.tooltip
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ js
│  │  │  │  │     ├─ excanvas.min.js
│  │  │  │  │     ├─ jquery.flot.js
│  │  │  │  │     ├─ jquery.flot.tooltip.js
│  │  │  │  │     ├─ jquery.flot.tooltip.min.js
│  │  │  │  │     └─ jquery.flot.tooltip.source.js
│  │  │  │  ├─ font-awesome
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .npmignore
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  ├─ css
│  │  │  │  │  │  ├─ font-awesome.css
│  │  │  │  │  │  └─ font-awesome.min.css
│  │  │  │  │  ├─ fonts
│  │  │  │  │  │  ├─ fontawesome-webfont.eot
│  │  │  │  │  │  ├─ fontawesome-webfont.svg
│  │  │  │  │  │  ├─ fontawesome-webfont.ttf
│  │  │  │  │  │  ├─ fontawesome-webfont.woff
│  │  │  │  │  │  └─ FontAwesome.otf
│  │  │  │  │  ├─ less
│  │  │  │  │  │  ├─ bordered-pulled.less
│  │  │  │  │  │  ├─ core.less
│  │  │  │  │  │  ├─ extras.less
│  │  │  │  │  │  ├─ fixed-width.less
│  │  │  │  │  │  ├─ font-awesome.less
│  │  │  │  │  │  ├─ icons.less
│  │  │  │  │  │  ├─ larger.less
│  │  │  │  │  │  ├─ list.less
│  │  │  │  │  │  ├─ mixins.less
│  │  │  │  │  │  ├─ path.less
│  │  │  │  │  │  ├─ rotated-flipped.less
│  │  │  │  │  │  ├─ spinning.less
│  │  │  │  │  │  ├─ stacked.less
│  │  │  │  │  │  └─ variables.less
│  │  │  │  │  └─ scss
│  │  │  │  │     ├─ font-awesome.scss
│  │  │  │  │     ├─ _bordered-pulled.scss
│  │  │  │  │     ├─ _core.scss
│  │  │  │  │     ├─ _extras.scss
│  │  │  │  │     ├─ _fixed-width.scss
│  │  │  │  │     ├─ _icons.scss
│  │  │  │  │     ├─ _larger.scss
│  │  │  │  │     ├─ _list.scss
│  │  │  │  │     ├─ _mixins.scss
│  │  │  │  │     ├─ _path.scss
│  │  │  │  │     ├─ _rotated-flipped.scss
│  │  │  │  │     ├─ _spinning.scss
│  │  │  │  │     ├─ _stacked.scss
│  │  │  │  │     └─ _variables.scss
│  │  │  │  ├─ jquery
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ dist
│  │  │  │  │     ├─ jquery.js
│  │  │  │  │     ├─ jquery.min.js
│  │  │  │  │     └─ jquery.min.map
│  │  │  │  └─ metisMenu
│  │  │  │     ├─ .bower.json
│  │  │  │     ├─ dist
│  │  │  │     │  ├─ metisMenu.min.css
│  │  │  │     │  └─ metisMenu.min.js
│  │  │  │     └─ README.md
│  │  │  ├─ dist
│  │  │  │  ├─ css
│  │  │  │  │  └─ sb-admin-2.css
│  │  │  │  └─ js
│  │  │  │     └─ sb-admin-2.js
│  │  │  ├─ less
│  │  │  │  ├─ mixins.less
│  │  │  │  ├─ sb-admin-2.less
│  │  │  │  └─ variables.less
│  │  │  └─ README.md
│  │  └─ statistics.json
│  ├─ mixed_load_high_report
│  │  ├─ content
│  │  │  ├─ css
│  │  │  │  ├─ dashboard.css
│  │  │  │  ├─ jquery-ui.min.css
│  │  │  │  ├─ jquery-ui.structure.min.css
│  │  │  │  ├─ jquery-ui.theme.min.css
│  │  │  │  ├─ legends.css
│  │  │  │  └─ theme.blue.css
│  │  │  ├─ js
│  │  │  │  ├─ curvedLines.js
│  │  │  │  ├─ customGraph.js
│  │  │  │  ├─ dashboard-commons.js
│  │  │  │  ├─ dashboard.js
│  │  │  │  ├─ graph.js
│  │  │  │  ├─ hashtable.js
│  │  │  │  ├─ jquery-ui.min.js
│  │  │  │  ├─ jquery.cookie.js
│  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  ├─ jquery.numberformatter-1.2.3.min.js
│  │  │  │  └─ jquery.tablesorter.min.js
│  │  │  └─ pages
│  │  │     ├─ CustomsGraphs.html
│  │  │     ├─ icon-apache.png
│  │  │     ├─ OverTime.html
│  │  │     ├─ ResponseTimes.html
│  │  │     └─ Throughput.html
│  │  ├─ index.html
│  │  ├─ sbadmin2-1.0.7
│  │  │  ├─ bower.json
│  │  │  ├─ bower_components
│  │  │  │  ├─ bootstrap
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ dist
│  │  │  │  │  │  ├─ css
│  │  │  │  │  │  │  └─ bootstrap.min.css
│  │  │  │  │  │  ├─ fonts
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│  │  │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│  │  │  │  │  │  └─ js
│  │  │  │  │  │     └─ bootstrap.min.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .travis.yml
│  │  │  │  │  ├─ API.md
│  │  │  │  │  ├─ component.json
│  │  │  │  │  ├─ CONTRIBUTING.md
│  │  │  │  │  ├─ excanvas.js
│  │  │  │  │  ├─ excanvas.min.js
│  │  │  │  │  ├─ FAQ.md
│  │  │  │  │  ├─ flot.jquery.json
│  │  │  │  │  ├─ jquery.colorhelpers.js
│  │  │  │  │  ├─ jquery.flot.canvas.js
│  │  │  │  │  ├─ jquery.flot.categories.js
│  │  │  │  │  ├─ jquery.flot.crosshair.js
│  │  │  │  │  ├─ jquery.flot.errorbars.js
│  │  │  │  │  ├─ jquery.flot.fillbetween.js
│  │  │  │  │  ├─ jquery.flot.image.js
│  │  │  │  │  ├─ jquery.flot.js
│  │  │  │  │  ├─ jquery.flot.navigate.js
│  │  │  │  │  ├─ jquery.flot.pie.js
│  │  │  │  │  ├─ jquery.flot.resize.js
│  │  │  │  │  ├─ jquery.flot.selection.js
│  │  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  │  ├─ jquery.flot.symbol.js
│  │  │  │  │  ├─ jquery.flot.threshold.js
│  │  │  │  │  ├─ jquery.flot.time.js
│  │  │  │  │  ├─ Makefile
│  │  │  │  │  ├─ NEWS.md
│  │  │  │  │  ├─ package.json
│  │  │  │  │  ├─ PLUGINS.md
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot-axislabels
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ jquery.flot.axislabels.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot.tooltip
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ js
│  │  │  │  │     ├─ excanvas.min.js
│  │  │  │  │     ├─ jquery.flot.js
│  │  │  │  │     ├─ jquery.flot.tooltip.js
│  │  │  │  │     ├─ jquery.flot.tooltip.min.js
│  │  │  │  │     └─ jquery.flot.tooltip.source.js
│  │  │  │  ├─ font-awesome
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .npmignore
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  ├─ css
│  │  │  │  │  │  ├─ font-awesome.css
│  │  │  │  │  │  └─ font-awesome.min.css
│  │  │  │  │  ├─ fonts
│  │  │  │  │  │  ├─ fontawesome-webfont.eot
│  │  │  │  │  │  ├─ fontawesome-webfont.svg
│  │  │  │  │  │  ├─ fontawesome-webfont.ttf
│  │  │  │  │  │  ├─ fontawesome-webfont.woff
│  │  │  │  │  │  └─ FontAwesome.otf
│  │  │  │  │  ├─ less
│  │  │  │  │  │  ├─ bordered-pulled.less
│  │  │  │  │  │  ├─ core.less
│  │  │  │  │  │  ├─ extras.less
│  │  │  │  │  │  ├─ fixed-width.less
│  │  │  │  │  │  ├─ font-awesome.less
│  │  │  │  │  │  ├─ icons.less
│  │  │  │  │  │  ├─ larger.less
│  │  │  │  │  │  ├─ list.less
│  │  │  │  │  │  ├─ mixins.less
│  │  │  │  │  │  ├─ path.less
│  │  │  │  │  │  ├─ rotated-flipped.less
│  │  │  │  │  │  ├─ spinning.less
│  │  │  │  │  │  ├─ stacked.less
│  │  │  │  │  │  └─ variables.less
│  │  │  │  │  └─ scss
│  │  │  │  │     ├─ font-awesome.scss
│  │  │  │  │     ├─ _bordered-pulled.scss
│  │  │  │  │     ├─ _core.scss
│  │  │  │  │     ├─ _extras.scss
│  │  │  │  │     ├─ _fixed-width.scss
│  │  │  │  │     ├─ _icons.scss
│  │  │  │  │     ├─ _larger.scss
│  │  │  │  │     ├─ _list.scss
│  │  │  │  │     ├─ _mixins.scss
│  │  │  │  │     ├─ _path.scss
│  │  │  │  │     ├─ _rotated-flipped.scss
│  │  │  │  │     ├─ _spinning.scss
│  │  │  │  │     ├─ _stacked.scss
│  │  │  │  │     └─ _variables.scss
│  │  │  │  ├─ jquery
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ dist
│  │  │  │  │     ├─ jquery.js
│  │  │  │  │     ├─ jquery.min.js
│  │  │  │  │     └─ jquery.min.map
│  │  │  │  └─ metisMenu
│  │  │  │     ├─ .bower.json
│  │  │  │     ├─ dist
│  │  │  │     │  ├─ metisMenu.min.css
│  │  │  │     │  └─ metisMenu.min.js
│  │  │  │     └─ README.md
│  │  │  ├─ dist
│  │  │  │  ├─ css
│  │  │  │  │  └─ sb-admin-2.css
│  │  │  │  └─ js
│  │  │  │     └─ sb-admin-2.js
│  │  │  ├─ less
│  │  │  │  ├─ mixins.less
│  │  │  │  ├─ sb-admin-2.less
│  │  │  │  └─ variables.less
│  │  │  └─ README.md
│  │  └─ statistics.json
│  ├─ mixed_load_low_report
│  │  ├─ content
│  │  │  ├─ css
│  │  │  │  ├─ dashboard.css
│  │  │  │  ├─ jquery-ui.min.css
│  │  │  │  ├─ jquery-ui.structure.min.css
│  │  │  │  ├─ jquery-ui.theme.min.css
│  │  │  │  ├─ legends.css
│  │  │  │  └─ theme.blue.css
│  │  │  ├─ js
│  │  │  │  ├─ curvedLines.js
│  │  │  │  ├─ customGraph.js
│  │  │  │  ├─ dashboard-commons.js
│  │  │  │  ├─ dashboard.js
│  │  │  │  ├─ graph.js
│  │  │  │  ├─ hashtable.js
│  │  │  │  ├─ jquery-ui.min.js
│  │  │  │  ├─ jquery.cookie.js
│  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  ├─ jquery.numberformatter-1.2.3.min.js
│  │  │  │  └─ jquery.tablesorter.min.js
│  │  │  └─ pages
│  │  │     ├─ CustomsGraphs.html
│  │  │     ├─ icon-apache.png
│  │  │     ├─ OverTime.html
│  │  │     ├─ ResponseTimes.html
│  │  │     └─ Throughput.html
│  │  ├─ index.html
│  │  ├─ sbadmin2-1.0.7
│  │  │  ├─ bower.json
│  │  │  ├─ bower_components
│  │  │  │  ├─ bootstrap
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ dist
│  │  │  │  │  │  ├─ css
│  │  │  │  │  │  │  └─ bootstrap.min.css
│  │  │  │  │  │  ├─ fonts
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│  │  │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│  │  │  │  │  │  └─ js
│  │  │  │  │  │     └─ bootstrap.min.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .travis.yml
│  │  │  │  │  ├─ API.md
│  │  │  │  │  ├─ component.json
│  │  │  │  │  ├─ CONTRIBUTING.md
│  │  │  │  │  ├─ excanvas.js
│  │  │  │  │  ├─ excanvas.min.js
│  │  │  │  │  ├─ FAQ.md
│  │  │  │  │  ├─ flot.jquery.json
│  │  │  │  │  ├─ jquery.colorhelpers.js
│  │  │  │  │  ├─ jquery.flot.canvas.js
│  │  │  │  │  ├─ jquery.flot.categories.js
│  │  │  │  │  ├─ jquery.flot.crosshair.js
│  │  │  │  │  ├─ jquery.flot.errorbars.js
│  │  │  │  │  ├─ jquery.flot.fillbetween.js
│  │  │  │  │  ├─ jquery.flot.image.js
│  │  │  │  │  ├─ jquery.flot.js
│  │  │  │  │  ├─ jquery.flot.navigate.js
│  │  │  │  │  ├─ jquery.flot.pie.js
│  │  │  │  │  ├─ jquery.flot.resize.js
│  │  │  │  │  ├─ jquery.flot.selection.js
│  │  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  │  ├─ jquery.flot.symbol.js
│  │  │  │  │  ├─ jquery.flot.threshold.js
│  │  │  │  │  ├─ jquery.flot.time.js
│  │  │  │  │  ├─ Makefile
│  │  │  │  │  ├─ NEWS.md
│  │  │  │  │  ├─ package.json
│  │  │  │  │  ├─ PLUGINS.md
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot-axislabels
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ jquery.flot.axislabels.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot.tooltip
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ js
│  │  │  │  │     ├─ excanvas.min.js
│  │  │  │  │     ├─ jquery.flot.js
│  │  │  │  │     ├─ jquery.flot.tooltip.js
│  │  │  │  │     ├─ jquery.flot.tooltip.min.js
│  │  │  │  │     └─ jquery.flot.tooltip.source.js
│  │  │  │  ├─ font-awesome
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .npmignore
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  ├─ css
│  │  │  │  │  │  ├─ font-awesome.css
│  │  │  │  │  │  └─ font-awesome.min.css
│  │  │  │  │  ├─ fonts
│  │  │  │  │  │  ├─ fontawesome-webfont.eot
│  │  │  │  │  │  ├─ fontawesome-webfont.svg
│  │  │  │  │  │  ├─ fontawesome-webfont.ttf
│  │  │  │  │  │  ├─ fontawesome-webfont.woff
│  │  │  │  │  │  └─ FontAwesome.otf
│  │  │  │  │  ├─ less
│  │  │  │  │  │  ├─ bordered-pulled.less
│  │  │  │  │  │  ├─ core.less
│  │  │  │  │  │  ├─ extras.less
│  │  │  │  │  │  ├─ fixed-width.less
│  │  │  │  │  │  ├─ font-awesome.less
│  │  │  │  │  │  ├─ icons.less
│  │  │  │  │  │  ├─ larger.less
│  │  │  │  │  │  ├─ list.less
│  │  │  │  │  │  ├─ mixins.less
│  │  │  │  │  │  ├─ path.less
│  │  │  │  │  │  ├─ rotated-flipped.less
│  │  │  │  │  │  ├─ spinning.less
│  │  │  │  │  │  ├─ stacked.less
│  │  │  │  │  │  └─ variables.less
│  │  │  │  │  └─ scss
│  │  │  │  │     ├─ font-awesome.scss
│  │  │  │  │     ├─ _bordered-pulled.scss
│  │  │  │  │     ├─ _core.scss
│  │  │  │  │     ├─ _extras.scss
│  │  │  │  │     ├─ _fixed-width.scss
│  │  │  │  │     ├─ _icons.scss
│  │  │  │  │     ├─ _larger.scss
│  │  │  │  │     ├─ _list.scss
│  │  │  │  │     ├─ _mixins.scss
│  │  │  │  │     ├─ _path.scss
│  │  │  │  │     ├─ _rotated-flipped.scss
│  │  │  │  │     ├─ _spinning.scss
│  │  │  │  │     ├─ _stacked.scss
│  │  │  │  │     └─ _variables.scss
│  │  │  │  ├─ jquery
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ dist
│  │  │  │  │     ├─ jquery.js
│  │  │  │  │     ├─ jquery.min.js
│  │  │  │  │     └─ jquery.min.map
│  │  │  │  └─ metisMenu
│  │  │  │     ├─ .bower.json
│  │  │  │     ├─ dist
│  │  │  │     │  ├─ metisMenu.min.css
│  │  │  │     │  └─ metisMenu.min.js
│  │  │  │     └─ README.md
│  │  │  ├─ dist
│  │  │  │  ├─ css
│  │  │  │  │  └─ sb-admin-2.css
│  │  │  │  └─ js
│  │  │  │     └─ sb-admin-2.js
│  │  │  ├─ less
│  │  │  │  ├─ mixins.less
│  │  │  │  ├─ sb-admin-2.less
│  │  │  │  └─ variables.less
│  │  │  └─ README.md
│  │  └─ statistics.json
│  ├─ mixed_load_medium_report
│  │  ├─ content
│  │  │  ├─ css
│  │  │  │  ├─ dashboard.css
│  │  │  │  ├─ jquery-ui.min.css
│  │  │  │  ├─ jquery-ui.structure.min.css
│  │  │  │  ├─ jquery-ui.theme.min.css
│  │  │  │  ├─ legends.css
│  │  │  │  └─ theme.blue.css
│  │  │  ├─ js
│  │  │  │  ├─ curvedLines.js
│  │  │  │  ├─ customGraph.js
│  │  │  │  ├─ dashboard-commons.js
│  │  │  │  ├─ dashboard.js
│  │  │  │  ├─ graph.js
│  │  │  │  ├─ hashtable.js
│  │  │  │  ├─ jquery-ui.min.js
│  │  │  │  ├─ jquery.cookie.js
│  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  ├─ jquery.numberformatter-1.2.3.min.js
│  │  │  │  └─ jquery.tablesorter.min.js
│  │  │  └─ pages
│  │  │     ├─ CustomsGraphs.html
│  │  │     ├─ icon-apache.png
│  │  │     ├─ OverTime.html
│  │  │     ├─ ResponseTimes.html
│  │  │     └─ Throughput.html
│  │  ├─ index.html
│  │  ├─ sbadmin2-1.0.7
│  │  │  ├─ bower.json
│  │  │  ├─ bower_components
│  │  │  │  ├─ bootstrap
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ dist
│  │  │  │  │  │  ├─ css
│  │  │  │  │  │  │  └─ bootstrap.min.css
│  │  │  │  │  │  ├─ fonts
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│  │  │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│  │  │  │  │  │  └─ js
│  │  │  │  │  │     └─ bootstrap.min.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .travis.yml
│  │  │  │  │  ├─ API.md
│  │  │  │  │  ├─ component.json
│  │  │  │  │  ├─ CONTRIBUTING.md
│  │  │  │  │  ├─ excanvas.js
│  │  │  │  │  ├─ excanvas.min.js
│  │  │  │  │  ├─ FAQ.md
│  │  │  │  │  ├─ flot.jquery.json
│  │  │  │  │  ├─ jquery.colorhelpers.js
│  │  │  │  │  ├─ jquery.flot.canvas.js
│  │  │  │  │  ├─ jquery.flot.categories.js
│  │  │  │  │  ├─ jquery.flot.crosshair.js
│  │  │  │  │  ├─ jquery.flot.errorbars.js
│  │  │  │  │  ├─ jquery.flot.fillbetween.js
│  │  │  │  │  ├─ jquery.flot.image.js
│  │  │  │  │  ├─ jquery.flot.js
│  │  │  │  │  ├─ jquery.flot.navigate.js
│  │  │  │  │  ├─ jquery.flot.pie.js
│  │  │  │  │  ├─ jquery.flot.resize.js
│  │  │  │  │  ├─ jquery.flot.selection.js
│  │  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  │  ├─ jquery.flot.symbol.js
│  │  │  │  │  ├─ jquery.flot.threshold.js
│  │  │  │  │  ├─ jquery.flot.time.js
│  │  │  │  │  ├─ Makefile
│  │  │  │  │  ├─ NEWS.md
│  │  │  │  │  ├─ package.json
│  │  │  │  │  ├─ PLUGINS.md
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot-axislabels
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ jquery.flot.axislabels.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot.tooltip
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ js
│  │  │  │  │     ├─ excanvas.min.js
│  │  │  │  │     ├─ jquery.flot.js
│  │  │  │  │     ├─ jquery.flot.tooltip.js
│  │  │  │  │     ├─ jquery.flot.tooltip.min.js
│  │  │  │  │     └─ jquery.flot.tooltip.source.js
│  │  │  │  ├─ font-awesome
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .npmignore
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  ├─ css
│  │  │  │  │  │  ├─ font-awesome.css
│  │  │  │  │  │  └─ font-awesome.min.css
│  │  │  │  │  ├─ fonts
│  │  │  │  │  │  ├─ fontawesome-webfont.eot
│  │  │  │  │  │  ├─ fontawesome-webfont.svg
│  │  │  │  │  │  ├─ fontawesome-webfont.ttf
│  │  │  │  │  │  ├─ fontawesome-webfont.woff
│  │  │  │  │  │  └─ FontAwesome.otf
│  │  │  │  │  ├─ less
│  │  │  │  │  │  ├─ bordered-pulled.less
│  │  │  │  │  │  ├─ core.less
│  │  │  │  │  │  ├─ extras.less
│  │  │  │  │  │  ├─ fixed-width.less
│  │  │  │  │  │  ├─ font-awesome.less
│  │  │  │  │  │  ├─ icons.less
│  │  │  │  │  │  ├─ larger.less
│  │  │  │  │  │  ├─ list.less
│  │  │  │  │  │  ├─ mixins.less
│  │  │  │  │  │  ├─ path.less
│  │  │  │  │  │  ├─ rotated-flipped.less
│  │  │  │  │  │  ├─ spinning.less
│  │  │  │  │  │  ├─ stacked.less
│  │  │  │  │  │  └─ variables.less
│  │  │  │  │  └─ scss
│  │  │  │  │     ├─ font-awesome.scss
│  │  │  │  │     ├─ _bordered-pulled.scss
│  │  │  │  │     ├─ _core.scss
│  │  │  │  │     ├─ _extras.scss
│  │  │  │  │     ├─ _fixed-width.scss
│  │  │  │  │     ├─ _icons.scss
│  │  │  │  │     ├─ _larger.scss
│  │  │  │  │     ├─ _list.scss
│  │  │  │  │     ├─ _mixins.scss
│  │  │  │  │     ├─ _path.scss
│  │  │  │  │     ├─ _rotated-flipped.scss
│  │  │  │  │     ├─ _spinning.scss
│  │  │  │  │     ├─ _stacked.scss
│  │  │  │  │     └─ _variables.scss
│  │  │  │  ├─ jquery
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ dist
│  │  │  │  │     ├─ jquery.js
│  │  │  │  │     ├─ jquery.min.js
│  │  │  │  │     └─ jquery.min.map
│  │  │  │  └─ metisMenu
│  │  │  │     ├─ .bower.json
│  │  │  │     ├─ dist
│  │  │  │     │  ├─ metisMenu.min.css
│  │  │  │     │  └─ metisMenu.min.js
│  │  │  │     └─ README.md
│  │  │  ├─ dist
│  │  │  │  ├─ css
│  │  │  │  │  └─ sb-admin-2.css
│  │  │  │  └─ js
│  │  │  │     └─ sb-admin-2.js
│  │  │  ├─ less
│  │  │  │  ├─ mixins.less
│  │  │  │  ├─ sb-admin-2.less
│  │  │  │  └─ variables.less
│  │  │  └─ README.md
│  │  └─ statistics.json
│  ├─ order_service_report
│  │  ├─ content
│  │  │  ├─ css
│  │  │  │  ├─ dashboard.css
│  │  │  │  ├─ jquery-ui.min.css
│  │  │  │  ├─ jquery-ui.structure.min.css
│  │  │  │  ├─ jquery-ui.theme.min.css
│  │  │  │  ├─ legends.css
│  │  │  │  └─ theme.blue.css
│  │  │  ├─ js
│  │  │  │  ├─ curvedLines.js
│  │  │  │  ├─ customGraph.js
│  │  │  │  ├─ dashboard-commons.js
│  │  │  │  ├─ dashboard.js
│  │  │  │  ├─ graph.js
│  │  │  │  ├─ hashtable.js
│  │  │  │  ├─ jquery-ui.min.js
│  │  │  │  ├─ jquery.cookie.js
│  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  ├─ jquery.numberformatter-1.2.3.min.js
│  │  │  │  └─ jquery.tablesorter.min.js
│  │  │  └─ pages
│  │  │     ├─ CustomsGraphs.html
│  │  │     ├─ icon-apache.png
│  │  │     ├─ OverTime.html
│  │  │     ├─ ResponseTimes.html
│  │  │     └─ Throughput.html
│  │  ├─ index.html
│  │  ├─ sbadmin2-1.0.7
│  │  │  ├─ bower.json
│  │  │  ├─ bower_components
│  │  │  │  ├─ bootstrap
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ dist
│  │  │  │  │  │  ├─ css
│  │  │  │  │  │  │  └─ bootstrap.min.css
│  │  │  │  │  │  ├─ fonts
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│  │  │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│  │  │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│  │  │  │  │  │  └─ js
│  │  │  │  │  │     └─ bootstrap.min.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .travis.yml
│  │  │  │  │  ├─ API.md
│  │  │  │  │  ├─ component.json
│  │  │  │  │  ├─ CONTRIBUTING.md
│  │  │  │  │  ├─ excanvas.js
│  │  │  │  │  ├─ excanvas.min.js
│  │  │  │  │  ├─ FAQ.md
│  │  │  │  │  ├─ flot.jquery.json
│  │  │  │  │  ├─ jquery.colorhelpers.js
│  │  │  │  │  ├─ jquery.flot.canvas.js
│  │  │  │  │  ├─ jquery.flot.categories.js
│  │  │  │  │  ├─ jquery.flot.crosshair.js
│  │  │  │  │  ├─ jquery.flot.errorbars.js
│  │  │  │  │  ├─ jquery.flot.fillbetween.js
│  │  │  │  │  ├─ jquery.flot.image.js
│  │  │  │  │  ├─ jquery.flot.js
│  │  │  │  │  ├─ jquery.flot.navigate.js
│  │  │  │  │  ├─ jquery.flot.pie.js
│  │  │  │  │  ├─ jquery.flot.resize.js
│  │  │  │  │  ├─ jquery.flot.selection.js
│  │  │  │  │  ├─ jquery.flot.stack.js
│  │  │  │  │  ├─ jquery.flot.symbol.js
│  │  │  │  │  ├─ jquery.flot.threshold.js
│  │  │  │  │  ├─ jquery.flot.time.js
│  │  │  │  │  ├─ Makefile
│  │  │  │  │  ├─ NEWS.md
│  │  │  │  │  ├─ package.json
│  │  │  │  │  ├─ PLUGINS.md
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot-axislabels
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ jquery.flot.axislabels.js
│  │  │  │  │  └─ README.md
│  │  │  │  ├─ flot.tooltip
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ js
│  │  │  │  │     ├─ excanvas.min.js
│  │  │  │  │     ├─ jquery.flot.js
│  │  │  │  │     ├─ jquery.flot.tooltip.js
│  │  │  │  │     ├─ jquery.flot.tooltip.min.js
│  │  │  │  │     └─ jquery.flot.tooltip.source.js
│  │  │  │  ├─ font-awesome
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ .npmignore
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  ├─ css
│  │  │  │  │  │  ├─ font-awesome.css
│  │  │  │  │  │  └─ font-awesome.min.css
│  │  │  │  │  ├─ fonts
│  │  │  │  │  │  ├─ fontawesome-webfont.eot
│  │  │  │  │  │  ├─ fontawesome-webfont.svg
│  │  │  │  │  │  ├─ fontawesome-webfont.ttf
│  │  │  │  │  │  ├─ fontawesome-webfont.woff
│  │  │  │  │  │  └─ FontAwesome.otf
│  │  │  │  │  ├─ less
│  │  │  │  │  │  ├─ bordered-pulled.less
│  │  │  │  │  │  ├─ core.less
│  │  │  │  │  │  ├─ extras.less
│  │  │  │  │  │  ├─ fixed-width.less
│  │  │  │  │  │  ├─ font-awesome.less
│  │  │  │  │  │  ├─ icons.less
│  │  │  │  │  │  ├─ larger.less
│  │  │  │  │  │  ├─ list.less
│  │  │  │  │  │  ├─ mixins.less
│  │  │  │  │  │  ├─ path.less
│  │  │  │  │  │  ├─ rotated-flipped.less
│  │  │  │  │  │  ├─ spinning.less
│  │  │  │  │  │  ├─ stacked.less
│  │  │  │  │  │  └─ variables.less
│  │  │  │  │  └─ scss
│  │  │  │  │     ├─ font-awesome.scss
│  │  │  │  │     ├─ _bordered-pulled.scss
│  │  │  │  │     ├─ _core.scss
│  │  │  │  │     ├─ _extras.scss
│  │  │  │  │     ├─ _fixed-width.scss
│  │  │  │  │     ├─ _icons.scss
│  │  │  │  │     ├─ _larger.scss
│  │  │  │  │     ├─ _list.scss
│  │  │  │  │     ├─ _mixins.scss
│  │  │  │  │     ├─ _path.scss
│  │  │  │  │     ├─ _rotated-flipped.scss
│  │  │  │  │     ├─ _spinning.scss
│  │  │  │  │     ├─ _stacked.scss
│  │  │  │  │     └─ _variables.scss
│  │  │  │  ├─ jquery
│  │  │  │  │  ├─ .bower.json
│  │  │  │  │  ├─ bower.json
│  │  │  │  │  └─ dist
│  │  │  │  │     ├─ jquery.js
│  │  │  │  │     ├─ jquery.min.js
│  │  │  │  │     └─ jquery.min.map
│  │  │  │  └─ metisMenu
│  │  │  │     ├─ .bower.json
│  │  │  │     ├─ dist
│  │  │  │     │  ├─ metisMenu.min.css
│  │  │  │     │  └─ metisMenu.min.js
│  │  │  │     └─ README.md
│  │  │  ├─ dist
│  │  │  │  ├─ css
│  │  │  │  │  └─ sb-admin-2.css
│  │  │  │  └─ js
│  │  │  │     └─ sb-admin-2.js
│  │  │  ├─ less
│  │  │  │  ├─ mixins.less
│  │  │  │  ├─ sb-admin-2.less
│  │  │  │  └─ variables.less
│  │  │  └─ README.md
│  │  └─ statistics.json
│  └─ product_service_report
│     ├─ content
│     │  ├─ css
│     │  │  ├─ dashboard.css
│     │  │  ├─ jquery-ui.min.css
│     │  │  ├─ jquery-ui.structure.min.css
│     │  │  ├─ jquery-ui.theme.min.css
│     │  │  ├─ legends.css
│     │  │  └─ theme.blue.css
│     │  ├─ js
│     │  │  ├─ curvedLines.js
│     │  │  ├─ customGraph.js
│     │  │  ├─ dashboard-commons.js
│     │  │  ├─ dashboard.js
│     │  │  ├─ graph.js
│     │  │  ├─ hashtable.js
│     │  │  ├─ jquery-ui.min.js
│     │  │  ├─ jquery.cookie.js
│     │  │  ├─ jquery.flot.stack.js
│     │  │  ├─ jquery.numberformatter-1.2.3.min.js
│     │  │  └─ jquery.tablesorter.min.js
│     │  └─ pages
│     │     ├─ CustomsGraphs.html
│     │     ├─ icon-apache.png
│     │     ├─ OverTime.html
│     │     ├─ ResponseTimes.html
│     │     └─ Throughput.html
│     ├─ index.html
│     ├─ sbadmin2-1.0.7
│     │  ├─ bower.json
│     │  ├─ bower_components
│     │  │  ├─ bootstrap
│     │  │  │  ├─ .bower.json
│     │  │  │  ├─ dist
│     │  │  │  │  ├─ css
│     │  │  │  │  │  └─ bootstrap.min.css
│     │  │  │  │  ├─ fonts
│     │  │  │  │  │  ├─ glyphicons-halflings-regular.eot
│     │  │  │  │  │  ├─ glyphicons-halflings-regular.svg
│     │  │  │  │  │  ├─ glyphicons-halflings-regular.ttf
│     │  │  │  │  │  ├─ glyphicons-halflings-regular.woff
│     │  │  │  │  │  └─ glyphicons-halflings-regular.woff2
│     │  │  │  │  └─ js
│     │  │  │  │     └─ bootstrap.min.js
│     │  │  │  └─ README.md
│     │  │  ├─ flot
│     │  │  │  ├─ .bower.json
│     │  │  │  ├─ .travis.yml
│     │  │  │  ├─ API.md
│     │  │  │  ├─ component.json
│     │  │  │  ├─ CONTRIBUTING.md
│     │  │  │  ├─ excanvas.js
│     │  │  │  ├─ excanvas.min.js
│     │  │  │  ├─ FAQ.md
│     │  │  │  ├─ flot.jquery.json
│     │  │  │  ├─ jquery.colorhelpers.js
│     │  │  │  ├─ jquery.flot.canvas.js
│     │  │  │  ├─ jquery.flot.categories.js
│     │  │  │  ├─ jquery.flot.crosshair.js
│     │  │  │  ├─ jquery.flot.errorbars.js
│     │  │  │  ├─ jquery.flot.fillbetween.js
│     │  │  │  ├─ jquery.flot.image.js
│     │  │  │  ├─ jquery.flot.js
│     │  │  │  ├─ jquery.flot.navigate.js
│     │  │  │  ├─ jquery.flot.pie.js
│     │  │  │  ├─ jquery.flot.resize.js
│     │  │  │  ├─ jquery.flot.selection.js
│     │  │  │  ├─ jquery.flot.stack.js
│     │  │  │  ├─ jquery.flot.symbol.js
│     │  │  │  ├─ jquery.flot.threshold.js
│     │  │  │  ├─ jquery.flot.time.js
│     │  │  │  ├─ Makefile
│     │  │  │  ├─ NEWS.md
│     │  │  │  ├─ package.json
│     │  │  │  ├─ PLUGINS.md
│     │  │  │  └─ README.md
│     │  │  ├─ flot-axislabels
│     │  │  │  ├─ .bower.json
│     │  │  │  ├─ jquery.flot.axislabels.js
│     │  │  │  └─ README.md
│     │  │  ├─ flot.tooltip
│     │  │  │  ├─ .bower.json
│     │  │  │  ├─ bower.json
│     │  │  │  └─ js
│     │  │  │     ├─ excanvas.min.js
│     │  │  │     ├─ jquery.flot.js
│     │  │  │     ├─ jquery.flot.tooltip.js
│     │  │  │     ├─ jquery.flot.tooltip.min.js
│     │  │  │     └─ jquery.flot.tooltip.source.js
│     │  │  ├─ font-awesome
│     │  │  │  ├─ .bower.json
│     │  │  │  ├─ .npmignore
│     │  │  │  ├─ bower.json
│     │  │  │  ├─ css
│     │  │  │  │  ├─ font-awesome.css
│     │  │  │  │  └─ font-awesome.min.css
│     │  │  │  ├─ fonts
│     │  │  │  │  ├─ fontawesome-webfont.eot
│     │  │  │  │  ├─ fontawesome-webfont.svg
│     │  │  │  │  ├─ fontawesome-webfont.ttf
│     │  │  │  │  ├─ fontawesome-webfont.woff
│     │  │  │  │  └─ FontAwesome.otf
│     │  │  │  ├─ less
│     │  │  │  │  ├─ bordered-pulled.less
│     │  │  │  │  ├─ core.less
│     │  │  │  │  ├─ extras.less
│     │  │  │  │  ├─ fixed-width.less
│     │  │  │  │  ├─ font-awesome.less
│     │  │  │  │  ├─ icons.less
│     │  │  │  │  ├─ larger.less
│     │  │  │  │  ├─ list.less
│     │  │  │  │  ├─ mixins.less
│     │  │  │  │  ├─ path.less
│     │  │  │  │  ├─ rotated-flipped.less
│     │  │  │  │  ├─ spinning.less
│     │  │  │  │  ├─ stacked.less
│     │  │  │  │  └─ variables.less
│     │  │  │  └─ scss
│     │  │  │     ├─ font-awesome.scss
│     │  │  │     ├─ _bordered-pulled.scss
│     │  │  │     ├─ _core.scss
│     │  │  │     ├─ _extras.scss
│     │  │  │     ├─ _fixed-width.scss
│     │  │  │     ├─ _icons.scss
│     │  │  │     ├─ _larger.scss
│     │  │  │     ├─ _list.scss
│     │  │  │     ├─ _mixins.scss
│     │  │  │     ├─ _path.scss
│     │  │  │     ├─ _rotated-flipped.scss
│     │  │  │     ├─ _spinning.scss
│     │  │  │     ├─ _stacked.scss
│     │  │  │     └─ _variables.scss
│     │  │  ├─ jquery
│     │  │  │  ├─ .bower.json
│     │  │  │  ├─ bower.json
│     │  │  │  └─ dist
│     │  │  │     ├─ jquery.js
│     │  │  │     ├─ jquery.min.js
│     │  │  │     └─ jquery.min.map
│     │  │  └─ metisMenu
│     │  │     ├─ .bower.json
│     │  │     ├─ dist
│     │  │     │  ├─ metisMenu.min.css
│     │  │     │  └─ metisMenu.min.js
│     │  │     └─ README.md
│     │  ├─ dist
│     │  │  ├─ css
│     │  │  │  └─ sb-admin-2.css
│     │  │  └─ js
│     │  │     └─ sb-admin-2.js
│     │  ├─ less
│     │  │  ├─ mixins.less
│     │  │  ├─ sb-admin-2.less
│     │  │  └─ variables.less
│     │  └─ README.md
│     └─ statistics.json
├─ test_results
│  ├─ cart_service_test.jtl
│  ├─ homepage_baseline_test.jtl
│  ├─ mixed_load_extreme_test.jtl
│  ├─ mixed_load_high_test.jtl
│  ├─ mixed_load_low_test.jtl
│  ├─ mixed_load_medium_test.jtl
│  ├─ order_service_test.jtl
│  └─ product_service_test.jtl
└─ troubleshooting_guide.md

```