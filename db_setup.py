import pymysql
import configparser
import random
import os
from faker import Faker

def get_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    return config

def update_config(db_name):
    config = get_config()
    config.set('mysql', 'database', db_name)
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def setup_db():
    config = get_config()
    host = config.get('mysql', 'host')
    port = config.getint('mysql', 'port')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    
    # 1. Connect without db to find the target database
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    target_db = config.get('mysql', 'database')
    
    with conn.cursor() as cursor:
        cursor.execute("SHOW DATABASES")
        dbs = [row[0] for row in cursor.fetchall() if row[0] not in ('information_schema', 'mysql', 'performance_schema', 'sys')]
        
        found = False
        for db in dbs:
            cursor.execute(f"USE `{db}`")
            cursor.execute("SHOW TABLES")
            tables = [row[0].lower() for row in cursor.fetchall()]
            if 'user' in tables and 'goods' in tables and 'order' in tables:
                target_db = db
                found = True
                break
                
        if not found:
            print("Warning: Could not automatically detect the database with `user`, `goods`, `order` tables.")
            print(f"Falling back to {target_db}.")
        else:
            print(f"Found target database: {target_db}")
            update_config(target_db)
            
        cursor.execute(f"USE `{target_db}`")
        
        # 2. Check and add create_time columns if necessary
        def add_column_if_not_exists(table, column, definition):
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{target_db}' AND TABLE_NAME='{table}' AND COLUMN_NAME='{column}'")
            if not cursor.fetchone():
                print(f"Adding '{column}' to '{table}'...")
                cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}")

        add_column_if_not_exists('user', 'create_time', 'DATETIME DEFAULT CURRENT_TIMESTAMP')
        add_column_if_not_exists('order', 'create_time', 'DATETIME DEFAULT CURRENT_TIMESTAMP')
        
        # 3. Create Dispute table
        print("Creating Dispute table if it does not exist...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `dispute` (
              `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '纠纷单唯一标识',
              `reporter_id` INT NOT NULL COMMENT '举报人的用户id',
              `target_type` VARCHAR(20) NOT NULL COMMENT '举报对象类型',
              `target_id` INT NOT NULL COMMENT '被举报的具体对象ID',
              `reason` TEXT NOT NULL COMMENT '举报原因描述',
              `evidence_img` VARCHAR(255) COMMENT '截图证据路径',
              `status` VARCHAR(20) DEFAULT '待处理' COMMENT '处理状态',
              `admin_note` TEXT COMMENT '管理员备注',
              `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '举报发起时间',
              `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '管理员最后修改时间',
              CONSTRAINT `fk_dispute_reporter` FOREIGN KEY (`reporter_id`) REFERENCES `user` (`id`)
            ) ENGINE=InnoDB;
        """)
        
        # 4. Generate some mock data just in case
        cursor.execute("SELECT id FROM `user`")
        users = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM `goods`")
        goods = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM `order`")
        orders = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM `comment`")
        comments = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT COUNT(*) FROM `dispute`")
        if cursor.fetchone()[0] == 0 and users:
            print("Generating mock data for dispute...")
            fake = Faker('zh_CN')
            statuses = ['待处理', '处理中', '已处罚', '已驳回']
            types_pool = []
            if goods: types_pool.append(('商品', goods))
            if orders: types_pool.append(('订单', orders))
            if comments: types_pool.append(('评论', comments))
            
            for _ in range(15):
                if not types_pool: break
                reporter_id = random.choice(users)
                target_type, target_pool = random.choice(types_pool)
                target_id = random.choice(target_pool)
                reason = fake.sentence()
                evidence_img = f"static/mock_img_{random.randint(1,5)}.png"
                status = random.choice(statuses)
                admin_note = fake.sentence() if status in ['已处罚', '已驳回'] else ""
                
                cursor.execute("""
                    INSERT INTO `dispute` (reporter_id, target_type, target_id, reason, evidence_img, status, admin_note, create_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, DATE_SUB(NOW(), INTERVAL %s DAY))
                """, (reporter_id, target_type, target_id, reason, evidence_img, status, admin_note, random.randint(0, 5)))
                
        # Commit all changes
        conn.commit()
        print("Database setup complete.")
        
    conn.close()

if __name__ == '__main__':
    setup_db()
