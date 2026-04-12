package main

import (
	"log"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDB() {
	// Connect using user root and the docker port 3308
	dsn := "root:root@tcp(127.0.0.1:3308)/campus_trade?charset=utf8mb4&parseTime=True&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect database", err)
	}
	log.Println("Database connection established for Go Backend!")
	DB = db
}
