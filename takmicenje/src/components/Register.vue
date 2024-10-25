<template>
  <div class="content">
    <div class="form">
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <input type="text" v-model="username" placeholder="Username" required />
        <input type="password" v-model="password" placeholder="Password" required />
        <button type="submit">Register</button>
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
      async registerUser() {
        try {
          const response = await axios.post('http://localhost:8000/register', {
            username: this.username,
            password: this.password
          });
          alert(response.data.message); // Show registration success message
        } catch (error) {
          this.errorMessage = error.response.data.detail || "Registration failed";
        }
      }
    }
  };
  </script>
  