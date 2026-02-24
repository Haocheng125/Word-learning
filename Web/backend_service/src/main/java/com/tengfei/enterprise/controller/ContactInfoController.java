package com.tengfei.enterprise.controller;

import com.tengfei.enterprise.dto.ApiResponse;
import com.tengfei.enterprise.entity.ContactInfo;
import com.tengfei.enterprise.service.ContactInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/contact")
@CrossOrigin(origins = "*")
public class ContactInfoController {
    
    @Autowired
    private ContactInfoService contactInfoService;
    
    @GetMapping
    public ApiResponse<ContactInfo> getContactInfo() {
        ContactInfo contactInfo = contactInfoService.getContactInfo();
        return ApiResponse.success(contactInfo);
    }
    
    @PostMapping
    public ApiResponse<ContactInfo> saveOrUpdate(@RequestBody ContactInfo contactInfo) {
        ContactInfo saved = contactInfoService.saveOrUpdate(contactInfo);
        return ApiResponse.success(saved);
    }
}
