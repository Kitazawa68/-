package com.campus.trade.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "comment")
public class Comment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, length = 500)
    private String content;

    @Column(name = "time", columnDefinition = "DATETIME DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime time;

    @Column(name = "user_id", nullable = false)
    private Integer userId;

    @Column(columnDefinition = "INT DEFAULT 0")
    private Integer pid;

    @Column(name = "root_id", columnDefinition = "INT DEFAULT 0")
    private Integer rootId;

    @Column(nullable = false)
    private Integer fid; // 关联的商品或求购的id

    @PrePersist
    protected void onCreate() {
        if (time == null) {
            time = LocalDateTime.now();
        }
    }

    // Getters and Setters

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public LocalDateTime getTime() { return time; }
    public void setTime(LocalDateTime time) { this.time = time; }

    public Integer getUserId() { return userId; }
    public void setUserId(Integer userId) { this.userId = userId; }

    public Integer getPid() { return pid; }
    public void setPid(Integer pid) { this.pid = pid; }

    public Integer getRootId() { return rootId; }
    public void setRootId(Integer rootId) { this.rootId = rootId; }

    public Integer getFid() { return fid; }
    public void setFid(Integer fid) { this.fid = fid; }
}
