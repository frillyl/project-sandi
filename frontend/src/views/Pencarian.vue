<template>
  <div class="pencarian">
    <!-- Navbar Section -->
    <Navbar />

    <div class="container">
      <div class="content-wrapper">
        <div class="controls">
          <input type="text" v-model="searchQuery" placeholder="Cari Arsip..." />
          <select v-model="sortBy">
            <option value="">Urutkan Berdasarkan</option>
            <option value="judul_asc">Judul (A-Z)</option>
            <option value="judul_desc">Judul (Z-A)</option>
            <option value="tanggal_asc">Tanggal (Terlama-Terbaru)</option>
            <option value="tanggal_desc">Tanggal (Terbaru-Terlama)</option>
          </select>
          <select v-model="selectedCategory">
            <option value="">Semua Kategori</option>
            <option v-for="kategori in kategoriUnik" :key="kategori" :value="kategori">
              {{ kategori }}
            </option>
          </select>
          <select v-model="selectedKlasifikasi">
            <option value="">Semua Klasifikasi</option>
            <option v-for="klasifikasi in klasifikasiUnik" :key="klasifikasi" :value="klasifikasi">
              {{ klasifikasi }}
            </option>
          </select>
          <button class="btn-reset" @click="resetFilters">
            <i class="fa-solid fa-filter-circle-xmark"></i> Reset
          </button>
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
            <p v-if="!arsip.hasil_ocr || !arsip.summary_abstractive" class="status-processing">
              <i class="fa-solid fa-spinner fa-spin"></i> Sedang Diproses...
            </p>
          </div>
        </div>

        <div v-if="arsipTersaring.length < filteredTotal" class="load-more-wrapper">
          <button @click="loadMore" class="btn-load-more">Muat Lebih Banyak</button>
        </div>
      </div>

      <p v-if="loadingArsip" class="loading-arsip">
        <i class="fa-solid fa-spinner fa-spin"></i> Memuat ulang data arsip...
      </p>

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
            <p>{{ selectedArsip.summary_abstractive }}</p>
          </div>

          <div class="arsip-section">
            <h3><i class="fa-solid fa-book-open-reader"></i> Dokumen Serupa</h3>
            <ul v-if="loadingDetail">
              <li>Memuat rekomendasi...</li>
            </ul>
            <ul v-else>
              <li v-if="rekomendasi.length === 0">Tidak ada rekomendasi.</li>
              <li v-for="item in rekomendasi" :key="item.id" class="rekomendasi-item">
                <a
                  v-if="item.file_path"
                  :href="getFileUrl(item)"
                  target="_blank"
                  rel="noopener"
                  class="rekomendasi-link"
                  ><i class="fa-solid fa-file-pdf"></i> {{ item.judul }}</a
                >
              </li>
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
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'

const arsipList = ref([])
const loadingArsip = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedKlasifikasi = ref('')
const sortBy = ref('')
const showModal = ref(false)
const selectedArsip = ref({})
const ringkasan = ref('')
const rekomendasi = ref([])
const loadingDetail = ref(false)
const visibleCount = ref(8)
const loadStep = 8
const bookmarks = ref([])

let refreshInterval = null
const adaArsipDiproses = computed(() => {
  return arsipList.value.some(
    (arsip) =>
      !arsip.hasil_ocr ||
      arsip.hasil_ocr.trim() === '' ||
      !arsip.summary_abstractive ||
      arsip.summary_abstractive.trim() === '',
  )
})

