package com.tengfei.enterprise.service;

import com.tengfei.enterprise.entity.SuccessCase;
import com.tengfei.enterprise.repository.SuccessCaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SuccessCaseService {
    
    @Autowired
    private SuccessCaseRepository successCaseRepository;
    
    public List<SuccessCase> getAllCases() {
        return successCaseRepository.findAllByOrderByDisplayOrderAsc();
    }
    
    public SuccessCase getCaseById(Long id) {
        return successCaseRepository.findById(id).orElse(null);
    }
    
    public SuccessCase save(SuccessCase successCase) {
        return successCaseRepository.save(successCase);
    }
    
    public void delete(Long id) {
        successCaseRepository.deleteById(id);
    }
}
