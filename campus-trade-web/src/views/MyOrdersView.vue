<template>
  <div class="my-orders glass-panel">
    <div class="header">
      <h3 class="title-gradient">买家中心 - 我的订单</h3>
    </div>
    
    <el-tabs v-model="activeTab">
      <el-tab-pane label="全部订单" name="all"></el-tab-pane>
      <el-tab-pane label="待接单" name="PENDING"></el-tab-pane>
      <el-tab-pane label="待发货" name="PAID"></el-tab-pane>
      <el-tab-pane label="待收货" name="SHIPPED"></el-tab-pane>
      <el-tab-pane label="已完成" name="COMPLETED"></el-tab-pane>
    </el-tabs>

    <div class="order-list" v-loading="loading">
       <el-empty v-if="filteredOrders.length === 0" description="暂无符合条件的订单，快去首页发现好物吧" />
       
       <div class="order-card" v-for="order in filteredOrders" :key="order.id">
         <div class="order-header">
           <span class="order-no">订单编号：{{ order.orderNo }}</span>
           <el-tag :type="getStatusType(order.status)" size="small" effect="dark">{{ getStatusText(order.status) }}</el-tag>
         </div>
         <div class="order-body">
           <div class="good-img">
             <el-icon :size="30" color="#c0c4cc"><GoodsFilled /></el-icon>
           </div>
           <div class="good-info">
             <h4>{{ order.goodName }}</h4>
             <p class="seller-info">发货模式: 校园当面交易/快递</p>
           </div>
           <div class="good-price">
             <span class="total-label">付款金额</span>
             <span class="total-price">¥{{ order.total.toFixed(2) }}</span>
           </div>
         </div>
         <div class="order-footer">
           <el-button v-if="order.status === 'PENDING'" type="primary" size="small" round>立即付款</el-button>
           <el-button v-if="order.status === 'SHIPPED'" type="success" size="small" round>确认收货</el-button>
           <el-button v-if="order.status === 'COMPLETED'" type="warning" size="small" round>发起售后纠纷(提交AI处理)</el-button>
           <el-button size="small" round>联系卖家</el-button>
         </div>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { GoodsFilled } from '@element-plus/icons-vue'
import axios from 'axios'

const activeTab = ref('all')
const loading = ref(false)
const orders = ref<any[]>([])

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orders.value
  return orders.value.filter(o => o.status === activeTab.value)
})

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    'PENDING': 'info',
    'PAID': 'warning',
    'SHIPPED': 'primary',
    'COMPLETED': 'success'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'PENDING': '待确认',
    'PAID': '买家已付款',
    'SHIPPED': '卖家已发货',
    'COMPLETED': '交易成功'
  }
  return map[status] || status
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/mall/orders')
    orders.value = res.data.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.my-orders {
  padding: 30px 40px;
  max-width: 900px;
  margin: 0 auto;
  border-radius: 20px;
  min-height: 500px;
}

.header {
  margin-bottom: 30px;
}

.header h3 {
  font-size: 24px;
  margin: 0;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.order-card {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.order-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.order-header {
  padding: 12px 20px;
  background: #F9FAFB;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  font-size: 13px;
  color: var(--text-muted);
}

.order-no {
  font-family: monospace;
}

.order-body {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.good-img {
  width: 80px;
  height: 80px;
  background: #F3F4F6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.good-info {
  flex: 1;
}

.good-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: var(--text-dark);
}

.seller-info {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
}

.good-price {
  text-align: right;
}

.total-label {
  font-size: 13px;
  color: var(--text-muted);
  margin-right: 8px;
}

.total-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-dark);
}

.order-footer {
  padding: 12px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
