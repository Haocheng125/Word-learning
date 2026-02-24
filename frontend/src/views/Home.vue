<template>
  <div class="home-page">
    <!-- 导航栏 -->
    <header class="page-header" :class="{ scrolled: isScrolled }">
      <div class="container">
        <div class="logo">
          <div class="logo-icon">📚</div>
          <span class="logo-text">单词学习</span>
        </div>
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>
          <router-link to="/database-format">数据库格式</router-link>
          <router-link to="/download">桌面版下载</router-link>

          <span class="user-info">{{ authStore.user?.username }}</span>
          <button class="btn btn-secondary btn-sm" @click="handleLogout">退出</button>
        </nav>
      </div>
    </header>
    
    <!-- Hero 区域 -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">🚀 高效单词学习平台</div>
        <h1>轻松掌握<span>英语单词</span></h1>
        <p>基于科学记忆方法，为您提供个性化的单词学习体验，让背单词变得简单有趣</p>
      </div>
    </section>
    
    <!-- 单词书区域 -->
    <section class="wordbooks-section">
      <div class="container">
        <div class="section-header">
          <div class="section-tag">选择单词书</div>
          <h2>开始您的学习之旅</h2>
          <p>从以下单词书中选择一本，开始您的英语学习之旅</p>
        </div>
        
        <div v-if="loading" class="loading">加载中...</div>
        
        <div v-else-if="wordbooks.length === 0" class="empty">
          <div class="empty-icon">📚</div>
          <p>暂无单词书，请联系管理员上传词库</p>
        </div>
        
        <div v-else class="wordbook-grid">
          <div 
            v-for="book in wordbooks" 
            :key="book.id" 
            class="wordbook-card card"
          >
            <div class="book-icon">📖</div>
            <h3>{{ book.name }}</h3>
            <p class="description">{{ book.description || '暂无描述' }}</p>
            <div class="meta">
              <span>共 {{ book.word_count }} 个单词</span>
            </div>
            
            <div v-if="book.user_progress" class="progress-info">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: getProgressPercent(book) + '%' }"
                ></div>
              </div>
              <span class="progress-text">
                已学 {{ book.user_progress.current_index - 1 }} / {{ book.word_count }}
              </span>
            </div>
            
            <button 
              class="btn btn-primary btn-block"
              @click="startLearning(book.id)"
            >
              {{ book.user_progress ? '继续学习' : '开始学习' }}
            </button>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 学习统计 -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">📚</div>
            <div class="stat-number">{{ totalBooks }}</div>
            <div class="stat-label">可用单词书</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📝</div>
            <div class="stat-number">{{ totalWords }}</div>
            <div class="stat-label">总单词数</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">🎯</div>
            <div class="stat-number">{{ learnedWords }}</div>
            <div class="stat-label">已学单词</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import http from '../api/http'

const router = useRouter()
const authStore = useAuthStore()

const wordbooks = ref([])
const loading = ref(true)
const isScrolled = ref(false)

onMounted(async () => {
  await fetchWordbooks()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

async function fetchWordbooks() {
  loading.value = true
  try {
    const response = await http.get('/wordbooks')
    if (response.success) {
      wordbooks.value = response.wordbooks
    }
  } catch (err) {
    console.error('获取单词书失败:', err)
  } finally {
    loading.value = false
  }
}

function getProgressPercent(book) {
  if (!book.user_progress || book.word_count === 0) return 0
  return Math.round(((book.user_progress.current_index - 1) / book.word_count) * 100)
}

function startLearning(bookId) {
  router.push(`/learn/${bookId}`)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}

// 计算属性
const totalBooks = computed(() => wordbooks.value.length)

const totalWords = computed(() => {
  return wordbooks.value.reduce((total, book) => total + book.word_count, 0)
})

const learnedWords = computed(() => {
  return wordbooks.value.reduce((total, book) => {
    if (book.user_progress) {
      return total + (book.user_progress.current_index - 1)
    }
    return total
  }, 0)
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(90deg, var(--text-light), var(--accent-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 120px 5%;
  background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(10, 14, 23, 0.9) 100%);
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(0, 168, 255, 0.5), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(0, 102, 255, 0.4), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(2px 2px at 130px 80px, rgba(0, 212, 255, 0.4), transparent);
  background-size: 200px 100px;
  animation: sparkle 8s linear infinite;
}

@keyframes sparkle {
  0% { transform: translateY(0); }
  100% { transform: translateY(-100px); }
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 800px;
}

.hero-badge {
  display: inline-block;
  padding: 10px 24px;
  background: rgba(0, 102, 255, 0.2);
  border: 1px solid rgba(0, 168, 255, 0.3);
  border-radius: 50px;
  font-size: 14px;
  color: var(--accent-blue);
  margin-bottom: 32px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.hero h1 {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 24px;
  color: var(--text-light);
}

.hero h1 span {
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  font-size: 18px;
  color: var(--text-gray);
  margin-bottom: 40px;
  line-height: 1.6;
}

.wordbooks-section {
  padding: 120px 0;
  background: var(--dark-bg);
}

.section-header {
  text-align: center;
  margin-bottom: 80px;
}

.section-tag {
  display: inline-block;
  padding: 8px 20px;
  background: rgba(0, 102, 255, 0.15);
  border-radius: 50px;
  font-size: 14px;
  color: var(--accent-blue);
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.section-header h2 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--text-light);
}

.section-header p {
  font-size: 16px;
  color: var(--text-gray);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.wordbook-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 32px;
  margin-bottom: 60px;
}

.wordbook-card {
  position: relative;
  overflow: hidden;
}

.wordbook-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.wordbook-card:hover::before {
  transform: scaleX(1);
}

.book-icon {
  font-size: 32px;
  margin-bottom: 20px;
  color: var(--accent-blue);
}

.wordbook-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 12px;
}

.wordbook-card .description {
  color: var(--text-gray);
  font-size: 14px;
  margin-bottom: 20px;
  line-height: 1.6;
  min-height: 48px;
}

.wordbook-card .meta {
  color: var(--text-gray);
  font-size: 14px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.progress-info {
  margin-bottom: 24px;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 14px;
  color: var(--text-gray);
}

.stats-section {
  padding: 80px 0;
  background: linear-gradient(180deg, var(--dark-bg) 0%, #0d1321 100%);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  text-align: center;
}

.stat-item {
  padding: 32px;
  background: var(--card-bg);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.4s ease;
}

.stat-item:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 102, 255, 0.3);
  box-shadow: 0 10px 40px rgba(0, 102, 255, 0.15);
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 16px;
  color: var(--accent-blue);
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 14px;
  color: var(--text-gray);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 36px;
  }
  
  .hero p {
    font-size: 16px;
  }
  
  .section-header h2 {
    font-size: 28px;
  }
  
  .wordbook-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  
  .wordbooks-section {
    padding: 80px 0;
  }
  
  .stats-section {
    padding: 60px 0;
  }
}
</style>
