<template>
  <div class="goods-wrapper glass-panel">
    <div class="header-tools">
      <h3 class="title-gradient">在售商品池</h3>
      <div class="actions">
        <el-input placeholder="搜索商品名称..." class="search-input" prefix-icon="Search" />
        <el-button type="primary" icon="Plus" round>审核新商品</el-button>
      </div>
    </div>
    
    <div class="table-container">
      <el-table :data="onSaleGoods" style="width: 100%" v-loading="loading" stripe>
        <el-table-column prop="goodName" label="商品名称" min-width="200">
          <template #default="{ row }">
            <div class="good-name-col">
              <el-avatar shape="square" :size="36" style="background: var(--primary)">{{ row.goodName.charAt(0) }}</el-avatar>
              <span>{{ row.goodName }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="售卖价格" width="120">
          <template #default="{ row }">
            <span class="price-text">¥ {{ row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="详情描述" show-overflow-tooltip min-width="200" />
        <el-table-column prop="sellerName" label="发布人(卖家)" width="150">
          <template #default="{ row }">
            <el-tag type="info" round>{{ row.sellerName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default>
            <el-button link type="primary" size="small">查看评论</el-button>
            <el-button link type="danger" size="small">强制下架</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const onSaleGoods = ref([])

const fetchGoods = async () => {
  try {
    const res = await axios.get('/api/goods/on-sale')
    onSaleGoods.value = res.data
  } catch (error) {
    console.error('Failed to fetch goods', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchGoods()
})
</script>

<style scoped>
.goods-wrapper {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 500px;
}

.header-tools {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-tools h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 16px;
}

.search-input {
  width: 260px;
}
:deep(.search-input .el-input__wrapper) {
  border-radius: 20px;
}

.good-name-col {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  color: var(--text-dark);
}

.price-text {
  font-weight: 700;
  color: #10B981;
  font-size: 15px;
}
</style>
