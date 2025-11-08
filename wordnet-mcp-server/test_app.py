"""
WordNet MCP 服务的测试文件
"""

import pytest
from app import get_synonyms, get_antonyms, get_hypernyms, get_hyponyms, get_definition, get_word_info

def test_get_synonyms():
    """测试同义词功能"""
    synonyms = get_synonyms("happy")
    assert len(synonyms) > 0
    assert isinstance(synonyms, list)
    assert all(isinstance(s, str) for s in synonyms)

def test_get_antonyms():
    """测试反义词功能"""
    # 使用一个有明确反义词的词
    antonyms = get_antonyms("good")
    assert isinstance(antonyms, list)
    # 注意：某些词可能没有反义词，所以不一定要验证长度

def test_get_hypernyms():
    """测试上位词功能"""
    hypernyms = get_hypernyms("dog")
    assert isinstance(hypernyms, list)
    assert len(hypernyms) > 0

def test_get_hyponyms():
    """测试下位词功能"""
    hyponyms = get_hyponyms("animal")
    assert isinstance(hyponyms, list)
    assert len(hyponyms) > 0

def test_get_definition():
    """测试定义功能"""
    definitions = get_definition("python")
    assert isinstance(definitions, list)
    for definition in definitions:
        assert "pos" in definition
        assert "definition" in definition
        assert "examples" in definition

def test_get_word_info():
    """测试综合信息功能"""
    info = get_word_info("book")
    assert "synonyms" in info
    assert "antonyms" in info
    assert "hypernyms" in info
    assert "hyponyms" in info
    assert "definitions" in info

if __name__ == "__main__":
    # 简单的手动测试
    print("Testing get_synonyms('happy'):")
    print(get_synonyms("happy"))
    
    print("\nTesting get_word_info('book'):")
    print(get_word_info("book")) 