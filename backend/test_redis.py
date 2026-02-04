#!/usr/bin/env python
"""测试 Redis 连接"""
import sys

try:
    import redis
    
    # 尝试连接 Redis
    r = redis.Redis(host='127.0.0.1', port=6379, db=1, socket_connect_timeout=5)
    
    # 测试 ping
    response = r.ping()
    
    if response:
        print("✅ Redis 连接成功！")
        print(f"   服务器地址: 127.0.0.1:6379")
        print(f"   数据库: 1")
        
        # 测试读写
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        print(f"   读写测试: {value.decode('utf-8')}")
        r.delete('test_key')
        
        print("\n✅ Redis 工作正常，可以使用！")
        sys.exit(0)
    else:
        print("❌ Redis ping 失败")
        sys.exit(1)
        
except redis.ConnectionError as e:
    print(f"❌ Redis 连接失败: {e}")
    print("\n解决方案:")
    print("1. 检查 Redis 服务是否运行")
    print("2. 检查端口 6379 是否被占用")
    print("3. 检查防火墙设置")
    sys.exit(1)
    
except ImportError:
    print("❌ redis 模块未安装")
    print("\n请运行: pip install redis")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    sys.exit(1)