const fetchArsip = async () => {
  loadingArsip.value = true
  try {
    const response = await axios.get(
      'https://incomplete-fan-renewal-impossible.trycloudflare.com/api/arsip',
    )
    arsipList.value = response.data

    if (!adaArsipDiproses.value && refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  } catch (error) {
    console.error('Gagal Mengambil Data Arsip: ', error)
  } finally {
    loadingArsip.value = false
  }
}

watch(arsipList, () => {
  if (adaArsipDiproses.value && !refreshInterval) {
    refreshInterval = setInterval(() => {
      if (adaArsipDiproses.value && !showModal.value) {
        fetchArsip
      }
    }, 20000)
  }
})

const kategoriUnik = computed(() => {
  return [
    ...new Set(
      arsipList.value
        .filter((item) => item && item.kategori) // pastikan data valid
        .map((item) => item.kategori),
    ),
  ]
})

const klasifikasiUnik = computed(() => {
  return [
    ...new Set(
      arsipList.value.filter((item) => item && item.klasifikasi).map((item) => item.klasifikasi),
    ),
  ]
})

const arsipTersaring = computed(() => {
  let hasil = [...arsipList.value]

  if (searchQuery.value.trim() !== '') {
    const query = searchQuery.value.toLowerCase()
    hasil = hasil.filter(
      (item) =>
        (item.judul && item.judul.toLowerCase().includes(query)) ||
        (item.hasil_ocr && item.hasil_ocr.toLowerCase().includes(query)),
    )
  }

  if (selectedCategory.value.trim() !== '') {
    hasil = hasil.filter((item) => item.kategori === selectedCategory.value)
  }

  if (selectedKlasifikasi.value.trim() !== '') {
    hasil = hasil.filter((item) => item.klasifikasi === selectedKlasifikasi.value)
  }

  switch (sortBy.value) {
    case 'judul_asc':
      hasil.sort((a, b) => a.judul.localeCompare(b.judul))
      break
    case 'judul_desc':
      hasil.sort((a, b) => b.judul.localeCompare(a.judul))
      break
    case 'tanggal_asc':
      hasil.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
      break
    case 'tanggal_desc':
      hasil.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      break
    default:
      break
  }

  return hasil.slice(0, visibleCount.value)
})

const filteredTotal = computed(() => {
  let hasil = [...arsipList.value]

  if (searchQuery.value.trim() !== '') {
    const query = searchQuery.value.toLowerCase()
    hasil = hasil.filter(
      (item) =>
        (item.judul && item.judul.toLowerCase().includes(query)) ||
        (item.hasil_ocr && item.hasil_ocr.toLowerCase().includes(query)),
    )
  }

  if (selectedCategory.value.trim() !== '') {
    hasil = hasil.filter((item) => item.kategori === selectedCategory.value)
  }

  if (selectedKlasifikasi.value.trim() !== '') {
    hasil = hasil.filter((item) => item.klasifikasi === selectedKlasifikasi.value)
  }

  return hasil.length
})

const fetchBookmarks = async () => {
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get(
      'https://incomplete-fan-renewal-impossible.trycloudflare.com/api/bookmarks',
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
        `https://incomplete-fan-renewal-impossible.trycloudflare.com/api/bookmarks/${arsip.id}`,
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
        'https://incomplete-fan-renewal-impossible.trycloudflare.com/api/bookmarks',
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
  return `https://suspected-outputs-telephone-mating.trycloudflare.com/storage/${arsip.file_path}`
}

const downloadFile = async (arsip) => {
  try {
    const response = await axios.get(
      `https://incomplete-fan-renewal-impossible.trycloudflare.com/api/arsip/download/${arsip.id}`,
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
  if (!arsip.hasil_ocr || !arsip.summary_abstractive) {
    Swal.fire({
      icon: 'info',
      title: 'Sedang Diproses',
      text: 'Arsip ini masih dalam proses OCR dan Peringkasan. Silahkan tunggu beberapa saat lagi.',
    })
    return
  }
  selectedArsip.value = arsip
  showModal.value = true
  ringkasan.value = ''
  rekomendasi.value = []
  loadingDetail.value = true

  try {
    const resSummary = await axios.get(
      `https://suspected-outputs-telephone-mating.trycloudflare.com/summarize_abstractive/${arsip.id}`,
    )
    ringkasan.value = resSummary.data.summary_abstractive
  } catch (error) {
    console.error('Gagal memuat ringkasan:', error)
    ringkasan.value = '[Gagal memuat ringkasan]'
  } finally {
    loadingDetail.value = false
  }

  try {
    const resRekomendasi = await axios.get(
      `https://suspected-outputs-telephone-mating.trycloudflare.com/recommendation/${arsip.id}`,
    )
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

const resetFilters = () => {
  searchQuery.value = ''
  sortBy.value = ''
  selectedCategory.value = ''
  visibleCount.value = 8
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch([searchQuery, selectedCategory, selectedKlasifikasi, sortBy], () => {
  visibleCount.value = 8
})

onMounted(() => {
  fetchArsip()
  fetchBookmarks()

  refreshInterval = setInterval(() => {
    if (adaArsipDiproses.value && !showModal.value) {
      fetchArsip()
    }
  }, 20000)
})
</script>

<style scoped>
.pencarian {
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
  gap: 1.5rem;
}

.controls {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 1rem;
  /* margin-bottom: 1.5rem; */
}

.controls input,
.controls select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--neutral-300);
  border-radius: 6px;
  background-color: white;
  color: var(--neutral-900);
  font-size: 0.95rem;
  transition: border-color 0.2s ease;
}

.controls input:focus,
.controls select:focus {
  border-color: var(--primary);
  outline: none;
}

.controls select {
  cursor: pointer;
}

.btn-reset {
  background-color: var(--error);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s ease;
}

.btn-reset:hover {
  background-color: #c9302c;
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
  /* width: 250px; */
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  position: relative;
}

.arsip-card:hover {
  transform: translateY(-6px);
  /* background-color: var(--secondary);
  color: var(--on-secondary); */
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.arsip-card img {
  width: 100%;
  height: 160px;
  object-fit: contain;
  border-radius: 8px;
  background-color: var(--neutral-50);
}

.arsip-card h3 {
  margin-top: 1rem;
  color: var(--neutral-900);
  font-size: 1.1rem;
}

.arsip-card p {
  margin: 0.25rem 0;
  color: var(--neutral-600);
  font-size: 0.9rem;
}

.status-processing {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--warning);
  font-style: italic;
}

.bookmark-icon {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 1.3rem;
  color: var(--warning);
  cursor: pointer;
  z-index: 2;
  transition: transform 0.2s ease;
}

.bookmark-icon:hover {
  transform: scale(1.1);
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

.loading-arsip {
  font-style: italic;
  font-size: 0.9rem;
  color: var(--neutral-600);
  margin-bottom: 1rem;
  display: flex;
  text-align: center;
  gap: 0.5rem;
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
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  animation: fadeIn 0.3s ease-in-out;
}

/* .modal-header {
  margin-bottom: 1.5rem;
} */

.arsip-title {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: var(--primary);
}

.arsip-meta {
  font-size: 0.9rem;
  color: var(--neutral-600);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.arsip-actions {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
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

.rekomendasi-item {
  margin: 0.5rem 0;
  list-style: none;
}

.rekomendasi-link {
  color: var(--info);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s ease;
}

.rekomendasi-link:hover {
  color: #4338ca;
  text-decoration: underline;
}

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

/* Responsive */
@media (max-width: 768px) {
  .controls {
    flex-direction: column;
    align-items: stretch;
  }

  .controls input,
  .controls select,
  .btn-reset {
    width: 100%;
  }

  .arsip-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn {
    justify-content: center;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 1rem;
  }

  .arsip-card h3 {
    font-size: 1rem;
  }

  .arsip-card p {
    font-size: 0.8rem;
  }

  .modal-content {
    padding: 1rem;
    width: 95%;
  }

  .arsip-title {
    font-size: 1.2rem;
  }

  .arsip-meta {
    font-size: 0.8rem;
    flex-direction: column;
    align-items: flex-start;
  }

  .arsip-section h3 {
    font-size: 1rem;
  }

  .arsip-section p,
  .arsip-section ul {
    font-size: 0.85rem;
  }

  .close-btn {
    top: 0.5rem;
    right: 0.5rem;
  }
}
</style>
