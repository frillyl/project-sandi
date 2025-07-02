<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <div class="navbar-logo">
          <h1>SANDI</h1>
        </div>
        <button class="hamburger" @click="toggleMobileMenu">
          <i class="fa-solid fa-bars"></i>
        </button>
        <ul class="navbar-menu" :class="{ show: isMobileMenuOpen }">
          <li class="navbar-item">
            <router-link
              to="/demo/dashboard"
              class="navbar-link"
              :class="{ active: route.path === '/demo/dashboard' }"
              ><i class="fa-solid fa-house menu-icon"></i> Dashboard</router-link
            >
          </li>
          <li
            class="navbar-item"
            ref="dataMasterRef"
            v-if="
              isUserLoaded &&
              (userRole?.toLowerCase() === 'admin' || userRole?.toLowerCase() === 'arsiparis')
            "
          >
            <span
              class="navbar-link"
              :class="{ active: route.path.startsWith('/demo/master') }"
              @click="toggleDropdown"
              ><i class="fa-solid fa-folder-tree menu-icon"></i> Data Master</span
            >
            <transition name="slide-fade">
              <ul v-if="isDropdownOpen" class="dropdown-menu">
                <li v-if="userRole?.toLowerCase() === 'admin'">
                  <router-link
                    to="/demo/master/pengguna"
                    class="dropdown-link"
                    :class="{ active: route.path === '/demo/master/pengguna' }"
                    @click="handleSubmenuClick"
                    ><i class="fa-solid fa-users menu-icon"></i> Pengguna</router-link
                  >
                </li>
                <li>
                  <router-link
                    to="/demo/master/klasifikasi"
                    class="dropdown-link"
                    :class="{ active: route.path === '/demo/master/klasifikasi' }"
                    @click="handleSubmenuClick"
                    ><i class="fa-solid fa-list menu-icon"></i> Klasifikasi</router-link
                  >
                </li>
              </ul>
            </transition>
          </li>
          <li class="navbar-item">
            <router-link
              to="/demo/arsip"
              class="navbar-link"
              :class="{ active: route.path === '/demo/arsip' }"
              v-if="isUserLoaded && (userRole === 'admin' || userRole === 'arsiparis')"
              ><i class="fa-solid fa-plus menu-icon"></i> Entri Data Arsip</router-link
            >
          </li>
          <li class="navbar-item">
            <router-link
              to="/demo/arsip/cari"
              class="navbar-link"
              :class="{ active: route.path === '/demo/arsip/cari' }"
              ><i class="fa-solid fa-magnifying-glass menu-icon"></i> Cari Data Arsip</router-link
            >
          </li>
        </ul>
      </div>
      <div class="navbar-profile" ref="profileRef">
        <div class="profile-info" @click="toggleProfileDropdown">
          <img :src="ProfileImage" alt="Profile Image" class="profile-avatar" />
          <span class="profile-name" v-if="isUserLoaded">{{ userName }}</span>
          <i class="fa-solid fa-caret-down"></i>
        </div>
        <transition name="slide-fade">
          <ul v-if="isProfileDropdownOpen" class="profile-dropdown">
            <!-- <li>
              <router-link to="/demo/profile" class="dropdown-link"
                ><i class="fa-solid fa-user-gear menu-icon"></i> Profile Saya</router-link
              >
            </li> -->
            <li>
              <router-link to="/demo/bookmark" class="dropdown-link"
                ><i class="fa-solid fa-bookmark menu-icon"></i> Bookmark</router-link
              >
            </li>
            <li>
              <router-link to="#" class="dropdown-link" @click="logout"
                ><i class="fa-solid fa-right-from-bracket menu-icon"></i> Logout</router-link
              >
            </li>
          </ul>
        </transition>
      </div>
    </div>
  </nav>
</template>

