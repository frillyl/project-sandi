<template>
  <div class="master-klasifikasi">
    <!-- Navbar -->
    <Navbar />

    <div class="container">
      <div class="header">
        <div class="title">
          <i class="fa-solid fa-list"></i>
          <h2>Daftar Klasifikasi</h2>
        </div>

        <div class="actions">
          <input
            v-model="search"
            type="text"
            placeholder="Cari Klasifikasi..."
            class="search-input"
          />
          <button class="btn tambah" @click="openModal">
            <i class="fa-solid fa-plus"></i> Tambah Klasifikasi
          </button>
        </div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Kode</th>
              <th>Klasifikasi</th>
              <th>Deskripsi</th>
              <th>Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredList" :key="item.id">
              <td>{{ item.kode }}</td>
              <td>{{ item.klasifikasi }}</td>
              <td>{{ item.deskripsi }}</td>
              <td class="actions-cell">
                <button class="btn edit" @click="editItem(item)">
                  <i class="fa-solid fa-pen-to-square"></i> Edit
                </button>
                <button class="btn hapus" @click="confirmDelete(item.id)">
                  <i class="fa-solid fa-trash"></i> Hapus
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Form -->
    <transition name="fade">
      <div class="modal" v-if="showModal" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <i :class="form.id ? 'fa-solid fa-pencil' : 'fa-solid fa-plus-circle'"></i>
            <h3>{{ form.id ? 'Edit Klasifikasi' : 'Tambah Klasifikasi' }}</h3>
          </div>
          <hr />
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="kode">Kode</label>
              <input
                type="text"
                id="kode"
                v-model="form.kode"
                :class="{ 'input-error': kodeError }"
                placeholder="K1.001.1.123"
                required
              />
              <span v-if="kodeError" class="error-msg"
                ><i class="fa-solid fa-circle-exclamation"></i> {{ kodeError }}
              </span>
            </div>
            <div class="form-group">
              <label for="klasifikasi">Klasifikasi</label>
              <input
                type="text"
                id="klasifikasi"
                v-model="form.klasifikasi"
                :class="{ 'input-error': klasifikasiError }"
                placeholder="Surat Masuk"
                required
              />
              <span v-if="klasifikasiError" class="error-msg"
                ><i class="fa-solid fa-circle-exclamation"></i> {{ klasifikasiError }}</span
              >
            </div>
            <div class="form-group">
              <label for="deskripsi">Deskripsi</label>
              <textarea
                id="deskripsi"
                v-model="form.deskripsi"
                placeholder="Deskripsi (opsional)"
              ></textarea>
            </div>
            <div class="modal-actions">
              <button type="submit" class="btn-submit">
                {{ form.id ? 'Update' : 'Tambah' }}
              </button>
              <button type="button" @click="closeModal" class="btn-cancel">Batal</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import Navbar from '@/components/Navbar.vue'

const API_URL = 'http://localhost:8000/api/klasifikasi'
const list = ref([])
const showModal = ref(false)
const search = ref('')

const form = ref({
  id: null,
  kode: '',
  klasifikasi: '',
  deskripsi: '',
})

const filteredList = computed(() => {
  return list.value.filter(
    (item) =>
      item.kode.toLowerCase().includes(search.value.toLowerCase()) ||
      item.klasifikasi.toLowerCase().includes(search.value.toLowerCase()),
  )
})

function getList() {
  axios
    .get(API_URL)
    .then((res) => (list.value = res.data))
    .catch((err) => console.error('Gagal memuat data:', err))
}

async function submitForm() {
  if (!isFormValid.value) {
    Swal.fire('Validasi Gagal', 'Periksa input Anda.', 'error')
    return
  }
  try {
    if (form.value.id) {
      await axios.put(`${API_URL}/${form.value.id}`, form.value)
      Swal.fire({
        icon: 'success',
        title: 'Berhasil',
        text: 'Klasifikasi Berhasil Diubah!',
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true,
      })
    } else {
      await axios.post(API_URL, form.value)
      Swal.fire({
        icon: 'success',
        title: 'Berhasil',
        text: 'Klasifikasi Berhasil Ditambahkan!',
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true,
      })
    }
    closeModal()
    getList()
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.errors?.kode?.[0] || 'Terjadi kesalahan.', 'error')
  }
}

function editItem(item) {
  form.value = { ...item }
  showModal.value = true
}

function confirmDelete(id) {
  Swal.fire({
    title: 'Yakin?',
    text: 'Data akan dihapus permanen!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Ya, Hapus!',
    cancelButtonText: 'Batal',
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await axios.delete(`${API_URL}/${id}`)
        Swal.fire({
          icon: 'success',
          title: 'Berhasil',
          text: 'Klasifikasi Berhasil Dihapus!',
          timer: 2000,
          showConfirmButton: false,
          timerProgressBar: true,
        })
        getList()
      } catch (err) {
        Swal.fire('Gagal', 'Data gagal dihapus.', 'error')
      }
    }
  })
}

const kodeError = computed(() => {
  if (!form.value.kode.trim()) return 'Kode wajib diisi'
  return ''
})
const klasifikasiError = computed(() => {
  if (!form.value.klasifikasi.trim()) return 'Klasifikasi wajib diisi'
  return ''
})
const isFormValid = computed(() => !kodeError.value && !klasifikasiError.value)

function openModal() {
  form.value = { id: null, kode: '', klasifikasi: '', deskripsi: '' }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  form.value = { id: null, kode: '', klasifikasi: '', deskripsi: '' }
}

onMounted(getList)
</script>

<style scoped>
.master-klasifikasi {
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
  gap: 10px;
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
  background-color: var(--primary);
  color: var(--on-primary);
  text-align: center;
}

.actions-cell {
  display: flex;
  gap: 10px;
  justify-content: center;
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

.btn.reset {
  background-color: #939393;
}

.btn.reset:hover {
  background-color: #757575;
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
  width: 90%;
  max-width: 500px;
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

.form-group input,
.form-group textarea {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.form-group select.form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border 0.2s ease;
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
  transition: opacity 0.3s;
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

  .table-container table thead {
    display: none;
  }

  .table-container table,
  .table-container tbody,
  .table-container tr,
  .table-container td {
    display: block;
    width: 100%;
  }

  .table-container tr {
    margin-bottom: 15px;
    border-bottom: 2px solid #ccc;
  }

  .table-container td {
    text-align: right;
    padding: 1rem;
    padding-left: 50%;
    position: relative;
    box-sizing: border-box;
  }

  .table-container td::before {
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    font-weight: bold;
    color: #555;
  }

  .table-container td:nth-of-type(1)::before {
    content: 'Kode';
  }

  .table-container td:nth-of-type(2)::before {
    content: 'Klasifikasi';
  }

  .table-container td:nth-of-type(3)::before {
    content: 'Deskripsi';
  }

  .table-container td:nth-of-type(4)::before {
    content: 'Aksi';
  }
}
</style>
