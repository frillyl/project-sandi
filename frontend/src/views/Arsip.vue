<template>
  <div class="arsip">
    <!-- Navbar Section -->
    <Navbar />

    <div class="container">
      <div class="header">
        <div class="title">
          <i class="fa-solid fa-box-archive"></i>
          <h2>Daftar Arsip</h2>
        </div>

        <div class="actions">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cari Arsip..."
            class="search-input"
          />
          <button class="btn tambah" @click="openModal">
            <i class="fa-solid fa-plus"></i> Tambah Arsip
          </button>
        </div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Judul</th>
              <th>Kategori</th>
              <th>Klasifikasi</th>
              <th>Tanggal</th>
              <th>Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="arsip in filteredArsip" :key="arsip.id">
              <td data-label="Judul">{{ arsip.judul }}</td>
              <td data-label="Kategori">{{ arsip.kategori }}</td>
              <td data-label="Klasifikasi">{{ arsip.klasifikasi }}</td>
              <td data-label="Tanggal">{{ formatDate(arsip.created_at) }}</td>
              <td class="actions-cell">
                <button class="btn edit" @click="openEditModal(arsip)">
                  <i class="fa-solid fa-pen-to-square"></i> Edit
                </button>
                <button class="btn hapus" @click="deleteArsip(arsip.id)">
                  <i class="fa-solid fa-trash"></i> Hapus
                </button>
                <a :href="getFileUrl(arsip)" target="_blank" rel="noopener" class="btn preview">
                  <i class="fa-solid fa-eye"></i> Lihat
                </a>
                <button class="btn download" @click="downloadFile(arsip)">
                  <i class="fa-solid fa-download"></i> Unduh
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Form Arsip -->
    <transition name="fade">
      <div class="modal" v-if="showModal" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <i class="fa-solid fa-file-circle-plus"></i>
            <h3>{{ isEditMode ? 'Edit Arsip' : 'Tambah Arsip' }}</h3>
          </div>
          <hr />
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="judul">Judul Arsip</label>
              <input
                type="text"
                id="judul"
                v-model="form.judul"
                placeholder="Masukkan Judul Arsip"
                :class="{ 'input-error': judulError }"
              />
              <span class="error-msg" v-if="judulError"
                ><i class="fa-solid fa-circle-exclamation"></i>{{ judulError }}</span
              >
            </div>
            <div class="form-group">
              <label for="kategori">Kategori</label>
              <select
                id="kategori"
                v-model="form.kategori"
                :class="{ 'input-error': kategoriError }"
              >
                <option value="">--- Pilih Kategori ---</option>
                <option value="Umum">Umum</option>
                <option value="Pribadi">Pribadi</option>
                <option value="Rahasia">Rahasia</option>
              </select>
              <span class="error-msg" v-if="kategoriError"
                ><i class="fa-solid fa-circle-exclamation"></i>{{ kategoriError }}</span
              >
            </div>
            <div class="form-group">
              <label for="klasifikasi">Klasifikasi</label>
              <select
                id="klasifikasi"
                v-model="form.klasifikasi"
                :class="{ 'input-error': klasifikasiError }"
              >
                <option value="">--- Pilih Klasifikasi ---</option>
                <option
                  v-for="klasifikasi in klasifikasiList"
                  :key="klasifikasi.id"
                  :value="klasifikasi.klasifikasi"
                >
                  {{ klasifikasi.klasifikasi }}
                </option>
              </select>
              <span class="error-msg" v-if="klasifikasiError">
                <i class="fa-solid fa-circle-exclamation"></i> {{ klasifikasiError }}
              </span>
            </div>
            <div class="form-group">
              <label for="file">Unggah Dokumen</label>
              <small v-if="isEditMode" style="display: block; margin-bottom: 5px"
                >(Biarkan kosong jika tidak ingin mengganti file)</small
              >
              <input
                type="file"
                id="file"
                accept=".pdf"
                @change="handleFileUpload"
                :class="{ 'input-error': fileError }"
              />
              <span class="error-msg" v-if="fileError"
                ><i class="fa-solid fa-circle-exclamation"></i>{{ fileError }}</span
              >
            </div>
            <div class="modal-actions">
              <button type="submit" class="btn-submit">
                {{ isEditMode ? 'Simpan Perubahan' : 'Tambah' }}
              </button>
              <button type="button" class="btn-cancel" @click="closeModal">Batal</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'

