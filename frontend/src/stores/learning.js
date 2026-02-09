import { defineStore } from 'pinia'
import { ref } from 'vue'
import http from '../api/http'

export const useLearningStore = defineStore('learning', () => {
  const currentWord = ref(null)
  const showTranslation = ref(false)
  const progress = ref({
    current_index: 1,
    total_words: 0,
    progress_percentage: 0
  })
  const wordbookId = ref(null)
  const loading = ref(false)
  
  async function fetchProgress(id) {
    wordbookId.value = id
    const response = await http.get(`/progress/${id}`)
    if (response.success) {
      progress.value = response.progress
    }
    return response
  }
  
  async function fetchWord(id, sequence) {
    loading.value = true
    try {
      const response = await http.get(`/words/${id}/${sequence}`)
      if (response.success) {
        currentWord.value = response.word
        showTranslation.value = false
      }
      return response
    } finally {
      loading.value = false
    }
  }
  
  async function updateProgress(currentIndex) {
    const response = await http.post(`/progress/${wordbookId.value}`, {
      current_index: currentIndex
    })
    if (response.success) {
      progress.value.current_index = currentIndex
      progress.value.progress_percentage = Math.round(
        ((currentIndex - 1) / progress.value.total_words) * 100
      )
    }
    return response
  }
  
  async function nextWord() {
    if (progress.value.current_index < progress.value.total_words) {
      const newIndex = progress.value.current_index + 1
      await fetchWord(wordbookId.value, newIndex)
      await updateProgress(newIndex)
    }
  }
  
  async function previousWord() {
    if (progress.value.current_index > 1) {
      const newIndex = progress.value.current_index - 1
      await fetchWord(wordbookId.value, newIndex)
      await updateProgress(newIndex)
    }
  }
  
  function toggleTranslation() {
    showTranslation.value = !showTranslation.value
  }
  
  async function addToVocabulary(wordId) {
    const response = await http.post('/vocabulary', { word_id: wordId })
    if (response.success && currentWord.value) {
      currentWord.value.is_in_vocabulary = true
    }
    return response
  }
  
  async function removeFromVocabulary(wordId) {
    const response = await http.delete(`/vocabulary/word/${wordId}`)
    if (response.success && currentWord.value) {
      currentWord.value.is_in_vocabulary = false
    }
    return response
  }
  
  function reset() {
    currentWord.value = null
    showTranslation.value = false
    progress.value = { current_index: 1, total_words: 0, progress_percentage: 0 }
    wordbookId.value = null
  }
  
  return {
    currentWord,
    showTranslation,
    progress,
    wordbookId,
    loading,
    fetchProgress,
    fetchWord,
    updateProgress,
    nextWord,
    previousWord,
    toggleTranslation,
    addToVocabulary,
    removeFromVocabulary,
    reset
  }
})
