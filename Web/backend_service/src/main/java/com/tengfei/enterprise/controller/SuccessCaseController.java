package com.tengfei.enterprise.controller;

import com.tengfei.enterprise.dto.ApiResponse;
import com.tengfei.enterprise.entity.SuccessCase;
import com.tengfei.enterprise.service.SuccessCaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cases")
@CrossOrigin(origins = "*")
public class SuccessCaseController {
    
    @Autowired
    private SuccessCaseService successCaseService;
    
    @GetMapping
    public ApiResponse<List<SuccessCase>> getAllCases() {
        List<SuccessCase> cases = successCaseService.getAllCases();
        return ApiResponse.success(cases);
    }
    
    @GetMapping("/{id}")
    public ApiResponse<SuccessCase> getCaseById(@PathVariable Long id) {
        SuccessCase successCase = successCaseService.getCaseById(id);
        return ApiResponse.success(successCase);
    }
    
    @PostMapping
    public ApiResponse<SuccessCase> save(@RequestBody SuccessCase successCase) {
        SuccessCase saved = successCaseService.save(successCase);
        return ApiResponse.success(saved);
    }
    
    @PutMapping("/{id}")
    public ApiResponse<SuccessCase> update(@PathVariable Long id, @RequestBody SuccessCase successCase) {
        successCase.setId(id);
        SuccessCase saved = successCaseService.save(successCase);
        return ApiResponse.success(saved);
    }
    
    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        successCaseService.delete(id);
        return ApiResponse.success(null);
    }
}
