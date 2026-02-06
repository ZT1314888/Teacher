# 教室预约管理系统 - 项目部署指南

## 项目简介

本项目是一个基于 **Django + Vue 3** 的教室预约管理系统，采用前后端分离架构。

- **后端**: Django 4.2 + Django REST Framework + SimpleJWT
- **前端**: Vue 3 + Element Plus + TailwindCSS + Vite
- **数据库**: MySQL 8.0+
- **缓存**: Redis（可选）

## 项目结构

```
Teacher/
├── backend/                # Django 后端
│   ├── apps/               # 应用模块
│   │   ├── users/          # 用户管理
│   │   ├── classrooms/     # 教室管理
│   │   ├── reservations/   # 预约管理
│   │   ├── announcements/  # 公告管理
│   │   ├── courses/        # 课程管理
│   │   ├── notifications/  # 通知管理
│   │   └── stats/          # 统计分析
│   ├── config/             # Django 配置
│   │   ├── settings.py     # 项目设置
│   │   ├── urls.py         # 路由配置
│   │   └── wsgi.py         # WSGI 入口
│   ├── manage.py           # Django 管理脚本
│   └── .env.example        # 环境变量模板
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/            # API 接口
│   │   ├── components/     # 公共组件
│   │   ├── views/          # 页面视图
│   │   ├── router/         # 路由配置
│   │   ├── store/          # Vuex 状态管理
│   │   └── main.js         # 入口文件
│   ├── package.json        # 前端依赖
│   └── vite.config.js      # Vite 配置
├── database/               # 数据库脚本
├── scripts/                # 辅助脚本
└── environment.yml         # Conda 环境配置（备用）
```

---

## 环境要求

| 工具 | 版本要求 |
|------|---------|
| Python | >= 3.12 |
| Node.js | >= 18 |
| MySQL | >= 8.0 |
| uv | 最新版 |
| npm | >= 9 |
| Redis | >= 7.0（可选） |

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/ZT1314888/Teacher.git
cd Teacher
```

### 2. 安装 uv（Python 包管理器）

如果尚未安装 `uv`，请先安装：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. 创建虚拟环境并安装后端依赖

```bash
# 在项目根目录下执行
uv venv
uv sync
```

### 4. 安装前端依赖

```bash
cd frontend
npm install
cd ..
```

### 5. 配置数据库

#### 5.1 创建 MySQL 数据库

登录 MySQL 并执行：

```sql
CREATE DATABASE IF NOT EXISTS Teacher
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

或使用命令行：

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS Teacher CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

#### 5.2 配置环境变量

复制环境变量模板并修改：

```bash
cp backend/.env.example backend/.env
```

编辑 `backend/.env` 文件，填写你的数据库信息：

```ini
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=Teacher
DATABASE_USER=root
DATABASE_PASSWORD=your_mysql_password
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Redis 配置（可选，设为 False 则使用内存缓存）
USE_REDIS=False
REDIS_URL=redis://127.0.0.1:6379/1
```

#### 5.3 执行数据库迁移

```bash
cd backend
../.venv/bin/python manage.py makemigrations
../.venv/bin/python manage.py migrate
```

### 6. 创建管理员账号

```bash
cd backend
../.venv/bin/python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

也可以通过浏览器访问 `http://localhost:8000/register-admin/` 注册管理员。

---

## 启动项目

### 启动后端服务

```bash
cd backend
../.venv/bin/python manage.py runserver
```

后端服务运行在：http://localhost:8000

### 启动前端服务

打开一个新的终端窗口：

```bash
cd frontend
npm run dev
```

前端服务运行在：http://localhost:5173

---

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:5173 |
| 后端 API | http://localhost:8000/api/ |
| 后台管理 | http://localhost:8000/admin/ |

---

## 常用命令

### 后端命令

```bash
cd backend

# 创建并应用数据库迁移
../.venv/bin/python manage.py makemigrations
../.venv/bin/python manage.py migrate

# 创建超级管理员
../.venv/bin/python manage.py createsuperuser

# 收集静态文件
../.venv/bin/python manage.py collectstatic --noinput

# 启动开发服务器
../.venv/bin/python manage.py runserver

# 指定端口启动
../.venv/bin/python manage.py runserver 8001
```

### 前端命令

```bash
cd frontend

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 停止服务

```bash
# 方法 1：在运行服务的终端按 Ctrl+C

# 方法 2：终止占用端口的进程
# 停止后端（端口 8000）
kill -9 $(lsof -ti:8000)

# 停止前端（端口 5173）
kill -9 $(lsof -ti:5173)
```

---

## 技术栈详情

### 后端依赖

| 包名 | 用途 |
|------|------|
| Django | Web 框架 |
| djangorestframework | REST API |
| djangorestframework-simplejwt | JWT 认证 |
| django-simpleui | 后台管理美化 |
| django-cors-headers | 跨域支持 |
| django-filter | 数据过滤 |
| django-ckeditor | 富文本编辑器 |
| django-redis | Redis 缓存 |
| python-decouple | 环境变量管理 |
| Pillow | 图片处理 |
| pymysql | MySQL 驱动 |
| cryptography | 加密支持 |

### 前端依赖

| 包名 | 用途 |
|------|------|
| Vue 3 | 前端框架 |
| Element Plus | UI 组件库 |
| Vue Router | 路由管理 |
| Vuex | 状态管理 |
| Axios | HTTP 请求 |
| TailwindCSS | CSS 工具类 |
| FullCalendar | 日历组件 |
| Vite | 构建工具 |

---

## 常见问题

### Q: 端口被占用怎么办？

```bash
# 查看占用端口的进程
lsof -i :8000

# 终止进程
kill -9 $(lsof -ti:8000)
```

### Q: 数据库连接失败？

1. 确认 MySQL 服务已启动
2. 确认 `backend/.env` 中的数据库配置正确
3. 确认数据库 `Teacher` 已创建

### Q: 前端请求后端 API 报跨域错误？

确保后端服务运行在 `http://localhost:8000`，前端 Vite 配置中已设置代理：

```js
// frontend/vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### Q: Redis 未安装怎么办？

项目默认不依赖 Redis。在 `backend/.env` 中设置 `USE_REDIS=False` 即可使用内存缓存（仅适用于开发环境）。
