<template>
  <div class="learn-page">
    <header class="page-header">
      <div class="container">
        <h1>背单词</h1>
        <nav>
          <router-link to="/">返回首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>
        </nav>
      </div>
    </header>
    
    <main class="container">
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="!currentWord" class="empty">
        <div class="empty-icon">📖</div>
        <p>暂无单词</p>
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
      </div>
      
      <div v-else class="learn-content">
        <!-- 进度条 -->
        <div class="progress-section">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: progress.progress_percentage + '%' }"
            ></div>
          </div>
          <div class="progress-text">
            {{ progress.current_index }} / {{ progress.total_words }}
          </div>
        </div>
        
        <!-- 单词卡片 -->
        <div 
          class="word-card card"
          :class="{ flipped: showTranslation }"
          @click="toggleTranslation"
        >
          <div class="word-content">
            <div class="word-english">{{ currentWord.word }}</div>
            <div class="word-phonetic" v-if="currentWord.phonetic">
              [{{ currentWord.phonetic }}]
            </div>
            <div 
              class="word-translation"
              :class="{ visible: showTranslation }"
            >
              {{ currentWord.translation }}
            </div>
            <p class="hint" v-if="!showTranslation">点击卡片查看释义</p>
          </div>
        </div>
        
        <!-- 控制按钮 -->
        <div class="controls">
          <button 
            class="btn btn-secondary"
            :disabled="progress.current_index <= 1"
            @click="handlePrevious"
          >
            ← 上一个
          </button>
          
          <button 
            class="btn"
            :class="currentWord.is_in_vocabulary ? 'btn-success' : 'btn-primary'"
            @click="handleVocabulary"
          >
            {{ currentWord.is_in_vocabulary ? '✓ 已加入生词本' : '+ 加入生词本' }}
          </button>
          
          <button 
            class="btn btn-secondary"
            :disabled="progress.current_index >= progress.total_words"
            @click="handleNext"
          >
            下一个 →
          </button>
        </div>
        
        <!-- 快捷键提示 -->
        <div class="shortcuts">
          <span>快捷键: 空格(翻转) ←→(切换) S(生词本)</span>
        </div>
      </div>
      
      <!-- 完成提示 -->
      <div v-if="showComplete" class="complete-modal">
        <div class="complete-content card">
          <div class="complete-icon">🎉</div>
          <h2>恭喜完成！</h2>
          <p>你已完成本单词书的学习</p>
          <div class="complete-actions">
            <button class="btn btn-secondary" @click="handleReset">重新开始</button>
            <router-link to="/" class="btn btn-primary">返回首页</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLearningStore } from '../stores/learning'
import http from '../api/http'

const route = useRoute()
const router = useRouter()
const learningStore = useLearningStore()

const loading = ref(true)
const showComplete = ref(false)

const currentWord = computed(() => learningStore.currentWord)
const showTranslation = computed(() => learningStore.showTranslation)
const progress = computed(() => learningStore.progress)

onMounted(async () => {
  const wordbookId = parseInt(route.params.id)
  await initLearning(wordbookId)
  
  // 添加键盘事件监听
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  learningStore.reset()
})

async function initLearning(wordbookId) {
  loading.value = true
  try {
    await learningStore.fetchProgress(wordbookId)
    await learningStore.fetchWord(wordbookId, progress.value.current_index)
  } catch (err) {
    console.error('初始化学习失败:', err)
  } finally {
    loading.value = false
  }
}

function toggleTranslation() {
  learningStore.toggleTranslation()
}

async function handleNext() {
  if (progress.value.current_index >= progress.value.total_words) {
    showComplete.value = true
    return
  }
  await learningStore.nextWord()
}

async function handlePrevious() {
  await learningStore.previousWord()
}

async function handleVocabulary() {
  if (!currentWord.value) return
  
  if (currentWord.value.is_in_vocabulary) {
    await learningStore.removeFromVocabulary(currentWord.value.id)
  } else {
    await learningStore.addToVocabulary(currentWord.value.id)
  }
}

async function handleReset() {
  const wordbookId = parseInt(route.params.id)
  await http.post(`/progress/${wordbookId}/reset`)
  showComplete.value = false
  await initLearning(wordbookId)
}

function handleKeydown(e) {
  switch (e.code) {
    case 'Space':
      e.preventDefault()
      toggleTranslation()
      break
    case 'ArrowLeft':
      handlePrevious()
      break
    case 'ArrowRight':
      handleNext()
      break
    case 'KeyS':
      handleVocabulary()
      break
  }
}
</script>

<style scoped>
.learn-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 0;
}

.progress-section {
  margin-bottom: 32px;
}

.progress-bar {
  height: 12px;
  background-color: #ebeef5;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #67c23a);
  border-radius: 6px;
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  color: #606266;
  font-size: 16px;
}

.word-card {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  margin-bottom: 32px;
}

.word-card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.word-content {
  text-align: center;
  padding: 40px;
}

.word-english {
  font-size: 48px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 16px;
}

.word-phonetic {
  font-size: 24px;
  color: #909399;
  margin-bottom: 24px;
}

.word-translation {
  font-size: 28px;
  color: #67c23a;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s;
}

.word-translation.visible {
  opacity: 1;
  transform: translateY(0);
}

.hint {
  color: #c0c4cc;
  font-size: 14px;
  margin-top: 24px;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

.controls .btn {
  min-width: 140px;
}

.shortcuts {
  text-align: center;
  color: #c0c4cc;
  font-size: 12px;
}

.complete-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.complete-content {
  text-align: center;
  padding: 48px;
  max-width: 400px;
}

.complete-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.complete-content h2 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 12px;
}

.complete-content p {
  color: #909399;
  margin-bottom: 24px;
}

.complete-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style>
