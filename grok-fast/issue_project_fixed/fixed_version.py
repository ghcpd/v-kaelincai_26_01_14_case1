"""
Issue #446 Fixed Script
Fixed: Random user agents now use weighted selection based on usage percentages

当使用特定参数（browsers, os, min_version）时，UserAgent现在正确使用加权随机选择。
"""

from fake_useragent import UserAgent

print("测试Issue #446修复: 使用多个参数创建UserAgent\n")
print("=" * 80)

# 创建UserAgent实例，使用与issue中相同的参数
ua = UserAgent(
    browsers=["Chrome", "Firefox", "Edge", "Opera", "Safari", "Android",
              "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile",
              "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile"],
    os=["Windows", "Chrome OS", "Mac OS X", "Android", "iOS"],
    min_version=131,
)

print("生成10个随机User-Agent字符串：\n")

# 生成10个user agent并观察
user_agents = []
for i in range(1, 11):
    agent = ua.random
    user_agents.append(agent)
    print(f"{i}. {agent}")

# 统计重复
print("\n" + "=" * 80)
print("\n统计分析：")
unique_agents = set(user_agents)
print(f"总共生成: {len(user_agents)} 个")
print(f"唯一的: {len(unique_agents)} 个")
print(f"重复率: {((len(user_agents) - len(unique_agents)) / len(user_agents) * 100):.1f}%")

if len(unique_agents) == len(user_agents):
    print("\n✅ 成功：所有生成的User-Agent都是唯一的，随机性良好！")
elif len(unique_agents) >= 8:
    print("\n⚠️  注意：重复率较低，随机性可接受")
else:
    print("\n❌ 警告：生成的User-Agent存在较多重复，随机性不足！")