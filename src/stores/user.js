import { defineStore } from "pinia"
import axios from "axios"

export const useUserStore = defineStore({
  id: 'user',

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      username: null,
      email_address: null,
      first_name: null,
      last_name: null,
      access: null,
      refresh: null,
    }
  }),

  actions: {
    initStore() {
      if (localStorage.getItem('user.access')) {
        this.user.access = localStorage.getItem('user.access')
        this.user.refresh = localStorage.getItem('user.refresh')
        this.user.id = localStorage.getItem('user.id')
        this.user.username = localStorage.getItem('user.username')
        this.user.email_address = localStorage.getItem('user.email_address')
        this.user.first_name = localStorage.getItem('user.first_name')
        this.user.last_name = localStorage.getItem('user.last_name')
        this.user.isAuthenticated = true

        this.refreshToken()

        console.log("Initialised user: ", this.user)
      }
    },

    setToken(data) {
      console.log('setToken', data)

      this.user.access = data.access
      this.user.refresh = data.refresh
      this.user.isAuthenticated = true

      localStorage.setItem('user.access', data.access)
      localStorage.setItem('user.refresh', data.refresh)
    },

    removeToken() {
      console.log("removeToken")

      this.user.access = null
      this.user.refresh = null
      this.user.id = null
      this.user.username = null
      this.user.email_address = null
      this.user.first_name = null
      this.user.last_name = null
      this.user.isAuthenticated = false

      localStorage.setItem('user.access', '')
      localStorage.setItem('user.refresh', '')
      localStorage.setItem('user.id', '')
      localStorage.setItem('user.username', '')
      localStorage.setItem('user.email_address', '')
      localStorage.setItem('user.first_name', '')
      localStorage.setItem('user.last_name', '')
    },

    setUserInfo(user) {
      this.user.id = user.id
      this.user.username = user.username
      this.user.email_address = user.email_address
      this.user.first_name = user.first_name
      this.user.last_name = user.last_name

      localStorage.setItem('user.id', this.user.id)
      localStorage.setItem('user.username', this.user.username)
      localStorage.setItem('user.email_address', this.user.email_address)
      localStorage.setItem('user.first_name', this.user.first_name)
      localStorage.setItem('user.last_name', this.user.last_name)

      console.log('User', this.user)
    },

    refreshToken() {
      axios.post('/refresh/')
    }
  }
})