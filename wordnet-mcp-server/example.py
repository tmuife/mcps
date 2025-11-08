"""
WordNet MCP 服务使用示例
运行前请确保 WordNet MCP 服务已经启动
"""

# 假设WordNet MCP服务已经启动
# 下面展示如何在Cursor或其他MCP客户端中调用服务

def example_usage():
    # 这些函数在MCP客户端中可用
    # 此处仅作为示意，实际使用时无需定义这些函数
    
    # 1. 获取单词 "happy" 的同义词
    # 调用: get_synonyms("happy")
    # 返回: ["happy", "glad", "felicitous", ...]
    
    # 2. 获取单词 "good" 的反义词
    # 调用: get_antonyms("good")
    # 返回: ["bad", "evil", "ill", ...]
    
    # 3. 获取单词 "dog" 的上位词
    # 调用: get_hypernyms("dog")
    # 返回: ["canine", "domestic animal", ...]
    
    # 4. 获取单词 "animal" 的下位词
    # 调用: get_hyponyms("animal")
    # 返回: ["mammal", "bird", "fish", ...]
    
    # 5. 获取单词 "set" 的定义
    # 调用: get_definition("set")
    # 返回: [{"pos": "n", "definition": "...", "examples": [...]}, ...]
    
    # 6. 获取单词 "run" 的综合信息
    # 调用: get_word_info("run")
    # 返回包含同义词、反义词、上位词、下位词和定义的字典
    
    print("这是一个示例文件，展示如何使用WordNet MCP服务")
    print("请在Cursor或其他MCP客户端中调用相应的函数")

if __name__ == "__main__":
    example_usage() 