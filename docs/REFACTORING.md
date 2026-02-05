# 基于Python高校教室预约系统 - 重构方案

> 本文档基于开题报告需求与现有代码分析，制定系统重构方案。

---

## 一、项目概况

### 1.1 基本信息

| 项目 | 内容 |
|------|------|
| 课题名称 | 基于Python高校教室预约系统的设计与实现 |
| 学生 | 彭彦超 |
| 指导教师 | 秦正斌（助教/硕士） |

### 1.2 技术栈

| 层次 | 技术 |
|------|------|
| 后端 | Django + DRF + MySQL |
| 前端 | Vue 3 + Element Plus |
| 认证 | JWT (SimpleJWT) |
| 缓存 | Redis（可选） |

---

## 二、现状分析

### 2.1 已完成功能

| 模块 | 状态 |
|------|------|
| 用户管理（三种角色） | ✅ 完整 |
| 教室管理 | ✅ 完整 |
| 预约管理 | ✅ 完整 |
| 公告管理 | ✅ 完整 |
| 课程管理 | ⚠️ 部分完成 |
| 权限控制 | ✅ 完整 |
| JWT 认证 | ✅ 完整 |

### 2.2 待补充功能（开题报告需求）

| 需求 | 当前状态 |
|------|----------|
| 数据统计报表 | ❌ 需新增 |
| 智能推荐教室 | ❌ 需新增 |
| 高并发优化 | ⚠️ 需优化 |

---

## 三、系统目标与范围

### 3.1 系统目标

- 建立“预约-审核-使用-统计”的完整闭环
- 降低预约冲突与人工沟通成本
- 提升教室资源利用率与管理效率

### 3.2 范围界定

**In Scope（本次重构覆盖）**

- 预约全流程数字化（含审核、取消、统计）
- 角色权限细分（学生/教师/管理员）
- 统计报表与可视化基础
- 规则型智能推荐
- 并发控制与缓存优化

**Out of Scope（明确不做）**

- 跨校区协同与复杂排课联动
- 设备物联实时状态联动（仅记录设备配置，不做在线状态）
- 大规模机器学习推荐模型

**Later（后续迭代方向）**

- 分层审核（学院级-校级）
- 设备联动状态与工单系统

---

## 四、重构方案

### 4.1 新增模块

#### 数据统计模块 (stats)

```
backend/apps/stats/
├── models.py          # ClassroomUsageStats, DailyReservationSummary
├── views.py           # 仪表盘、使用率、汇总、导出
├── serializers.py
└── urls.py
```

**API 接口：**
- `GET /api/stats/dashboard/` - 仪表盘统计
- `GET /api/stats/classroom-usage/` - 教室使用率
- `GET /api/stats/daily-summary/` - 每日汇总
- `GET /api/stats/export/` - 导出报表

#### 智能推荐模块

```
backend/apps/classrooms/services/recommendation.py
```

**API 接口：**
- `POST /api/classrooms/recommend/` - 智能推荐教室

#### 通知模块 (notifications)

```
backend/apps/notifications/
├── models.py          # Notification（审批/拒绝/提醒/取消/系统）
├── views.py
├── serializers.py
└── urls.py
```

**API 接口：**
- `GET /api/notifications/` - 通知列表
- `POST /api/notifications/mark-read/` - 标记已读
- `POST /api/notifications/mark-all-read/` - 全部已读

### 4.2 角色权限矩阵

| 能力 | 学生 | 教师 | 管理员 |
|------|------|------|--------|
| 注册/登录 | ✅ | ✅ | ✅ |
| 预约教室 | ✅ | ✅ | ✅ |
| 取消预约 | ✅ | ✅ | ✅ |
| 审核预约 | ❌ | ❌ | ✅ |
| 查看教室使用统计 | ✅（仅个人） | ✅（仅个人/教学相关） | ✅（全局） |
| 管理教室资源 | ❌ | ❌ | ✅ |
| 管理用户 | ❌ | ❌ | ✅ |

默认采用单级审核（管理员审核），不引入学院级/校级分层审批。

### 4.3 预约流程与状态机

**状态定义：** `pending`（待审核）、`approved`（已通过）、`rejected`（已拒绝）、`cancelled`（已取消）、`expired`（已过期）

**预约冲突检测规则：**

- 同一教室、同一日期，时间区间重叠即为冲突
- 重叠判断：`start < existing_end` 且 `end > existing_start`

**取消规则（默认）：**

- 距开始时间 >= 2 小时可取消（可配置）
- 已开始或已结束不可取消

### 4.4 教室类型与属性模型

**教室类型：** 多媒体教室、普通教室、实验室、阶梯教室

**关键属性字段：**

- 容量（可容纳人数）
- 设备配置（投影、音响、麦克风、电脑等）
- 楼栋/楼层/房间号
- 可用时间段（学期/节次）

**预约筛选约束：**

- 人数 <= 容量
- 设备需求必须被教室配置满足

### 4.5 数据模型变更清单

**新增模型：**

- `ClassroomType`：`name`, `description`
- `ClassroomEquipment`：`name`, `description`
- `ReservationStatusLog`：`reservation`, `from_status`, `to_status`, `operator`, `created_at`
- `Notification`：`user`, `type`, `content`, `is_read`, `created_at`

