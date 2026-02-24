package com.tengfei.enterprise.repository;

import com.tengfei.enterprise.entity.AboutUs;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AboutUsRepository extends JpaRepository<AboutUs, Long> {
}
