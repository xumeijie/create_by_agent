"""
报告模块 (Report Module)

用于生成和管理测试执行报告：

模块内容：
  - report_generator.py: 数据的HTML和Allure报告生成器
    - HTMLReportGenerator: 生成HTML格式的可视化报告
    - AllureReportGenerator: 生成Allure框架的报告（支持企业级统计）

使用流程：
  1. 收集测试执行结果
  2. 使用报告生成器处理结果
  3. 生成HTML或Allure格式的报告
  4. 通过浏览器或CI工具查看报告

快速使用：
    from reports.report_generator import HTMLReportGenerator
    
    # 生成报告
    generator = HTMLReportGenerator(output_path="reports/html")
    report_file = generator.generate_report(test_results)
    print(f"报告已生成: {report_file}")

报告文件位置：
    - Pytest HTML: reports/report.html
    - Coverage报告: htmlcov/index.html
    - Allure报告: reports/allure-report/
"""
