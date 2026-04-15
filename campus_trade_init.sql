CREATE DATABASE IF NOT EXISTS campus_trade DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE campus_trade;

CREATE TABLE `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `username` VARCHAR(50) NOT NULL COMMENT '用户账号',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `name` VARCHAR(50) COMMENT '姓名',
  `phone` VARCHAR(20) COMMENT '手机号',
  `email` VARCHAR(100) COMMENT '邮箱',
  `role` VARCHAR(20) DEFAULT 'USER' COMMENT '身份(USER/ADMIN)'
) ENGINE=InnoDB COMMENT='用户表';

CREATE TABLE `goods` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `name` VARCHAR(100) NOT NULL COMMENT '商品名称',
  `price` DECIMAL(10,2) NOT NULL COMMENT '价格',
  `content` TEXT COMMENT '详情',
  `image` VARCHAR(500) COMMENT '商品图片URL',
  `status` VARCHAR(20) DEFAULT 'ON_SALE' COMMENT '上架状态',
  `user_id` INT NOT NULL COMMENT '所属用户id',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB COMMENT='商品表';

CREATE TABLE `purchase` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `name` VARCHAR(50) NOT NULL COMMENT '用户姓名',
  `address` VARCHAR(255) COMMENT '收货地址',
  `phone` VARCHAR(20) COMMENT '电话号码',
  `user_id` INT NOT NULL COMMENT '发布求购的用户id',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB COMMENT='求购表';

CREATE TABLE `order` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `order_no` VARCHAR(50) NOT NULL UNIQUE COMMENT '订单编号',
  `good_name` VARCHAR(100) COMMENT '商品名称',
  `total` DECIMAL(10,2) NOT NULL COMMENT '总价',
  `status` VARCHAR(20) DEFAULT 'PENDING' COMMENT '状态',
  `user_id` INT NOT NULL COMMENT '买家id(关联用户)',
  `sale_id` INT NOT NULL COMMENT '卖家id(关联用户)',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
  FOREIGN KEY (`sale_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB COMMENT='订单表';

CREATE TABLE `comment` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `content` VARCHAR(500) NOT NULL COMMENT '评论内容',
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间',
  `user_id` INT NOT NULL COMMENT '评论人id',
  `pid` INT DEFAULT 0 COMMENT '父级id',
  `root_id` INT DEFAULT 0 COMMENT '根节点id',
  `fid` INT NOT NULL COMMENT '关联id',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB COMMENT='评论表';

CREATE TABLE `collection` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  `user_id` INT NOT NULL COMMENT '用户id',
  `fid` INT NOT NULL COMMENT '关联id',
  `module` VARCHAR(50) NOT NULL COMMENT '所属模块(商品/求购)',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB COMMENT='收藏表';
