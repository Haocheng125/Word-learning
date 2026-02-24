package com.tengfei.enterprise.controller;

import com.tengfei.enterprise.dto.ApiResponse;
import com.tengfei.enterprise.dto.LoginRequest;
import com.tengfei.enterprise.service.AdminUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
public class AdminController {
    
    @Autowired
    private AdminUserService adminUserService;
    
    @PostMapping("/login")
    public ApiResponse<String> login(@RequestBody LoginRequest request) {
        boolean success = adminUserService.login(request.getUsername(), request.getPassword());
        if (success) {
            return ApiResponse.success("登录成功");
        } else {
            return ApiResponse.error("用户名或密码错误");
        }
    }
}
