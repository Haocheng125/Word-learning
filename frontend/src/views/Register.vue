<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-left">
        <div class="auth-hero">
          <div class="hero-content">
            <div class="hero-badge">🚀 欢迎加入</div>
            <h1>创建您的<span>学习账号</span></h1>
            <p>开始您的单词学习之旅，提升英语水平</p>
          </div>
        </div>
      </div>
      <div class="auth-right">
        <div class="auth-card card">
          <div class="auth-header">
            <div class="logo">
              <div class="logo-icon">📚</div>
              <span class="logo-text">单词学习</span>
            </div>
            <h2>注册</h2>
          </div>
          
          <div v-if="error" class="message message-error">{{ error }}</div>
          <div v-if="success" class="message message-success">{{ success }}</div>
          
          <form @submit.prevent="handleRegister">
            <div class="form-group">
              <label>用户名</label>
              <input 
                type="text" 
                v-model="form.username" 
                placeholder="请输入用户名"
                required
              />
            </div>
            
            <div class="form-group">
              <label>邮箱</label>
              <input 
                type="email" 
                v-model="form.email" 
                placeholder="请输入邮箱"
                required
              />
            </div>
            
            <div class="form-group">
              <label>密码</label>
              <input 
                type="password" 
                v-model="form.password" 
                placeholder="请输入密码（至少6位）"
                required
                minlength="6"
              />
            </div>
            
            <div class="form-group">
              <label>确认密码</label>
              <input 
                type="password" 
                v-model="form.confirmPassword" 
                placeholder="请再次输入密码"
                required
              />
            </div>
            
            <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </form>
          
          <p class="auth-link">
            已有账号？<router-link to="/login">立即登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleRegister() {
  error.value = ''
  success.value = ''
  
  if (form.password !== form.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  
  try {
    const response = await authStore.register(form.username, form.email, form.password)
    if (response.success) {
      success.value = '注册成功，即将跳转到登录页...'
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    }
  } catch (err) {
    error.value = err.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--dark-bg) 0%, #0d1321 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  max-width: 1000px;
  width: 100%;
  height: 80vh;
  max-height: 700px;
}

.auth-left {
  background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(0, 168, 255, 0.05) 100%);
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  position: relative;
  overflow: hidden;
}

.auth-left::before {
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

.auth-hero {
  position: relative;
  z-index: 10;
  text-align: center;
}

.hero-content {
  max-width: 400px;
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

.hero-content h1 {
  font-size: 40px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 24px;
  color: var(--text-light);
}

.hero-content h1 span {
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-content p {
  font-size: 16px;
  color: var(--text-gray);
  line-height: 1.6;
}

.auth-right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 48px;
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
  margin-bottom: 24px;
}

.logo-icon {
  font-size: 32px;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(90deg, var(--text-light), var(--accent-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-card h2 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-light);
  margin-bottom: 8px;
}

.btn-block {
  width: 100%;
  padding: 16px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 50px;
  margin-top: 24px;
}

.auth-link {
  text-align: center;
  margin-top: 24px;
  color: var(--text-gray);
  font-size: 14px;
}

.auth-link a {
  color: var(--accent-blue);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.auth-link a:hover {
  color: var(--primary-blue);
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-container {
    grid-template-columns: 1fr;
    height: auto;
    max-height: none;
  }
  
  .auth-left {
    display: none;
  }
  
  .auth-card {
    padding: 32px;
    margin: 20px;
  }
  
  .auth-header h2 {
    font-size: 24px;
  }
}
</style>
