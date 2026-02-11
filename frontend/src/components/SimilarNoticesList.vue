<script setup lang="ts">
import type { Notice } from '../types';

defineProps<{
  notices: Notice[];
}>();

const formatDate = (dateStr?: string) => {
  if (!dateStr) return 'N/A';
  try {
    return new Date(dateStr).toLocaleDateString();
  } catch {
    return dateStr;
  }
};

const formatValue = (value?: number) => {
  if (!value) return 'N/A';
  return new Intl.NumberFormat('nb-NO', {
    style: 'currency',
    currency: 'NOK',
    maximumFractionDigits: 0,
  }).format(value);
};

const formatScore = (score: number) => {
  return (score * 100).toFixed(1) + '%';
};
</script>

<template>
  <div class="similar-notices">
    <h2>Similar Notices</h2>
    <div v-if="!notices || notices.length === 0" class="no-notices">
      No similar notices found.
    </div>
    <div v-else class="notices-table-wrapper">
      <table class="notices-table">
        <thead>
          <tr>
            <th>Similarity</th>
            <th>Title</th>
            <th>Buyer</th>
            <th>CPV Codes</th>
            <th>Published</th>
            <th>Deadline</th>
            <th>Estimated Value</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="notice in notices" :key="notice.notice_id">
            <td class="similarity-score">
              <span class="score-badge">{{ formatScore(notice.similarity_score) }}</span>
            </td>
            <td class="notice-title">{{ notice.title || 'N/A' }}</td>
            <td>{{ notice.buyer || 'N/A' }}</td>
            <td>
              <div class="cpv-codes">
                <span v-if="!notice.cpv_codes || notice.cpv_codes.length === 0">N/A</span>
                <span v-else v-for="(cpv, idx) in notice.cpv_codes" :key="idx" class="cpv-code">
                  {{ cpv }}
                </span>
              </div>
            </td>
            <td>{{ formatDate(notice.published_date) }}</td>
            <td>{{ formatDate(notice.deadline) }}</td>
            <td>{{ formatValue(notice.estimated_value_nok) }}</td>
            <td>
              <a v-if="notice.url" :href="notice.url" target="_blank" rel="noopener noreferrer" class="notice-link">
                View Notice
              </a>
              <span v-else>N/A</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.similar-notices {
  margin: 2rem 0;
}

.similar-notices h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.no-notices {
  padding: 2rem;
  text-align: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  color: #666;
}

.notices-table-wrapper {
  overflow-x: auto;
}

.notices-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.notices-table thead {
  background-color: #42b883;
  color: white;
}

.notices-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
}

.notices-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.notices-table tbody tr:hover {
  background-color: #f5f5f5;
}

.notices-table tbody tr:last-child td {
  border-bottom: none;
}

.similarity-score {
  text-align: center;
}

.score-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: #42b883;
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
}

.notice-title {
  font-weight: 500;
  max-width: 300px;
}

.cpv-codes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.cpv-code {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  background-color: #e3f2fd;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #1976d2;
}

.notice-link {
  color: #42b883;
  text-decoration: none;
  font-weight: 500;
}

.notice-link:hover {
  text-decoration: underline;
}
</style>
