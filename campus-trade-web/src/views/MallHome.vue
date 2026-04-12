<template>
  <div class="mall-home">
    <!-- Banner -->
    <div class="hero-banner">
      <div class="hero-text">
        <h1 class="title-gradient">发现闲置的美好</h1>
        <p>让每一件物品都在校园里找到它的下一个归宿。买卖无缝，平台护航，AI极速判罚。</p>
      </div>
      <img src="https://cdni.iconscout.com/illustration/premium/thumb/online-shopping-device-2911132-2431613.png" alt="Hero Illustration" class="hero-img"/>
    </div>

    <!-- Goods Flow -->
    <div class="section-title">
      <h2>新鲜上架 🔥</h2>
      <div class="filter-sort">
        <el-radio-group v-model="sortBy" size="small">
          <el-radio-button label="最新发布" />
          <el-radio-button label="价格最低" />
        </el-radio-group>
      </div>
    </div>

    <!-- We will use a mockup for now until we connect to Go API -->
    <div class="goods-grid" v-loading="loading">
      <div class="good-card" v-for="(item, index) in localGoods" :key="index">
        <div class="good-img-placeholder">
          <img v-if="item.image" :src="item.image" class="real-image" />
          <el-icon v-else :size="40" color="#D1D5DB"><Picture /></el-icon>
        </div>
        <div class="good-info">
          <h3 class="good-title">{{ item.name || item.goodName }}</h3>
          <p class="good-desc">{{ item.content }}</p>
          <div class="good-meta">
            <span class="price">¥{{ item.price.toFixed(2) }}</span>
            <div class="seller">
              <el-avatar :size="20">{{ (item.seller?.name || item.sellerName || '?').charAt(0) }}</el-avatar>
              <span>{{ item.seller?.name || item.sellerName || '匿名卖家' }}</span>
            </div>
          </div>
          <el-button color="#4F46E5" class="buy-btn" round block @click="buyDialog = true">立即购买</el-button>
        </div>
      </div>
    </div>
    
    <div class="load-more-container" v-if="localGoods.length > 0">
      <el-button round size="large" @click="loadMore" :loading="loadingMore" v-if="hasMore" style="width: 200px;">加载更多好物 ...</el-button>
      <p v-else class="no-more">没有更多数据了，到底啦~</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Picture } from '@element-plus/icons-vue'

const loading = ref(true)
const sortBy = ref('最新发布')
const localGoods = ref<any[]>([])

const page = ref(1)
const loadingMore = ref(false)
const hasMore = ref(true)

const buyDialog = ref(false)

const fetchGoods = async (isAppend = false) => {
  try {
    if (!isAppend) loading.value = true
    const res = await axios.get('/api/mall/goods', { params: { size: 12, page: page.value } })
    const fetchedData = res.data.data || []
    
    if (fetchedData.length < 12) {
      hasMore.value = false
    }
    
    if (isAppend) {
      localGoods.value.push(...fetchedData)
    } else {
      localGoods.value = fetchedData
    }
  } catch (error) {
    console.error('Failed to fetch goods', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = () => {
  if (!hasMore.value) return
  page.value++
  loadingMore.value = true
  fetchGoods(true)
}

onMounted(() => {
  fetchGoods()
})
</script>

<style scoped>
.mall-home {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.hero-banner {
  background: white;
  border-radius: 20px;
  padding: 40px 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.hero-text {
  max-width: 500px;
}

.hero-text h1 {
  font-size: 36px;
  margin-bottom: 20px;
}

.hero-text p {
  color: var(--text-muted);
  font-size: 16px;
  line-height: 1.6;
}

.hero-img {
  width: 300px;
  object-fit: contain;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title h2 {
  font-size: 24px;
  color: var(--text-dark);
  margin: 0;
}

.goods-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.good-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.good-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.good-img-placeholder {
  height: 200px;
  background: #F9FAFB;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.good-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.good-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-dark);
}

.good-desc {
  margin: 0 0 16px 0;
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.good-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  margin-bottom: 16px;
}

.price {
  font-size: 20px;
  font-weight: 700;
  color: #10B981;
}

.seller {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
}

.buy-btn {
  width: 100%;
}

.load-more-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  margin-top: 10px;
}

.no-more {
  color: var(--text-muted);
  font-size: 14px;
}
</style>
