@echo off
echo ====================================================
echo         Selenium 自动化测试执行器
echo ====================================================
echo.

REM 设置编码为UTF-8
chcp 65001 > nul

REM 检查当前目录
echo 📂 当前目录: %CD%
echo.

REM 检查必要文件是否存在
if not exist "run_complete_tests.py" (
    echo ❌ 错误: 未找到 run_complete_tests.py 文件
    echo 请确保在正确的目录中执行此脚本
    pause
    exit /b 1
)

if not exist "test_cases" (
    echo ❌ 错误: 未找到 test_cases 目录
    echo 请确保在正确的目录中执行此脚本
    pause
    exit /b 1
)

echo ✅ 文件检查通过
echo.

REM 显示菜单
:menu
echo 请选择执行选项:
echo 1. 完整测试 (Chrome + Firefox + Edge)
echo 2. 仅 Chrome 测试
echo 3. 仅 Firefox 测试
echo 4. 仅 Edge 测试
echo 5. 快速验证测试
echo 6. 查看现有报告
echo 7. 清理报告目录
echo 8. 退出
echo.

set /p choice=请输入选项 (1-8): 

if "%choice%"=="1" goto full_test
if "%choice%"=="2" goto chrome_only
if "%choice%"=="3" goto firefox_only
if "%choice%"=="4" goto edge_only
if "%choice%"=="5" goto quick_test
if "%choice%"=="6" goto view_reports
if "%choice%"=="7" goto clean_reports
if "%choice%"=="8" goto exit
goto invalid_choice

:full_test
echo.
echo 🚀 执行完整测试 (所有浏览器)...
python run_complete_tests.py
goto end

:chrome_only
echo.
echo 🔵 执行 Chrome 浏览器测试...
python run_complete_tests.py --chrome-only
goto end

:firefox_only
echo.
echo 🦊 执行 Firefox 浏览器测试...
python run_complete_tests.py --firefox-only
goto end

:edge_only
echo.
echo 🔷 执行 Edge 浏览器测试...
python run_complete_tests.py --edge-only
goto end

:quick_test
echo.
echo ⚡ 执行快速验证测试...
echo 测试用户注册功能...
python -m pytest test_cases/test_user_registration.py::TestUserRegistration::test_user_registration_success --browser=chrome --base-url=http://127.0.0.1:8080 -v -s
if %errorlevel% equ 0 (
    echo ✅ 快速验证测试通过
) else (
    echo ❌ 快速验证测试失败
)
goto end

:view_reports
echo.
echo 📊 查看现有报告...
if exist "reports" (
    echo 报告目录内容:
    dir reports /b
    echo.
    
    REM 检查HTML报告
    if exist "reports\chrome_report.html" (
        echo 发现 Chrome 测试报告，是否打开? (Y/N)
        set /p open_chrome=
        if /i "%open_chrome%"=="Y" start reports\chrome_report.html
    )
    
    if exist "reports\firefox_report.html" (
        echo 发现 Firefox 测试报告，是否打开? (Y/N)
        set /p open_firefox=
        if /i "%open_firefox%"=="Y" start reports\firefox_report.html
    )
    
    if exist "reports\edge_report.html" (
        echo 发现 Edge 测试报告，是否打开? (Y/N)
        set /p open_edge=
        if /i "%open_edge%"=="Y" start reports\edge_report.html
    )
    
    if exist "reports\selenium_summary_report.md" (
        echo 发现汇总报告，是否查看? (Y/N)
        set /p view_summary=
        if /i "%view_summary%"=="Y" type reports\selenium_summary_report.md
    )
    
    if exist "reports\performance_metrics.json" (
        echo 发现性能数据，是否查看摘要? (Y/N)
        set /p view_perf=
        if /i "%view_perf%"=="Y" (
            echo 性能数据文件大小:
            for %%i in (reports\performance_metrics.json) do echo   %%~zi bytes
            echo 前10条记录:
            python -c "import json; data=json.load(open('reports/performance_metrics.json')); [print(f'{r[\"page\"]}: {r[\"load_time\"]}s ({r[\"browser\"]})') for r in data[:10]]" 2>nul
        )
    )
) else (
    echo ❌ 未找到 reports 目录
    echo 请先执行测试生成报告
)
goto end

:clean_reports
echo.
echo 🧹 清理报告目录...
if exist "reports" (
    echo 警告: 这将删除所有现有报告文件
    echo 是否确定要继续? (Y/N)
    set /p confirm=
    if /i "%confirm%"=="Y" (
        echo 正在备份现有报告...
        set backup_dir=reports_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
        set backup_dir=%backup_dir: =0%
        if not exist "%backup_dir%" mkdir "%backup_dir%"
        xcopy reports "%backup_dir%" /E /I /Y > nul 2>&1
        echo 备份完成: %backup_dir%
        
        echo 正在清理报告目录...
        rmdir /s /q reports
        mkdir reports
        echo ✅ 报告目录已清理
    ) else (
        echo 取消清理操作
    )
) else (
    echo ❌ 未找到 reports 目录
)
goto end

:invalid_choice
echo.
echo ❌ 无效选项，请重新选择
echo.
goto menu

:end
echo.
echo 操作完成！
echo.
echo 是否返回主菜单? (Y/N)
set /p return_menu=
if /i "%return_menu%"=="Y" (
    echo.
    goto menu
)

:exit
echo.
echo 👋 感谢使用 Selenium 自动化测试执行器
echo.
pause
exit /b 0