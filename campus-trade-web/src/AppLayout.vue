<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="glass-sidebar">
      <div class="logo-box">
        <el-icon :size="28" color="var(--primary)"><Shop /></el-icon>
        <h2 class="title-gradient">Campus Trade</h2>
      </div>
      <el-menu
        :default-active="route.path"
        class="custom-menu"
        router
        background-color="transparent"
        text-color="var(--text-dark)"
        active-text-color="var(--primary)"
      >
        <el-menu-item index="/admin">
          <el-icon><DataBoard /></el-icon>
          <span>数据主控台</span>
        </el-menu-item>
        <el-menu-item index="/admin/goods">
          <el-icon><Goods /></el-icon>
          <span>商品池管理</span>
        </el-menu-item>
        <el-menu-item divided @click="backToMall">
          <el-icon><HomeFilled /></el-icon>
          <span>返回买卖商城</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="glass-header">
        <div class="header-breadcrumb">
          <h3>{{ route.meta.title }}</h3>
        </div>
        <div class="header-user">
          <el-avatar size="small" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
          <span class="username">Admin</span>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { Shop, DataBoard, Goods, HomeFilled } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const backToMall = () => {
  router.push('/')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.glass-sidebar {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 4px 0 24px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
}

.logo-box {
  height: 80px;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
}

.logo-box h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.custom-menu {
  border-right: none;
  padding: 0 12px;
}

.el-menu-item {
  border-radius: 8px;
  margin-bottom: 4px;
  height: 50px;
  font-weight: 500;
}

.el-menu-item.is-active {
  background: rgba(79, 70, 229, 0.1) !important;
  font-weight: 600;
}

.glass-header {
  height: 70px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  justify-items: center;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.header-breadcrumb h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-dark);
}

.header-user {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 20px;
  background: rgba(255,255,255,0.5);
  transition: all 0.2s ease;
}

.header-user:hover {
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-dark);
}

.main-content {
  padding: 30px 40px;
  overflow-y: auto;
}
</style>
