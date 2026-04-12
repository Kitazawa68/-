<template>
  <div class="buy-requests glass-panel">
    <div class="header">
      <h2 class="title-gradient">许愿池 - 校友求购专区 ✨</h2>
      <p>手头有闲置？看看有没有同学刚好需要！精准匹配，全自动 AI 搭线变现。</p>
      <el-button type="primary" size="large" round icon="Plus" @click="publishRequest">发布我的心愿单</el-button>
    </div>

    <div class="request-grid">
      <div class="request-card" v-for="item in mockRequests" :key="item.id">
        <div class="r-head">
          <el-avatar :size="30">{{ item.user.charAt(0) }}</el-avatar>
          <span class="r-user">{{ item.user }} 的急切求购</span>
          <span class="r-time">{{ item.time }}</span>
        </div>
        <h3 class="r-title">{{ item.name }}</h3>
        <p class="r-desc">{{ item.desc }}</p>
        <div class="r-foot">
          <div class="r-price">愿意出价：<span>¥{{ item.price }}</span></div>
          <el-button color="#8B5CF6" round size="small" @click="connectBuyer">我有此物，联系买家</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const mockRequests = ref([
  { id: 1, user: '计算机系_李磊', name: '求购一本算法导论(第三版)', desc: '马上期末了，求好心学长割爱，外观无破损即可，急出价！', price: '45.00', time: '10分钟前' },
  { id: 2, user: '音乐系_小梦', name: '收一把入门级吉他', desc: '社团需要，希望音准没问题，带包带拨片更好。', price: '150.00', time: '半小时前' },
  { id: 3, user: '考研党_张伟', name: '求一张图书馆长期座位卡', desc: '每天早上起不来去抢座，求研友合租。', price: '面议', time: '2小时前' },
  { id: 4, user: '电竞社_王冰', name: '高价收二手 RTX 3060 显卡', desc: '主机升级，箱说全优先，拒绝矿卡，面交验机。', price: '1100.00', time: '1天前' }
])

const publishRequest = () => {
  ElMessage.info('求购大厅系统正在与数据库并网中，敬请期待！')
}

const connectBuyer = () => {
  ElMessage.success('已向买家发送【我有此物】的站内信通知！')
}
</script>

<style scoped>
.buy-requests {
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto;
  border-radius: 20px;
  min-height: 600px;
}
.header {
  text-align: center;
  margin-bottom: 50px;
}
.header h2 { font-size: 32px; margin-bottom: 12px; }
.header p { color: var(--text-muted); margin-bottom: 24px; }
.request-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.request-card {
  background: white; border: 1px solid var(--border-color);
  padding: 24px; border-radius: 16px; transition: all 0.3s;
}
.request-card:hover { transform: translateY(-4px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
.r-head { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.r-user { font-weight: 600; flex: 1; color: var(--text-dark); }
.r-time { color: var(--text-muted); font-size: 13px; }
.r-title { margin: 0 0 10px 0; font-size: 18px; color: var(--text-dark); }
.r-desc { color: #6B7280; font-size: 14px; line-height: 1.6; margin-bottom: 20px; }
.r-foot { display: flex; justify-content: space-between; align-items: center; padding-top: 16px; border-top: 1px dashed var(--border-color); }
.r-price { color: var(--text-muted); font-size: 14px; }
.r-price span { color: #E02E24; font-size: 22px; font-weight: 800; margin-left: 8px; }
</style>
