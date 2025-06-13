# Selenium功能测试项目

## 项目概述

本项目是对SockShop微服务系统进行功能测试的Selenium自动化测试套件，基于Selenium IDE录制的用户操作流程，优化为pytest测试代码。

## 系统功能覆盖

### ✅ 已测试功能
- 用户注册和登录
- 商品目录浏览和筛选
- 商品详情查看
- 用户地址管理
- 愿望清单功能

### ❌ 系统限制
- 购物车功能不完整
- 订单处理流程缺失
- 支付功能未完全实现

## 项目结构

```
selenium_tests/
├── conftest.py                         ✅ pytest配置
├── requirements.txt                    ✅ 依赖列表
├── test_cases/
│   ├── test_user_registration.py       ✅ 用户注册测试
│   ├── test_user_login.py              ✅ 用户登录测试
│   ├── test_product_browsing.py        ✅ 商品浏览测试
│   └── test_complete_workflow.py       ✅ 完整流程测试
├── utils/
│   └── analyze_results.py              ✅ 结果分析
├── run_selenium_tests.sh               ✅ 执行脚本
├── setup_project.sh                   ✅ 项目设置
├── quick_test.py                      ✅ 环境验证
├── .gitignore                         ✅ Git忽略文件
└── README.md                          ✅ 项目说明
```

## 快速开始

### 环境要求
- Python 3.8+
- Chrome/Firefox/Edge浏览器
- SockShop系统运行在 http://127.0.0.1:8080

### 安装依赖
```bash
pip install -r requirements.txt
````

### 执行测试

```bash
# 执行所有测试
bash run_selenium_tests.sh

# 或者指定浏览器执行
pytest test_cases/ --browser=chrome --base-url=http://127.0.0.1:8080 --html=reports/test_report.html

# 并行执行（如果安装了pytest-xdist）
pytest test_cases/ -n 2
```

## 测试报告

测试完成后查看以下报告：

- `reports/chrome_report.html` - Chrome浏览器测试报告
- `reports/firefox_report.html` - Firefox浏览器测试报告
- `reports/performance_metrics.json` - 页面性能数据
- `reports/selenium_summary_report.md` - 测试汇总分析

## 配置说明

### 浏览器配置

支持Chrome、Firefox、Edge三种浏览器，通过`--browser`参数指定：

```bash
pytest --browser=chrome    # Chrome浏览器
pytest --browser=firefox   # Firefox浏览器
pytest --browser=edge      # Edge浏览器
```

### URL配置

通过`--base-url`参数指定SockShop系统地址：

```bash
pytest --base-url=http://localhost:8080
pytest --base-url=http://your-sockshop-url
```

## 开发指南

### 添加新测试用例

1. 在`test_cases/`目录创建新的测试文件
2. 继承测试基类并使用`driver_setup` fixture
3. 使用`record_performance`函数记录性能数据
4. 添加适当的等待和错误处理

### 测试数据管理

- 使用时间戳生成唯一的测试数据
- 避免硬编码测试数据
- 在测试结束后清理测试数据

### 最佳实践

- 使用显式等待而不是硬编码sleep
- 为每个关键操作添加断言验证
- 失败时自动截图保存到reports目录
- 使用描述性的测试方法名

## 故障排除

### 常见问题

1. **浏览器驱动问题**: 使用webdriver-manager自动管理
2. **元素定位失败**: 检查页面加载状态，使用WebDriverWait
3. **模态框交互**: 确保等待模态框完全显示后再操作
4. **网络超时**: 增加等待时间或检查网络连接

### 调试技巧

- 使用`--capture=no`参数查看实时输出
- 检查`reports/`目录下的失败截图
- 启用浏览器GUI模式观察操作过程

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 添加测试用例
4. 提交Pull Request

## 许可证

本项目用于教学目的，遵循MIT许可证。


```
sockshop
├─ conftest.py
├─ README.md
├─ reports
│  ├─ chrome_complete_report.html
│  ├─ edge_complete_report.html
│  ├─ performance_metrics.json
│  └─ selenium_summary_report.md
├─ requirements.txt
├─ run_selenium_tests.bat
├─ run_selenium_tests.py
├─ SockShop_Functional_Tests.side
├─ test_cases
│  ├─ .pytest_cache
│  │  ├─ CACHEDIR.TAG
│  │  ├─ README.md
│  │  └─ v
│  │     └─ cache
│  │        ├─ lastfailed
│  │        ├─ nodeids
│  │        └─ stepwise
│  ├─ test_complete_workflow.py
│  ├─ test_product_browsing.py
│  ├─ test_user_login.py
│  ├─ test_user_registration.py
│  └─ __pycache__
│     ├─ test_complete_workflow.cpython-312-pytest-8.3.5.pyc
│     ├─ test_product_browsing.cpython-312-pytest-8.3.5.pyc
│     ├─ test_user_login.cpython-312-pytest-8.3.5.pyc
│     └─ test_user_registration.cpython-312-pytest-8.3.5.pyc
├─ test_testcompleteshoppingworkflow.py
├─ test_testloginfailurescenarios.py
├─ test_testproductbrowsing.py
├─ test_testuserlogin.py
├─ test_testuserregistration.py
└─ utils
   └─ analyze_results.py

```