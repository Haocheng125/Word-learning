package com.tengfei.enterprise.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "contact_info")
public class ContactInfo {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(length = 200)
    private String address;
    
    @Column(length = 50)
    private String phone;
    
    @Column(length = 100)
    private String email;
    
    @Column(length = 100)
    private String workingHours;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