const arsipList = ref([])
const klasifikasiList = ref([])
const showModal = ref(false)
const isEditMode = ref(false)
const selectedId = ref(null)
const searchQuery = ref('')

const filteredArsip = computed(() => {
  return arsipList.value.filter((arsip) => {
    const keyword = searchQuery.value.toLowerCase()
    return (
      arsip.judul.toLowerCase().includes(keyword) ||
      arsip.kategori.toLowerCase().includes(keyword) ||
      (arsip.created_at && arsip.created_at.toLowerCase().includes(keyword))
    )
  })
})

const openEditModal = (arsip) => {
  isEditMode.value = true
  selectedId.value = arsip.id
  form.value = {
    judul: arsip.judul,
    kategori: arsip.kategori,
    klasifikasi: arsip.klasifikasi,
    file: null,
  }
  showModal.value = true
}

const fetchArsip = async () => {
  try {
    const response = await axios.get(
      'https://pupils-immigrants-gmt-associations.trycloudflare.com/api/arsip',
    )
    arsipList.value = response.data
  } catch (error) {
    console.error('Gagal Mengambil Data Arsip:', error)
  }
}

const fetchKlasifikasi = async () => {
  try {
    const response = await axios.get(
      'https://pupils-immigrants-gmt-associations.trycloudflare.com/api/klasifikasi',
    )
    klasifikasiList.value = response.data
  } catch (error) {
    console.error('Gagal mengambil data klasifikasi:', error)
  }
}

const form = ref({
  judul: '',
  kategori: '',
  klasifikasi: '',
  file: null,
})

const errors = ref({})

