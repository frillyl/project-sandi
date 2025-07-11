<template>
  <div class="login">
    <div class="login-container">
      <!-- Left Section -->
      <div class="left-section">
        <div class="pattern"></div>
        <img
          :src="LupaPasswordIllustration"
          alt="Forgot Password Illustration"
          class="illustration"
        />
      </div>

      <!-- Right Section -->
      <div class="right-section">
        <form @submit.prevent="submitEmail" class="login-card">
          <h3 class="animated delay-1">LUPA PASSWORD</h3>
          <p class="info-text animated delay-2">
            Masukkan email Anda untuk menerima tautan reset password.
          </p>
          <div class="input-group animated delay-3">
            <input v-model="email" type="email" placeholder="Email" required />
            <i class="fa-solid fa-envelope"></i>
          </div>
          <button type="submit" class="animated delay-4">
            <i class="fa-solid fa-paper-plane"></i> Kirim Tautan Reset
          </button>
          <router-link to="/demo/login" class="back-link animated delay-5">
            <i class="fa-solid fa-arrow-left"></i> Kembali ke Login
          </router-link>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'
import LupaPasswordIllustration from '@/assets/images/forgot-password.svg'

const email = ref('')
const router = useRouter()

const submitEmail = async () => {
  try {
    await axios.post(
      'https://smaller-owned-sides-tourist.trycloudflare.com/api/forgot-password',
      {
        email: email.value,
      },
    )
    Swal.fire({
      icon: 'success',
      title: 'Email Terkirim',
      text: 'Link reset telah dikirim. Silahkan periksa email Anda.',
      showConfirmButton: false,
      timerProgressBar: true,
      timer: 1500,
    })
    setTimeout(() => {
      router.push({ name: 'Login' })
    }, 1500)
  } catch (err) {
    Swal.fire('Gagal', 'Email tidak ditemukan.', 'error')
  }
}
</script>

<style scoped>
.login {
  display: flex;
  height: 100vh;
}

.login-container {
  display: flex;
  flex: 1;
}

.left-section {
  flex: 1;
  background-color: var(--primary);
  color: var(--on-primary);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.left-section .pattern {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' fill='%23d1c4e9' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='1' cy='1' r='1'/%3E%3C/svg%3E");
  opacity: 0.2;
}

.left-section .illustration {
  width: 60%;
  max-width: 300px;
  z-index: 1;
}

.illustration {
  animation: zoomIn 1s ease;
}

.animated {
  opacity: 0;
  animation: fadeSlideUp 0.6s ease-out forwards;
}

.delay-1 {
  animation-delay: 0.2s;
}

.delay-2 {
  animation-delay: 0.4s;
}

.delay-3 {
  animation-delay: 0.6s;
}

.delay-4 {
  animation-delay: 0.8s;
}

.delay-5 {
  animation-delay: 1s;
}

.right-section {
  flex: 1;
  background: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: #ffffff;
  padding: 2.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 23px rgba(0, 0, 0, 0.08);
  max-width: 400px;
  width: 100%;
  animation: fadeSlideUp 0.6s ease-out;
}

.login-card h3 {
  color: var(--primary);
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 700;
  font-size: 1.5rem;
}

.input-group {
  position: relative;
  margin-bottom: 1.2rem;
}

.input-group input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 1.5px solid var(--primary);
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
}

.input-group input:focus {
  border-color: var(info);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 1.2);
  transition: all 0.3s ease;
}

.input-group i {
  position: absolute;
  right: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--primary);
}

.forgot-link {
  display: block;
  text-align: right;
  font-size: 0.85rem;
  color: var(--primary);
  text-decoration: none;
  margin-bottom: 1.5rem;
}

.forgot-link:hover {
  text-decoration: underline;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: var(--primary);
  color: var(--on-primary);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background: var(--secondary);
  color: var(--on-secondary);
  transform: scale(1.03);
}

/* Responsive */
@media (max-width: 768px) {
  .left-section {
    display: none;
  }

  .right-section {
    flex: 1;
    padding: 1.5rem;
  }

  .login-card {
    padding: 2rem 1.5rem;
  }
}

/* Animations */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes zoomIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.info-text {
  font-size: 0.9rem;
  margin-bottom: 1rem;
  color: #555;
  text-align: center;
}

.back-link {
  display: block;
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.85rem;
  color: var(--primary);
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}
</style>
