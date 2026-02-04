# 快速启动指南

## 🚀 5 分钟快速启动

### 前置条件

- ✅ Python 3.8+
- ✅ MySQL 8.0+
- ✅ Redis
- ✅ Node.js 14+

---

## 后端启动

### 1️⃣ 配置环境变量（30 秒）
```bash
cd backend
copy .env.example .env  # Windows
# 或
cp .env.example .env    # Linux/Mac
```

编辑 `.env` 文件，修改数据库密码：
```env
DATABASE_PASSWORD=你的MySQL密码
```

### 2️⃣ 创建数据库（30 秒）
```sql
CREATE DATABASE classroom_reservation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3️⃣ 安装依赖（1 分钟）
```bash
pip install -r requirements.txt
```

### 4️⃣ 启动 Redis（10 秒）
```bash
redis-server
```

在新终端测试连接：
```bash
redis-cli ping
# 应该返回: PONG
```

### 5️⃣ 数据库迁移（30 秒）
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ 启动后端（10 秒）
```bash
python manage.py runserver
```

✅ 后端运行在: http://localhost:8000

---

## 前端启动

### 1️⃣ 安装依赖（1 分钟）
```bash
cd frontend
npm install
```

### 2️⃣ 启动前端（10 秒）
```bash
npm run serve
```

✅ 前端运行在: http://localhost:8080

---

## 🎉 完成！

打开浏览器访问: http://localhost:8080

使用刚才创建的超级用户登录。

---

## ⚠️ 常见问题

### 问题 1: `ModuleNotFoundError: No module named 'decouple'`
**解决**: 
```bash
pip install python-decouple
```

### 问题 2: `RuntimeError: 'cryptography' package is required`
**解决**: 
```bash
pip install cryptography
```

### 问题 3: Redis 连接失败
**解决**: 
1. 检查 Redis 是否运行: `redis-cli ping`
2. 如果未安装，Windows 用户: `choco install redis-64`
3. 启动 Redis: `redis-server`

### 问题 4: MySQL 连接失败
**解决**: 
1. 检查 MySQL 服务是否运行
2. 检查 `.env` 文件中的数据库配置
3. 确认数据库已创建

### 问题 5: 前端无法连接后端
**解决**: 
1. 确认后端在 8000 端口运行
2. 检查浏览器控制台的错误信息
3. 确认 CORS 配置正确

---

## 📚 更多文档

- [详细配置说明](CONFIG.md)
- [P0 问题修复总结](../P0_FIXES_SUMMARY.md)
- [完整启动说明](../启动说明.txt)

---

## 🔍 验证安装

运行以下命令验证配置：

```bash
# 检查 Django 配置
python manage.py check

# 查看已安装的应用
python manage.py showmigrations

# 测试数据库连接
python manage.py dbshell
```

如果看到 `System check identified no issues (1 silenced).`，说明配置正确！
