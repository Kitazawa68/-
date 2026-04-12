import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('../MallLayout.vue'),
      children: [
        {
          path: '',
          name: 'MallHome',
          component: () => import('../views/MallHome.vue'),
          meta: { title: '首页' }
        },
        {
          path: 'buy-requests',
          name: 'BuyRequests',
          component: () => import('../views/BuyRequestsView.vue'),
          meta: { title: '求购区' }
        },
        {
          path: 'compare',
          name: 'Compare',
          component: () => import('../views/PriceComparisonView.vue'),
          meta: { title: '全网天眼雷达比价' }
        },
        {
          path: 'profile/orders',
          name: 'MyOrders',
          component: () => import('../views/MyOrdersView.vue'),
          meta: { title: '我的订单' }
        }
      ]
    },
    {
      path: '/admin',
      component: () => import('../AppLayout.vue'),
      children: [
        {
          path: '',
          name: 'Dashboard',
          component: () => import('../views/DashboardView.vue'),
          meta: { title: '控制台' }
        },
        {
          path: 'goods',
          name: 'GoodsAdmin',
          component: () => import('../views/GoodsView.vue'),
          meta: { title: '在售商品档案' }
        }
      ]
    }
  ]
})

export default router
