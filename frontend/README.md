# 前端开发文档

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.3.4 | 前端框架 |
| Tailwind CSS | 3.x | CSS 框架 |
| Heroicons | 2.x | 图标库 |
| Element Plus | 2.4.0 | UI 组件库（部分保留）|

## 项目结构

```
frontend/
├── src/
│   ├── assets/styles/
│   │   └── main.css              # Tailwind CSS 入口 + 自定义样式
│   ├── views/
│   │   ├── Booking.vue             # 预约流程页（新增）✨
│   │   ├── Classrooms.vue          # 教室列表页（已更新）✨
│   │   └── MyReservations.vue      # 我的预约页（已更新）✨
│   ├── api/                         # API 接口
│   ├── router/                      # 路由配置
│   ├── store/                       # Vuex 状态管理
│   └── App.vue                      # 根组件
├── tailwind.config.js               # Tailwind 配置 ✨
└── package.json
```

## 设计规范

### 配色方案

| 颜色 | 用途 | Hex 值 |
|------|------|-------|
| Primary | 主色调（深青色） | `#0F4C3A` |
| Secondary | 背景色/次要色 | `#F3F4F6` |
| Accent | 强调色（金色） | `#FBBF24` |
| Success | 成功/可用 | `#10B981` |
| Danger | 错误/占用 | `#EF4444` |
| Warning | 警告/待审核 | `#F59E0B` |

### 组件样式

| 组件 | 样式 |
|------|------|
| 按钮 | 大圆角 (rounded-xl)、阴影、hover 效果 |
| 卡片 | 白色背景、轻微阴影 (shadow-card) |
| 输入框 | 自定义边框、focus 状态 |
| 标签 Badge | 圆角、状态颜色区分 |

## 页面功能

### 1. 预约流程页 (Booking.vue)

**功能：**
- 三步预约流程：选择教室类型 → 选择日期时间 → 确认提交
- 左侧进度栏显示当前步骤
- 月份导航日历
- 时间段网格选择（可用/已占用/已选状态）
- 预约用途和参与人数输入

**文件位置：** `frontend/src/views/Booking.vue`

### 2. 教室列表页 (Classrooms.vue)

**功能：**
- 顶部筛选栏（类型、楼栋、容量、搜索）
- 教室卡片网格布局
- 设施图标展示（投影仪、电脑、麦克风、白板、空调）
- 状态标签（可用/维护中）
- 详情和预约操作按钮

**文件位置：** `frontend/src/views/Classrooms.vue`

### 3. 我的预约页 (MyReservations.vue)

**功能：**
- 用户欢迎信息和角色显示
- 三种状态标签页：进行中、已完成、已取消
- 预约卡片列表（日期块、信息、操作区）
- 取消预约功能（带时间限制检查）
- 取消确认对话框

**文件位置：** `frontend/src/views/MyReservations.vue`

## 自定义样式类

### 按钮类
- `.btn-primary` - 主要按钮（深青色）
- `.btn-secondary` - 次要按钮（白底灰边）
- `.btn-danger` - 危险按钮（红色）

### 卡片类
- `.card` - 基础卡片样式
- `.classroom-card` - 教室卡片（悬停效果）

### 状态类
- `.badge` - 基础徽章
- `.badge-success` - 成功徽章
- `.badge-warning` - 警告徽章
- `.badge-danger` - 危险徽章

### 交互类
- `.time-slot` - 时间段选择项
- `.calendar-day` - 日历日期项

## 使用指南

### 启动开发服务器

```bash
cd frontend
npm run serve
```

前端将在 http://localhost:8081 运行。

### 自定义样式

在组件中使用 Tailwind 类名即可：

```vue
<template>
  <button class="btn-primary">确定</button>
  <div class="card">内容</div>
  <span class="badge badge-success">可用</span>
</template>
```

### 颜色使用

```vue
<!-- 主色背景 -->
<div class="bg-primary">主色背景</div>

<!-- 主色文字 -->
<span class="text-primary">主色文字</span>

<!-- 强调色 -->
<div class="text-accent">强调文字</div>
```

## 待完成功能

1. **连接后端 API**
   - 替换模拟数据为真实 API 调用
   - 添加错误处理和加载状态

2. **完善路由配置**
   - 更新 router 配置，添加新页面路由
   - 配置路由守卫

3. **状态管理**
   - 整合 Vuex store 管理用户登录状态
   - 管理全局通知状态

4. **响应式优化**
   - 添加移动端适配
   - 优化平板显示效果

5. **测试**
   - 组件单元测试
   - 端到端测试
