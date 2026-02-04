# 配置说明文档

## 环境变量配置

本项目使用 `.env` 文件管理敏感配置信息。

### 首次部署步骤

1. **复制环境变量模板**
   ```bash
   cp .env.example .env
   ```

2. **修改 .env 文件中的配置**
   ```bash
   # 必须修改的配置项
   SECRET_KEY=your-secret-key-here-change-in-production
   DATABASE_PASSWORD=your_mysql_password
   
   # 生产环境必须修改
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

3. **生成安全的 SECRET_KEY**
   ```python
   # 在 Python 终端中运行
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

### 配置项说明

#### Django 核心配置
- `SECRET_KEY`: Django 密钥，用于加密签名（生产环境必须修改）
- `DEBUG`: 调试模式（生产环境必须设为 False）
- `ALLOWED_HOSTS`: 允许访问的域名列表，用逗号分隔

#### 数据库配置
- `DATABASE_NAME`: 数据库名称
- `DATABASE_USER`: 数据库用户名
- `DATABASE_PASSWORD`: 数据库密码
- `DATABASE_HOST`: 数据库主机地址
- `DATABASE_PORT`: 数据库端口

#### Redis 配置
- `REDIS_URL`: Redis 连接地址（格式：redis://host:port/db）

### 安全注意事项

⚠️ **重要提醒**：
1. `.env` 文件已添加到 `.gitignore`，不会被提交到版本控制
2. 生产环境必须使用强密码和随机 SECRET_KEY
3. 生产环境必须设置 `DEBUG=False`
4. 生产环境必须配置正确的 `ALLOWED_HOSTS`
5. 不要在代码中硬编码任何敏感信息


**启动 Redis**:
```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
```

**测试 Redis 连接**:
```bash
redis-cli ping
# 应该返回 PONG
```

### 验证配置

运行以下命令验证配置是否正确：

```bash
python manage.py check
```

如果配置正确，应该显示：
```
System check identified no issues (1 silenced).
```
