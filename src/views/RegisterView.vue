<template>
  <main class="px-8 py-6 bg-gray-100">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-left col-span-2">
        <div class="p-12 bg-white border border-gray-200 rounded-lg">
          <h1 class="mb-6 text-2xl">Register</h1>

          <p class="mb-6 text-gray-500">
            Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
            dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit
            mate. Lorem ipsum dolor sit mate.
          </p>

          <p class="font-bold">
            Already have an account?
            <RouterLink :to="{name: 'login'}" class="underline">Click here</RouterLink> to log in!
          </p>
        </div>
      </div>

      <div class="main-center col-span-2 space-y-4">
        <div class="p-12 bg-white border border-gray-200 rounded-lg">
          <form class="space-y-6" @submit.prevent="submitForm">
            <div>
              <label>Username</label><br />
              <input
                type="text"
                v-model="form.username"
                placeholder="Your new account's username"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
              />
            </div>

            <div class="flex justify-between">
              <div>
                <label>First name</label><br />
                <input
                  type="text"
                  v-model="form.first_name"
                  placeholder="Your first name"
                  class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
                />
              </div>

              <div>
                <label>Last name</label><br />
                <input
                  type="text"
                  v-model="form.last_name"
                  placeholder="Your last name"
                  class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
                />
              </div>
            </div>

            <div>
              <label>E-mail</label><br />
              <input
                type="email"
                v-model="form.email_address"
                placeholder="Your e-mail address"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
              />
            </div>

            <div>
              <label>Password</label><br />
              <input
                type="password"
                v-model="form.password1"
                placeholder="Your password"
                minlength="8"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
              />
            </div>

            <div>
              <label>Confirm Password</label><br />
              <input
                type="password"
                v-model="form.password2"
                placeholder="Re-enter your password"
                minlength="8"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
              />
            </div>

            <template v-if="errors.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6">
                <p v-for="error in errors" :key="error">{{ error }}</p>
              </div>
            </template>

            <div class="flex justify-center items-center">
              <button class="py-4 px-6 bg-orange-600 text-white rounded-lg transition-all hover:bg-orange-500">
                Register
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { useToastStore } from '../stores/toast';
import axios from 'axios'

export default {
  setup() {
    const toastStore = useToastStore()

    return {
      toastStore
    }
  },

  data() {
    return {
      form: {
        email_address: '',
        username: '',
        first_name: '',
        last_name: '',
        password1: '',
        password2: ''
      }
    }
  },

  methods: {
    submitForm() {
      this.errors = []

      if (this.form.email_address === '') {
        this.errors.push('Your e-mail is missing')
      }
      this.errors = []

      if (this.form.name === '') {
        this.errors.push('Your name is missing')
      }
      this.errors = []

      if (this.form.password1 === '') {
        this.errors.push('Your password is missing')
      }
      this.errors = []

      if (this.form.password1 !== this.form.password2) {
        this.errors.push('The password does not match')
      }

      if (this.errors.length === 0) {
        axios
          .post('/register/', this.form)
          .then(response => {
            if (response.data.message === 'success') {
              this.toastStore.showToast(5000, 'The user is registered. Please log in', 'bg-emerald-500')

              this.form.email_address = '';
              this.form.username = '';
              this.form.first_name = '';
              this.form.last_name = '';
              this.form.password1 = '';
              this.form.password2 = '';
            } else {
              this.toastStore.showToast(5000, 'Something went wrong, please try again.', 'bg-red-300')
            }
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  }
}
</script>