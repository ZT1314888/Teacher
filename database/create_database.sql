-- 教室预约系统数据库创建脚本
-- 使用方法：在 MySQL 命令行或 Navicat 等工具中执行此脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS classroom_reservation 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE classroom_reservation;

-- 显示创建结果
SELECT 'Database classroom_reservation created successfully!' AS Message;
