<template>
  <div class="download-page">
    <header class="page-header">
      <div class="container">
        <h1>单词学习</h1>
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/vocabulary">生词本</router-link>
          <router-link to="/download">桌面版下载</router-link>

          <span class="user-info">{{ authStore.user?.username }}</span>
          <button class="btn btn-secondary btn-sm" @click="handleLogout">退出</button>
        </nav>
      </div>
    </header>
    
    <main class="container">
      <div class="download-section">
        <div class="hero">
          <div class="hero-icon">💻</div>
          <h2>单词学习助手 - 桌面版</h2>
          <p class="subtitle">离线使用，随时随地背单词</p>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h3>PDF导入</h3>
            <p>支持从PDF文件批量导入单词</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📖</div>
            <h3>卡片学习</h3>
            <p>直观的卡片式学习界面</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">✅</div>
            <h3>进度追踪</h3>
            <p>记录学习进度，智能复习</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔌</div>
            <h3>离线使用</h3>
            <p>无需网络，本地存储数据</p>
          </div>
        </div>

        <div class="download-area">
          <div class="download-card card">
            <div class="download-header">
              <h3>Windows 版本</h3>
              <span class="version-tag">v1.0.0</span>
            </div>
            <div class="download-info">
              <p><strong>系统要求：</strong>Windows 7/10/11</p>
              <p><strong>文件大小：</strong>约 50MB</p>
            </div>
            <button 
              class="btn btn-primary btn-large btn-block"
              @click="handleDownload"
              :disabled="downloading"
            >
              {{ downloading ? '准备中...' : '📥 下载单词学习助手.exe' }}
            </button>
            <p class="download-hint">如未自动下载，请检查浏览器设置</p>
          </div>

          <div class="instructions-card card">
            <h3>📋 安装说明</h3>
            <ol>
              <li>点击上方按钮下载安装包</li>
              <li>双击运行 <strong>单词学习助手.exe</strong></li>
              <li>程序无需安装，直接运行即可使用</li>
              <li>首次运行会在同级目录创建数据库文件</li>
            </ol>
          </div>
        </div>

        <div class="source-section">
          <h3>🔧 开发者选项</h3>
          <p>如果你想从源码运行或自行打包：</p>
          <div class="code-block">
            <pre><code># 克隆项目
cd 背单词

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py

# 或打包成 exe
build.bat</code></pre>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import http from '../api/http'

const router = useRouter()
const authStore = useAuthStore()
const downloading = ref(false)

async function handleDownload() {
  downloading.value = true
  
  try {
    const apiUrl = http.defaults.baseURL || ''
    const downloadUrl = `${apiUrl}/admin/download/desktop-app`
    
    window.open(downloadUrl, '_blank')
  } catch (error) {
    alert('下载失败，请稍后重试')
    console.error('下载错误:', error)
  } finally {
    downloading.value = false
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.download-section {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 0;
}

.hero {
  text-align: center;
  margin-bottom: 48px;
}

.hero-icon {
  font-size: 72px;
  margin-bottom: 16px;
}

.hero h2 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 18px;
  color: #909399;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.feature-card {
  text-align: center;
  padding: 24px;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
}

.feature-card p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.download-area {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 48px;
}

.download-card,
.instructions-card {
  padding: 24px;
}

.download-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.download-header h3 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.version-tag {
  background: linear-gradient(90deg, #409eff, #67c23a);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.download-info {
  margin-bottom: 24px;
}

.download-info p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}

.btn-large {
  padding: 16px 24px;
  font-size: 16px;
}

.download-hint {
  text-align: center;
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
}

.instructions-card h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  color: #303133;
}

.instructions-card ol {
  margin: 0;
  padding-left: 20px;
  color: #606266;
  line-height: 2;
}

.instructions-card li {
  margin-bottom: 8px;
}

.source-section {
  padding: 24px;
  background: #f5f7fa;
  border-radius: 8px;
}

.source-section h3 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 18px;
  color: #303133;
}

.source-section p {
  color: #606266;
  margin-bottom: 16px;
}

.code-block {
  background: #1e1e1e;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
}

.code-block pre {
  margin: 0;
}

.code-block code {
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-block {
  width: 100%;
}

.user-info {
  color: #606266;
  margin-right: 8px;
}
</style>
