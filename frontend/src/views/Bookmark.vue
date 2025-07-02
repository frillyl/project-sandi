<template>
  <div class="bookmark">
    <!-- Navbar Section -->
    <Navbar />

    <div class="container">
      <div class="content-wrapper">
        <div class="bookmark-info">
          <h2><i class="fa-solid fa-bookmark"></i> Bookmark</h2>
          <p>Berikut adalah daftar arsip yang telah Anda tandai sebagai favorit.</p>
        </div>
        <div class="grid">
          <div
            class="arsip-card"
            v-for="arsip in arsipTersaring"
            :key="arsip.id"
            @click="openModal(arsip)"
          >
            <div class="bookmark-icon" @click.stop="toggleBookmark(arsip)">
              <i :class="['fa-bookmark', isBookmarked(arsip.id) ? 'fas' : 'far']"></i>
            </div>
            <img :src="Thumbnail" alt="Thumbnail" />
            <h3>{{ arsip.judul }}</h3>
            <p>{{ arsip.kategori }}</p>
            <p>{{ arsip.klasifikasi }}</p>
            <p>{{ formatTanggal(arsip.created_at) }}</p>
          </div>
        </div>

        <div v-if="arsipTersaring.length < filteredTotal" class="load-more-wrapper">
          <button @click="loadMore" class="btn-load-more">Muat Lebih Banyak</button>
        </div>
      </div>

      <!-- Modal Detail -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="close-btn" @click="closeModal"><i class="fa-solid fa-xmark"></i></button>
          <h2 class="arsip-title">{{ selectedArsip.judul }}</h2>
          <p class="arsip-meta">
            <span><strong>Kategori:</strong> {{ selectedArsip.kategori }}</span>
            <span
              ><strong>Tanggal Upload:</strong> {{ formatTanggal(selectedArsip.created_at) }}</span
            >
          </p>

          <div class="arsip-actions">
            <a :href="getFileUrl(selectedArsip)" target="_blank" class="btn btn-view" rel="noopener"
              ><i class="fa-solid fa-eye"></i> Lihat</a
            >
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
import Thumbnail from '@/assets/images/pdf.png'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'

const arsipList = ref([])
const showModal = ref(false)
const selectedArsip = ref({})
const ringkasan = ref('')
const rekomendasi = ref([])
const loadingDetail = ref(false)
const visibleCount = ref(8)
const loadStep = 8
const bookmarks = ref([])

const fetchArsip = async () => {
  try {
    const response = await axios.get(
      'https://avi-initiative-basics-xml.trycloudflare.com/api/arsip',
    )
    arsipList.value = response.data
  } catch (error) {
    console.error('Gagal Mengambil Data Arsip: ', error)
  }
}

const arsipTersaring = computed(() => {
  return arsipList.value.filter((item) => isBookmarked(item.id)).slice(0, visibleCount.value)
})

const filteredTotal = computed(() => {
  return arsipList.value.filter((item) => isBookmarked(item.id)).length
})

const fetchBookmarks = async () => {
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get(
      'https://avi-initiative-basics-xml.trycloudflare.com/api/bookmarks',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    bookmarks.value = response.data.map((bookmark) => bookmark.arsip_id)
  } catch (error) {
    console.error('Gagal mengambil data bookmark: ', error)
  }
}

const isBookmarked = (arsipId) => {
  return bookmarks.value.includes(arsipId)
}

