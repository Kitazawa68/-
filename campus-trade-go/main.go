package main

import (
	"log"
	"net/http"
	"path/filepath"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize Database connection
	InitDB()

	// Initialize Gin router
	r := gin.Default()

	// Enable CORS for development
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE, UPDATE")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	})

	api := r.Group("/api/mall")
	{
		api.GET("/ping", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{"message": "Welcome to Campus Trade Go API"})
		})

		// GET /api/mall/goods
		// Pagination API to support the massive visual waterfall
		api.GET("/goods", func(c *gin.Context) {
			page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
			pageSize, _ := strconv.Atoi(c.DefaultQuery("size", "20"))
			search := c.Query("keyword")

			offset := (page - 1) * pageSize

			var goods []Goods
			var total int64

			query := DB.Model(&Goods{}).Preload("Seller").Where("status = ?", "ON_SALE")

			if search != "" {
				query = query.Where("name LIKE ? OR content LIKE ?", "%"+search+"%", "%"+search+"%")
			}

			// Perform massive concurrent counting and querying
			query.Count(&total)
			query.Order("id DESC").Offset(offset).Limit(pageSize).Find(&goods)

			c.JSON(http.StatusOK, gin.H{
				"total": total,
				"page":  page,
				"size":  pageSize,
				"data":  goods,
			})
		})

		// POST /api/mall/goods
		// Publish a new item
		api.POST("/goods", func(c *gin.Context) {
			var newGood Goods
			if err := c.ShouldBindJSON(&newGood); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			
			// Always force new items to pending audit to satisfy the platform requirements!
			newGood.Status = "PENDING_AUDIT"
			// Hardcode userID 1 for demo purposes since we don't have JWT auth configured yet
			newGood.UserID = 1 
			
			if err := DB.Create(&newGood).Error; err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create good"})
				return
			}

			c.JSON(http.StatusOK, gin.H{"message": "Success! Item is pending for Admin Audit.", "data": newGood})
		})

		// POST /api/mall/upload
		api.POST("/upload", func(c *gin.Context) {
			file, err := c.FormFile("file")
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": "No file uploaded"})
				return
			}
			filename := strconv.FormatInt(time.Now().UnixNano(), 10) + "_" + file.Filename
			savePath := filepath.Join("uploads", filename)
			if err := c.SaveUploadedFile(file, savePath); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save file"})
				return
			}
			c.JSON(http.StatusOK, gin.H{"url": "/api/mall/uploads/" + filename})
		// GET /api/mall/orders
		api.GET("/orders", func(c *gin.Context) {
			var orders []Order
			// Mock user ID = 1 since no auth
			DB.Where("user_id = ?", 1).Order("id DESC").Find(&orders)
			c.JSON(http.StatusOK, gin.H{"data": orders})
		})
	}

	// Serve static files
	r.Static("/api/mall/uploads", "./uploads")

	log.Println("Starting Forward-Facing Go API Server on port 8081...")
	if err := r.Run(":8081"); err != nil {
		log.Fatal("Server failed to start:", err)
	}
}
