package com.tengfei.enterprise.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "success_case")
public class SuccessCase {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(length = 200, nullable = false)
    private String title;
    
    @Column(length = 50)
    private String category;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    @Column(length = 500)
    private String imageUrl;
    
    @Column(length = 100)
    private String result1Label;
    
    @Column(length = 50)
    private String result1Value;
    
    @Column(length = 100)
    private String result2Label;
    
    @Column(length = 50)
    private String result2Value;
    
    @Column(name = "display_order")
    private Integer displayOrder;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
