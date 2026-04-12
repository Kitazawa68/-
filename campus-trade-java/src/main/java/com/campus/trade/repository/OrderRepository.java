package com.campus.trade.repository;

import com.campus.trade.entity.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public interface OrderRepository extends JpaRepository<Order, Integer> {
    // 2. 查询某个买家购买的所有订单及卖家信息
    @Query(value = "SELECT o.order_no as orderNo, o.good_name as goodName, o.total, o.status, seller.name AS sellerName " +
                   "FROM `order` o JOIN user seller ON o.sale_id = seller.id WHERE o.user_id = :userId", 
           nativeQuery = true)
    List<Map<String, Object>> findBuyerOrders(@Param("userId") Integer userId);
}
