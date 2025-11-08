"""
为Cursor添加WordNet MCP服务的辅助脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def get_project_path():
    """获取项目的绝对路径"""
    return os.path.abspath(os.path.dirname(__file__))

def configure_cursor_mcp():
    """将WordNet MCP服务添加到Cursor配置"""
    project_path = get_project_path()
    app_path = os.path.join(project_path, "app.py")
    
    print(f"WordNet MCP服务路径: {app_path}")
    print("开始配置Cursor MCP服务...")
    
    try:
        # 检查Python解释器路径
        python_path = sys.executable
        print(f"使用Python解释器: {python_path}")
        
        # 生成配置命令
        command = f"{python_path} {app_path}"
        name = "WordNet MCP"
        
        print(f"服务名称: {name}")
        print(f"执行命令: {command}")
        
        # 打印配置指南
        print("\n===== Cursor MCP服务配置指南 =====")
        print("1. 打开Cursor应用")
        print("2. 进入MCP服务配置界面")
        print("3. 添加新的MCP服务，使用以下信息:")
        print(f"   - 名称: {name}")
        print(f"   - 命令: {python_path}")
        print(f"   - 参数: {app_path}")
        print("4. 点击保存，完成配置")
        print("=====================================")
        
        # 提示用户可以使用MCP Installer工具
        print("\n你也可以使用MCP Installer工具自动添加:")
        print(f"MCP_Installer.add_to_cursor_config(")
        print(f'    name="{name}",')
        print(f'    command="{python_path}",')
        print(f'    args=["{app_path}"]')
        print(f")")
        
    except Exception as e:
        print(f"配置失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("WordNet MCP服务 - Cursor配置工具")
    configure_cursor_mcp() 