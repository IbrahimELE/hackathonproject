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
    }
  }),

  actions: {
    initStore() {
      if (localStorage.getItem('user.access')) {
        this.user.id = localStorage.getItem('user.id')
        this.user.username = localStorage.getItem('user.username')
        this.user.email_address = localStorage.getItem('user.email_address')
        this.user.first_name = localStorage.getItem('user.first_name')
        this.user.last_name = localStorage.getItem('user.last_name')
        this.user.isAuthenticated = true

        // this.refreshToken()

        console.log("Initialised user: ", this.user)
      }
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
  }
})