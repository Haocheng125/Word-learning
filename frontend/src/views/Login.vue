<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h2>登录</h2>
      
      <div v-if="error" class="message message-error">{{ error }}</div>
      
      <form @submit.prevent="handleLogin">
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
            placeholder="请输入密码"
            required
          />
        </div>
        
        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <p class="auth-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
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
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    const response = await authStore.login(form.email, form.password)
    if (response.success) {
      router.push('/')
    }
  } catch (err) {
    error.value = err.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  margin: 20px;
}

.auth-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}

.btn-block {
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  color: #909399;
}

.auth-link a {
  color: #409eff;
  text-decoration: none;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>
