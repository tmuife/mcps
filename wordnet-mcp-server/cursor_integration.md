# 在Cursor中集成WordNet MCP服务

本文档详细介绍如何在Cursor中配置和使用WordNet MCP服务。

## 安装

首先，确保你已经安装了必要的依赖：

```bash
# 使用uv安装依赖
uv add nltk httpx "mcp[cli]"
```

## 启动MCP服务

在项目根目录下，使用以下任一命令启动MCP服务：

```bash
# 方法1：直接运行Python脚本
uv run python app.py

# 方法2：使用MCP CLI
uv run mcp
```

## 在Cursor中添加MCP服务

在Cursor中，按照以下步骤添加WordNet MCP服务：

1. 打开Cursor
2. 进入MCP服务配置界面
3. 添加新的MCP服务，输入以下信息：
   - 名称：WordNet MCP
   - 命令：python
   - 参数：app.py
   - 或者直接指定服务路径：[项目绝对路径]/app.py

## 使用MCP服务

一旦配置完成，你可以在Cursor中使用以下函数：

- `get_synonyms(word)` - 获取同义词
- `get_antonyms(word)` - 获取反义词
- `get_hypernyms(word)` - 获取上位词
- `get_hyponyms(word)` - 获取下位词
- `get_definition(word)` - 获取定义
- `get_word_info(word)` - 获取综合信息

## 示例操作

1. 输入一个单词，选择所需的功能
2. 服务将返回相应的结果
3. 结果可以在Cursor界面中查看和使用

## 故障排除

如果遇到问题，请检查：

1. MCP服务是否正在运行
2. Cursor中的MCP服务配置是否正确
3. 检查网络连接是否正常
4. 确保已经正确安装了所有依赖 