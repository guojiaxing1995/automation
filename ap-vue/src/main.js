import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import scheduler from './scheduler.vue'
import spiderBatch from './spiderBatch.vue'
import interfaceTest from './interface.vue'
import report from './report.vue'
import search from './search.vue'
import $ from 'jquery'
import echarts from 'echarts'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

Vue.prototype.$echarts = echarts

Vue.use(ElementUI)

window.URL = "http://127.0.0.1:5005";
//window.URL = "https://www.guojiaxing.red";

const routes = {
    '/': interfaceTest,
    '/spiderBatch': spiderBatch,
    '/scheduler': scheduler,
    '/report': report,
    '/search': search,

}
/*const routes = [
    { name: "interfaceTest", path: "/", component: interfaceTest },
    { name: "spiderBatch", path: "/spiderBatch", component: spiderBatch },
    { name: "scheduler", path: "/scheduler", component: scheduler },
    { name: "report", path: "/report", component: report },
    { name: "search", path: "/search", component: search }
]*/
/*const routes = [
    { name: "interfaceTest", path: "/", component: interfaceTest },
    { name: "spiderBatch", path: "/spiderBatch", component: spiderBatch },
    { name: "scheduler", path: "/scheduler", component: scheduler },
    { name: "report", path: "/report", component: report },
    { name: "search", path: "/search", component: search }
]

const router = new VueRouter({
    routes
})

const app = new Vue({
    router
}).$mount('#app')*/

new Vue({
  el: '#app',
  /*render: h => h(spiderBatch)*/
    data: {
        currentRoute: window.location.pathname
    },
    computed: {
        ViewComponent () {
            return routes[this.currentRoute] || interfaceTest
        }
    },
    render (h) { return h(this.ViewComponent) }
})
