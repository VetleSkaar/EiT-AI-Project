<template>
  <div id="app">
    <header>
      <h1>📋 Tender Draft Analysis</h1>
      <p class="subtitle">AI-powered analysis for tender submissions</p>
      <nav>
        <button 
          @click="currentView = 'form'" 
          :class="{ active: currentView === 'form' }"
          class="nav-btn"
        >
          New Draft
        </button>
        <button 
          @click="currentView = 'rubric'" 
          :class="{ active: currentView === 'rubric' }"
          class="nav-btn"
        >
          Edit Rubric
        </button>
      </nav>
    </header>

    <main>
      <DraftForm 
        v-if="currentView === 'form'" 
        @draft-created="handleDraftCreated"
      />
      
      <AnalysisResults 
        v-else-if="currentView === 'results' && currentDraftId" 
        :draft-id="currentDraftId"
        @close="currentView = 'form'"
      />
      
      <RubricEditor 
        v-else-if="currentView === 'rubric'"
        @close="currentView = 'form'"
      />
    </main>

    <footer>
      <p>
        MVP Demo | Backend: FastAPI + Hash-based Vector Search + Ollama (Mock Mode)
      </p>
    </footer>
  </div>
</template>

<script>
import DraftForm from './components/DraftForm.vue'
import AnalysisResults from './components/AnalysisResults.vue'
import RubricEditor from './components/RubricEditor.vue'

export default {
  name: 'App',
  components: {
    DraftForm,
    AnalysisResults,
    RubricEditor,
  },
  data() {
    return {
      currentView: 'form', // 'form', 'results', or 'rubric'
      currentDraftId: null,
    }
  },
  methods: {
    handleDraftCreated(draft) {
      this.currentDraftId = draft.id
      this.currentView = 'results'
    },
  },
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: white;
  padding: 30px 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 5px;
  font-size: 32px;
}

.subtitle {
  color: #7f8c8d;
  margin-bottom: 20px;
}

nav {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.nav-btn {
  padding: 10px 20px;
  border: 2px solid #42b983;
  background: white;
  color: #42b983;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: #42b983;
  color: white;
}

.nav-btn.active {
  background: #42b983;
  color: white;
}

main {
  flex: 1;
  padding: 40px 20px;
  background: white;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

footer {
  background: rgba(0, 0, 0, 0.2);
  color: white;
  text-align: center;
  padding: 15px;
  font-size: 14px;
}
</style>
