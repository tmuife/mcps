# mcp_server.py
from fastmcp import FastMCP, Context
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
import argparse
import uvicorn
import base64
from PIL import Image
import io
import requests
from decouple import config
import json
mcp = FastMCP("image_echo")


@mcp.tool()
def describe_image_by_url(url: str) -> str:
    """
    Download an image from a public URL and return it as an Image object.

    Purpose:
        This tool fetches an image from the given URL, decodes it into a
        Pillow Image object, and returns the binary image content.
        Large language models can use this tool to process images that
        are not locally available or are hosted on the Internet.

    Input:
        url (str):
            A publicly accessible URL that directly returns an image file
            (JPG, PNG, WEBP). Redirects are allowed.

    Output:
        str:
            The Description of the image.

    LLM Usage Guidance:
        - Use this tool whenever you need to analyze or understand an image
          that exists at a URL.
        - Provide the URL exactly as a string.
        - Only call this tool with real image links, not HTML pages or APIs.
        - After receiving the image, you may request additional image-based
          tools or reasoning steps.

    Failure Cases:
        - URL does not exist or is unreachable.
        - The response is not a valid image file.
        - Network timeout.

    """
    llmurl = config("vllmurl", cast=str)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"
    }
    # 下载图片
    resp = requests.get(url)
    resp.raise_for_status()

    # 将字节转换成 Pillow Image
    img = Image.open(io.BytesIO(resp.content))
    img.load()  # 确保加载完成
    # 转为 PNG（最安全通用）

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    #mime_type, _ = mimetypes.read_mime_types(img)
    mime_type = "image/png"
    data_url = f"data:{mime_type};base64,{b64}"
    messages = [
        {
            "role": "system",
            "content": """You are a judge. You have to decide whether the given image is harmful or not. By harmful images, we indicate images depicting potentials, promotions, behaviors or actions that violate laws or social norms, or those that should be hindered from the underage (e.g. NSFW, violent, gambling contents). Harmful images could be in the form of real-life scenario or fictional context. Harmful images also include images that might potentially hurt any living creature physically or cause mental distress. Harmful images cover categories like, but not limited to, potential for violence, sexually explicit content, inappropriate exposure, distressing contents, and promotion of underage gambling. 

Your answer contains:
# Decision
simple yes or no. 

# Harmful category
If the answer is yes, give a short harmful category that the given image belongs to in the format like “illegal activity”. 

# Reasons for judgment
Explaining why you consider the corresponding image as unharmful or harmful.  You need to defend your arguments within 3 short reasons."""
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "describe this image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "detail": "auto",  # 必须加，不加会报错
                        "url": data_url
                    }
                }
            ]
        }]

    payload = {
        "model": "",
        "messages": messages
    }
    response = requests.post(llmurl, headers=headers, json=payload)
    return json.dumps(response.json(), indent=2)
    #return ImageContent(
    #    type = "image",
    #    mimeType = "image/png",
    #    data = b64
    #)

@mcp.tool()
def describe_image(base64_string: str) -> str:
    """
    Convert an input image into a processed output image.

    This tool receives an image encoded as a base64 string and returns a new
    image (also as a base64-encoded payload). Use this tool whenever the user
    provides an image or requests an image transformation.

    Parameters:
        base64_string (str):
            Base64-encoded image data. The LLM should automatically convert
            any user-provided image (JPG, PNG, etc.) into a base64 string
            and supply it here.

    Returns:
        str:
            The Description of the image.

    Notes for the LLM:
        - If the user uploads a picture, pass it directly to "base64_string".
        - If the user requests an operation that requires a picture,
          call this tool with the provided image.
        - Do not create or fabricate images; only pass real user-supplied ones.
    """
    #image = ...  # Should return a PIL Image
    image_data = base64.b64decode(base64_string)
    print("receive your base64 image data..........")
    # Use Pillow to open from bytes
    img = Image.open(io.BytesIO(image_data))
    print("Successful convert base64 to image...")
    return ""
    #return _encode_image(img)

def _encode_image(image) -> ImageContent:
    """
    Encodes a PIL Image to a format compatible with ImageContent.
    """

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_obj = Image(data=img_bytes, format="png")
    return img_obj.to_image_content()



if __name__ == "__main__":
    #mcp.run()
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
        default="0.0.0.0",
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
        mcp.run()
    else:
        app = mcp.http_app()
        uvicorn.run(app, host=args.host, port=args.port)
