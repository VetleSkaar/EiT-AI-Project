<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { analyzeDraft } from '../api';
import type { Notice, AnalysisResult } from '../types';
import SimilarNoticesList from '../components/SimilarNoticesList.vue';
import RecommendationCard from '../components/RecommendationCard.vue';

const route = useRoute();
const router = useRouter();

const draftId = ref<number>(0);
const loading = ref(false);
const analyzing = ref(false);
const error = ref('');

const retrievedNotices = ref<Notice[]>([]);
const analysis = ref<AnalysisResult | null>(null);

onMounted(() => {
  const id = route.params.id;
  if (typeof id === 'string') {
    draftId.value = parseInt(id, 10);
  } else if (Array.isArray(id)) {
    draftId.value = parseInt(id[0], 10);
  }

  if (isNaN(draftId.value) || draftId.value <= 0) {
    error.value = 'Invalid draft ID';
    return;
  }
});

const handleAnalyze = async () => {
  analyzing.value = true;
  error.value = '';

  try {
    const response = await analyzeDraft(draftId.value);
    retrievedNotices.value = response.retrieved_notices || [];
    analysis.value = response.analysis || null;
  } catch (err: any) {
    console.error('Error analyzing draft:', err);
    error.value = err.response?.data?.detail || 'Failed to analyze draft. Please try again.';
  } finally {
    analyzing.value = false;
  }
};

const goBack = () => {
  router.push('/');
};
</script>

<template>
  <div class="draft-results-page">
    <div class="container">
      <div class="header">
        <button @click="goBack" class="btn-back">← Back to Create Draft</button>
        <h1>Draft Analysis</h1>
        <p class="draft-id">Draft ID: {{ draftId }}</p>
      </div>

      <div v-if="error && !analyzing" class="error-message">
        {{ error }}
      </div>

      <!-- Analysis Trigger -->
      <div v-if="!analysis && !analyzing" class="analyze-section">
        <p class="info-text">Click the button below to analyze this draft and find similar notices.</p>
        <button @click="handleAnalyze" :disabled="analyzing || loading" class="btn btn-analyze">
          <span v-if="analyzing">Analyzing...</span>
          <span v-else>🔍 Analyze Draft</span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="analyzing" class="loading-section">
        <div class="spinner"></div>
        <p>Analyzing draft and finding similar notices...</p>
        <small>This may take a moment while we search through the database and generate AI insights.</small>
      </div>

      <!-- Results -->
      <div v-if="analysis && !analyzing" class="results">
        <!-- Similar Notices -->
        <SimilarNoticesList :notices="retrievedNotices" />

        <!-- Analysis & Recommendation -->
        <RecommendationCard :analysis="analysis" />

        <!-- Re-analyze Button -->
        <div class="actions">
          <button @click="handleAnalyze" :disabled="analyzing" class="btn btn-secondary">
            Re-analyze Draft
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.draft-results-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-back {
  background: none;
  border: none;
  color: #42b883;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
  display: inline-block;
}

.btn-back:hover {
  text-decoration: underline;
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.draft-id {
  color: #666;
  font-size: 0.95rem;
}

.error-message {
  padding: 1rem;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
  font-weight: 500;
  margin-bottom: 2rem;
}

.analyze-section {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-text {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.loading-section {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e0e0e0;
  border-top-color: #42b883;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-section p {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.loading-section small {
  color: #888;
}

.results {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.actions {
  text-align: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-analyze {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.125rem;
  padding: 1rem 2.5rem;
}

.btn-analyze:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e0e0e0;
}

@media (max-width: 768px) {
  .draft-results-page {
    padding: 1rem;
  }

  .header {
    padding: 1.5rem;
  }

  .analyze-section,
  .loading-section {
    padding: 2rem 1rem;
  }
}
</style>
