package com.campus.trade.repository;

import com.campus.trade.entity.Comment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public interface CommentRepository extends JpaRepository<Comment, Integer> {
    // 3. 查询某个商品下的所有评论及评论人
    @Query(value = "SELECT c.content, c.time, u.name AS commentator " +
                   "FROM comment c JOIN user u ON c.user_id = u.id WHERE c.fid = :goodsId", 
           nativeQuery = true)
    List<Map<String, Object>> findCommentsByGoodsId(@Param("goodsId") Integer goodsId);
}
