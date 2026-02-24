package com.tengfei.enterprise.service;

import com.tengfei.enterprise.entity.ProductService;
import com.tengfei.enterprise.repository.ProductServiceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductServiceService {
    
    @Autowired
    private ProductServiceRepository productServiceRepository;
    
    public List<ProductService> getAllProducts() {
        return productServiceRepository.findAllByOrderByDisplayOrderAsc();
    }
    
    public ProductService getProductById(Long id) {
        return productServiceRepository.findById(id).orElse(null);
    }
    
    public ProductService save(ProductService productService) {
        return productServiceRepository.save(productService);
    }
    
    public void delete(Long id) {
        productServiceRepository.deleteById(id);
    }
}
