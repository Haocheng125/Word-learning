package com.tengfei.enterprise.service;

import com.tengfei.enterprise.entity.Consultation;
import com.tengfei.enterprise.repository.ConsultationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ConsultationService {
    
    @Autowired
    private ConsultationRepository consultationRepository;
    
    public List<Consultation> getAllConsultations() {
        return consultationRepository.findAllByOrderByCreatedAtDesc();
    }
    
    public Consultation save(Consultation consultation) {
        return consultationRepository.save(consultation);
    }
    
    public void delete(Long id) {
        consultationRepository.deleteById(id);
    }
}
