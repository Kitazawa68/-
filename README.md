# 校园二手交易平台 (Campus Trade)

这是一个基于 前后端分离架构 的校园二手交易系统项目。

## 目录结构
- `campus-trade-java`: 后端服务 (Spring Boot + MySQL)
- `campus-trade-web`: 前端服务 (Vue + Vite)
- `generate_10k.sql`: 数据库初始化和模拟数据脚本

## 前置环境要求
在开始之前，请确保你的本地安装了以下环境：
- [Node.js](https://nodejs.org/en/) (建议版本 v16+，用于前段运行)
- [JDK](https://www.oracle.com/java/technologies/downloads/) (建议版本 11 或 17，用于后端运行)
- [MySQL](https://dev.mysql.com/downloads/installer/) (建议版本 8.x，**本地安装**)

## 🛠️ 第一步：运行本地数据库

1. 本地启动你的 MySQL 服务。
2. 创建一个名为 `campus_trade` 的数据库：
   ```sql
   CREATE DATABASE campus_trade CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 在该数据库中执行同级目录下的 `generate_10k.sql` 文件生成海量测试数据（如果不需要那么多数据可跳过该步，由于项目启用了 `spring.jpa.hibernate.ddl-auto=update`，数据库表结构会自动生成）：
   ```bash
   mysql -u root -p campus_trade < generate_10k.sql
   ```

## 🚀 第二步：启动后端服务

后端的配置文件在 `campus-trade-java/src/main/resources/application.properties`。
默认情况下，连接试图访问：
- **Host**: `localhost`
- **Port**: `3308`
- **User**: `root`
- **Password**: `root`

> [!TIP]
> 如果您本地的 MySQL 是跑在 **3306** 端口（默认），或是密码不同，你**不要直接修改 properties 文件**以免产生代码冲突！
> 你可以通过设置**环境变量**在本地覆盖这些值：
> 
> ```bash
> # Windows (命令行):
> set DB_PORT=3306
> set DB_PASS=你的密码
> 
> # Mac/Linux:
> export DB_PORT=3306
> export DB_PASS=你的密码
> ```
> 
> 然后在该命令行终端下启动项目：

```bash
cd campus-trade-java
./mvnw spring-boot:run
```

如果顺利运行，后端服务将会在 `http://localhost:8080` 启动。

## 💻 第三步：启动前端服务

前端启动比较简单，进入前端目录安装依赖即可。

```bash
cd campus-trade-web
npm install
npm run dev
```

前端服务如果在 Vite 中启动成功，通常会运行在 `http://localhost:5173` （也有的配置是 3000）。请通过终端中打印的 `Local: http://localhost:xxxx/` 链接进入系统。

## 🤝 团队 Git 协作流

由于我们共同维护这个大工程，请大家遵守以下规范：
1. **不要**把你本地的日志文件 (`*.log`) 提交上来。
2. 拉取最新代码：`git pull origin main`
3. 提交代码：
   ```bash
   git add .
   git commit -m "feat: 新增某功能 / fix: 修复某Bug"
   git push origin main
   ```
