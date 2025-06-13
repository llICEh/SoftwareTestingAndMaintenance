# Online Boutique 功能测试项目

## 📖 项目概述

本项目是基于Google Cloud的Online Boutique微服务演示应用的功能测试，使用Selenium IDE录制用户操作流程，导出为Python代码，通过pytest执行自动化测试。

## 🏗 系统架构

Online Boutique是一个完整的微服务电商应用，包含11个微服务：
- **frontend**: Go语言前端服务
- **cartservice**: C#购物车服务  
- **productcatalogservice**: Go商品目录服务
- **currencyservice**: Node.js货币转换服务
- **paymentservice**: Node.js支付服务
- **checkoutservice**: Go结算服务
- 以及其他支持服务...

## 🛠 技术栈

- **功能测试**: Selenium IDE + Python + pytest
- **数据分析**: Python + json
- **报告生成**: pytest-html + Markdown
- **浏览器支持**: Chrome, Edge, Firefox

## 📁 项目结构

```
online_boutique_tests/
├── test_cases/                    # 测试用例
│   ├── test_homepage_browsing.py      # 首页浏览测试
│   ├── test_product_detail.py         # 商品详情测试
│   ├── test_shopping_cart.py          # 购物车功能测试
│   ├── test_complete_purchase.py      # 完整购买流程测试
│   └── test_error_handling.py         # 错误处理测试
├── utils/                         # 工具脚本
│   └── analyze_results.py             # 结果分析脚本
├── reports/                       # 测试报告
│   ├── performance_metrics.json       # 性能数据
│   └── online_boutique_summary_report.md  # 汇总报告
├── conftest.py                    # pytest配置
├── run_online_boutique_tests.py   # 测试执行器
├── requirements.txt               # Python依赖
└── README.md                      # 项目说明
```

## 🚀 快速开始

### 环境准备

1. **部署Online Boutique**:
```bash
kubectl apply -f ./release/kubernetes-manifests.yaml
kubectl get service frontend-external
```

2. **安装Python依赖**:
```bash
pip install -r requirements.txt
```

3. **验证服务可访问**:
```bash
curl http://127.0.0.1:8080
```

### 执行测试

```bash
# 执行完整测试（Chrome + Edge）
python run_online_boutique_tests.py

# 执行单个浏览器测试
pytest test_cases/ --browser=chrome --base-url=http://127.0.0.1:8080 --html=reports/chrome_report.html

# 生成分析报告
python utils/analyze_results.py
```

## 🧪 测试覆盖

### 功能模块
- ✅ **首页浏览**: 商品展示、推荐功能、货币转换
- ✅ **商品详情**: 详情页加载、商品信息显示
- ✅ **购物车功能**: 添加商品、数量选择、多商品管理
- ✅ **完整购买**: 端到端购买流程（浏览→购物车→支付→确认）
- ✅ **错误处理**: 表单验证、支付验证、边界情况

### 特色功能
- 🌍 **多货币支持**: USD, EUR, GBP, JPY, CAD
- 🤖 **智能推荐**: 基于购物车的商品推荐
- 🛒 **完整购物车**: 与SockShop不同，支持完整的购物车功能
- 💳 **支付流程**: 完整的地址和支付信息处理

## 📊 测试结果

### 性能指标
- 页面平均加载时间: < 3秒
- 购买流程响应时间: < 5秒
- 货币转换响应时间: < 1秒
- 跨浏览器兼容性: Chrome, Edge

### 测试优势对比

| 测试维度 | Online Boutique | SockShop |
|---------|----------------|----------|
| 业务完整性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 功能覆盖度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 真实场景 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 错误处理 | ⭐⭐⭐⭐ | ⭐⭐ |
| 用户体验 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 测试亮点

1. **真实电商体验**: 完整的从浏览到支付的端到端流程
2. **无用户认证复杂性**: 专注核心业务功能测试
3. **丰富业务场景**: 货币转换、推荐算法、购物车管理
4. **完善错误处理**: 表单验证、支付验证、数据格式检查

## 🔧 开发指南

### 添加新测试用例

1. 使用Selenium IDE录制新的用户操作流程
2. 导出为Python代码
3. 按照现有模式优化代码
4. 添加性能监控和错误处理
5. 更新测试覆盖文档

### 自定义配置

```python
# conftest.py 中修改默认配置
def pytest_addoption(parser):
    parser.addoption("--base-url", default="http://your-domain.com")
    parser.addoption("--browser", default="chrome")
```

### 扩展浏览器支持

```python
# 在conftest.py中添加新浏览器
elif browser_type.lower() == "safari":
    driver = webdriver.Safari()
```

## 📈 监控和报告

### 性能监控
```json
{
  "page": "首页加载",
  "load_time": 2.34,
  "browser": "chrome",
  "timestamp": "2025-06-08 10:30:00",
  "status": "fast"
}
```

### 报告生成
- **HTML报告**: pytest-html生成的详细测试报告
- **性能报告**: JSON格式的性能数据收集
- **汇总报告**: Markdown格式的综合分析报告

## 🚀 CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Online Boutique Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python run_online_boutique_tests.py
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/new-test`)
3. 提交更改 (`git commit -am 'Add new test'`)
4. 推送到分支 (`git push origin feature/new-test`)
5. 创建 Pull Request

## 📞 支持与联系

- 项目问题: [GitHub Issues](https://github.com/your-repo/issues)
- 文档问题: [Wiki](https://github.com/your-repo/wiki)
- 邮件联系: your-email@example.com

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
```
onlineboutique
├─ .pytest_cache
│  ├─ CACHEDIR.TAG
│  ├─ README.md
│  └─ v
│     └─ cache
│        ├─ lastfailed
│        ├─ nodeids
│        └─ stepwise
├─ conftest.py
├─ OnlineBoutique_Functional_Tests.side
├─ README.md
├─ reports
│  ├─ chrome_online_boutique_report.html
│  ├─ edge_online_boutique_report.html
│  ├─ online_boutique_summary_report.md
│  └─ performance_metrics.json
├─ run_online_boutique_tests.py
├─ test_cases
│  ├─ test_complete_purchase.py
│  ├─ test_error_handling.py
│  ├─ test_homepage_browsing.py
│  ├─ test_product_detail.py
│  ├─ test_shopping_cart.py
│  └─ __pycache__
│     ├─ test_complete_purchase.cpython-312-pytest-8.3.5.pyc
│     ├─ test_error_handling.cpython-312-pytest-8.3.5.pyc
│     ├─ test_homepage_browsing.cpython-312-pytest-8.3.5.pyc
│     ├─ test_product_detail.cpython-312-pytest-8.3.5.pyc
│     └─ test_shopping_cart.cpython-312-pytest-8.3.5.pyc
├─ test_testcompletepurchaseworkflow.py
├─ test_testerrorhandlingscenarios.py
├─ test_testhomepagebrowsing.py
├─ test_testproductdetailview.py
├─ test_testshoppingcartworkflow.py
├─ utils
│  └─ analyze_results.py
└─ __pycache__
   └─ conftest.cpython-312-pytest-8.3.5.pyc

```