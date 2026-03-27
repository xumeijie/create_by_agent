# Poetry Setup Guide

本项目使用 **Poetry** 来管理虚拟环境和依赖。

## 前提条件

### 安装 Poetry

**macOS/Linux:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**验证安装:**
```bash
poetry --version
```

## 项目设置

### 1. 初始化虚拟环境

```bash
# 在项目根目录运行
poetry install
```

此命令将：
- 创建虚拟环境
- 安装所有依赖（包括开发依赖）
- 生成 `poetry.lock` 文件（锁定依赖版本）

### 2. 激活虚拟环境

```bash
# 使用 poetry 运行命令
poetry run pytest

# 或进入虚拟环境
poetry shell
# 现在可以直接运行命令
pytest
exit  # 退出虚拟环境
```

## 常用命令

### 添加依赖

```bash
# 添加生产依赖
poetry add requests

# 添加开发依赖
poetry add --group dev pytest-html

# 指定版本
poetry add requests==2.31.0
```

### 更新依赖

```bash
# 更新所有依赖
poetry update

# 更新特定包
poetry update requests
```

### 查看依赖

```bash
# 显示依赖树
poetry show --tree

# 检查过期的包
poetry show --outdated
```

### 运行脚本

```bash
# 运行 pytest
poetry run pytest

# 运行特定测试
poetry run pytest tests/test_unit.py

# 运行单个测试
poetry run pytest tests/test_unit.py::TestDataGenerator::test_random_string

# 并行运行测试
poetry run pytest -n auto

# 生成覆盖率报告
poetry run pytest --cov=. --cov-report=html
```

### 代码质量工具

```bash
# 代码格式化
poetry run black .

# 导入排序
poetry run isort .

# 代码检查
poetry run flake8 .

# 类型检查
poetry run mypy core adapters utils
```

## 虚拟环境位置

poetry 会在以下位置创建虚拟环境：

**macOS/Linux:**
```
~/Library/Caches/pypoetry/virtualenvs/
```

**Windows:**
```
%APPDATA%\pypoetry\Cache\virtualenvs\
```

**或在项目目录中（推荐）：**

编辑 `poetry.toml` 或运行：
```bash
poetry config virtualenvs.in-project true
```

然后重新运行 `poetry install` 会在 `.venv` 目录创建虚拟环境。

## 切换到项目内虚拟环境

如果希望虚拟环境在项目目录中（`.venv`）：

```bash
# 配置 poetry
poetry config virtualenvs.in-project true

# 删除现有虚拟环境（如果有）
poetry env remove <python-version>

# 重新创建虚拟环境
poetry install
```

## 导出依赖到 requirements.txt

如果需要 `requirements.txt` 用于其他工具：

```bash
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --with dev --output requirements-dev.txt
```

## 在 CI/CD 中使用 Poetry

### GitHub Actions
```yaml
- uses: python-setup-poetry@v2
  with:
    python-version: "3.11"
    poetry-version: "1.7.0"

- run: poetry install
- run: poetry run pytest
```

### Jenkins
```groovy
stage('Setup') {
    steps {
        sh '''
            pip install poetry
            poetry install
        '''
    }
}

stage('Test') {
    steps {
        sh 'poetry run pytest'
    }
}
```

## 常见问题

### 问题：Poetry 找不到 Python

```bash
# 指定 Python 版本
poetry env use python3.11

# 查看可用的 Python 版本
poetry env list
```

### 问题：依赖冲突

```bash
# 清除缓存并重新安装
poetry cache clear . --all
poetry install
```

### 问题：更新包导致问题

```bash
# 回到锁定的版本
rm poetry.lock
poetry install
```

## 更多信息

- [Poetry 官方文档](https://python-poetry.org/docs/)
- [Poetry 配置参考](https://python-poetry.org/docs/configuration/)
- [依赖版本规范](https://python-poetry.org/docs/dependency-specification/)
