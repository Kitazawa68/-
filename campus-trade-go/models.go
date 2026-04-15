package main

// User maps to the MySQL `user` table
type User struct {
	ID       uint   `gorm:"primaryKey" json:"id"`
	Username string `gorm:"column:username" json:"username"`
	Name     string `gorm:"column:name" json:"name"`
	Phone    string `gorm:"column:phone" json:"phone"`
	Email    string `gorm:"column:email" json:"email"`
	Role     string `gorm:"column:role" json:"role"`
}

// TableName overrides the table name used by User to `user`
func (User) TableName() string {
	return "user"
}

// Goods maps to the MySQL `goods` table
type Goods struct {
	ID      uint   `gorm:"primaryKey" json:"id"`
	Name    string `gorm:"column:name" json:"name"`
	Price   float64`gorm:"column:price" json:"price"`
	Content string `gorm:"column:content" json:"content"`
	Status  string `gorm:"column:status" json:"status"`
	Image   string `gorm:"column:image" json:"image"`
	UserID  uint   `gorm:"column:user_id" json:"userId"`
	Seller  User   `gorm:"foreignKey:UserID" json:"seller"` // Belongs To relationship
}

func (Goods) TableName() string {
	return "goods"
}

// Order maps to the MySQL `order` table
type Order struct {
	ID        uint      `gorm:"primaryKey" json:"id"`
	OrderNo   string    `gorm:"column:order_no" json:"orderNo"`
	GoodName  string    `gorm:"column:good_name" json:"goodName"`
	Total     float64   `gorm:"column:total" json:"total"`
	Status    string    `gorm:"column:status" json:"status"`
	UserID    uint      `gorm:"column:user_id" json:"userId"`
	SaleID    uint      `gorm:"column:sale_id" json:"saleId"`
}

func (Order) TableName() string {
	return "order"
}

// Dispute maps to the admin `dispute` table
type Dispute struct {
	ID          uint   `gorm:"primaryKey" json:"id"`
	ReporterID  uint   `gorm:"column:reporter_id" json:"reporterId"`
	TargetType  string `gorm:"column:target_type" json:"targetType"`
	TargetID    uint   `gorm:"column:target_id" json:"targetId"`
	Reason      string `gorm:"column:reason" json:"reason"`
	EvidenceImg string `gorm:"column:evidence_img" json:"evidenceImg"`
	Status      string `gorm:"column:status" json:"status"`
	AdminNote   string `gorm:"column:admin_note" json:"adminNote"`
}

func (Dispute) TableName() string {
	return "dispute"
}
