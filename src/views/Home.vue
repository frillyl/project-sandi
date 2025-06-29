<template>
  <div class="home">
    <!-- Navbar Section -->
    <nav class="navbar">
      <div class="navbar-container">
        <div class="logo">SANDI</div>
        <button class="menu-toggle" @click="toggleMenu">
          <span :class="{ open: menuOpen }"></span>
          <span :class="{ open: menuOpen }"></span>
          <span :class="{ open: menuOpen }"></span>
        </button>
        <ul :class="['nav-links', { open: menuOpen }]">
          <li><a href="#about" @click="closeMenu">Tentang</a></li>
          <li><a href="#goals" @click="closeMenu">Tujuan</a></li>
          <li><a href="#features" @click="closeMenu">Fitur</a></li>
          <li><a href="#tech" @click="closeMenu">Teknologi</a></li>
        </ul>
      </div>
    </nav>
    <!-- Hero Section -->
    <section class="hero" data-aos="fade-up" data-aos-duration="1000">
      <div class="hero-pattern"></div>
      <div class="hero-overlay"></div>
      <div class="hero-wave">
        <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
          <path
            class="wave wave-1"
            fill="#5e35b1"
            d="M0,224L60,197.3C120,171,240,117,360,101.3C480,85,600,107,720,112C840,117,960,107,1080,128C1200,149,1320,203,1380,229.3L1440,256L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
          />
          <path
            class="wave wave-2"
            fill="#7e57c2"
            fill-opacity="0.7"
            d="M0,288L80,272C160,256,320,224,480,192C640,160,800,128,960,117.3C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"
          />
          <path
            class="wave wave-3"
            fill="#d1c4e9"
            fill-opacity="0.5"
            d="M0,320L60,293.3C120,267,240,213,360,202.7C480,192,600,224,720,213.3C840,203,960,149,1080,144C1200,139,1320,181,1380,202.7L1440,224L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
          />
          <path
            class="wave wave-4"
            fill="#FFFFFF"
            fill-opacity="1"
            d="M0,280 C360,200 1080,360 1440,280 L1440,320 L0,320Z"
          />
        </svg>
      </div>
      <div class="hero-content">
        <h1>SANDI</h1>
        <p>Solusi Cerdas Untuk Arsip Digital</p>
        <a href="/demo/login" class="hero-button"><i class="fa-solid fa-rocket"></i>Demo</a>
      </div>
    </section>

    <!-- About Section -->
    <section class="about" id="about" data-aos="fade-right" data-aos-duration="1000">
      <div class="about-container">
        <div class="about-text">
          <h2>Tentang</h2>
          <p>
            SANDI merupakan aplikasi arsip digital berbasis web yang dilengkapi dengan fitur
            kecerdasan buatan (AI) untuk membantu pengguna dalam melakukan peringkasan isi dokumen
            serta rekomendasi dokumen serupa. Aplikasi ini dikembangkan dengan pendekatan arsitektur
            microservices dan memanfaatkan layanan cloud untuk efisiensi pengelolaan infrastruktur
            dan skalabilitas.
          </p>
        </div>
        <div class="about-image">
          <img :src="AboutIllustration" alt="About Icon" />
        </div>
      </div>
    </section>
    <div class="about-wave">
      <svg viewBox="0 0 1440 320" class="w-full h-auto" preserveAspectRatio="none">
        <path
          fill="#FFFFFF"
          d="M0,288L80,272C160,256,320,224,480,192C640,160,800,128,960,117.3C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"
        />
        <path
          fill="#d1c4e9"
          fill-opacity="0.7"
          d="M0,224L60,197.3C120,171,240,117,360,101.3C480,85,600,107,720,112C840,117,960,107,1080,128C1200,149,1320,203,1380,229.3L1440,256L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
        />
        <path
          fill="#b39ddb"
          fill-opacity="0.5"
          d="M0,320L60,293.3C120,267,240,213,360,202.7C480,192,600,224,720,213.3C840,203,960,149,1080,144C1200,139,1320,181,1380,202.7L1440,224L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
        />
        <path
          fill="#ede7f6"
          fill-opacity="1"
          d="M0,280 C360,200 1080,360 1440,280 L1440,320 L0,320Z"
        />
      </svg>
    </div>

    <!-- Goals & Features Section -->
    <!-- Goals -->
    <section class="goals-features">
      <div class="goals-features-container">
        <div class="goals" id="goals" data-aos="fade-right" data-aos-duration="1000">
          <h2><i class="fa-solid fa-bullseye"></i> Tujuan</h2>
          <ul>
            <li data-aos="fade-up" data-aos-delay="100">
              <i class="fa-solid fa-check-circle"></i> Membangun aplikasi arsip digital yang dapat
              mengunggah, menyimpan, dan mengelola dokumen digital.
            </li>
            <li data-aos="fade-up" data-aos-delay="200">
              <i class="fa-solid fa-check-circle"></i> Mengimplementasikan fitur peringkasan
              otomatis menggunakan algoritma TextRank.
            </li>
            <li data-aos="fade-up" data-aos-delay="300">
              <i class="fa-solid fa-check-circle"></i> Menyediakan rekomendasi dokumen serupa
              berbasis perhitungan kemiripan teks menggunakan TF-IDF dan Cosine Similarity.
            </li>
            <li data-aos="fade-up" data-aos-delay="400">
              <i class="fa-solid fa-check-circle"></i> Menerapkan arsitektur microservice untuk
              pemisahan tanggung jawab layanan dan kemudahan pengembangan atau pemeliharaan.
            </li>
            <li data-aos="fade-up" data-aos-delay="500">
              <i class="fa-solid fa-check-circle"></i> Menerapkan deployment ke cloud menggunakan
              Google Cloud Platform agar sistem dapat diakses secara online.
            </li>
          </ul>
        </div>
        <div class="features" id="features" data-aos="fade-left" data-aos-duration="1000">
          <h2><i class="fa-solid fa-star"></i> Fitur</h2>
          <ul>
            <li data-aos="fade-up" data-aos-delay="100">
              <i class="fa-solid fa-check-circle"></i> Manajemen arsip digital yang mencakup unggah
              dokumen, ekstraksi teks secara otomatis, serta penyimpanan dan pencarian.
            </li>
            <li data-aos="fade-up" data-aos-delay="200">
              <i class="fa-solid fa-check-circle"></i> Peringkasan dokumen secara otomatis dengan
              metode ekstraktif menggunakan algoritma TextRank.
            </li>
            <li data-aos="fade-up" data-aos-delay="300">
              <i class="fa-solid fa-check-circle"></i> Rekomendasi dokumen serupa berdasarkan
              analisis kemiripan isi menggunakan pendekatan TF-IDF dan Cosine Similarity.
            </li>
          </ul>
        </div>
      </div>
    </section>
    <div class="goals-features-wave">
      <svg viewBox="0 0 1440 320" class="w-full h-auto" preserveAspectRatio="none">
        <path
          fill="#5e35b1"
          d="M0,224L60,197.3C120,171,240,117,360,101.3C480,85,600,107,720,112C840,117,960,107,1080,128C1200,149,1320,203,1380,229.3L1440,256L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
        />
        <path
          fill="#7e57c2"
          fill-opacity="0.7"
          d="M0,288L80,272C160,256,320,224,480,192C640,160,800,128,960,117.3C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"
        />
        <path
          fill="#d1c4e9"
          fill-opacity="0.5"
          d="M0,320L60,293.3C120,267,240,213,360,202.7C480,192,600,224,720,213.3C840,203,960,149,1080,144C1200,139,1320,181,1380,202.7L1440,224L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
        />
        <path
          fill="#FFFFFF"
          fill-opacity="1"
          d="M0,280 C360,200 1080,360 1440,280 L1440,320 L0,320Z"
        />
      </svg>
    </div>

    <!-- Technology Section -->
    <section class="tech" id="tech">
      <div class="tech-content">
        <h2 data-aos="fade-up" data-aos-duration="800">Teknologi</h2>
        <div class="tech-container">
          <div class="block" data-aos="zoom-in-up" data-aos-delay="100" data-aos-duration="600">
            <h3><i class="fas fa-laptop-code"></i> Frontend</h3>
            <p>
              Frontend dikembangkan dengan Vue.js 3 serta menggunakan Axios dan Vue Router untuk
              komunikasi data dan navigasi. Antarmuka ini digunakan untuk mengunggah dokumen,
              menampilkan ringkasan, dan rekomendasi.
            </p>
          </div>
          <div class="block" data-aos="zoom-in-up" data-aos-delay="200" data-aos-duration="600">
            <h3><i class="fas fa-server"></i> Backend</h3>
            <p>
              Backend menggunakan Laravel untuk menyediakan REST API, autentikasi, pengelolaan
              arsip, dan komunikasi dengan layanan AI melalui HTTP.
            </p>
          </div>
          <div class="block" data-aos="zoom-in-up" data-aos-delay="300" data-aos-duration="600">
            <h3><i class="fas fa-cogs"></i> Microservices</h3>
            <p>
              Microservices dibangun dengan FastAPI, mencakup layanan OCR (Tesseract), summarization
              (TextRank/Sumy), dan recommendation (TF-IDF + Cosine Similarity dengan scikit-learn).
            </p>
          </div>
          <div class="block" data-aos="zoom-in-up" data-aos-delay="400" data-aos-duration="600">
            <h3><i class="fas fa-database"></i> Database</h3>
            <p>
              Database menggunakan MySQL yang dikelola melalui Cloud SQL untuk menyimpan data
              pengguna, metadata dokumen, hasil ringkasan, dan rekomendasi.
            </p>
          </div>
          <div class="block" data-aos="zoom-in-up" data-aos-delay="500" data-aos-duration="600">
            <h3><i class="fas fa-cloud-upload-alt"></i> Deployment</h3>
            <p>
              Deployment dilakukan di Google Cloud Platform menggunakan Cloud Run untuk menjalankan
              layanan ter-container, Cloud SQL untuk database, dan Cloud Storage untuk penyimpanan
              dokumen.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer Section -->
    <footer class="footer" data-aos="fade-up" data-aos-duration="800">
      <div class="footer-content">
        <p>&copy; 2025 <strong>SANDI</strong> - Solusi Cerdas Untuk Arsip Digital</p>
        <p>Hak Cipta Dilindungi Undang-Undang.</p>
      </div>
    </footer>

    <button
      v-show="showBackToTop"
      class="back-to-top"
      @click="scrollToTop"
      aria-label="Back to top"
    >
      <i class="fa-solid fa-arrow-up"></i>
    </button>
  </div>
