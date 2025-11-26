#!/usr/bin/env python3
"""
WordEasy 健康检查和自动修复脚本
检查项目状态并修复常见问题
"""
import os
import sys
import subprocess
import json
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_section(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def check_python_version():
    """检查Python版本"""
    print_section("检查 Python 环境")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python版本过低: {version.major}.{version.minor}.{version.micro} (需要 3.8+)")
        return False

def check_backend_dependencies():
    """检查后端依赖"""
    print_section("检查 Python 依赖")
    
    required_packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} 已安装")
        except ImportError:
            missing.append(package)
            print_error(f"{package} 未安装")
    
    if missing:
        print_warning(f"缺少依赖: {', '.join(missing)}")
        print(f"运行: cd backend && pip install -r requirements.txt")
        return False
    
    return True

def check_database():
    """检查数据库"""
    print_section("检查数据库")
    
    db_path = Path("backend/data/wordeasy.db")
    data_dir = Path("backend/data")
    
    # 检查目录
    if not data_dir.exists():
        print_warning("数据目录不存在，正在创建...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print_success("已创建数据目录")
    else:
        print_success("数据目录存在")
    
    # 检查数据库文件
    if not db_path.exists():
        print_warning("数据库文件不存在")
        print("首次运行时会自动创建，或运行: cd backend && python init_db.py")
        return False
    else:
        # 检查数据库大小
        size = db_path.stat().st_size
        print_success(f"数据库文件存在 ({size / 1024:.1f} KB)")
        return True

def check_node_modules():
    """检查Node模块"""
    print_section("检查 Node.js 依赖")
    
    node_modules = Path("frontend/node_modules")
    package_json = Path("frontend/package.json")
    
    if not package_json.exists():
        print_error("package.json 不存在")
        return False
    
    if not node_modules.exists():
        print_warning("node_modules 不存在")
        print("运行: cd frontend && npm install")
        return False
    
    print_success("node_modules 存在")
    return True

def check_ports():
    """检查端口占用"""
    print_section("检查端口")
    
    ports = [8000, 5173]
    occupied = []
    
    for port in ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                occupied.append(port)
                print_warning(f"端口 {port} 被占用")
            else:
                print_success(f"端口 {port} 可用")
        except Exception as e:
            print_warning(f"无法检查端口 {port}: {e}")
    
    if occupied:
        print("\n释放端口:")
        print("Windows: netstat -ano | findstr :<PORT> 然后 taskkill /PID <PID> /F")
        print("Linux/Mac: lsof -ti:<PORT> | xargs kill -9")
        return False
    
    return True

def check_file_structure():
    """检查文件结构"""
    print_section("检查项目结构")
    
    required_files = [
        "backend/app/main.py",
        "backend/app/database.py",
        "backend/app/models.py",
        "backend/app/crud.py",
        "backend/app/schemas.py",
        "backend/requirements.txt",
        "frontend/src/main.js",
        "frontend/src/App.vue",
        "frontend/package.json",
        "frontend/vite.config.js",
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"{file_path}")
        else:
            missing.append(file_path)
            print_error(f"{file_path} 缺失")
    
    if missing:
        print_error(f"缺少 {len(missing)} 个关键文件")
        return False
    
    return True

def auto_fix_data_directory():
    """自动修复数据目录"""
    data_dir = Path("backend/data")
    if not data_dir.exists():
        print_warning("正在创建数据目录...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print_success("已创建数据目录")
        return True
    return True

def auto_fix_gitignore():
    """自动修复.gitignore"""
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        print_warning("正在创建 .gitignore...")
        with open(gitignore, "w", encoding="utf-8") as f:
            f.write("# Python\n__pycache__/\n*.pyc\nvenv/\n*.db\n\n")
            f.write("# Node\nnode_modules/\ndist/\n\n")
            f.write("# IDE\n.vscode/\n.idea/\n")
        print_success("已创建 .gitignore")
        return True
    return True

def run_health_check():
    """运行完整健康检查"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║         WordEasy 健康检查工具                          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # 检查是否在项目根目录
    if not (Path("backend").exists() and Path("frontend").exists()):
        print_error("请在项目根目录运行此脚本")
        sys.exit(1)
    
    checks = [
        ("Python版本", check_python_version),
        ("Python依赖", check_backend_dependencies),
        ("数据库", check_database),
        ("Node依赖", check_node_modules),
        ("端口状态", check_ports),
        ("文件结构", check_file_structure),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"{name} 检查失败: {e}")
            results[name] = False
    
    # 自动修复
    print_section("自动修复")
    auto_fix_data_directory()
    auto_fix_gitignore()
    
    # 总结
    print_section("检查总结")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status} {name}{Colors.END}")
    
    print(f"\n通过: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ 所有检查通过！项目状态良好{Colors.END}")
        print(f"\n可以启动项目:")
        print(f"  Windows: {Colors.BLUE}restart.bat{Colors.END}")
        print(f"  Linux/Mac: {Colors.BLUE}./start.sh{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ 发现 {total - passed} 个问题{Colors.END}")
        print(f"\n请根据上述提示修复问题，或运行:")
        print(f"  {Colors.BLUE}python setup.py{Colors.END} (自动安装)")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_health_check()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}检查被用户中断{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"发生错误: {e}")
        sys.exit(1)
