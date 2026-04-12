package com.campus.trade.controller;

import com.campus.trade.entity.User;
import com.campus.trade.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin/users")
@CrossOrigin(origins = "*") // 允许前端 Vue 跨域调用
public class UserController {

    @Autowired
    private UserRepository userRepository;

    // 获取所有用户列表
    @GetMapping
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // 后台添加一个新用户
    @PostMapping
    public User createUser(@RequestBody User user) {
        return userRepository.save(user);
    }
}
