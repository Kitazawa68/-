# 校园二手交易平台 (Campus Trade)

一个基于 **前后端分离 + 管理后台** 架构的校园二手交易系统。

## 📁 目录结构

```
├── app.py                      # 管理后台入口 (Streamlit)
├── config.ini                  # 管理后台数据库配置
├── db.py / db_setup.py         # 数据库连接 & 自动建表
├── fix_db.py                   # 一键执行所有 SQL 初始化脚本
├── requirements.txt            # Python 依赖
├── components/                 # 管理后台功能模块
│   ├── module_a_dispute.py     # 纠纷工作台
│   ├── module_b_analyze.py     # 平台健康度分析
│   ├── module_c_dashboard.py   # 基础流水看板
│   ├── module_d_goods.py       # 商品库管理
│   ├── module_e_users.py       # 用户风控管理
│   └── module_f_orders.py      # 订单安全审计
├── student_side/--main/        # 学生端源码
│   ├── campus-trade-go/        # Go 后端 (Gin + GORM, 端口 8081)
│   ├── campus-trade-java/      # Java 后端 (Spring Boot + JPA, 端口 8080)
│   ├── campus-trade-web/       # Vue 前端 (Vite + Vue3 + Element Plus)
│   └── *.sql                   # 数据库初始化脚本
├── 一键启动后台.bat             # Windows 一键启动管理后台
└── 一键启动学生端.bat           # Windows 一键启动学生端
```

## 🔧 前置环境要求

请确保本地已安装以下环境：

| 环境 | 版本建议 | 用途 |
|------|---------|------|
| [MySQL](https://dev.mysql.com/downloads/installer/) | 8.x | 数据库 |
| [Python](https://www.python.org/downloads/) | 3.9+ | 管理后台运行 |
| [Node.js](https://nodejs.org/en/) | v18+ | 前端运行 |
| [Go](https://golang.google.cn/dl/) | 1.21+ | Go 后端运行 |
| [JDK](https://www.oracle.com/java/technologies/downloads/) | 17 | Java 后端运行 |

## 🛠️ 第一步：初始化数据库

1. 启动你本地的 MySQL 服务。

2. **修改数据库连接配置**（如果你的密码不是 `123456` 或端口不是 `3306`）：

   编辑根目录的 `config.ini`：
   ```ini
   [mysql]
   host = 127.0.0.1
   port = 3306
   user = root
   password = 你的密码
   database = campus_trade
   ```

3. 运行一键初始化脚本（自动建库、建表、生成模拟数据）：
   ```bash
   pip install pymysql faker
   python fix_db.py
   ```

   > 该脚本会自动执行 `campus_trade_init.sql`、`campus_trade_mock_data.sql`、`generate_10k.sql`，并创建管理后台所需的 `dispute` 表。

## 🚀 第二步：启动学生端

### 方式一：使用一键启动脚本 (Windows)

直接双击 `一键启动学生端.bat`，会自动启动 Go 后端和 Vue 前端。

### 方式二：手动启动

**启动 Go 后端** (端口 8081)：
```bash
cd student_side/--main/campus-trade-go
go mod tidy
go run .
```

**启动 Vue 前端**（新开一个终端）：
```bash
cd student_side/--main/campus-trade-web
npm install
npm run dev
```

前端服务启动后，请通过终端中打印的 `Local: http://localhost:xxxx/` 链接进入系统（通常是 `http://localhost:5173`）。

> [!TIP]
> **如果你的 MySQL 端口或密码不同**，Go 后端需要修改 `student_side/--main/campus-trade-go/database.go` 中的 DSN 连接串。
>
> Java 后端则支持环境变量覆盖，无需改文件：
> ```bash
> # Windows:
> set DB_PORT=3306
> set DB_PASS=你的密码
>
> # Mac/Linux:
> export DB_PORT=3306
> export DB_PASS=你的密码
> ```

## 📊 第三步：启动管理后台

### 方式一：使用一键启动脚本 (Windows)

双击 `一键启动后台.bat`。

### 方式二：手动启动

```bash
# 安装 Python 依赖（首次运行）
pip install -r requirements.txt

# 执行数据库补充建表（首次运行）
python db_setup.py

# 启动管理后台
streamlit run app.py
```

管理后台默认运行在 `http://localhost:8501`。

**登录密码**: `admin123`

## ⚙️ 数据库连接配置一览

本项目有多个后端服务，默认配置如下：

| 服务 | 端口 | DB端口 | 用户名 | 密码 | 配置文件 |
|------|------|--------|--------|------|---------|
| 管理后台 (Python) | 8501 | 3306 | root | 123456 | `config.ini` |
| Go 后端 | 8081 | 3306 | root | 123456 | `student_side/--main/campus-trade-go/database.go` |
| Java 后端 | 8080 | 3306 | root | 123456 | `student_side/--main/campus-trade-java/src/main/resources/application.properties` |

> [!IMPORTANT]
> 请确保所有服务连接的是 **同一个 MySQL 实例和同一个 `campus_trade` 数据库**。如果你本地 MySQL 的端口或密码不同，请统一修改上表中的三个配置文件。

## 🤝 团队 Git 协作规范

1. **不要**提交日志文件（`*.log`）、编译产物（`target/`、`*.exe`）和依赖目录（`node_modules/`、`.venv/`）。
2. 拉取最新代码后再开始工作：
   ```bash
   git pull origin main
   ```
3. 提交代码：
   ```bash
   git add .
   git commit -m "feat: 新增某功能 / fix: 修复某Bug"
   git push origin main
   ```
