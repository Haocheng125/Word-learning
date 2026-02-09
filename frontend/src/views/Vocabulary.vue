<template>
  <div class="vocabulary-page">
    <header class="page-header">
      <div class="container">
        <h1>我的生词本</h1>
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>
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
        <div class="stats">
          共 {{ total }} 个生词
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
import { ref, computed, onMounted } from 'vue'
import http from '../api/http'

const vocabulary = ref([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const limit = ref(20)

const totalPages = computed(() => Math.ceil(total.value / limit.value))

onMounted(async () => {
  await fetchVocabulary()
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
</script>

<style scoped>
.stats {
  margin-bottom: 24px;
  color: #606266;
}

.vocabulary-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.vocabulary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
}

.word-info {
  flex: 1;
}

.word-english {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.word-phonetic {
  font-size: 16px;
  color: #909399;
  margin-bottom: 8px;
}

.word-translation {
  font-size: 18px;
  color: #67c23a;
  margin-bottom: 8px;
}

.word-meta {
  font-size: 12px;
  color: #c0c4cc;
  display: flex;
  gap: 16px;
}

.word-actions {
  margin-left: 16px;
}

.btn-sm {
  padding: 6px 16px;
  font-size: 12px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
}

.page-info {
  color: #606266;
}
</style>
