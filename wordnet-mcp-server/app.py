import nltk
from nltk.corpus import wordnet as wn
from fastmcp import FastMCP
import argparse
from decouple import config
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
# Authentication middleware
def check_auth(request):
    """Check if the request has valid Bearer token authentication."""
    #auth_token = os.getenv("FASTMCP_AUTH_TOKEN")
    auth_token = config("api-token")
    if not auth_token:
        return True  # No auth required if token not set

    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        from starlette.responses import JSONResponse
        return JSONResponse({"error": "Missing or invalid Authorization header"}, status_code=401)

    token = auth_header[7:]  # Remove "Bearer " prefix
    if token != auth_token:
        from starlette.responses import JSONResponse
        return JSONResponse({"error": "Invalid token"}, status_code=401)
    return True
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        auth_result = check_auth(request)
        if auth_result != True:
            return auth_result
        return await call_next(request)

mcp = FastMCP(name="WordNet MCP")

# 确保WordNet数据已下载
def download_wordnet():
    nltk.download('wordnet')

# 下载所需数据
download_wordnet()

@mcp.tool()
def get_synonyms(word: str) -> list[str]:
    """获取给定单词的同义词列表"""
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

@mcp.tool()
def get_antonyms(word: str) -> list[str]:
    """获取给定单词的反义词列表"""
    antonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            for antonym in lemma.antonyms():
                antonyms.add(antonym.name().replace('_', ' '))
    return list(antonyms)

@mcp.tool()
def get_hypernyms(word: str) -> list[str]:
    """获取给定单词的上位词（更一般的概念）"""
    hypernyms = set()
    for syn in wn.synsets(word):
        for hypernym in syn.hypernyms():
            hypernyms.add(hypernym.name().split('.')[0].replace('_', ' '))
    return list(hypernyms)

@mcp.tool()
def get_hyponyms(word: str) -> list[str]:
    """获取给定单词的下位词（更具体的概念）"""
    hyponyms = set()
    for syn in wn.synsets(word):
        for hyponym in syn.hyponyms():
            hyponyms.add(hyponym.name().split('.')[0].replace('_', ' '))
    return list(hyponyms)

@mcp.tool()
def get_definition(word: str) -> list[dict]:
    """获取给定单词的所有定义"""
    definitions = []
    for syn in wn.synsets(word):
        definitions.append({
            "pos": syn.pos(),
            "definition": syn.definition(),
            "examples": syn.examples()
        })
    return definitions

@mcp.tool()
def get_word_info(word: str) -> dict:
    """获取单词的综合信息（同义词、反义词、定义等）"""
    return {
        "synonyms": get_synonyms(word),
        "antonyms": get_antonyms(word),
        "hypernyms": get_hypernyms(word),
        "hyponyms": get_hyponyms(word),
        "definitions": get_definition(word)
    }

def main():
    """命令行入口点，用于通过uvx命令启动服务"""
    # 确保WordNet数据已下载
    download_wordnet()
    # 启动MCP服务
    mcp.run()

if __name__ == "__main__":
    # 启动MCP服务
    parser = argparse.ArgumentParser(description="Words MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport method to use (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to when using HTTP/SSE transport (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to when using HTTP/SSE transport (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        download_wordnet()
        mcp.run(transport='stdio')
    else:
        download_wordnet()
        #mcp.run(transport=args.transport, host=args.host, port=args.port)
        app = mcp.http_app()
        auth_token = config("api-token")
        if auth_token:
            app.add_middleware(AuthMiddleware)
            uvicorn.run(app, host=args.host, port=args.port)