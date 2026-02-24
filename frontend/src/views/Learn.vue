<template>
  <div class="learn-page">
    <!-- 导航栏 -->
    <header class="page-header" :class="{ scrolled: isScrolled }">
      <div class="container">
        <div class="logo">
          <div class="logo-icon">📚</div>
          <span class="logo-text">背单词</span>
        </div>
        <nav>
          <router-link to="/">返回首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>
          <router-link to="/database-format">数据库格式</router-link>
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
const isScrolled = ref(false)

const currentWord = computed(() => learningStore.currentWord)
const showTranslation = computed(() => learningStore.showTranslation)
const progress = computed(() => learningStore.progress)

onMounted(async () => {
  const wordbookId = parseInt(route.params.id)
  await initLearning(wordbookId)
  
  // 添加键盘事件监听
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('scroll', handleScroll)
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
  if (progress.value.current_index >= progress.total_words) {
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

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}
</script>

<style scoped>
.learn-page {
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

.learn-content {
  max-width: 700px;
  margin: 0 auto;
  padding: 80px 20px;
}

.progress-section {
  margin-bottom: 48px;
}

.progress-bar {
  height: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
  border-radius: 6px;
  transition: width 0.6s ease;
  box-shadow: 0 0 10px rgba(0, 102, 255, 0.5);
}

.progress-text {
  text-align: center;
  color: var(--text-gray);
  font-size: 18px;
  font-weight: 500;
}

.word-card {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.4s ease;
  margin-bottom: 48px;
  position: relative;
  overflow: hidden;
}

.word-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, rgba(0, 102, 255, 0.05) 0%, transparent 70%);
  transition: all 0.4s ease;
}

.word-card:hover {
  transform: scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 102, 255, 0.2);
  border-color: rgba(0, 102, 255, 0.5);
}

.word-content {
  text-align: center;
  padding: 60px 40px;
  position: relative;
  z-index: 10;
}

.word-english {
  font-size: 64px;
  font-weight: bold;
  color: var(--text-light);
  margin-bottom: 24px;
  text-shadow: 0 2px 10px rgba(0, 102, 255, 0.3);
}

.word-phonetic {
  font-size: 32px;
  color: var(--accent-blue);
  margin-bottom: 32px;
  font-style: italic;
}

.word-translation {
  font-size: 36px;
  color: #00b894;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  line-height: 1.4;
}

.word-translation.visible {
  opacity: 1;
  transform: translateY(0);
}

.hint {
  color: var(--text-gray);
  font-size: 16px;
  margin-top: 32px;
  font-style: italic;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 32px;
}

.controls .btn {
  min-width: 160px;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.controls .btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 102, 255, 0.4);
}

.shortcuts {
  text-align: center;
  color: var(--text-gray);
  font-size: 14px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-top: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.complete-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 14, 23, 0.9);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.complete-content {
  text-align: center;
  padding: 60px;
  max-width: 480px;
  position: relative;
  overflow: hidden;
}

.complete-content::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 102, 255, 0.1) 0%, transparent 70%);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
  100% { transform: scale(1); opacity: 0.5; }
}

.complete-icon {
  font-size: 80px;
  margin-bottom: 24px;
  position: relative;
  z-index: 10;
}

.complete-content h2 {
  font-size: 32px;
  color: var(--text-light);
  margin-bottom: 16px;
  position: relative;
  z-index: 10;
  background: linear-gradient(90deg, var(--text-light), var(--accent-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.complete-content p {
  color: var(--text-gray);
  margin-bottom: 32px;
  font-size: 18px;
  position: relative;
  z-index: 10;
}

.complete-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  position: relative;
  z-index: 10;
}

.complete-actions .btn {
  padding: 16px 32px;
  font-size: 16px;
  border-radius: 50px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .learn-content {
    padding: 60px 16px;
  }
  
  .word-english {
    font-size: 48px;
  }
  
  .word-phonetic {
    font-size: 24px;
  }
  
  .word-translation {
    font-size: 28px;
  }
  
  .controls {
    flex-direction: column;
    align-items: center;
  }
  
  .controls .btn {
    width: 100%;
    max-width: 300px;
  }
  
  .complete-content {
    padding: 48px 24px;
    margin: 0 16px;
  }
}
</style>