</template>

<script setup>
import AboutIllustration from '@/assets/images/about.svg'
import { ref, onMounted, onBeforeUnmount, onUnmounted } from 'vue'

const menuOpen = ref(false)
const showBackToTop = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

const handleClickOutside = (event) => {
  const nav = document.querySelector('.navbar')
  if (menuOpen.value && !nav.contains(event.target)) {
    closeMenu()
  }
}

const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.home {
  min-height: 100%;
  /* background: linear-gradient(to bottom, var(--primary) 50%, var(--secondary) 75%, #ffffff 100%); */
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: var(--primary);
  color: var(--on-primary);
  padding: 1rem 2rem;
  display: flex;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-weight: bold;
  font-size: 1.5rem;
  letter-spacing: 0.1em;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
}

.nav-links li a {
  color: var(--on-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-links li a:hover {
  color: var(--secondary);
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--on-primary);
  cursor: pointer;
}

.hero {
  position: relative;
  min-height: 100vh;
  padding: 4rem 1rem;
  background: linear-gradient(to bottom, var(--primary) 50%, var(--secondary) 75%, #ffffff 100%);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--on-primary);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(#ffffff 1.5px, transparent 1.5px);
  background-size: calc(1vw + 10px) calc(1vw + 10px);
  opacity: 0.25;
  z-index: 0;
  pointer-events: none;
  animation: pulse 25s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  filter: blur(0.3px);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.hero-wave {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: auto;
  z-index: 2;
  overflow: hidden;
}

.hero-wave svg {
  display: block;
  width: 200%;
  max-height: 500px;
  transform: translateX(-25%);
}

.wave {
  animation: waveMotion 10s linear infinite;
  transform: translateX(0);
}

.wave-1 {
  animation-duration: 12s;
}

.wave-2 {
  animation-duration: 18s;
  animation-direction: reverse;
}

.wave-3 {
  animation-duration: 25s;
}

.wave-4 {
  animation-duration: 15s;
  animation-direction: reverse;
}

.hero-content {
  position: relative;
  z-index: 3;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hero-content h1,
.hero-content p {
  opacity: 0;
  animation: fadeSlideUp 1s ease-out forwards;
}

.hero-content h1 {
  animation-delay: 0.3s;
}

.hero-content p {
  animation-delay: 0.6s;
}

.hero h1 {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1rem;
  letter-spacing: 0.1em;
}

.hero p {
  font-size: 1.5rem;
  font-weight: 400;
}

.hero-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 0.75rem 1rem;
  background-color: var(--secondary);
  color: var(--on-secondary);
  font-weight: 600;
  font-size: 1.1rem;
  border: none;
  border-radius: 9999px;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  animation: fadeSlideUp 1s ease-out forwards;
  animation-delay: 1s;
  opacity: 0;
}

.hero-button:hover {
  background-color: var(--primary);
  color: var(--on-primary);
  transform: scale(1.1);
}

.about {
  padding: 4rem 2rem;
  background-color: #ffffff;
}

.about-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: auto;
  flex-wrap: wrap;
  gap: 2rem;
}

.about-text {
  flex: 1 1 400px;
}

.about-text h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--primary);
}

