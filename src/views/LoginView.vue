<template>
  <main class="px-8 py-6 bg-gray-100">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-left col-span-2">
        <div class="p-12 bg-white border border-gray-200 rounded-lg">
          <h1 class="mb-6 text-2xl">Log in</h1>

          <p class="mb-6 text-gray-500">
            Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
            dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit
            mate. Lorem ipsum dolor sit mate.
          </p>

          <p class="font-bold">
            Don't have an account?
            <RouterLink :to="{name: 'register'}" class="underline">Click here</RouterLink> to create one!
          </p>
        </div>
      </div>

      <div class="main-center col-span-2 space-y-4">
        <div class="p-12 bg-white border border-gray-200 rounded-lg">
          <form class="space-y-6" :submit.prevent="submitForm()">
            <div>
              <label>E-mail</label><br />
              <input
                type="email"
                v-model="form.email"
                placeholder="Your e-mail address"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
              />
            </div>

            <div>
              <label>Password</label><br />
              <input
                type="password"
                v-model="form.password"
                placeholder="Your password"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
              />
            </div>

            <div class="flex justify-center items-center">
              <button class="py-4 px-6 bg-orange-600 text-white rounded-lg transition-all hover:bg-orange-500">
                Log in
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { useUserStore } from '../stores/user'
import axios from 'axios'

export default {
  setup() {
    const userStore = useUserStore()

    return {
      userStore
    }
  },

  data() {
    return {
      form: {
        email_address: '',
        password: '',
      }
    }
  },

  methods: {
    async submitForm() {
      this.errors = []

      if (this.form.email_address === '') {
        this.errors.push('Your e-mail is missing')
      }

      if (this.form.password === '') {
        this.errors.push('Your password is missing')
      }

      if (this.errors.length === 0) {
        await axios
          .post('/login/', this.form)
          .then(response => {
            this.userStore.setToken(response);

            axios.defaults.headers.common["Authorization"] = "Bearer " + response.access
          })
          .catch(error => {
            console.log('error', error)
          })

          await axios
          .post('/me/', this.form)
          .then(response => {
            this.userStore.setUserInfo(response);

            this.$router.push('/')
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  }
}
</script>
