package com.tengfei.enterprise.controller;

import com.tengfei.enterprise.dto.ApiResponse;
import com.tengfei.enterprise.entity.ProductService;
import com.tengfei.enterprise.service.ProductServiceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "*")
public class ProductServiceController {
    
    @Autowired
    private ProductServiceService productServiceService;
    
    @GetMapping
    public ApiResponse<List<ProductService>> getAllProducts() {
        List<ProductService> products = productServiceService.getAllProducts();
        return ApiResponse.success(products);
    }
    
    @GetMapping("/{id}")
    public ApiResponse<ProductService> getProductById(@PathVariable Long id) {
        ProductService product = productServiceService.getProductById(id);
        return ApiResponse.success(product);
    }
    
    @PostMapping
    public ApiResponse<ProductService> save(@RequestBody ProductService productService) {
        ProductService saved = productServiceService.save(productService);
        return ApiResponse.success(saved);
    }
    
    @PutMapping("/{id}")
    public ApiResponse<ProductService> update(@PathVariable Long id, @RequestBody ProductService productService) {
        productService.setId(id);
        ProductService saved = productServiceService.save(productService);
        return ApiResponse.success(saved);
    }
    
    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        productServiceService.delete(id);
        return ApiResponse.success(null);
    }
}
