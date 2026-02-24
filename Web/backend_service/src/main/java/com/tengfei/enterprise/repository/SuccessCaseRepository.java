package com.tengfei.enterprise.repository;

import com.tengfei.enterprise.entity.SuccessCase;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SuccessCaseRepository extends JpaRepository<SuccessCase, Long> {
    List<SuccessCase> findAllByOrderByDisplayOrderAsc();
}
