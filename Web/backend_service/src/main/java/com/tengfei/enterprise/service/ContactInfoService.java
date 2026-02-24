package com.tengfei.enterprise.service;

import com.tengfei.enterprise.entity.ContactInfo;
import com.tengfei.enterprise.repository.ContactInfoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class ContactInfoService {
    
    @Autowired
    private ContactInfoRepository contactInfoRepository;
    
    public ContactInfo getContactInfo() {
        return contactInfoRepository.findAll().stream().findFirst().orElse(null);
    }
    
    public ContactInfo saveOrUpdate(ContactInfo contactInfo) {
        Optional<ContactInfo> existing = contactInfoRepository.findAll().stream().findFirst();
        if (existing.isPresent()) {
            contactInfo.setId(existing.get().getId());
        }
        return contactInfoRepository.save(contactInfo);
    }
}
