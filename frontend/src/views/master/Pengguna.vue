<template>
  <div class="master-pengguna">
    <!-- Navbar -->
    <Navbar />

    <div class="container">
      <div class="header">
        <div class="title">
          <i class="fa-solid fa-users"></i>
          <h2>Daftar Pengguna</h2>
        </div>

        <div class="actions">
          <input v-model="search" type="text" placeholder="Cari Pengguna..." class="search-input" />
          <button class="btn tambah" @click="openModal">
            <i class="fa-solid fa-plus"></i> Tambah Pengguna
          </button>
        </div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Nama</th>
              <th>Email</th>
              <th>Role</th>
              <th>Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role.charAt(0).toUpperCase() + user.role.slice(1) }}</td>
              <td class="actions-cell">
                <button class="btn edit" @click="editUser(user)">
                  <i class="fa-solid fa-pen-to-square"></i> Edit
                </button>
                <button class="btn hapus" @click="confirmDelete(user.id)">
                  <i class="fa-solid fa-trash"></i> Hapus
                </button>
                <button class="btn reset" @click="resetPassword(user.id)">
                  <i class="fa-solid fa-arrows-rotate"></i> Reset Password
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
            <i :class="form.id ? 'fa-solid fa-user-pen' : 'fa-solid fa-user-plus'"></i>
            <h3>{{ form.id ? 'Edit Pengguna' : 'Tambah Pengguna' }}</h3>
          </div>
          <hr />
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="name">Nama</label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                :class="{ 'input-error': nameError }"
                placeholder="John Doe"
                required
              />
              <span v-if="nameError" class="error-msg"
                ><i class="fa-solid fa-circle-exclamation"></i> {{ nameError }}
              </span>
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input
                type="email"
                id="email"
                v-model="form.email"
                :class="{ 'input-error': emailError }"
                placeholder="john@example.com"
                required
              />
              <span v-if="emailError" class="error-msg"
                ><i class="fa-solid fa-circle-exclamation"></i> {{ emailError }}</span
              >
            </div>
            <div class="form-group">
              <label for="role">Role</label>
              <select
                v-model="form.role"
                id="role"
                :class="{ 'input-error': roleError }"
                class="form-select"
                required
              >
                <option value="">--- Pilih Role ---</option>
                <option value="arsiparis">Arsiparis</option>
                <option value="user">User</option>
              </select>
              <span v-if="roleError" class="error-msg">
                <i class="fa-solid fa-circle-exclamation"></i> {{ roleError }}
              </span>
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
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import Navbar from '@/components/Navbar.vue'

const API_URL = 'http://localhost:8000/api/users'
const users = ref([])
const showModal = ref(false)
const search = ref('')
const emailInUse = ref(false)

const filteredUsers = computed(() => {
  return users.value.filter(
    (user) =>
      user.name.toLowerCase().includes(search.value.toLowerCase()) ||
      user.email.toLowerCase().includes(search.value.toLowerCase()),
  )
})

const form = ref({
  id: null,
  name: '',
  email: '',
  role: '',
})

const getUsers = async () => {
  try {
    const res = await axios.get(API_URL)
    users.value = res.data
  } catch (error) {
    console.error('Gagal Memuat Data Pengguna:', error)
  }
}

const submitForm = async () => {
  if (!isFormValid.value) {
    Swal.fire('Validasi Gagal', 'Silakan Periksa Inputan Anda.', 'error')
    return
  }

  try {
    if (form.value.id) {
      await axios.put(`${API_URL}/${form.value.id}`, {
        name: form.value.name,
        email: form.value.email,
        role: form.value.role,
      })
      Swal.fire({
        icon: 'success',
        title: 'Berhasil',
        text: 'Data Pengguna Berhasil Diperbarui!',
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true,
      })
    } else {
      await axios.post(API_URL, {
        name: form.value.name,
        email: form.value.email,
        role: form.value.role,
      })
      Swal.fire({
        icon: 'success',
        title: 'Berhasil',
        text: 'Data Pengguna Berhasil Ditambahkan!',
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true,
      })
    }

    closeModal()
    getUsers()
  } catch (error) {
    if (error.response?.data?.errors?.email) {
      Swal.fire('Gagal', error.response.data.errors.email[0], 'error')
    } else {
      Swal.fire('Gagal', 'Validasi Server Gagal atau Data Tidak Lengkap.', 'error')
    }
  }
}

const editUser = (user) => {
  form.value = {
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role,
  }
  showModal.value = true
}

const confirmDelete = (id) => {
  Swal.fire({
    title: 'Yakin?',
    text: 'Pengguna Akan Dihapus Permanen!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Ya, Hapus!',
    confirmButtonColor: 'var(--primary)',
    cancelButtonText: 'Batal',
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await axios.delete(`${API_URL}/${id}`)
        Swal.fire({
          icon: 'success',
          title: 'Berhasil',
          text: 'Pengguna Berhasil Dihapus!',
          timer: 2000,
          showConfirmButton: false,
          timerProgressBar: true,
        })
        getUsers()
      } catch (error) {
        Swal.fire('Gagal', 'Gagal Menghapus Pengguna.', 'error')
      }
    }
  })
}

const resetPassword = async (userId) => {
  try {
    await axios.post(
      `http://localhost:8000/api/users/${userId}/reset-password`,
    )
    Swal.fire({
      icon: 'success',
      title: 'Berhasil',
      text: 'Password Berhasil Direset!',
      timer: 2000,
      showConfirmButton: false,
      timerProgressBar: true,
    })
  } catch (error) {
    Swal.fire('Gagal', 'Gagal me-reset password.', 'error')
  }
}

// Validasi input
const nameError = computed(() => {
  if (!form.value.name.trim()) return 'Nama wajib diisi'
  return ''
})

const emailError = computed(() => {
  const email = form.value.email.trim()
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  if (!email) return 'Email wajib diisi'
  if (!valid) return 'Format email tidak valid'
  if (emailInUse.value) return 'Email sudah digunakan'
  return ''
})

const roleError = computed(() => {
  if (!form.value.role) return 'Role wajib dipilih'
  return ''
})

const isFormValid = computed(() => {
  return !nameError.value && !emailError.value && !roleError.value
})

const openModal = () => {
  form.value = { id: null, name: '', email: '', role: '' }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  form.value = { id: null, name: '', email: '', role: '' }
  emailInUse.value = false
}

// Validasi email unik secara real-time (untuk tambah user)
watch(
  () => form.value.email,
  async (newEmail) => {
    emailInUse.value = false
    if (!newEmail || form.value.id) return
    try {
      const response = await axios.get(`${API_URL}?email=${newEmail}`)
      emailInUse.value = response.data.exists
    } catch (err) {
      console.error('Cek Email Gagal: ', err)
    }
  },
)

// Load data saat komponen dimount
onMounted(() => {
  getUsers()
})
</script>

<style scoped>
.master-pengguna {
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
  background-color: var(--neutral-600);
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
    padding-left: 50%;
    position: relative;
  }

  .table-container td::before {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    white-space: nowrap;
    font-weight: bold;
    color: #555;
  }

  .table-container td:nth-of-type(1)::before {
    content: 'Nama';
  }

  .table-container td:nth-of-type(2)::before {
    content: 'Email';
  }

  .table-container td:nth-of-type(3)::before {
    content: 'Role';
  }

  .table-container td:nth-of-type(4)::before {
    content: 'Aksi';
  }
}
</style>
