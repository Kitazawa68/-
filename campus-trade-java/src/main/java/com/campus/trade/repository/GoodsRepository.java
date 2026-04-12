package com.campus.trade.repository;

import com.campus.trade.entity.Goods;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public interface GoodsRepository extends JpaRepository<Goods, Integer> {
    // 1. 查询所有正在上架的商品，并联表获取卖家姓名
    @Query(value = "SELECT g.name AS goodName, g.price, g.content, u.name AS sellerName " +
                   "FROM goods g JOIN user u ON g.user_id = u.id WHERE g.status = 'ON_SALE'", 
           nativeQuery = true)
    List<Map<String, Object>> findOnSaleGoodsWithSeller();
}
