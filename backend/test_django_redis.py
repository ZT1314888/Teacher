#!/usr/bin/env python
"""测试 Django Redis 配置"""
import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from django.conf import settings

print("=" * 60)
print("Django Redis 配置测试")
print("=" * 60)

# 1. 检查配置
print("\n1️⃣ 检查 Redis 配置:")
print(f"   USE_REDIS: {settings.CACHES['default']['BACKEND']}")
print(f"   LOCATION: {settings.CACHES['default']['LOCATION']}")
print(f"   SESSION_ENGINE: {settings.SESSION_ENGINE}")

# 2. 测试缓存写入
print("\n2️⃣ 测试缓存写入:")
try:
    cache.set('test_key', 'Hello Redis!', timeout=60)
    print("   ✅ 缓存写入成功")
except Exception as e:
    print(f"   ❌ 缓存写入失败: {e}")
    sys.exit(1)

# 3. 测试缓存读取
print("\n3️⃣ 测试缓存读取:")
try:
    value = cache.get('test_key')
    if value == 'Hello Redis!':
        print(f"   ✅ 缓存读取成功: {value}")
    else:
        print(f"   ❌ 缓存值不匹配: {value}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ 缓存读取失败: {e}")
    sys.exit(1)

# 4. 测试缓存删除
print("\n4️⃣ 测试缓存删除:")
try:
    cache.delete('test_key')
    value = cache.get('test_key')
    if value is None:
        print("   ✅ 缓存删除成功")
    else:
        print(f"   ❌ 缓存删除失败，值仍存在: {value}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ 缓存删除失败: {e}")
    sys.exit(1)

# 5. 测试缓存统计
print("\n5️⃣ 缓存统计:")
try:
    # 写入一些测试数据
    for i in range(5):
        cache.set(f'test_{i}', f'value_{i}', timeout=300)
    
    # 读取数据
    values = [cache.get(f'test_{i}') for i in range(5)]
    print(f"   ✅ 批量操作成功，写入并读取 {len(values)} 条数据")
    
    # 清理测试数据
    for i in range(5):
        cache.delete(f'test_{i}')
    
except Exception as e:
    print(f"   ❌ 批量操作失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ Django Redis 配置测试全部通过！")
print("=" * 60)
print("\n💡 提示:")
print("   - Redis 缓存已正常工作")
print("   - Session 将存储在 Redis 中")
print("   - 可以在视图中使用 cache.get() 和 cache.set()")
print("   - 建议缓存频繁查询的数据以提高性能")
print()