.about-text p {
  font-size: 1.1rem;
  line-height: 1.6;
}

.about-image {
  flex: 1 1 400px;
  text-align: center;
}

.about-image img {
  max-width: 100%;
  height: auto;
}

.about-wave {
  position: relative;
  width: 100%;
  height: auto;
  z-index: 1;
  overflow: hidden;
  background: #ffffff;
}

.about-wave svg {
  display: block;
  width: 100%;
  height: auto;
}

.goals-features {
  padding: 80px 40px;
  background: #ede7f6;
}

.goals-features-container {
  max-width: 1200px;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  justify-content: space-between;
}

.goals,
.features {
  background: white;
  border-radius: 20px;
  padding: 30px 40px;
  flex: 1 1 400px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.goals:hover,
.features:hover {
  transform: translateY(-5px);
}

.goals h2,
.features h2 {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.goals ul,
.features ul {
  list-style: none;
  padding: 0;
}

.goals li,
.features li {
  margin-bottom: 15px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  line-height: 1.6;
}

.goals li i,
.features li i {
  color: var(--primary);
  margin-right: 10px;
}

.goals-features-wave {
  position: relative;
  width: 100%;
  height: auto;
  z-index: 1;
  overflow: hidden;
  background: #ede7f6;
}

.goals-features-wave svg {
  display: block;
  width: 100%;
  height: auto;
}

.tech {
  display: flex;
  padding: 60px 20px 0;
}

.tech-content {
  max-width: 1200px;
  margin: auto;
  text-align: center;
  padding-bottom: 80px;
}

.tech h2 {
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  color: var(--primary);
}

.tech-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.tech .block {
  background: #ffffff;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  flex: 1 1 300px;
  max-width: 350px;
  transition: transform 0.3s ease;
  text-align: left;
}

.tech .block:hover {
  transform: translateY(-8px);
}

.tech .block h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.4rem;
  color: var(--primary);
  margin-bottom: 1rem;
}

.tech .block p {
  font-size: 1rem;
  color: #333333;
  line-height: 1.6;
}

.footer {
  background-color: var(--primary);
  color: var(--on-primary);
  text-align: center;
  padding: 2rem 1rem;
  font-size: 0.9rem;
  position: relative;
}

.footer-content p {
  margin: 0.5rem 0;
}

.back-to-top {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #5e35b1;
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  font-size: 20px;
  cursor: pointer;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: opacity 0.3s ease-in-out;
}

.back-to-top:hover {
  background-color: #4527a0;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero svg {
    max-height: 400px;
  }

  .hero h1 {
    font-size: 3rem;
  }

  .hero p {
    font-size: 1.25rem;
  }
}

