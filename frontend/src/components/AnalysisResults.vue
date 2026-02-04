<template>
  <div class="analysis-results">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Analyzing draft...</p>
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else-if="analysis" class="results">
      <h2>Analysis Results</h2>
      
      <div class="draft-info">
        <h3>{{ draft?.title }}</h3>
        <p class="draft-content">{{ draft?.content }}</p>
      </div>

      <div class="analysis-grid">
        <div class="analysis-card" :class="`level-${analysis.risk.level.toLowerCase()}`">
          <h4>Risk</h4>
          <div class="score">{{ (analysis.risk.score * 100).toFixed(0) }}%</div>
          <div class="level">{{ analysis.risk.level }}</div>
          <p>{{ analysis.risk.description }}</p>
        </div>

        <div class="analysis-card" :class="`level-${analysis.sustainability.level.toLowerCase()}`">
          <h4>Sustainability</h4>
          <div class="score">{{ (analysis.sustainability.score * 100).toFixed(0) }}%</div>
          <div class="level">{{ analysis.sustainability.level }}</div>
          <p>{{ analysis.sustainability.description }}</p>
        </div>

        <div class="analysis-card" :class="`level-${analysis.competition.level.toLowerCase()}`">
          <h4>Competition</h4>
          <div class="score">{{ (analysis.competition.score * 100).toFixed(0) }}%</div>
          <div class="level">{{ analysis.competition.level }}</div>
          <p>{{ analysis.competition.description }}</p>
        </div>

        <div class="analysis-card" :class="`level-${analysis.innovation.level.toLowerCase()}`">
          <h4>Innovation</h4>
          <div class="score">{{ (analysis.innovation.score * 100).toFixed(0) }}%</div>
          <div class="level">{{ analysis.innovation.level }}</div>
          <p>{{ analysis.innovation.description }}</p>
        </div>
      </div>

      <div class="recommendation">
        <h3>Recommendation</h3>
        <p>{{ analysis.recommendation }}</p>
      </div>

      <button @click="$emit('close')" class="btn-primary">Analyze Another Draft</button>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'AnalysisResults',
  props: {
    draftId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      analysis: null,
      draft: null,
      loading: true,
      error: null,
    }
  },
  async mounted() {
    await this.loadAnalysis()
  },
  methods: {
    async loadAnalysis() {
      this.loading = true
      this.error = null

      try {
        // Load draft details
        this.draft = await api.getDraft(this.draftId)
        
        // Trigger analysis
        this.analysis = await api.analyzeDraft(this.draftId)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to analyze draft'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.analysis-results {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #42b983;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.results h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.draft-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.draft-info h3 {
  margin-top: 0;
  color: #2c3e50;
}

.draft-content {
  color: #666;
  line-height: 1.6;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.analysis-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: transform 0.2s;
}

.analysis-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.analysis-card h4 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 18px;
}

.score {
  font-size: 36px;
  font-weight: bold;
  margin: 10px 0;
}

.level {
  font-size: 16px;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 10px;
}

.level-high .score,
.level-high .level {
  color: #e74c3c;
}

.level-high .level {
  background-color: #fee;
}

.level-medium .score,
.level-medium .level {
  color: #f39c12;
}

.level-medium .level {
  background-color: #ffeaa7;
}

.level-low .score,
.level-low .level {
  color: #27ae60;
}

.level-low .level {
  background-color: #d5f4e6;
}

.analysis-card p {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  text-align: left;
}

.recommendation {
  background: #e3f2fd;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.recommendation h3 {
  margin-top: 0;
  color: #1976d2;
}

.recommendation p {
  color: #666;
  line-height: 1.6;
}

button {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover {
  background-color: #359268;
}

.error-message {
  margin: 20px auto;
  padding: 20px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
  max-width: 600px;
  text-align: center;
}
</style>
