import Vue from 'vue'
import App from './App.vue'
import router from './router'
import * as echarts from 'echarts'
import VueHighlightJS from 'vue-highlightjs'
import 'highlight.js/styles/atom-one-dark.css'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)

Vue.use(VueHighlightJS)
Vue.config.productionTip = false
Vue.prototype.$echarts = echarts


new Vue({
  render: h => h(App),
  router,
}).$mount('#app')


