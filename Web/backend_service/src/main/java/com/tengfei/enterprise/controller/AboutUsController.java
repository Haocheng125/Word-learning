package com.tengfei.enterprise.controller;

import com.tengfei.enterprise.dto.ApiResponse;
import com.tengfei.enterprise.entity.AboutUs;
import com.tengfei.enterprise.service.AboutUsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/about")
@CrossOrigin(origins = "*")
public class AboutUsController {
    
    @Autowired
    private AboutUsService aboutUsService;
    
    @GetMapping
    public ApiResponse<AboutUs> getAboutUs() {
        AboutUs aboutUs = aboutUsService.getAboutUs();
        return ApiResponse.success(aboutUs);
    }
    
    @PostMapping
    public ApiResponse<AboutUs> saveOrUpdate(@RequestBody AboutUs aboutUs) {
        AboutUs saved = aboutUsService.saveOrUpdate(aboutUs);
        return ApiResponse.success(saved);
    }
}
