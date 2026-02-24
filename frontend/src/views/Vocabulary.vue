<template>
  <div class="vocabulary-page">
    <!-- 导航栏 -->
    <header class="page-header" :class="{ scrolled: isScrolled }">
      <div class="container">
        <div class="logo">
          <div class="logo-icon">📝</div>
          <span class="logo-text">我的生词本</span>
        </div>
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>
          <router-link to="/database-format">数据库格式</router-link>
        </nav>
      </div>
    </header>
    
    <main class="container">
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="vocabulary.length === 0" class="empty">
        <div class="empty-icon">📝</div>
        <p>生词本为空</p>
        <p>在学习时点击"加入生词本"来添加生词</p>
        <router-link to="/" class="btn btn-primary">去学习</router-link>
      </div>
      
      <div v-else>
        <div class="section-header">
          <div class="section-tag">生词本</div>
          <h2>我的生词</h2>
          <p>共 {{ total }} 个生词</p>
        </div>
        
        <div class="vocabulary-list">
          <div 
            v-for="item in vocabulary" 
            :key="item.id" 
            class="vocabulary-item card"
          >
            <div class="word-info">
              <div class="word-english">{{ item.word?.word }}</div>
              <div class="word-phonetic" v-if="item.word?.phonetic">
                [{{ item.word.phonetic }}]
              </div>
              <div class="word-translation">{{ item.word?.translation }}</div>
              <div class="word-meta">
                <span v-if="item.wordbook_name">来自：{{ item.wordbook_name }}</span>
                <span>添加于：{{ formatDate(item.added_at) }}</span>
              </div>
            </div>
            <div class="word-actions">
              <button 
                class="btn btn-danger btn-sm"
                @click="handleRemove(item.id)"
              >
                移除
              </button>
            </div>
          </div>
        </div>
        
        <!-- 分页 -->
        <div v-if="total > limit" class="pagination">
          <button 
            class="btn btn-secondary btn-sm"
            :disabled="page <= 1"
            @click="changePage(page - 1)"
          >
            上一页
          </button>
          <span class="page-info">{{ page }} / {{ totalPages }}</span>
          <button 
            class="btn btn-secondary btn-sm"
            :disabled="page >= totalPages"
            @click="changePage(page + 1)"
          >
            下一页
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import http from '../api/http'

const vocabulary = ref([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const limit = ref(20)
const isScrolled = ref(false)

const totalPages = computed(() => Math.ceil(total.value / limit.value))

onMounted(async () => {
  await fetchVocabulary()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

async function fetchVocabulary() {
  loading.value = true
  try {
    const response = await http.get('/vocabulary', {
      params: { page: page.value, limit: limit.value }
    })
    if (response.success) {
      vocabulary.value = response.vocabulary
      total.value = response.total
    }
  } catch (err) {
    console.error('获取生词本失败:', err)
  } finally {
    loading.value = false
  }
}

async function handleRemove(id) {
  if (!confirm('确定要从生词本中移除吗？')) return
  
  try {
    const response = await http.delete(`/vocabulary/${id}`)
    if (response.success) {
      await fetchVocabulary()
    }
  } catch (err) {
    console.error('移除失败:', err)
  }
}

function changePage(newPage) {
  page.value = newPage
  fetchVocabulary()
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}
</script>

<style scoped>
.vocabulary-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--dark-bg) 0%, #0d1321 100%);
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

.section-header {
  text-align: center;
  margin-bottom: 60px;
  padding: 40px 20px;
}

.section-tag {
  display: inline-block;
  padding: 8px 20px;
  background: rgba(0, 102, 255, 0.15);
  border-radius: 50px;
  font-size: 14px;
  color: var(--accent-blue);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.section-header h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--text-light);
}

.section-header p {
  font-size: 16px;
  color: var(--text-gray);
}

.vocabulary-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.vocabulary-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 32px;
  transition: all 0.4s ease;
}

.vocabulary-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 102, 255, 0.15);
  border-color: rgba(0, 102, 255, 0.3);
}

.word-info {
  flex: 1;
  margin-right: 24px;
}

.word-english {
  font-size: 28px;
  font-weight: bold;
  color: var(--text-light);
  margin-bottom: 8px;
  text-shadow: 0 2px 10px rgba(0, 102, 255, 0.3);
}

.word-phonetic {
  font-size: 18px;
  color: var(--accent-blue);
  margin-bottom: 12px;
  font-style: italic;
}

.word-translation {
  font-size: 20px;
  color: #00b894;
  margin-bottom: 16px;
  line-height: 1.4;
}

.word-meta {
  font-size: 14px;
  color: var(--text-gray);
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.word-actions {
  display: flex;
  align-items: flex-start;
  padding-top: 8px;
}

.btn-sm {
  padding: 8px 20px;
  font-size: 14px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.btn-sm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 48px;
  padding: 20px;
  background: var(--card-bg);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.page-info {
  color: var(--text-gray);
  font-size: 16px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .vocabulary-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .word-actions {
    margin-top: 20px;
    align-self: flex-end;
  }
  
  .word-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .section-header h2 {
    font-size: 24px;
  }
}
</style>
