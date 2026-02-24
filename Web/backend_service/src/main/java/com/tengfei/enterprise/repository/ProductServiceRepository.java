package com.tengfei.enterprise.repository;

import com.tengfei.enterprise.entity.ProductService;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductServiceRepository extends JpaRepository<ProductService, Long> {
    List<ProductService> findAllByOrderByDisplayOrderAsc();
}
