<template>
  <div class="dashboard-wrapper">
    <div class="stats-row">
      <div class="stat-card glass-panel" v-for="(stat, i) in stats" :key="i">
        <div class="stat-icon" :style="{ background: stat.color }">
          <el-icon color="#fff" :size="20"><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-title">{{ stat.title }}</p>
          <h3 class="stat-value">{{ stat.value }}</h3>
        </div>
      </div>
    </div>

    <div class="card-section glass-panel">
      <div class="card-header">
        <h3 class="title-gradient">系统活跃总览</h3>
        <el-button type="primary" size="small" round>查阅更多</el-button>
      </div>
      <div class="card-body">
        <el-table :data="recentUsers" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="用户ID" width="100" />
          <el-table-column prop="username" label="校园账号" width="180">
            <template #default="scope">
              <el-tag size="small" type="success">{{ scope.row.username }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="真实姓名" width="180" />
          <el-table-column prop="phone" label="联系方式" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const recentUsers = ref([])

const stats = [
  { title: '总活跃用户', value: '1,284', icon: 'User', color: 'linear-gradient(135deg, #4F46E5, #818CF8)' },
  { title: '今日新增商品', value: '42', icon: 'Goods', color: 'linear-gradient(135deg, #10B981, #34D399)' },
  { title: '待处理订单', value: '18', icon: 'Tickets', color: 'linear-gradient(135deg, #F59E0B, #FBBF24)' },
  { title: '评论互动数', value: '356', icon: 'ChatLineRound', color: 'linear-gradient(135deg, #EC4899, #F472B6)' }
]

const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/admin/users')
    recentUsers.value = res.data
  } catch (error) {
    console.error('Failed to fetch users', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.stat-card {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.stat-info p {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 4px;
}

.stat-info h3 {
  margin: 0;
  font-size: 24px;
  color: var(--text-dark);
  font-weight: 700;
  letter-spacing: -0.5px;
}

.card-section {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}
</style>
