<template>
  <div id="app">
    <!-- Navigation bar with links to each route -->
    <nav>
      <router-link to="/">Home</router-link>

      <div class="options">
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </div>
    </nav>

    <!-- Display content based on the current route -->
    <router-view />
  </div>
</template>

<style src="./assets/styles/main-app-styles.css"></style>

<script>

  export default {
    name: "App",
    data() {
      return {
        isDarkMode: "false",
        loggedIn: "false"
      };
    },
    methods: {
      toggleMode() {
        this.isDarkMode = !this.isDarkMode;
      }
    }
  };
</script>

