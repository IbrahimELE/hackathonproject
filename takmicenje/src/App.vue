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

<script>
export default {
  name: "App",
};
</script>

<style scoped>
/* Styling for the App component */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  margin: 20px;
  display: flex;
  justify-content: space-between;
}

div.options > * {
  margin-LEFT: 20px;
}

nav a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}

nav a.router-link-active {
  color: #35495e;
}
</style>
