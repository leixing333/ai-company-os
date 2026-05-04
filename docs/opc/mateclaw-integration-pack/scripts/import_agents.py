#!/usr/bin/env python3
"""
OPC Agent 批量导入脚本
将 opc_agents_import.json 中定义的 22 个数字员工批量导入到 MateClaw

使用方法：
    python import_agents.py --url http://localhost:8080 --username admin --password xxx
    
    或使用环境变量：
    export MATECLAW_URL=http://localhost:8080
    export MATECLAW_USERNAME=admin
    export MATECLAW_PASSWORD=your_password
    python import_agents.py
"""

import os
import sys
import argparse
import logging

# 将 api 目录加入 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from mateclaw_client import MateClawClient, MateClawAPIError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="OPC Agent 批量导入工具 - 将 OPC 数字员工导入到 MateClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python import_agents.py --url http://localhost:8080 --username admin --password mypass
  python import_agents.py  # 使用环境变量 MATECLAW_URL, MATECLAW_USERNAME, MATECLAW_PASSWORD
        """
    )
    parser.add_argument(
        "--url",
        default=os.getenv("MATECLAW_URL", "http://localhost:8080"),
        help="MateClaw 服务地址 (默认: http://localhost:8080)"
    )
    parser.add_argument(
        "--username",
        default=os.getenv("MATECLAW_USERNAME", "admin"),
        help="管理员用户名 (默认: admin)"
    )
    parser.add_argument(
        "--password",
        default=os.getenv("MATECLAW_PASSWORD", ""),
        help="管理员密码"
    )
    parser.add_argument(
        "--import-file",
        default=os.path.join(os.path.dirname(__file__), '..', 'agents', 'opc_agents_import.json'),
        help="导入文件路径 (默认: ../agents/opc_agents_import.json)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅验证文件格式，不实际导入"
    )
    args = parser.parse_args()

    print("\n" + "="*50)
    print("  OPC Agent 批量导入工具 v1.0")
    print("="*50)
    print(f"  目标服务器: {args.url}")
    print(f"  管理员账号: {args.username}")
    print(f"  导入文件:   {args.import_file}")
    if args.dry_run:
        print("  模式:       DRY RUN（仅验证，不导入）")
    print("="*50 + "\n")

    # 验证导入文件存在
    if not os.path.exists(args.import_file):
        print(f"❌ 错误：导入文件不存在: {args.import_file}")
        sys.exit(1)

    if args.dry_run:
        import json
        with open(args.import_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 文件格式验证通过")
        print(f"   工作空间数量: {len(data.get('workspaces', []))}")
        print(f"   Agent 数量:   {len(data.get('agents', []))}")
        print("\nAgent 列表：")
        for agent in data.get('agents', []):
            print(f"   - [{agent.get('workspace_id', '?')}] {agent['name']} ({agent['role']})")
        return

    # 验证密码不为空
    if not args.password:
        print("❌ 错误：请提供管理员密码（--password 参数或 MATECLAW_PASSWORD 环境变量）")
        sys.exit(1)

    # 初始化客户端
    client = MateClawClient(
        base_url=args.url,
        username=args.username,
        password=args.password
    )

    # 测试连接
    print("正在连接 MateClaw 服务器...")
    try:
        client._login()
        print("✅ 连接成功！\n")
    except MateClawAPIError as e:
        print(f"❌ 连接失败: {e}")
        print("\n请检查：")
        print("  1. MateClaw 服务是否已启动")
        print("  2. 服务地址是否正确")
        print("  3. 用户名和密码是否正确")
        sys.exit(1)

    # 执行批量导入
    print("开始批量导入 Agent...\n")
    try:
        results = client.batch_import_agents(args.import_file)
    except Exception as e:
        print(f"❌ 导入过程中发生错误: {e}")
        sys.exit(1)

    # 输出结果
    print("\n" + "="*50)
    print("  导入结果")
    print("="*50)
    
    success_count = len(results['success'])
    failed_count = len(results['failed'])
    
    if success_count > 0:
        print(f"\n✅ 成功导入 {success_count} 个 Agent：")
        for item in results['success']:
            print(f"   ✓ {item['name']} (ID: {item.get('id', 'N/A')})")
    
    if failed_count > 0:
        print(f"\n❌ 导入失败 {failed_count} 个 Agent：")
        for item in results['failed']:
            print(f"   ✗ {item['name']}: {item['error']}")
        print("\n提示：失败的 Agent 可能已存在，或者工具配置不匹配。请登录 MateClaw 控制台手动检查。")
    
    print(f"\n总计：{success_count + failed_count} 个，成功 {success_count} 个，失败 {failed_count} 个")
    
    if failed_count == 0:
        print("\n🎉 所有 Agent 导入成功！")
        print("下一步：登录 MateClaw 控制台，验证 Agent 配置并发送第一个测试任务。")
    else:
        print(f"\n⚠️  有 {failed_count} 个 Agent 导入失败，请检查日志并手动处理。")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
