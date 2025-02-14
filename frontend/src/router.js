import { createRouter, createWebHistory } from 'vue-router';
import UsersList from './pages/UsersList.vue';
import UserDetails from './pages/UserDetails.vue';

const routes = [
  {
    path: '/',
    redirect: '/users',
  },
  {
    path: '/users',
    name: 'UsersList',
    component: UsersList,
  },
  {
    path: '/users/:id',
    name: 'UserDetails',
    component: UserDetails,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
