<template>
  <div class="rubric-editor">
    <h3>Analysis Rubric</h3>
    <p class="description">
      Customize the evaluation criteria for draft analysis. These settings affect how drafts are scored.
    </p>

    <div class="rubric-items">
      <div v-for="item in rubricItems" :key="item.id" class="rubric-item">
        <div class="rubric-header">
          <h4>{{ item.name }}</h4>
          <span class="weight">Weight: {{ item.weight }}%</span>
        </div>
        
        <div class="rubric-content">
          <label>
            Description:
            <textarea
              v-model="item.description"
              rows="3"
              @change="saveRubric"
            ></textarea>
          </label>

          <label>
            Weight (%):
            <input
              type="range"
              v-model.number="item.weight"
              min="0"
              max="100"
              @change="saveRubric"
            />
          </label>

          <div class="scoring-levels">
            <label>
              <strong>Low (0-33%):</strong>
              <input
                type="text"
                v-model="item.lowCriteria"
                placeholder="Criteria for low score"
                @change="saveRubric"
              />
            </label>
            
            <label>
              <strong>Medium (34-66%):</strong>
              <input
                type="text"
                v-model="item.mediumCriteria"
                placeholder="Criteria for medium score"
                @change="saveRubric"
              />
            </label>
            
            <label>
              <strong>High (67-100%):</strong>
              <input
                type="text"
                v-model="item.highCriteria"
                placeholder="Criteria for high score"
                @change="saveRubric"
              />
            </label>
          </div>
        </div>
      </div>
    </div>

    <div class="rubric-actions">
      <button @click="resetToDefaults" class="btn-secondary">
        Reset to Defaults
      </button>
      <button @click="$emit('close')" class="btn-primary">
        Close
      </button>
    </div>

    <div v-if="saved" class="save-message">
      ✓ Rubric saved successfully
    </div>
  </div>
</template>

<script>
export default {
  name: 'RubricEditor',
  data() {
    return {
      saved: false,
      rubricItems: this.loadRubric(),
    }
  },
  methods: {
    loadRubric() {
      const stored = localStorage.getItem('analysisRubric')
      if (stored) {
        try {
          return JSON.parse(stored)
        } catch {
          return this.getDefaultRubric()
        }
      }
      return this.getDefaultRubric()
    },
    getDefaultRubric() {
      return [
        {
          id: 'risk',
          name: 'Risk Assessment',
          weight: 25,
          description: 'Evaluate potential risks and challenges in the tender draft',
          lowCriteria: 'Minimal risks identified, standard procedures',
          mediumCriteria: 'Some risks present, manageable with planning',
          highCriteria: 'Significant risks, requires extensive mitigation',
        },
        {
          id: 'sustainability',
          name: 'Sustainability',
          weight: 25,
          description: 'Assess environmental and long-term sustainability aspects',
          lowCriteria: 'Basic sustainability considerations',
          mediumCriteria: 'Good sustainability practices incorporated',
          highCriteria: 'Excellent sustainability, eco-friendly focus',
        },
        {
          id: 'competition',
          name: 'Competition Level',
          weight: 25,
          description: 'Evaluate market competition and similar tenders',
          lowCriteria: 'Low competition, unique opportunity',
          mediumCriteria: 'Moderate competition, some similar tenders',
          highCriteria: 'High competition, many similar opportunities',
        },
        {
          id: 'innovation',
          name: 'Innovation Potential',
          weight: 25,
          description: 'Assess technological and process innovation opportunities',
          lowCriteria: 'Standard approach, minimal innovation',
          mediumCriteria: 'Some innovative elements present',
          highCriteria: 'Highly innovative, cutting-edge approach',
        },
      ]
    },
    saveRubric() {
      localStorage.setItem('analysisRubric', JSON.stringify(this.rubricItems))
      this.saved = true
      setTimeout(() => {
        this.saved = false
      }, 2000)
    },
    resetToDefaults() {
      if (confirm('Reset rubric to default values?')) {
        this.rubricItems = this.getDefaultRubric()
        this.saveRubric()
      }
    },
  },
}
</script>

<style scoped>
.rubric-editor {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.description {
  color: #666;
  margin-bottom: 30px;
}

.rubric-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}

.rubric-item {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
}

.rubric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #42b983;
}

.rubric-header h4 {
  margin: 0;
  color: #2c3e50;
}

.weight {
  font-weight: bold;
  color: #42b983;
}

.rubric-content label {
  display: block;
  margin-bottom: 15px;
  font-weight: bold;
  color: #34495e;
}

textarea,
input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  margin-top: 5px;
}

input[type="range"] {
  width: 100%;
  margin-top: 5px;
}

.scoring-levels {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
}

.scoring-levels label {
  margin-bottom: 10px;
  font-weight: normal;
}

.scoring-levels strong {
  display: block;
  margin-bottom: 5px;
  color: #2c3e50;
}

.rubric-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
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

.btn-primary:hover {
  background-color: #359268;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.save-message {
  text-align: center;
  margin-top: 15px;
  padding: 10px;
  background-color: #d5f4e6;
  border-radius: 4px;
  color: #27ae60;
  font-weight: bold;
}
</style>
