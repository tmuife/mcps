.PHONY: bump-version build publish install clean test

# 获取当前版本号并递增
VERSION := $(shell grep -m 1 'version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
MAJOR := $(shell echo $(VERSION) | cut -d. -f1)
MINOR := $(shell echo $(VERSION) | cut -d. -f2)
PATCH := $(shell echo $(VERSION) | cut -d. -f3)
NEW_PATCH := $(shell expr $(PATCH) + 1)
NEW_VERSION := $(MAJOR).$(MINOR).$(NEW_PATCH)

# 默认目标
all: clean build

# 版本号递增
bump-version:
	@echo "当前版本: $(VERSION)"
	@echo "新版本: $(NEW_VERSION)"
	@sed -i.bak 's/version = "$(VERSION)"/version = "$(NEW_VERSION)"/' pyproject.toml
	@sed -i.bak 's/__version__ = "$(VERSION)"/__version__ = "$(NEW_VERSION)"/' src/wordnet_mcp_server/__init__.py
	@rm -f pyproject.toml.bak src/wordnet_mcp_server/__init__.py.bak
	@echo "版本号已更新到 $(NEW_VERSION)"

# 构建包
build: bump-version
	@echo "构建包..."
	@uv build
	@echo "构建完成"

# 发布到PyPI
publish: build
	@echo "发布到PyPI..."
	@uv publish
	@echo "发布完成"
	@echo "版本 $(NEW_VERSION) 已发布"

# 本地安装
install: build
	@echo "本地安装..."
	@uv pip install -e .
	@echo "安装完成"

# 运行测试
test:
	@echo "运行测试..."
	@uv run pytest tests/
	@echo "测试完成"

# 清理构建文件
clean:
	@echo "清理构建文件..."
	@rm -rf dist build *.egg-info
	@echo "清理完成"

# 帮助信息
help:
	@echo "可用命令:"
	@echo "  make bump-version  - 递增版本号"
	@echo "  make build         - 递增版本号并构建包"
	@echo "  make publish       - 递增版本号、构建并发布到PyPI"
	@echo "  make install       - 本地安装"
	@echo "  make test          - 运行测试"
	@echo "  make clean         - 清理构建文件" 