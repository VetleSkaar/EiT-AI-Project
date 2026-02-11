<script setup lang="ts">
import type { AnalysisResult } from '../types';

defineProps<{
  analysis: AnalysisResult;
}>();

const getDecisionClass = (decision: string) => {
  const lower = decision.toLowerCase();
  if (lower.includes('approve')) return 'decision-approve';
  if (lower.includes('reject')) return 'decision-reject';
  if (lower.includes('revise')) return 'decision-revise';
  return 'decision-default';
};

const formatConfidence = (confidence: number) => {
  return (confidence * 100).toFixed(1) + '%';
};
</script>

<template>
  <div class="recommendation-card">
    <h2>AI Analysis & Recommendation</h2>
    
    <!-- Overlap Summary -->
    <div class="section">
      <h3>Overlap Summary</h3>
      <p>{{ analysis.overlap_summary || 'No summary available' }}</p>
    </div>

    <!-- Qualitative Analysis -->
    <div class="section qualitative-analysis" v-if="analysis.qualitative_analysis">
      <h3>Qualitative Analysis</h3>
      
      <div class="analysis-item">
        <h4>🛡️ Risk Management</h4>
        <p>{{ analysis.qualitative_analysis.risk_management || 'Not analyzed' }}</p>
      </div>

      <div class="analysis-item">
        <h4>🌱 Sustainability & Social Values</h4>
        <p>{{ analysis.qualitative_analysis.sustainability_social_values || 'Not analyzed' }}</p>
      </div>

      <div class="analysis-item">
        <h4>🔍 Transparency & Fair Competition</h4>
        <p>{{ analysis.qualitative_analysis.transparency_fair_competition || 'Not analyzed' }}</p>
      </div>

      <div class="analysis-item">
        <h4>💡 Innovation & Forward Thinking</h4>
        <p>{{ analysis.qualitative_analysis.innovation_forward_thinking || 'Not analyzed' }}</p>
      </div>
    </div>

    <!-- Recommendation -->
    <div class="section recommendation" v-if="analysis.recommendation">
      <h3>Recommendation</h3>
      <div class="recommendation-content">
        <div :class="['decision-badge', getDecisionClass(analysis.recommendation.decision)]">
          {{ analysis.recommendation.decision || 'N/A' }}
        </div>
        <div class="rationale">
          <strong>Rationale:</strong>
          <p>{{ analysis.recommendation.rationale || 'No rationale provided' }}</p>
        </div>
      </div>
    </div>

    <!-- Confidence & Caveats -->
    <div class="section meta-info">
      <div class="confidence">
        <h4>Confidence Score</h4>
        <div class="confidence-bar-container">
          <div class="confidence-bar" :style="{ width: formatConfidence(analysis.confidence) }"></div>
        </div>
        <span class="confidence-value">{{ formatConfidence(analysis.confidence) }}</span>
      </div>

      <div class="caveats">
        <h4>⚠️ Caveats & Limitations</h4>
        <p>{{ analysis.caveats || 'No caveats provided' }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recommendation-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 2rem 0;
}

.recommendation-card h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  border-bottom: 2px solid #42b883;
  padding-bottom: 0.5rem;
}

.section {
  margin-bottom: 2rem;
}

.section h3 {
  color: #42b883;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.section h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.section p {
  line-height: 1.6;
  color: #555;
}

.qualitative-analysis {
  background-color: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #42b883;
}

.analysis-item {
  margin-bottom: 1.5rem;
}

.analysis-item:last-child {
  margin-bottom: 0;
}

.analysis-item h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.recommendation {
  border-left: 4px solid #ffa726;
  padding-left: 1.5rem;
}

.recommendation-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.decision-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  width: fit-content;
}

.decision-approve {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.decision-revise {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.decision-reject {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.decision-default {
  background-color: #e2e3e5;
  color: #383d41;
  border: 1px solid #d6d8db;
}

.rationale {
  margin-top: 0.5rem;
}

.rationale p {
  margin-top: 0.5rem;
}

.meta-info {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  background-color: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
}

.confidence h4 {
  margin-bottom: 1rem;
}

.confidence-bar-container {
  width: 100%;
  height: 24px;
  background-color: #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.confidence-bar {
  height: 100%;
  background: linear-gradient(90deg, #42b883, #35495e);
  transition: width 0.3s ease;
}

.confidence-value {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.125rem;
}

.caveats {
  border-left: 3px solid #ffa726;
  padding-left: 1rem;
}

.caveats p {
  color: #666;
  font-style: italic;
}

@media (max-width: 768px) {
  .meta-info {
    grid-template-columns: 1fr;
  }
}
</style>