<script setup>
import ProfileImage from '@/assets/images/user.png'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const isDropdownOpen = ref(false)
const dataMasterRef = ref(null)
const isProfileDropdownOpen = ref(false)
const isUserLoaded = ref(false)
const profileRef = ref(null)
const userName = ref('')
const userRole = ref('')
const isMobileMenuOpen = ref(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const fetchUserData = async () => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    try {
      const response = await axios.get('https://feeds-different-buried-safely.trycloudflare.com/api/user', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      console.log('Response dari API:', response.data) // Tambahkan ini
      userName.value = response.data.name
      userRole.value = response.data.role
      isUserLoaded.value = true
    } catch (error) {
      console.error('Gagal mengambil data pengguna', error)
    }
  }
}

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function toggleProfileDropdown() {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value
}

function closeDropdown() {
  isDropdownOpen.value = false
}

function handleSubmenuClick() {
  closeDropdown()
}

function handleClickOutside(event) {
  if (dataMasterRef.value && !dataMasterRef.value.contains(event.target)) {
    closeDropdown()
  }

  if (profileRef.value && !profileRef.value.contains(event.target)) {
    isProfileDropdownOpen.value = false
  }
}

// function isActive(path) {
//   return computed(() => route.path.startsWith(path))
// }

// function isExactActive(path) {
//   return computed(() => route.path === path)
// }

// function isPrefixActive(prefix) {
//   return computed(() => route.path.startsWith(prefix))
// }

// const isDataMasterActive = isPrefixActive('/demo/master')

function logout() {
  localStorage.removeItem('auth_token')
  Swal.fire({
    icon: 'success',
    title: 'Logout Berhasil',
    text: 'Anda Telah Keluar dari Sistem.',
    showConfirmButton: false,
    timerProgressBar: true,
    timer: 2000,
  }).then(() => {
    router.push({ name: 'Login' })
  })
}

onMounted(() => {
  fetchUserData()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.navbar {
  background: var(--primary);
  padding: 1rem;
  color: white;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.hamburger {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.navbar-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.menu-icon {
  margin-right: 0.25rem;
}

.navbar-item {
  position: relative;
  cursor: pointer;
}

.navbar-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: background 0.3s;
}

.navbar-link:hover {
  background: var(--secondary);
  color: var(--on-secondary);
}

.navbar-link.active {
  background: var(--secondary);
  color: var(--on-secondary);
  font-weight: bold;
}

.navbar-profile {
  position: relative;
  margin-left: auto;
  cursor: pointer;
}

.profile-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid white;
  object-fit: cover;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.profile-name {
  font-weight: 500;
  color: white;
}

.profile-dropdown {
  position: absolute;
  right: 0;
  top: 3rem;
  background: white;
  color: black;
  padding: 0.5rem 0;
  min-width: 200px;
  border-radius: 0.5rem;
  list-style: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  z-index: 20;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
  transform-origin: top;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
  transform-origin: top;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px) scaleY(0.95);
}

.slide-fade-to-enter-to {
  opacity: 1;
  transform: translateY(0) scaleY(1);
}

.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scaleY(1);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scaleY(0.95);
}

.dropdown-menu {
  position: absolute;
  top: 2.5rem;
  left: 0;
  background: white;
  color: black;
  padding: 0.5rem 0;
  min-width: 200px;
  border-radius: 0.5rem;
  list-style: none;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.dropdown-link {
  display: block;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: black;
  border-radius: 0.5rem;
  transition: background 0.3s;
}

.dropdown-link:hover {
  background: var(--secondary);
  color: var(--on-secondary);
}

.dropdown-link.active {
  background: var(--secondary);
  color: var(--on-secondary);
}

/* Responsive */
@media (max-width: 768px) {
  .navbar-container {
    flex-wrap: wrap;
    align-items: flex-start;
  }

  .navbar-left {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }

  .navbar-menu {
    display: none;
    flex-direction: column;
    width: 100%;
    gap: 1rem;
    margin-top: 1rem;
  }

  .navbar-menu.show {
    display: flex;
  }

  .hamburger {
    display: block;
  }

  .navbar-profile {
    margin-left: 0;
    margin-top: 1rem;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .profile-info {
    width: 100%;
    justify-content: space-between;
  }

  .dropdown-menu,
  .profile-dropdown {
    position: static;
    margin-top: 0.5rem;
    width: 100%;
  }
}
</style>
