package com.campus.trade.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "collection")
public class Collection {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "user_id", nullable = false)
    private Integer userId;

    @Column(nullable = false)
    private Integer fid; // 关联的id

    @Column(nullable = false, length = 50)
    private String module; // 所属模块(商品/求购)

    // Getters and Setters

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public Integer getUserId() { return userId; }
    public void setUserId(Integer userId) { this.userId = userId; }

    public Integer getFid() { return fid; }
    public void setFid(Integer fid) { this.fid = fid; }

    public String getModule() { return module; }
    public void setModule(String module) { this.module = module; }
}
