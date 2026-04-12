package com.campus.trade.controller;

import com.campus.trade.repository.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/orders")
@CrossOrigin(origins = "*")
public class OrderController {
    
    @Autowired
    private OrderRepository orderRepository;

    @GetMapping("/buyer/{userId}")
    public List<Map<String, Object>> getBuyerOrders(@PathVariable Integer userId) {
        return orderRepository.findBuyerOrders(userId);
    }
}
