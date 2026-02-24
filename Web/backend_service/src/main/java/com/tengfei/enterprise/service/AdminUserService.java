package com.tengfei.enterprise.service;

import com.tengfei.enterprise.entity.AdminUser;
import com.tengfei.enterprise.repository.AdminUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.util.Optional;

@Service
public class AdminUserService {
    
    @Autowired
    private AdminUserRepository adminUserRepository;
    
    @PostConstruct
    public void init() {
        // 初始化默认管理员账号
        if (adminUserRepository.count() == 0) {
            AdminUser admin = new AdminUser();
            admin.setUsername("admin");
            admin.setPassword("admin123");
            adminUserRepository.save(admin);
        }
    }
    
    public boolean login(String username, String password) {
        Optional<AdminUser> user = adminUserRepository.findByUsername(username);
        return user.isPresent() && user.get().getPassword().equals(password);
    }
}
