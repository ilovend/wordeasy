#!/usr/bin/env python3
"""
WordEasy 项目一键安装脚本
自动检测环境、安装依赖、初始化数据库
"""
import os
import sys
import subprocess
import platform

class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """打印步骤信息"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{message}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*50}{Colors.END}\n")

def print_success(message):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def run_command(command, cwd=None, check=True):
    """运行shell命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_error(f"命令执行失败: {e}")
        return False

def check_python_version():
    """检查Python版本"""
    print_step("检查 Python 版本")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    else:
        print_error(f"需要 Python 3.8+，当前版本: {version.major}.{version.minor}.{version.micro}")
        return False

def check_node_version():
    """检查Node.js版本"""
    print_step("检查 Node.js 版本")
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print_success(f"Node.js {version} ✓")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("未找到 Node.js，请先安装 Node.js 16+")
        print_warning("下载地址: https://nodejs.org/")
        return False

def create_backend_data_dir():
    """创建后端数据目录"""
    print_step("创建数据目录")
    data_dir = os.path.join("backend", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print_success(f"已创建目录: {data_dir}")
    else:
        print_success(f"目录已存在: {data_dir}")
    return True

def install_backend_dependencies():
    """安装后端依赖"""
    print_step("安装 Python 依赖")
    backend_dir = "backend"
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print_warning("建议使用虚拟环境，但将继续安装...")
    
    # 安装依赖
    if run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=backend_dir):
        print_success("Python 依赖安装成功")
        return True
    else:
        print_error("Python 依赖安装失败")
        return False

def install_frontend_dependencies():
    """安装前端依赖"""
    print_step("安装 Node.js 依赖")
    frontend_dir = "frontend"
    
    # 检查 package.json
    if not os.path.exists(os.path.join(frontend_dir, "package.json")):
        print_error(f"未找到 {frontend_dir}/package.json")
        return False
    
    # 安装依赖
    print("正在运行 npm install，这可能需要几分钟...")
    if run_command("npm install", cwd=frontend_dir):
        print_success("Node.js 依赖安装成功")
        return True
    else:
        print_error("Node.js 依赖安装失败")
        print_warning("尝试: cd frontend && npm install --legacy-peer-deps")
        return False

def init_database():
    """初始化数据库"""
    print_step("初始化数据库")
    backend_dir = "backend"
    
    # 检查 init_db.py
    if not os.path.exists(os.path.join(backend_dir, "init_db.py")):
        print_warning("未找到 init_db.py，跳过数据库初始化")
        print_warning("数据库将在首次启动时自动创建")
        return True
    
    # 运行初始化脚本
    if run_command(f"{sys.executable} init_db.py", cwd=backend_dir):
        print_success("数据库初始化成功")
        return True
    else:
        print_warning("数据库初始化失败，但可以在首次启动时自动创建")
        return True

def create_env_files():
    """创建环境配置文件"""
    print_step("创建配置文件")
    
    # 后端 .env (可选)
    backend_env = os.path.join("backend", ".env.example")
    if not os.path.exists(backend_env):
        with open(backend_env, "w", encoding="utf-8") as f:
            f.write("# 后端环境配置示例\n")
            f.write("# DATABASE_URL=sqlite:///./data/wordeasy.db\n")
            f.write("# CORS_ORIGINS=http://localhost:5173\n")
        print_success("已创建 backend/.env.example")
    
    # 前端 .env (可选)
    frontend_env = os.path.join("frontend", ".env.example")
    if not os.path.exists(frontend_env):
        with open(frontend_env, "w", encoding="utf-8") as f:
            f.write("# 前端环境配置示例\n")
            f.write("# VITE_API_BASE_URL=/api\n")
        print_success("已创建 frontend/.env.example")
    
    return True

def print_next_steps():
    """打印后续步骤"""
    print_step("安装完成！")
    
    print(f"{Colors.GREEN}{Colors.BOLD}🎉 恭喜！WordEasy 已准备就绪{Colors.END}\n")
    
    print(f"{Colors.BOLD}启动方式:{Colors.END}")
    print(f"\n{Colors.YELLOW}Windows 用户:{Colors.END}")
    print(f"  双击运行: {Colors.BLUE}restart.bat{Colors.END}")
    print(f"  或命令行: {Colors.BLUE}.\\restart.bat{Colors.END}")
    
    print(f"\n{Colors.YELLOW}macOS/Linux 用户:{Colors.END}")
    print(f"  {Colors.BLUE}chmod +x start.sh{Colors.END}")
    print(f"  {Colors.BLUE}./start.sh{Colors.END}")
    
    print(f"\n{Colors.YELLOW}手动启动:{Colors.END}")
    print(f"  后端: {Colors.BLUE}cd backend && python -m uvicorn app.main:app --reload{Colors.END}")
    print(f"  前端: {Colors.BLUE}cd frontend && npm run dev{Colors.END}")
    
    print(f"\n{Colors.BOLD}访问地址:{Colors.END}")
    print(f"  前端应用: {Colors.BLUE}http://localhost:5173{Colors.END}")
    print(f"  后端API:  {Colors.BLUE}http://localhost:8000{Colors.END}")
    print(f"  API文档:  {Colors.BLUE}http://localhost:8000/docs{Colors.END}")
    
    print(f"\n{Colors.BOLD}需要帮助?{Colors.END}")
    print(f"  查看文档: {Colors.BLUE}README.md{Colors.END}")
    print(f"  安装指南: {Colors.BLUE}INSTALL.md{Colors.END}")
    print(f"\n{Colors.GREEN}祝你使用愉快！{Colors.END}\n")

def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════╗")
    print("║     WordEasy 项目自动安装脚本              ║")
    print("║     自动检测环境并安装所有依赖              ║")
    print("╚════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # 检查是否在项目根目录
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print_error("请在项目根目录下运行此脚本")
        sys.exit(1)
    
    steps = [
        ("检查环境", [
            check_python_version,
            check_node_version
        ]),
        ("准备后端", [
            create_backend_data_dir,
            install_backend_dependencies,
            init_database
        ]),
        ("准备前端", [
            install_frontend_dependencies
        ]),
        ("创建配置", [
            create_env_files
        ])
    ]
    
    total_steps = sum(len(funcs) for _, funcs in steps)
    current_step = 0
    failed_steps = []
    
    for category, functions in steps:
        for func in functions:
            current_step += 1
            print(f"\n{Colors.BOLD}[{current_step}/{total_steps}]{Colors.END}", end=" ")
            
            try:
                if not func():
                    failed_steps.append(func.__name__)
            except Exception as e:
                print_error(f"执行 {func.__name__} 时出错: {e}")
                failed_steps.append(func.__name__)
    
    # 总结
    print("\n" + "="*50)
    if failed_steps:
        print_warning(f"安装完成，但有 {len(failed_steps)} 个步骤失败:")
        for step in failed_steps:
            print(f"  - {step}")
        print_warning("\n请检查错误信息并手动修复")
    else:
        print_success("所有步骤执行成功！")
    
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}安装被用户中断{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"发生未预期的错误: {e}")
        sys.exit(1)
