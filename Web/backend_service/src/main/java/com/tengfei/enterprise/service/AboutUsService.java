package com.tengfei.enterprise.service;

import com.tengfei.enterprise.entity.AboutUs;
import com.tengfei.enterprise.repository.AboutUsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class AboutUsService {
    
    @Autowired
    private AboutUsRepository aboutUsRepository;
    
    public AboutUs getAboutUs() {
        return aboutUsRepository.findAll().stream().findFirst().orElse(null);
    }
    
    public AboutUs saveOrUpdate(AboutUs aboutUs) {
        Optional<AboutUs> existing = aboutUsRepository.findAll().stream().findFirst();
        if (existing.isPresent()) {
            aboutUs.setId(existing.get().getId());
        }
        return aboutUsRepository.save(aboutUs);
    }
}
