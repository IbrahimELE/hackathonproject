<template>
  <div class="content">
    <div class="form">
      <div class="form-heading">
        <h2>Register</h2>
      </div>
      <form @submit.prevent="registerUser">
        <input type="text" v-model="username" placeholder="Username" required />
        <input type="text" v-model="first_name" placeholder="First Name" required />
        <input type="text" v-model="last_name" placeholder="Last Name" required />
        <input type="text" v-model="email_address" placeholder="E-Mail" required />
        <input type="password" v-model="password" placeholder="Password" required />
        <button type="submit">Submit</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<style src="../../assets/styles/form-styles.css"></style>
  
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
  