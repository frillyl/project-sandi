<template>
  <div class="dashboard">
    <!-- Navbar Section -->
    <Navbar />

    <div class="container">
      <h2 class="greeting">{{ greeting }}, {{ userName }}</h2>

      <div class="stats">
        <div class="stat-box total">
          <h3>Total Arsip</h3>
          <p>{{ totalArsip }}</p>
        </div>
        <div
          class="stat-box category"
          v-for="(jumlah, kategori) in arsipPerKategori"
          :key="kategori"
        >
          <h3>{{ kategori }}</h3>
          <p>{{ jumlah }} Arsip</p>
        </div>
      </div>

      <div class="chart-container">
        <h3>Statistik Arsip per Bulan</h3>
        <LineChart v-if="chartData" :chart-data="chartData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import LineChart from '@/components/LineChart.vue'

const userName = ref('')
const fetchUserData = async () => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    try {
      const response = await axios.get('http://localhost:8000/api/user', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      userName.value = response.data.name
    } catch (error) {
      console.error('Gagal mengambil data pengguna', error)
    }
  }
}

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 12) return 'Selamat Pagi'
  if (hour >= 12 && hour < 15) return 'Selamat Siang'
  if (hour >= 15 && hour < 18) return 'Selamat Sore'
  return 'Selamat Malam'
})

// Dummy data arsip (simulasi fetch dari API)
const totalArsip = ref(0)
const arsipPerKategori = ref({})
const chartData = ref(null)

// Simulasi fetch data
onMounted(async () => {
  await fetchUserData()
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/arsip/statistik')
    totalArsip.value = res.data.total
    arsipPerKategori.value = res.data.kategori

    const labels = Object.keys(res.data.bulanan)
    const data = Object.values(res.data.bulanan)

    chartData.value = {
      labels,
      datasets: [
        {
          label: 'Jumlah Arsip',
          data,
          borderColor: '#42a5f5',
          backgroundColor: 'rgba(66, 165, 245, 0.2)',
          fill: true,
          tension: 0.3,
        },
      ],
    }
  } catch (error) {
    console.error('Gagal Mengambil Data Arsip:', error)
  }
})
</script>

<style scoped>
.container {
  padding: 2rem;
}

.greeting {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.stat-box {
  background-color: #f0f4f8;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  flex: 1 1 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-box h3 {
  margin: 0 0 0.5rem;
  font-size: 1.2rem;
  color: #333;
}

.stat-box p {
  font-size: 1.6rem;
  font-weight: bold;
  color: #2c3e50;
}

.chart-container {
  margin-top: 2rem;
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  height: 350px;
}
</style>
