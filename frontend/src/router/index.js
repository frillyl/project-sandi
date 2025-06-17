import { createRouter, createWebHistory } from 'vue-router'
import {
  Home,
  Login,
  Dashboard,
  MPengguna,
  Arsip,
  Pencarian,
  GantiPassword,
  LupaPassword,
  ResetPassword,
  Klasifikasi,
  Bookmark,
} from '../views'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/demo/login',
    name: 'Login',
    component: Login,
    meta: { title: 'Demo - Login' },
  },
  {
    path: '/demo/lupa-password',
    name: 'Lupa Password',
    component: LupaPassword,
    meta: { title: 'Demo - Lupa Password' },
  },
  {
    path: '/demo/reset-password',
    name: 'Reset Password',
    component: ResetPassword,
    meta: { title: 'Demo - Reset Password' },
  },
  {
    path: '/demo/ganti-password',
    name: 'GantiPassword',
    component: GantiPassword,
    meta: { title: 'Demo - Ganti Password' },
  },
  {
    path: '/demo/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Demo - Dashboard', requiresAuth: true },
  },
  {
    path: '/demo/master/pengguna',
    name: 'MPengguna',
    component: MPengguna,
    meta: { title: 'Demo - Master Pengguna' },
  },
  {
    path: '/demo/master/klasifikasi',
    name: 'Klasifikasi',
    component: Klasifikasi,
    meta: { title: 'Demo - Klasifikasi' },
  },
  {
    path: '/demo/arsip',
    name: 'Arsip',
    component: Arsip,
    meta: { title: 'Demo - Arsip' },
  },
  {
    path: '/demo/arsip/cari',
    name: 'Pencarian',
    component: Pencarian,
    meta: { title: 'Demo - Pencarian' },
  },
  {
    path: '/demo/bookmark',
    name: 'Bookmark',
    component: Bookmark,
    meta: { title: 'Demo - Bookmark' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('auth_token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
