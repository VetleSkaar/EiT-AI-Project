<template>
  <div class="draft-form">
    <h2>Create New Draft</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">Title</label>
        <input
          id="title"
          v-model="draft.title"
          type="text"
          placeholder="Enter draft title"
          required
        />
      </div>

      <div class="form-group">
        <label for="content">Content</label>
        <textarea
          id="content"
          v-model="draft.content"
          rows="10"
          placeholder="Enter tender draft content..."
          required
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="isSubmitting" class="btn-primary">
          {{ isSubmitting ? 'Submitting...' : 'Submit Draft' }}
        </button>
        <button type="button" @click="resetForm" class="btn-secondary">
          Clear
        </button>
      </div>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'DraftForm',
  data() {
    return {
      draft: {
        title: '',
        content: '',
      },
      isSubmitting: false,
      error: null,
    }
  },
  methods: {
    async handleSubmit() {
      this.isSubmitting = true
      this.error = null

      try {
        const createdDraft = await api.createDraft(this.draft)
        this.$emit('draft-created', createdDraft)
        this.resetForm()
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to create draft'
      } finally {
        this.isSubmitting = false
      }
    },
    resetForm() {
      this.draft.title = ''
      this.draft.content = ''
      this.error = null
    },
  },
}
</script>

<style scoped>
.draft-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #34495e;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #42b983;
}

.form-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 10px 20px;
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

.btn-primary:hover:not(:disabled) {
  background-color: #359268;
}

.btn-primary:disabled {
  background-color: #95d5b2;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.error-message {
  margin-top: 20px;
  padding: 10px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
}
</style>