const toggleBookmark = async (arsip) => {
  const token = localStorage.getItem('auth_token')
  if (!token) {
    Swal.fire('Gagal', 'Anda harus login terlebih dahulu untuk bookmark.', 'warning')
    return
  }

  if (isBookmarked(arsip.id)) {
    try {
      await axios.delete(
        `https://avi-initiative-basics-xml.trycloudflare.com/api/bookmarks/${arsip.id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      bookmarks.value = bookmarks.value.filter((id) => id !== arsip.id)
      Swal.fire('Dihapus', 'Arsip dihapus dari bookmark.', 'success')
    } catch (error) {
      console.error('Gagal menghapus bookmark:', error)
      Swal.fire('Gagal', 'Tidak bisa menghapus bookmark.', 'error')
    }
  } else {
    try {
      await axios.post(
        'https://avi-initiative-basics-xml.trycloudflare.com/api/bookmarks',
        { arsip_id: arsip.id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      bookmarks.value.push(arsip.id)
      Swal.fire('Ditambahkan', 'Arsip ditambahkan ke bookmark.', 'success')
    } catch (error) {
      console.error('Gagal menambahkan bookmark:', error)
      Swal.fire('Gagal', 'Tidak bisa menambahkan bookmark.', 'error')
    }
  }
}

const loadMore = () => {
  visibleCount.value += loadStep
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
  return `https://avi-initiative-basics-xml.trycloudflare.com/storage/${arsip.file_path}`
}

const downloadFile = async (arsip) => {
  try {
    const response = await axios.get(
      `https://avi-initiative-basics-xml.trycloudflare.com/api/arsip/download/${arsip.id}`,
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

const openModal = async (arsip) => {
  selectedArsip.value = arsip
  showModal.value = true
  ringkasan.value = ''
  rekomendasi.value = []
  loadingDetail.value = true

  try {
    const resSummary = await axios.get(`https://ls-nw-ireland-sells.trycloudflare.com/summarize/${arsip.id}`)
    ringkasan.value = resSummary.data.summary
  } catch (error) {
    console.error('Gagal memuat ringkasan:', error)
    ringkasan.value = '[Gagal memuat ringkasan]'
  } finally {
    loadingDetail.value = false
  }

  try {
    const resRekomendasi = await axios.get(`https://ls-nw-ireland-sells.trycloudflare.com/recommendation/${arsip.id}`)
    rekomendasi.value = resRekomendasi.data.recommendations
  } catch (error) {
    console.error('Gagal memuat rekomendasi:', error)
    rekomendasi.value = []
  } finally {
    loadingDetail.value = false
  }
}

const closeModal = () => {
  showModal.value = false
  selectedArsip.value = {}
}

onMounted(() => {
  fetchArsip()
  fetchBookmarks()
})
</script>

<style scoped>
.bookmark {
  min-height: 100vh;
  background: #f9f9f9;
  padding-bottom: 2rem;
}

.container {
  padding: 2rem;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bookmark-info h2 {
  font-size: 1.75rem;
  color: var(--on-secondary);
  margin-bottom: 0.25rem;
}

.bookmark-info p {
  color: var(--neutral-600);
  margin-bottom: 1rem;
}

.btn-reset {
  background-color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s ease;
}

.btn-reset:hover {
  background-color: #c82333;
  color: white;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.arsip-card {
  background-color: white;
  border: 1px solid var(--neutral-300);
  border-radius: 12px;
  padding: 1rem;
  width: 250px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(31, 41, 55, 0.05);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  position: relative;
}

.arsip-card:hover {
  transform: translateY(-6px);
  /* background-color: var(--secondary);
  color: var(--on-secondary); */
  box-shadow: 0 4px 10px rgba(31, 41, 55, 0.1);
}

.arsip-card img {
  width: 100%;
  height: 160px;
  object-fit: contain;
  border-radius: 6px;
}

.arsip-card h3 {
  margin-top: 1rem;
  color: var(--neutral-900);
}

.arsip-card p {
  font-size: 0.9rem;
  color: var(--neutral-600);
}

/* .bookmark-info {
  margin-bottom: 2rem;
}

.bookmark-info h2 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: #333333;
} */

.bookmark-icon {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 1.25rem;
  color: var(--warning);
  cursor: pointer;
  z-index: 2;
  transition: transform 0.2s;
}

.bookmark-icon:hover {
  transform: scale(1.2);
}

.load-more-wrapper {
  text-align: center;
  margin-top: 2rem;
}

.btn-load-more {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary);
  color: var(--on-primary);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.btn-load-more:hover {
  background-color: var(--secondary);
  color: var(--on-secondary);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(31, 41, 55, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 16px;
  max-width: 640px;
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

.arsip-title {
  margin-bottom: 0.25rem;
  font-size: 1.5rem;
  color: #333;
}

.arsip-meta {
  font-size: 0.9rem;
  color: #555;
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

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--neutral-600);
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--neutral-900);
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
  .container {
    padding: 1.5rem;
  }

  .arsip-card {
    width: 100% !important;
  }
}

@media (max-width: 768) {
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
  }

  .arsip-card {
    padding: 0.75rem;
  }

  .arsip-card img {
    height: 140px;
  }

  .bookmark-info h2 {
    font-size: 1.5rem;
  }

  .bookmark-info p {
    font-size: 0.95rem;
  }

  .arsip-card h3 {
    font-size: 1rem;
  }

  .arsip-card p {
    font-size: 0.85rem;
  }

  .btn-load-more {
    width: 100%;
  }

  .arsip-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 1rem;
  }

  .grid {
    grid-template-columns: 1fr;
  }

  .arsip-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .modal-content {
    padding: 1rem;
    max-width: 95%;
  }

  .arsip-section p,
  .arsip-section ul {
    margin-left: 0.5rem;
    font-size: 0.9rem;
  }

  .close-btn {
    top: 0.75rem;
    right: 0.75rem;
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
