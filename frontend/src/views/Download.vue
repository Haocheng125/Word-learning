<template>
  <div class="download-page">
    <header class="page-header">
      <div class="container">
        <h1>单词学习</h1>
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
            <p class="download-hint">下载完成后直接运行即可，无需安装 Python！</p>
          </div>

          <div class="instructions-card card">
            <h3>🚀 快速开始</h3>
            <div class="option-tabs">
              <button 
                class="tab-btn" 
                :class="{ active: activeOption === 'source' }"
                @click="activeOption = 'source'"
              >
                从源码运行
              </button>
              <button 
                class="tab-btn" 
                :class="{ active: activeOption === 'package' }"
                @click="activeOption = 'package'"
              >
                自行打包 EXE
              </button>
            </div>

            <div v-if="activeOption === 'source'" class="tab-content">
              <h4>📋 步骤</h4>
              <ol>
                <li>下载项目源代码（或从本地获取）</li>
                <li>进入 <strong>背单词</strong> 文件夹</li>
                <li>按住 Shift + 右键，选择"在此处打开 PowerShell"</li>
                <li>运行：<code>python main.py</code></li>
              </ol>
              <div class="tip-box">
                <strong>💡 提示：</strong>需要先安装 Python 和依赖包
                <br>
                <code>pip install PyPDF2 pdfplumber</code>
              </div>
            </div>

            <div v-if="activeOption === 'package'" class="tab-content">
              <h4>📦 方式一：使用打包助手（推荐）</h4>
              <ol>
                <li>进入 <strong>背单词</strong> 文件夹</li>
                <li>运行打包助手：<code>python 打包助手.py</code></li>
                <li>按照提示操作即可</li>
              </ol>
              <div class="tip-box">
                <strong>✨ 打包助手会自动：</strong><br>
                • 检查并安装依赖<br>
                • 执行打包命令<br>
                • 询问是否复制到后端
              </div>
              
              <h4 style="margin-top: 24px;">📦 方式二：手动打包</h4>
              <ol>
                <li>安装 PyInstaller：<code>python -m pip install pyinstaller</code></li>
                <li>进入 <strong>背单词</strong> 文件夹</li>
                <li>运行打包命令：
                  <pre><code>python -m PyInstaller --onefile --windowed --name "单词学习助手" main.py</code></pre>
                </li>
                <li>打包完成后，EXE 在 <code>dist</code> 文件夹中</li>
                <li>将 EXE 复制到：<code>backend/uploads/downloads/</code></li>
              </ol>
              <div class="tip-box">
                <strong>💡 提示：</strong>打包可能需要几分钟时间，请耐心等待
              </div>
            </div>
          </div>
        </div>

        <div class="source-section">
          <h3>� 项目文件说明</h3>
          <div class="file-list">
            <div class="file-item">
              <span class="file-icon">📄</span>
              <span class="file-name">main.py</span>
              <span class="file-desc">主程序入口</span>
            </div>
            <div class="file-item">
              <span class="file-icon">🗄️</span>
              <span class="file-name">database.py</span>
              <span class="file-desc">数据库管理</span>
            </div>
            <div class="file-item">
              <span class="file-icon">📖</span>
              <span class="file-name">pdf_reader.py</span>
              <span class="file-desc">PDF 文件解析</span>
            </div>
            <div class="file-item">
              <span class="file-icon">📦</span>
              <span class="file-name">requirements.txt</span>
              <span class="file-desc">Python 依赖列表</span>
            </div>
            <div class="file-item">
              <span class="file-icon">📝</span>
              <span class="file-name">打包指南.md</span>
              <span class="file-desc">详细的打包教程</span>
            </div>
            <div class="file-item">
              <span class="file-icon">🔧</span>
              <span class="file-name">打包助手.py</span>
              <span class="file-desc">一键打包辅助工具</span>
            </div>
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
const activeOption = ref('source')

async function handleDownload() {
  downloading.value = true
  
  try {
    window.open('/admin/download/desktop-app', '_blank')
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
  max-width: 1000px;
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
  margin-bottom: 16px;
}

.download-info p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}

.alert {
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.alert-info {
  background: #ecf5ff;
  border: 1px solid #b3d8ff;
  color: #409eff;
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

.option-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 0;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: transparent;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: #409eff;
}

.tab-btn.active {
  color: #409eff;
  border-bottom-color: #409eff;
  font-weight: 500;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tab-content h4 {
  font-size: 16px;
  color: #303133;
  margin-bottom: 12px;
}

.tab-content ol {
  margin: 0;
  padding-left: 20px;
  color: #606266;
  line-height: 2;
}

.tab-content li {
  margin-bottom: 10px;
}

.tab-content code {
  background: #f5f7fa;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  color: #409eff;
}

.tab-content pre {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 12px;
  margin: 8px 0;
  overflow-x: auto;
}

.tab-content pre code {
  background: transparent;
  color: #d4d4d4;
  padding: 0;
}

.tip-box {
  background: #f0f9eb;
  border: 1px solid #c2e7b0;
  border-radius: 6px;
  padding: 12px 16px;
  margin-top: 16px;
  color: #67c23a;
  font-size: 13px;
  line-height: 1.6;
}

.source-section {
  padding: 24px;
  background: #f5f7fa;
  border-radius: 8px;
}

.source-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #303133;
}

.file-list {
  display: grid;
  gap: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.file-icon {
  font-size: 20px;
}

.file-name {
  font-weight: 500;
  color: #303133;
  min-width: 140px;
}

.file-desc {
  color: #909399;
  font-size: 14px;
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
