import { createRouter, createWebHistory } from 'vue-router';
import DraftForm from './pages/DraftForm.vue';
import DraftResults from './pages/DraftResults.vue';

const routes = [
  {
    path: '/',
    name: 'DraftForm',
    component: DraftForm,
  },
  {
    path: '/draft/:id',
    name: 'DraftResults',
    component: DraftResults,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
