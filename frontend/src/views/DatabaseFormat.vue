<template>
  <div class="database-format-page">
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

          <span class="user-info">{{ authStore.user?.username }}</span>
          <button class="btn btn-secondary btn-sm" @click="handleLogout">退出</button>
        </nav>
      </div>
    </header>
    
    <main class="container">
      <div class="section-header">
        <div class="section-tag">数据格式</div>
        <h2>数据库读取格式</h2>
        <p>了解系统支持的文件格式</p>
      </div>

      <div class="formats-container">
        <!-- PDF 格式 -->
        <div class="format-card card">
          <div class="format-header">
            <div class="format-icon">📄</div>
            <h3>PDF 文件格式</h3>
          </div>
          <div class="format-content">
            <p class="format-description">系统支持解析包含单词、音标和释义的 PDF 文件。</p>
            
            <div class="format-structure">
              <h4>支持的结构</h4>
              <div class="structure-item">
                <div class="structure-label">3列结构</div>
                <div class="structure-sample">
                  <pre>序号 | 单词 [音标] | 释义</pre>
                </div>
              </div>
              <div class="structure-item">
                <div class="structure-label">6列结构</div>
                <div class="structure-sample">
                  <pre>序号 | 单词 [音标] | 释义 | 序号 | 单词 [音标] | 释义</pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Excel 格式 -->
        <div class="format-card card">
          <div class="format-header">
            <div class="format-icon">📊</div>
            <h3>Excel 文件格式</h3>
          </div>
          <div class="format-content">
            <p class="format-description">系统支持解析 Excel 文件中的单词数据。</p>
            
            <div class="format-structure">
              <h4>支持的结构</h4>
              <div class="structure-item">
                <div class="structure-label">3列结构</div>
                <div class="structure-sample">
                  <pre>序号 | 单词 [音标] | 释义</pre>
                </div>
              </div>
              <div class="structure-item">
                <div class="structure-label">2列结构</div>
                <div class="structure-sample">
                  <pre>单词 [音标] | 释义</pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 雅思数据库说明 -->
        <div class="format-card card">
          <div class="format-header">
            <div class="format-icon">📚</div>
            <h3>雅思数据库</h3>
          </div>
          <div class="format-content">
            <p class="format-description">系统内置的雅思词汇数据库，包含常用雅思考试词汇。</p>
            <div class="format-features">
              <ul>
                <li>包含核心雅思词汇</li>
                <li>按难度等级划分</li>
                <li>每个单词提供准确的音标和释义</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isScrolled = ref(false)

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.database-format-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--dark-bg) 0%, #0d1321 100%);
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
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

.formats-container {
  max-width: 800px;
  margin: 0 auto 60px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.format-card {
  transition: all 0.4s ease;
}

.format-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 102, 255, 0.15);
  border-color: rgba(0, 102, 255, 0.3);
}

.format-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.format-icon {
  font-size: 24px;
}

.format-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-light);
  margin: 0;
}

.format-description {
  font-size: 16px;
  color: var(--text-gray);
  margin-bottom: 24px;
  line-height: 1.6;
}

.format-structure {
  margin-bottom: 24px;
}

.format-structure h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 16px;
}

.structure-item {
  margin-bottom: 16px;
}

.structure-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--accent-blue);
  margin-bottom: 8px;
}

.structure-sample {
  background: rgba(0, 102, 255, 0.1);
  border-radius: 8px;
  padding: 12px;
  border-left: 4px solid var(--primary-blue);
}

.structure-sample pre {
  margin: 0;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  color: var(--text-gray);
  white-space: pre-wrap;
}

.format-features ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.format-features li {
  font-size: 14px;
  color: var(--text-gray);
  margin-bottom: 10px;
  padding-left: 20px;
  position: relative;
}

.format-features li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--accent-blue);
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .section-header h2 {
    font-size: 24px;
  }
  
  .format-header h3 {
    font-size: 16px;
  }
}
</style>