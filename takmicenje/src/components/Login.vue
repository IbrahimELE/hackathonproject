<template>
  <div class="content">
    <div class="form">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <input type="text" v-model="username" placeholder="Username" required />
        <input type="password" v-model="password" placeholder="Password" required />
        <button type="submit">Login</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<style src="../assets/styles/form-styles.css"></style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://localhost:8000/login', {
          username: this.username,
          password: this.password
        });
        alert(response.data.message); // Show login success message
      } catch (error) {
        this.errorMessage = error.response.data.detail || "Login failed";
      }
    }
  }
};
</script>