const submitForm = async () => {
  errors.value = {}

  if (!form.value.judul) errors.value.judul = ['Judul wajib diisi']
  if (!form.value.kategori) errors.value.kategori = ['Kategori wajib dipilih']
  if (!isEditMode.value && !form.value.file) errors.value.file = ['File wajib diunggah']
  if (!form.value.klasifikasi) errors.value.klasifikasi = ['Klasifikasi wajib dipilih']

  if (Object.keys(errors.value).length > 0) return

  const formData = new FormData()
  formData.append('judul', form.value.judul)
  formData.append('kategori', form.value.kategori)
  formData.append('klasifikasi', form.value.klasifikasi)
  if (form.value.file) {
    formData.append('file', form.value.file)
  }

  try {
    if (isEditMode.value) {
      formData.append('_method', 'PUT')
      await axios.post(
        `https://pupils-immigrants-gmt-associations.trycloudflare.com/api/arsip/${selectedId.value}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      )
    } else {
      await axios.post(
        'https://pupils-immigrants-gmt-associations.trycloudflare.com/api/arsip',
        formData,
        {
          'Content-Type': 'multipart/form-data',
        },
      )
    }

    await fetchArsip()
    closeModal()
    resetForm()
    Swal.fire({
      icon: 'success',
      title: 'Berhasil',
      text: isEditMode.value ? 'Arsip berhasil diperbarui.' : 'Arsip berhasil ditambahkan.',
      timer: 2000,
      showConfirmButton: false,
      timerProgressBar: true,
    })
  } catch (error) {
    if (error.response && error.response.data.errors) {
      errors.value = error.response.data.errors
    } else {
      console.error('Gagal Mengunggah Arsip:', error)
      Swal.fire('Gagal', 'Terjadi Kesalahan Saat Mengunggah Arsip.', 'error')
    }
  }
}

const handleFileUpload = (event) => {
  form.value.file = event.target.files[0]
}

const deleteArsip = async (id) => {
  const result = await Swal.fire({
    title: 'Yakin?',
    text: 'Data Arsip yang Dihapus Tidak Bisa Dikembalikan!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Ya, Hapus!',
    confirmButtonColor: 'var(--primary)',
    cancelButtonText: 'Batal',
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`https://pupils-immigrants-gmt-associations.trycloudflare.com/api/arsip/${id}`)
      await fetchArsip()
      Swal.fire({
        icon: 'success',
        title: 'Berhasil',
        text: 'Pengguna Berhasil Dihapus!',
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true,
      })
    } catch (error) {
      console.error('Gagal Menghapus Arsip:', error)
      Swal.fire('Gagal!', 'Terjadi Kesalahan Saat Menghapus Arsip.', 'error')
    }
  }
}

const resetForm = () => {
  isEditMode.value = false
  selectedId.value = null
  form.value = {
    judul: '',
    kategori: '',
    klasifikasi: '',
    file: null,
  }
  errors.value = {}
}

const getFileUrl = (arsip) => {
  return `https://pupils-immigrants-gmt-associations.trycloudflare.com/storage/${arsip.file_path}`
}

const downloadFile = async (arsip) => {
  try {
    const response = await axios.get(
      `https://pupils-immigrants-gmt-associations.trycloudflare.com/api/arsip/download/${arsip.id}`,
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

const openModal = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('id-ID', options)
}

const judulError = computed(() => {
  if (!(form.value.judul || '').trim()) return 'Judul wajib diisi'
  return ''
})

const kategoriError = computed(() => {
  if (!(form.value.kategori || '').trim()) return 'Kategori wajib diisi'
  return ''
})

const klasifikasiError = computed(() => {
  if (!(form.value.klasifikasi || '').trim()) return 'Klasifikasi wajib dipilih'
  return ''
})

const fileError = computed(() => {
  if (!form.value.file && !isEditMode.value) {
    return 'File wajib diunggah'
  }
  return ''
})

onMounted(() => {
  fetchArsip()
  fetchKlasifikasi()
})
</script>

<style scoped>
.arsip {
  min-height: 100vh;
  background: #f9f9f9;
  padding-bottom: 2rem;
}

.container {
  margin-top: 50px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.title {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--on-secondary);
}

.title h2 {
  margin: 0;
  color: var(--on-secondary);
}

.actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-left: auto;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn.tambah {
  background-color: var(--primary);
}

.btn.tambah:hover {
  background-color: #d1c4e9;
  color: #311b92;
}

.table-container table {
  width: 100%;
  border-collapse: collapse;
}

.table-container th,
.table-container td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.table-container th {
  background-color: #f2f2f2;
  text-align: center;
}

.actions-cell {
  display: flex;
  gap: 6px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.btn.edit {
  background-color: var(--warning);
}

.btn.edit:hover {
  background-color: #db9737;
}

.btn.hapus {
  background-color: var(--error);
}

.btn.hapus:hover {
  background-color: #c9302c;
}

.btn.preview {
  background-color: var(--info);
  text-decoration: none;
}

.preview {
  font-size: 13.5px;
}

.btn.preview:hover {
  background-color: #4f46e5;
}

.btn.download {
  background-color: var(--success);
  text-decoration: none;
}

.btn.download:hover {
  background-color: #059669;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  position: relative;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: var(--on-secondary);
}

.modal-content hr {
  border: none;
  border-bottom: 2px solid var(--on-secondary);
  margin-bottom: 1.5rem;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
  color: #333;
}

.modal-header i {
  font-size: 20px;
  color: var(--on-secondary);
}

.modal-header h3 {
  font-size: 20px;
  margin: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: 600;
  font-size: 14px;
  color: var(--on-secondary);
}

.form-group input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.form-group select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.input-error {
  border: 1px solid var(--error) !important;
  background-color: #ffe6e6;
}

.error-msg {
  font-size: 12px;
}

.error-msg i {
  margin-right: 2px;
  font-size: 12px;
  color: var(--error);
}

.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-submit {
  background: var(--success);
  color: white;
  font-size: 14px;
  border-radius: 4px;
}

.btn-submit:hover {
  background: #059669;
  color: white;
}

.btn-cancel {
  background: var(--neutral-600);
  color: white;
  font-size: 14px;
  border-radius: 4px;
}

.btn-cancel:hover {
  background: #757575;
  color: white;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th,
td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

thead {
  background: #f0f0f0;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .btn.tambah {
    width: 100%;
    justify-content: center;
  }

  .actions-cell {
    flex-direction: column;
    gap: 5px;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .table-container table {
    font-size: 14px;
    word-break: break-word;
  }

  .modal-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 20px;
  }

  .table-container table,
  .table-container thead,
  .table-container tbody,
  .table-container th,
  .table-container td,
  .table-container tr {
    display: block;
    width: 100%;
  }

  .table-container thead {
    display: none;
  }

  .table-container tr {
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 10px;
    background: #fff;
  }

  .table-container td {
    text-align: right;
    padding-left: 50%;
    position: relative;
  }

  .table-container td::before {
    content: attr(data-label);
    position: absolute;
    left: 15px;
    width: 45%;
    padding-right: 10px;
    white-space: nowrap;
    font-weight: bold;
    text-align: left;
  }
}
</style>
