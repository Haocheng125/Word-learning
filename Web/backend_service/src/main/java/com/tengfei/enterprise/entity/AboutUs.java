package com.tengfei.enterprise.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "about_us")
public class AboutUs {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(length = 200)
    private String title;
    
    @Column(columnDefinition = "TEXT")
    private String content;
    
    @Column(length = 100)
    private String stat1Label;
    
    @Column(length = 50)
    private String stat1Value;
    
    @Column(length = 100)
    private String stat2Label;
    
    @Column(length = 50)
    private String stat2Value;
    
    @Column(length = 100)
    private String stat3Label;
    
    @Column(length = 50)
    private String stat3Value;
    
    @Column(length = 500)
    private String imageUrl;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
