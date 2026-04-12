package com.campus.trade.controller;

import com.campus.trade.repository.GoodsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/goods")
@CrossOrigin(origins = "*")
public class GoodsController {

    @Autowired
    private GoodsRepository goodsRepository;

    @GetMapping("/on-sale")
    public List<Map<String, Object>> getOnSaleGoods() {
        return goodsRepository.findOnSaleGoodsWithSeller();
    }
}
