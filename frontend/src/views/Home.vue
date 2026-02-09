<template>
  <div class="home-page">
    <header class="page-header">
      <div class="container">
        <h1>单词学习</h1>
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>

          <span class="user-info">{{ authStore.user?.username }}</span>
          <button class="btn btn-secondary btn-sm" @click="handleLogout">退出</button>
        </nav>
      </div>
    </header>
    
    <main class="container">
      <h2 class="section-title">选择单词书</h2>
      
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
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import http from '../api/http'

const router = useRouter()
const authStore = useAuthStore()

const wordbooks = ref([])
const loading = ref(true)

onMounted(async () => {
  await fetchWordbooks()
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
</script>

<style scoped>
.section-title {
  margin-bottom: 24px;
  color: #303133;
}

.wordbook-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.wordbook-card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.wordbook-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.wordbook-card h3 {
  font-size: 20px;
  color: #303133;
  margin-bottom: 8px;
}

.wordbook-card .description {
  color: #909399;
  font-size: 14px;
  margin-bottom: 16px;
  min-height: 42px;
}

.wordbook-card .meta {
  color: #606266;
  font-size: 14px;
  margin-bottom: 16px;
}

.progress-info {
  margin-bottom: 16px;
}

.progress-bar {
  height: 8px;
  background-color: #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #67c23a);
  border-radius: 4px;
  transition: width 0.3s;
}

.progress-text {
  font-size: 12px;
  color: #909399;
}

.user-info {
  color: #606266;
  margin-right: 8px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-block {
  width: 100%;
}
</style>