@media (max-width: 640px) {
  .hero svg {
    max-height: 300px;
  }

  .hero h1 {
    font-size: 2.25rem;
  }

  .hero p {
    font-size: 1rem;
  }
}

@media (max-width: 768px) {
  .menu-toggle {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 3px;
    width: 30px;
    height: 30px;
    background: none;
    border: none;
    cursor: pointer;
    z-index: 20;
  }

  .menu-toggle span {
    display: block;
    height: 3px;
    background-color: var(--on-primary);
    border-radius: 2px;
    transition: all 0.3s ease;
  }

  .menu-toggle span:nth-child(1) {
    width: 100%;
  }

  .menu-toggle span:nth-child(2) {
    width: 100%;
  }

  .menu-toggle span:nth-child(3) {
    width: 100%;
  }

  .menu-toggle span.open:nth-child(1) {
    transform: rotate(45deg) translateY(8px);
  }

  .menu-toggle span.open:nth-child(2) {
    opacity: 0;
  }

  .menu-toggle span.open:nth-child(3) {
    transform: rotate(-45deg) translateY(-8px);
  }

  .nav-links {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: var(--primary);
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 2rem;
    transform: translateY(-20px);
    opacity: 0;
    pointer-events: none;
    transition:
      transform 0.3s ease,
      opacity 0.3s ease;
    display: flex;
    z-index: 30;
  }

  .nav-links.open {
    display: flex;
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }

  .nav-links li {
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
  }

  .nav-links.open li {
    opacity: 1;
    transform: translateY(0);
  }

  .nav-links.open li:nth-child(1) {
    transition-delay: 0.1s;
  }

  .nav-links.open li:nth-child(2) {
    transition-delay: 0.2s;
  }

  .nav-links.open li:nth-child(3) {
    transition-delay: 0.3s;
  }

  .nav-links.open li:nth-child(4) {
    transition-delay: 0.4s;
  }

  .hero-button {
    width: 50%;
    font-size: 1rem;
    padding: 0.5rem 1rem;
    gap: 5px;
  }

  .about-container {
    flex-direction: column;
    text-align: center;
  }

  .about-text h2 {
    font-size: 1.75rem;
  }

  .about-text p {
    font-size: 1rem;
  }

  .about-text,
  .about-image {
    flex: 1 1 auto;
  }

  .about-image {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }

  .about-image img {
    max-width: 100%;
    height: auto;
  }

  .goals,
  .features {
    flex: 1 1 100%;
  }

  .goals-features-container {
    flex-direction: column;
    gap: 2rem;
  }
}

/* Animations */
@keyframes fadeSlideUp {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY();
  }
}

@keyframes waveMotion {
  0% {
    transform: translateX(0) translateY(0);
  }

  50% {
    transform: translateX(-50px) translateY(5px);
  }

  100% {
    transform: translateX(-100px) translateY(0);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.1;
    transform: scale(1);
  }

  50% {
    opacity: 0.5;
    transform: scale(1.5);
  }
}
</style>
