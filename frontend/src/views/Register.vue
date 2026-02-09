<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h2>注册</h2>
      
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
