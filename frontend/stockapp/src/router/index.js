import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index.vue'
import login from '@/components/login.vue'
import register from '@/components/register.vue'
import stock from '@/components/stock.vue'
import self from '@/components/self.vue'
import orderPage from '@/components/orderPage.vue'
import documentPage from '@/components/documentPage.vue'

Vue.use(Router)

var router =  new Router({
  routes:[
    {
      path:'/',
      name:'index',
      component:index
    },
    {
      path:'/login',
      name:'login',
      component:login
    },
    {
      path:'/register',
      name:'register',
      component:register
    },
    {
      path:'/stock/:stockno',
      name:'stock',
      component:stock
    },
    {
      path:'/self',
      name:'self',
      component:self
    },
    {
      path:'/order/:stockno',
      name:'orderPage',
      component:orderPage
    },
    {
      path:'/order',
      name:'nullOrderPage',
      component:orderPage
    },
    {
      path:'/documentation',
      name:'documentPage',
      component:documentPage
    }
  ]
})



export default router