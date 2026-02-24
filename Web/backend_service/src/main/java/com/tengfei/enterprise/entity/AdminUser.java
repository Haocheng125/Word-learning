package com.tengfei.enterprise.entity;

import lombok.Data;
import javax.persistence.*;

@Data
@Entity
@Table(name = "admin_user")
public class AdminUser {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(length = 50, unique = true, nullable = false)
    private String username;
    
    @Column(length = 100, nullable = false)
    private String password;
}
