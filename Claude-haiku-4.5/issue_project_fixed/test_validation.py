"""验证Issue #446修复效果"""
import sys
sys.path.insert(0, 'src')
from fake_useragent import UserAgent
import random

# 测试Issue #446原始场景
random.seed(123)
ua = UserAgent(
    browsers=['Chrome', 'Firefox', 'Edge', 'Opera', 'Safari'],
    os=['Windows', 'Mac OS X'],
    min_version=131
)

agents = [ua.random for _ in range(50)]
unique = len(set(agents))

print('Issue #446修复验证:')
print(f'  生成数量: 50')
print(f'  唯一数量: {unique}')
print(f'  重复率: {(50-unique)/50*100:.1f}%')
print(f'  期望: 唯一数量 >= 5 (90%重复率以下)')
print(f'  结果: {"✅ 修复成功" if unique >= 5 else "❌ 修复失败"}')
