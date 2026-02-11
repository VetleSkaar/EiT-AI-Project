<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createDraft } from '../api';

const router = useRouter();

const title = ref('');
const description = ref('');
const cpv = ref('');
const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
  // Validate
  if (!title.value.trim() || !description.value.trim()) {
    error.value = 'Title and description are required';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const draft = await createDraft({
      title: title.value.trim(),
      description: description.value.trim(),
      cpv: cpv.value.trim() || undefined,
    });

    // Navigate to the draft results page
    router.push(`/draft/${draft.id}`);
  } catch (err: any) {
    console.error('Error creating draft:', err);
    error.value = err.response?.data?.detail || 'Failed to create draft. Please try again.';
  } finally {
    loading.value = false;
  }
};

const clearForm = () => {
  title.value = '';
  description.value = '';
  cpv.value = '';
  error.value = '';
};
</script>

<template>
  <div class="draft-form-page">
    <div class="container">
      <h1>Create Procurement Draft</h1>
      <p class="subtitle">Enter the details of your procurement draft to find similar notices and get AI-powered analysis.</p>

      <form @submit.prevent="handleSubmit" class="draft-form">
        <div class="form-group">
          <label for="title">Title *</label>
          <input
            id="title"
            v-model="title"
            type="text"
            placeholder="Enter procurement title"
            :disabled="loading"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description *</label>
          <textarea
            id="description"
            v-model="description"
            rows="8"
            placeholder="Enter detailed description of the procurement"
            :disabled="loading"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="cpv">CPV Code (Optional)</label>
          <input
            id="cpv"
            v-model="cpv"
            type="text"
            placeholder="Enter CPV code (e.g., 45000000-7)"
            :disabled="loading"
          />
          <small class="help-text">Common Procurement Vocabulary code for categorization</small>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="loading" class="btn btn-primary">
            <span v-if="loading">Creating Draft...</span>
            <span v-else>Create Draft & Find Similar Notices</span>
          </button>
          <button type="button" @click="clearForm" :disabled="loading" class="btn btn-secondary">
            Clear Form
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.draft-form-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.draft-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #42b883;
}

.form-group input:disabled,
.form-group textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 150px;
}

.help-text {
  color: #888;
  font-size: 0.875rem;
}

.error-message {
  padding: 1rem;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 6px;
  color: #c33;
  font-weight: 500;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #42b883;
  color: white;
  flex: 1;
}

.btn-primary:hover:not(:disabled) {
  background-color: #35a372;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(66, 184, 131, 0.3);
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e0e0e0;
}

@media (max-width: 768px) {
  .draft-form-page {
    padding: 1rem;
  }

  .container {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
