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

      <!-- <div class="chart-container">
        <h3>Statistik Arsip per Bulan</h3>
        <LineChart v-if="chartData" :chart-data="chartData" />
      </div> -->

      <div class="bottom-section">
        <div class="left">
          <div class="chart-container">
            <h3 class="chart-title">Statistik Arsip per Bulan</h3>
            <LineChart v-if="chartData" :chart-data="chartData" />
          </div>
        </div>

        <div class="right">
          <div class="bookmark-header">
            <h3 class="bookmark-title">Bookmarks</h3>
            <router-link to="/demo/bookmark" class="lihat-semua">Lihat Semua</router-link>
          </div>

          <div class="bookmark-list">
            <div v-if="bookmarks.length === 0" class="bookmark-empty">
              Anda belum memiliki bookmark.
            </div>
            <div v-else class="bookmark-item" v-for="arsip in bookmarks" :key="arsip.arsip.id">
              <h4 @click="openModal(arsip)" class="clickable">{{ arsip.arsip.judul }}</h4>
              <p class="tanggal">{{ new Date(arsip.arsip.created_at).toLocaleDateString() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Detail -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="close-btn" @click="closeModal"><i class="fa-solid fa-xmark"></i></button>
          <h2 class="arsip-title">{{ selectedArsip.arsip.judul }}</h2>
          <p class="arsip-meta">
            <span><strong>Kategori:</strong> {{ selectedArsip.arsip.kategori }}</span>
            <span
              ><strong>Tanggal Upload:</strong>
              {{ formatTanggal(selectedArsip.arsip.created_at) }}</span
            >
          </p>

          <div class="arsip-actions">
            <a
              :href="getFileUrl(selectedArsip)"
              target="_blank"
              class="btn btn-view"
              rel="noopener"
            >
              <i class="fa-solid fa-eye"></i> Lihat
            </a>
            <button class="btn btn-download" @click="downloadFile(selectedArsip)">
              <i class="fa-solid fa-download"></i> Unduh
            </button>
          </div>

          <hr />

          <div class="arsip-section">
            <h3><i class="fa-solid fa-align-left"></i> Ringkasan Arsip</h3>
            <p v-if="loadingDetail">Memuat ringkasan...</p>
            <p v-else>{{ ringkasan }}</p>
          </div>

          <div class="arsip-section">
            <h3><i class="fa-solid fa-book-open-reader"></i> Dokumen Serupa</h3>
            <ul v-if="loadingDetail">
              <li>Memuat rekomendasi...</li>
            </ul>
            <ul v-else>
              <li v-if="rekomendasi.length === 0">Tidak ada rekomendasi.</li>
              <li v-for="item in rekomendasi" :key="item.id">{{ item.judul }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import LineChart from '@/components/LineChart.vue'
import Swal from 'sweetalert2'

const userName = ref('')
const fetchUserData = async () => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    try {
      const response = await axios.get(
        'https://hudson-assuming-kenneth-e.trycloudflare.com/api/user',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
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
const bookmarks = ref([])

const fetchBookmarks = async () => {
  const token = localStorage.getItem('auth_token')
  try {
    const response = await axios.get(
      'https://hudson-assuming-kenneth-e.trycloudflare.com/api/bookmarks',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    bookmarks.value = response.data.slice(0, 3)
  } catch (error) {
    console.error('Gagal mengambil data bookmark: ', error)
  }
}

const showModal = ref(false)
const selectedArsip = ref({})
const ringkasan = ref('')
const rekomendasi = ref([])
const loadingDetail = ref(false)

const openModal = async (arsip) => {
  selectedArsip.value = arsip
  showModal.value = true
  ringkasan.value = ''
  rekomendasi.value = []
  loadingDetail.value = true

  try {
    const resSummary = await axios.get(`https://jurisdiction-cables-pets-namespace.trycloudflare.com/summarize/${arsip.arsip.id}`)
    ringkasan.value = resSummary.data.summary
  } catch (error) {
    console.error('Gagal memuat ringkasan:', error)
    ringkasan.value = '[Gagal memuat ringkasan]'
  }

  try {
    const resRekomendasi = await axios.get(`https://jurisdiction-cables-pets-namespace.trycloudflare.com/recommendation/${arsip.arsip.id}`)
    rekomendasi.value = resRekomendasi.data.recommendations
  } catch (error) {
    console.error('Gagal memuat rekomendasi:', error)
    rekomendasi.value = []
  }

  loadingDetail.value = false
}

const closeModal = () => {
  showModal.value = false
  selectedArsip.value = {}
}

const formatTanggal = (tanggal) => {
  const d = new Date(tanggal)
  return d.toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const getFileUrl = (arsip) => {
  return `https://hudson-assuming-kenneth-e.trycloudflare.com/storage/${arsip.arsip.file_path}`
}

const downloadFile = async (arsip) => {
  try {
    const response = await axios.get(
      `https://hudson-assuming-kenneth-e.trycloudflare.com/api/arsip/download/${arsip.arsip.id}`,
      {
        responseType: 'blob',
      },
    )
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = arsip.judul + '.pdf'
    link.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Gagal mengunduh file:', error)
    Swal.fire('Gagal', 'Terjadi Kesalahan Saat Mengunduh File.', 'error')
  }
}

// Simulasi fetch data
onMounted(async () => {
  await fetchUserData()
  await fetchBookmarks()
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
.dashboard {
  min-height: 100vh;
  background: #f9f9f9;
  padding-bottom: 2rem;
}

.container {
  padding: 2rem;
}

.greeting {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: var(--on-secondary);
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.stat-box {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  flex: 1 1 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.stat-box:hover {
  transform: translateY(-2px);
}

.stat-box.total {
  background-color: var(--primary);
  color: var(--on-primary);
}

.stat-box.total h3 {
  color: var(--on-primary);
}

.stat-box h3 {
  margin: 0 0 0.5rem;
  font-size: 1.2rem;
  color: var(--on-secondary);
}

.stat-box p {
  font-size: 1.6rem;
  font-weight: 400;
}

.bottom-section {
  display: flex;
  margin-top: 2rem;
  gap: 2rem;
}

.left,
.right {
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  background: #ffffff;
}

.left {
  flex: 2;
}

.right {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.bookmark-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  color: var(--on-secondary);
}

.lihat-semua {
  font-size: 0.9rem;
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.bookmark-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.bookmark-empty {
  padding: 1rem;
  color: var(--neutral-600);
  font-style: italic;
  text-align: center;
}

.bookmark-item {
  background-color: var(--secondary);
  padding: 0.8rem;
  border-radius: 8px;
}

.bookmark-item h4 {
  margin: 0 0 0.3rem;
  font-size: 1rem;
  color: var(--primary);
}

.bookmark-item .tanggal {
  font-size: 0.8rem;
  color: var(--neutral-600);
}

.clickable:hover {
  cursor: pointer;
  color: var(--on-secondary);
}

.chart-container {
  /* margin-top: 2rem;
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); */
  height: 400px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease-in-out;
}

.modal-header {
  margin-bottom: 1.5rem;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--neutral-600);
}

.close-btn:hover {
  color: var(--neutral-900);
}

.arsip-title {
  margin-bottom: 0.25rem;
  font-size: 1.5rem;
  color: var(--neutral-900);
}

.arsip-meta {
  font-size: 0.9rem;
  color: var(--neutral-600);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.arsip-actions {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
}

.arsip-actions {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.btn-view {
  background-color: var(--info);
}

.btn-view:hover {
  background-color: #4f46e5;
}

.btn-download {
  background-color: var(--success);
}

.btn-download:hover {
  background-color: #059669;
}

.arsip-section {
  margin-top: 1.5rem;
}

.arsip-section h3 {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  color: var(--neutral-900);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.arsip-section p,
.arsip-section ul {
  font-size: 0.95rem;
  color: var(--neutral-600);
  margin-left: 1.2rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .bottom-section {
    flex-direction: column;
  }

  .left,
  .right {
    width: 100%;
    padding: 1rem;
  }

  .chart-container {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .greeting {
    font-size: 1.4rem;
    text-align: center;
  }

  .stats {
    flex-direction: column;
    align-items: stretch;
  }

  .stat-box {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
  }

  .bookmark-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .arsip-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .arsip-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .modal-content {
    padding: 1.2rem;
    overflow-y: auto;
    max-height: 90vh;
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-300) transparent;
  }

  .modal-content::-webkit-scrollbar {
    width: 6px;
  }

  .modal-content::-webkit-scrollbar-thumb {
    background-color: var(--neutral-300);
    border-radius: 4px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 1rem;
  }

  .stat-box p {
    font-size: 1.2rem;
  }

  .bookmark-item h4 {
    font-size: 0.95rem;
  }

  .bookmark-item .tanggal {
    font-size: 0.75rem;
  }

  .modal-content {
    width: 95%;
    padding: 1rem;
    max-height: 85vh;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-300) transparent;
  }

  .modal-content::-webkit-scrollbar {
    width: 6px;
  }

  .modal-content::-webkit-scrollbar-thumb {
    background-color: var(--neutral-300);
    border-radius: 4px;
  }

  .arsip-title {
    font-size: 1.2rem;
  }

  .arsip-meta {
    font-size: 0.85rem;
    gap: 0.3rem;
  }

  .arsip-section h3 {
    font-size: 0.95rem;
  }

  .arsip-section p,
  .arsip-section ul {
    font-size: 0.85rem;
  }
}

/* Animations */
@keyframes fadeIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
