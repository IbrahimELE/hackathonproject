// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Login from '../components/users/Login.vue';
import Register from '../components/users/Register.vue';

const routes = [
  { path: '/', component: Home, name: 'Home' },
  { path: '/login', component: Login, name: 'Login' },
  { path: '/register', component: Register, name: 'Register' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
