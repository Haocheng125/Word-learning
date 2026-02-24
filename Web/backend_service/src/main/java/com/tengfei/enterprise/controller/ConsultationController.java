package com.tengfei.enterprise.controller;

import com.tengfei.enterprise.dto.ApiResponse;
import com.tengfei.enterprise.entity.Consultation;
import com.tengfei.enterprise.service.ConsultationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/consultations")
@CrossOrigin(origins = "*")
public class ConsultationController {
    
    @Autowired
    private ConsultationService consultationService;
    
    @GetMapping
    public ApiResponse<List<Consultation>> getAllConsultations() {
        List<Consultation> consultations = consultationService.getAllConsultations();
        return ApiResponse.success(consultations);
    }
    
    @PostMapping
    public ApiResponse<Consultation> save(@RequestBody Consultation consultation) {
        Consultation saved = consultationService.save(consultation);
        return ApiResponse.success(saved);
    }
    
    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        consultationService.delete(id);
        return ApiResponse.success(null);
    }
}