**统计相关模型：**

- `ClassroomUsageStats`：`classroom`, `date`, `hours_used`, `reservation_count`
- `DailyReservationSummary`：`date`, `total_reservations`, `approved_count`, `rejected_count`

### 4.6 接口与响应规范

**统一响应格式：**

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

**分页约定：**

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "count": 100,
    "next": "/api/xxx?page=2",
    "previous": null,
    "results": []
  }
}
```

**错误码示例：**

- `401` 未认证
- `403` 无权限
- `409` 预约冲突
- `422` 参数校验失败

### 4.7 并发与冲突控制

**缓存锁 key 规则：**

```
reservation:lock:{classroom_id}:{date}:{start_time}
```

**锁超时策略：**

- 默认 10 秒，避免死锁
- 先锁 -> 冲突校验 -> 写入 -> 释放锁

### 4.8 统计与推荐的设计动机/边界

**动机：**

- 参考国外系统优势，补齐“统计可视化”和“智能推荐”能力
- 提高教室利用率与预约效率

**推荐算法（初版规则）：**

- 容量匹配（人数最接近且满足）
- 设备匹配（满足需求）
- 历史使用率（优先空闲率高的教室）

### 4.9 性能优化

#### Redis 缓存策略

| 缓存项 | Key | 过期时间 |
|--------|-----|----------|
| 教室列表 | `classroom:list` | 1小时 |
| 教室详情 | `classroom:detail:{id}` | 30分钟 |
| 可用教室 | `rooms:available:{date}:{time}` | 5分钟 |
| 用户预约 | `user:reservations:{id}` | 15分钟 |
| 统计数据 | `stats:dashboard:{date}` | 1天 |

#### 并发控制

使用缓存锁防止预约冲突：
```python
lock_key = f'reservation:lock:{classroom_id}:{date}:{start_time}'
```

#### 数据库优化

- 添加复合索引：`(date, status)`, `(user, date)`, `(classroom, date)`
- 使用 `select_related()` 优化查询
- 使用 `prefetch_related()` 优化多对多查询

### 4.10 代码规范

- **后端**: PEP 8 + 类型注解 + Docstring
- **前端**: Vue 3 风格指南 + Composition API
- **统一**: API 响应格式、异常处理、日志系统

---

## 五、实施计划

| 阶段 | 周期 | 内容 | 优先级 |
|------|------|------|--------|
| **一** | 1-2周 | 新增：统计、推荐、通知模块 | 高 |
| **二** | 1周 | Redis缓存、并发锁、索引优化 | 高 |
| **三** | 1周 | 代码规范、API格式、日志系统 | 中 |
| **四** | 1周 | 环境配置、启动脚本、文档 | 中 |

---

## 六、项目结构

```
Teacher/
├── backend/
│   ├── apps/
│   │   ├── users/           # 用户管理
│   │   ├── classrooms/      # 教室管理
│   │   ├── reservations/    # 预约管理
│   │   ├── announcements/   # 公告管理
│   │   ├── courses/         # 课程管理
│   │   ├── stats/           # 统计分析 [新增]
│   │   └── notifications/   # 通知管理 [新增]
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   └── development.py
│   │   └── urls.py
│   ├── core/                # 核心模块 [新增]
│   │   ├── responses.py
│   │   ├── exceptions.py
│   │   └── permissions.py
│   └── services/            # 业务服务 [新增]
│       └── recommendation.py
├── frontend/
│   └── src/
│       ├── views/Stats.vue         [新增]
│       └── components/
│           ├── NotificationBadge.vue [新增]
│           └── StatCard.vue         [新增]
├── scripts/               # 启动脚本 [已完成]
│   ├── start.sh
│   └── db.sh
├── docs/                  # 文档目录 [已完成]
├── logs/                  # 日志目录 [已完成]
└── .venv/                 # 虚拟环境
```

---

## 七、本地开发

### 6.1 环境要求

| 组件 | 版本 |
|------|------|
| Python | 3.12+ |
| Node.js | 18+ |
| MySQL | 8.0+ |
| Redis | 7+ |

### 6.2 快速启动

```bash
# 启动系统（前后端）
./scripts/start.sh

# 数据库迁移
./scripts/db.sh migrate

# 收集静态文件
./scripts/db.sh collectstatic

# 创建超级用户
./scripts/db.sh createsuperuser
```

### 6.3 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:8081/ |
| 后端 API | http://localhost:8000/api/ |
| 管理后台 | http://localhost:8000/admin/ |

---

## 八、预期成果

### 7.1 功能完整性

开题报告所有需求 100% 实现

### 7.2 技术指标

- API 响应时间 < 200ms
- 支持 500+ 并发用户
- 缓存命中率 > 80%
- 测试覆盖率 > 70%

### 7.3 代码质量

- 遵循 PEP 8 / Vue 3 规范
- 完整的类型注解和文档
- 完善的开发文档

---

## 九、测试与验证场景

- 预约冲突用例：同一教室同一时间段重复预约应被拒绝
- 取消规则：距开始时间 < 2 小时不可取消
- 权限边界：学生/教师不可审批或管理教室
- 统计一致性：缓存命中与数据库统计结果一致
