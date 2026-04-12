<template>
  <div class="mall-layout">
    <!-- 统一前台导航栏 -->
    <header class="mall-header glass-header">
      <div class="header-inner">
        <div class="logo">
          <el-icon :size="28" color="var(--primary)"><ShoppingCart /></el-icon>
          <h1 class="title-gradient">Campus Trade Mall</h1>
        </div>
        <div class="nav-links">
          <router-link to="/">发现闲置</router-link>
          <router-link to="/buy-requests">求购区</router-link>
          <router-link to="/compare">全网大盘比价</router-link>
        </div>
        <div class="user-actions">
          <el-button type="primary" round icon="Plus" @click="publish">发布闲置</el-button>
          
          <el-dropdown trigger="click">
            <div class="user-avatar-wrap">
              <el-avatar size="small" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
              <span>买家中心</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item icon="Tickets" @click="$router.push('/profile/orders')">我的订单</el-dropdown-item>
                <el-dropdown-item icon="Collection">我的收藏</el-dropdown-item>
                <el-dropdown-item divided icon="User">账号设置</el-dropdown-item>
                <!-- Only visible for Admin role typically, but put it here for demo navigation -->
                <el-dropdown-item divided @click="goToAdmin">进入后台监控中心</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <!-- 主体区域 -->
    <main class="mall-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部版式 -->
    <footer class="mall-footer">
      <p>© 2026 校园二手交易 - AI 智能护航计划</p>
    </footer>

    <!-- 发布闲置弹窗 -->
    <el-dialog v-model="publishDialogVisible" title="发布我的闲置" width="500px" destroy-on-close>
      <el-form :model="publishForm" label-width="80px">
        <el-form-item label="商品名称" required>
          <el-input v-model="publishForm.name" placeholder="起个吸引人的标题吧"></el-input>
        </el-form-item>
        <el-form-item label="预期价格" required>
          <el-input-number v-model="publishForm.price" :precision="2" :step="1" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="详细描述" required>
          <el-input v-model="publishForm.content" type="textarea" :rows="4" placeholder="描述一下物品的成色、入手渠道和出坑原因吧~"></el-input>
        </el-form-item>
        <el-form-item label="商品封面">
          <el-upload
            class="upload-area"
            action="/api/mall/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            name="file"
          >
            <img v-if="publishForm.image" :src="publishForm.image" class="uploaded-image" />
            <div v-else class="uploader-placeholder">
              <el-icon><Plus /></el-icon>
              <span>上传图片</span>
            </div>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="publishDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPublish" :loading="publishing">
            确认发布
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingCart, Plus, Tickets, Collection, User } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const publishDialogVisible = ref(false)
const publishing = ref(false)

const publishForm = reactive({
  name: '',
  price: 0,
  content: '',
  image: ''
})

const goToAdmin = () => {
  router.push('/admin')
}

const handleUploadSuccess = (res) => {
  publishForm.image = res.url
  ElMessage.success('图片归档完毕！')
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片格式的文件哦!')
  }
  return isImage
}

const publish = () => {
  publishForm.name = ''
  publishForm.price = 0
  publishForm.content = ''
  publishForm.image = ''
  publishDialogVisible.value = true
}

const submitPublish = async () => {
  if (!publishForm.name || !publishForm.content) {
    ElMessage.warning('名称和描述不能为空哦')
    return
  }
  
  publishing.value = true
  try {
    const res = await axios.post('/api/mall/goods', publishForm)
    ElMessage.success(res.data.message || '发布成功！已进入平台巡检审核队列。')
    publishDialogVisible.value = false
  } catch (err) {
    ElMessage.error('发布失败，请稍后再试')
  } finally {
    publishing.value = false
  }
}
</script>

<style scoped>
.mall-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
}

.glass-header {
  height: 64px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  gap: 24px;
  margin-left: 40px;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 15px;
  position: relative;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--primary);
}

.nav-links a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -20px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: var(--primary);
  border-radius: 3px 3px 0 0;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-avatar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 12px 4px 4px;
  border-radius: 20px;
  background: var(--bg-color);
  transition: all 0.2s;
}

.user-avatar-wrap:hover {
  background: #E5E7EB;
}

.user-avatar-wrap span {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-dark);
}

.mall-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 32px 20px;
  box-sizing: border-box;
}

.mall-footer {
  text-align: center;
  padding: 40px 0;
  color: #9CA3AF;
  font-size: 13px;
}

.upload-area {
  width: 100%;
  border: 1px dashed var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  position: relative;
  transition: border-color 0.3s;
}

.upload-area:hover {
  border-color: var(--primary);
}

.uploader-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 150px;
  background: #F9FAFB;
  color: var(--text-muted);
}

.uploader-placeholder .el-icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.uploaded-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}
</style>
