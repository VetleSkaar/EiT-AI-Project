<script setup>
import { ref, onMounted } from 'vue'
import HelloWorld from './components/HelloWorld.vue'

const apiMessage = ref('')
const apiStatus = ref('')
const error = ref('')

const fetchApiData = async () => {
  try {
    // Test root endpoint
    const rootResponse = await fetch('http://localhost:8000/')
    const rootData = await rootResponse.json()
    apiMessage.value = rootData.message
    
    // Test health endpoint
    const healthResponse = await fetch('http://localhost:8000/health')
    const healthData = await healthResponse.json()
    apiStatus.value = healthData.status
    
    error.value = ''
  } catch (err) {
    error.value = `Error connecting to API: ${err.message}`
    console.error('API Error:', err)
  }
}

onMounted(() => {
  fetchApiData()
})
</script>

<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
  
  <div class="api-test">
    <h2>API Connection Test</h2>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else class="success">
      <p><strong>API Message:</strong> {{ apiMessage }}</p>
      <p><strong>API Status:</strong> {{ apiStatus }}</p>
      <p class="success-text">✓ CORS is working correctly!</p>
    </div>
    <button @click="fetchApiData">Refresh API Data</button>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.api-test {
  margin: 2em auto;
  padding: 1em;
  max-width: 600px;
  border: 2px solid #646cff;
  border-radius: 8px;
  background-color: #1a1a1a;
}

.api-test h2 {
  color: #646cff;
  margin-bottom: 1em;
}

.success {
  color: #42b883;
}

.success-text {
  font-weight: bold;
  margin-top: 1em;
}

.error {
  color: #ff6b6b;
  font-weight: bold;
}

button {
  margin-top: 1em;
  padding: 0.6em 1.2em;
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

button:hover {
  background-color: #535bf2;
}
</style>
