import './assets/css/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import AOS from 'aos'
import 'aos/dist/aos.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = 'SANDI - Solusi Cerdas Untuk Arsip Digital'
  }

  setTimeout(() => {
    AOS.refresh()
  }, 100)
})

app.mount('#app')
AOS.init()
