DELIMITER $$

DROP PROCEDURE IF EXISTS SeedMassiveData$$

CREATE PROCEDURE SeedMassiveData()
BEGIN
    DECLARE i INT DEFAULT 1;
    
    -- Insert 100 random users
    WHILE i <= 100 DO
        INSERT INTO user(username, password, name, phone, email, role)
        VALUES (
            CONCAT('stu_', i),
            'e10adc3949ba59abbe56e057f20f883e', -- 123456
            CONCAT('同学_', i),
            CONCAT('13', FLOOR(RAND() * 900000000 + 100000000)),
            CONCAT('stu_', i, '@school.edu'),
            IF(RAND() > 0.9, 'ADMIN', 'USER')
        );
        SET i = i + 1;
    END WHILE;

    SET i = 1;
    
    -- Insert 10,000 random goods
    WHILE i <= 10000 DO
        INSERT INTO goods(user_id, name, price, content, `status`)
        VALUES (
            FLOOR(1 + RAND() * 100), 
            CONCAT(
                ELT(FLOOR(1 + RAND() * 5), '九成新', '极品', '毕业出', '亏本卖', '全新'),
                ELT(FLOOR(1 + RAND() * 5), 'iPhone 13', '高数课本', '电风扇', '山地自行车', '机械键盘'),
                '_', i
            ), 
            ROUND(RAND() * 2000, 2), 
            CONCAT('出回血，成色很不错的，走过路边不要错过，看中直接拍。编号:', i), 
            ELT(FLOOR(1 + RAND() * 3), 'ON_SALE', 'PENDING_AUDIT', 'SOLD')
        );
        SET i = i + 1;
    END WHILE;

    -- Insert some fake orders
    SET i = 1;
    WHILE i <= 50 DO
        INSERT INTO `order`(user_id, sale_id, order_no, good_name, total, `status`)
        VALUES (
            FLOOR(1 + RAND() * 100),
            FLOOR(1 + RAND() * 100),
            CONCAT('ORD', ROUND(RAND() * 10000000)),
            CONCAT('已购商品_', i),
            ROUND(RAND() * 500, 2),
            ELT(FLOOR(1 + RAND() * 4), 'PENDING', 'PAID', 'SHIPPED', 'COMPLETED')
        );
        SET i = i + 1;
    END WHILE;

END$$

DELIMITER ;

CALL SeedMassiveData();
