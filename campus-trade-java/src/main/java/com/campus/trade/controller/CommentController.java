package com.campus.trade.controller;

import com.campus.trade.repository.CommentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/comments")
@CrossOrigin(origins = "*")
public class CommentController {
    
    @Autowired
    private CommentRepository commentRepository;

    @GetMapping("/goods/{goodsId}")
    public List<Map<String, Object>> getGoodsComments(@PathVariable Integer goodsId) {
        return commentRepository.findCommentsByGoodsId(goodsId);
    }
}
