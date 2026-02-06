import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
// 必须在 main.css 之前导入，因为包含 CSS 变量定义
import './assets/styles/element-plus.css'
import './assets/styles/main.css'

const app = createApp(App)

app.use(store)
app.use(router)
app.use(ElementPlus, { locale: zhCn })

app.mount('#app')
