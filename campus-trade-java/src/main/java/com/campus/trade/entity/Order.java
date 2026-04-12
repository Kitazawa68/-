package com.campus.trade.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "`order`") // 注意：order是MySQL保留字，需要加反引号或者重命名表，我们按要求保留原表名
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "order_no", nullable = false, unique = true, length = 50)
    private String orderNo;

    @Column(name = "good_name", length = 100)
    private String goodName;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal total;

    @Column(length = 20)
    private String status = "PENDING";

    @Column(name = "user_id", nullable = false)
    private Integer userId; // 买家ID

    @Column(name = "sale_id", nullable = false)
    private Integer saleId; // 卖家ID

    // Getters and Setters

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getOrderNo() { return orderNo; }
    public void setOrderNo(String orderNo) { this.orderNo = orderNo; }

    public String getGoodName() { return goodName; }
    public void setGoodName(String goodName) { this.goodName = goodName; }

    public BigDecimal getTotal() { return total; }
    public void setTotal(BigDecimal total) { this.total = total; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Integer getUserId() { return userId; }
    public void setUserId(Integer userId) { this.userId = userId; }

    public Integer getSaleId() { return saleId; }
    public void setSaleId(Integer saleId) { this.saleId = saleId; }
}
