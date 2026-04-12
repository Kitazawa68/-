USE campus_trade;

-- Insert Mock Users (密码这里做简单演示不再加密，实际可用MD5或BCrypt)
INSERT INTO `user` (username, password, name, phone, email, role) VALUES 
('admin_user', '123456', '系统管理员', '13800138000', 'admin@stu.edu.cn', 'ADMIN'),
('john_doe', 'pass123', '张三', '13911112222', 'zhangsan@stu.edu.cn', 'USER'),
('jane_smith', 'pass123', '李四', '13733334444', 'lisi@stu.edu.cn', 'USER');

-- Insert Mock Goods (商品)
INSERT INTO `goods` (name, price, content, status, user_id) VALUES 
('九成新iPhone 13', 2500.00, '毕业出，带壳膜，电池92%', 'ON_SALE', 2),
('高等数学（第七版）上下册', 15.50, '有些笔记，不影响阅读', 'ON_SALE', 3),
('小米台灯', 45.00, '可调色温，几乎没怎么用', 'ON_SALE', 2);

-- Insert Mock Purchases (求购)
INSERT INTO `purchase` (name, address, phone, user_id) VALUES 
('王五（收）', '东区13栋', '13612345678', 3),
('张三（本人收）', '西区8栋', '13911112222', 2);

-- Insert Mock Orders (订单)
INSERT INTO `order` (order_no, good_name, total, status, user_id, sale_id) VALUES 
('ORD_20240101_001', '高等数学（第七版）上下册', 15.50, 'COMPLETED', 2, 3),
('ORD_20240105_002', '小米台灯', 45.00, 'PENDING', 3, 2);

-- Insert Mock Comments (评论)
INSERT INTO `comment` (content, user_id, fid) VALUES 
('手机能刀吗？', 3, 1),
('15块包邮送到东区可以吗？', 2, 2);

-- Insert Mock Collections (收藏)
INSERT INTO `collection` (user_id, fid, module) VALUES 
(3, 1, 'goods'),
(2, 2, 'goods');
