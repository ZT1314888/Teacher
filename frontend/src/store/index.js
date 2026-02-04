import { createStore } from 'vuex'
import { getUserInfo } from '@/api/auth'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('access_token') || null
  },
  
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.user?.role === 'admin',
    isTeacher: state => state.user?.role === 'teacher',
    isStudent: state => state.user?.role === 'student'
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('access_token', token)
      } else {
        localStorage.removeItem('access_token')
      }
    },
    
    SET_USER(state, user) {
      state.user = user
    },
    
    LOGOUT(state) {
      state.user = null
      state.token = null
      localStorage.clear()
    }
  },
  
  actions: {
    async fetchUserInfo({ commit }) {
      try {
        const user = await getUserInfo()
        commit('SET_USER', user)
        return user
      } catch (error) {
        commit('LOGOUT')
        throw error
      }
    },
    
    login({ commit }, { access, refresh }) {
      commit('SET_TOKEN', access)
      localStorage.setItem('refresh_token', refresh)
    },
    
    logout({ commit }) {
      commit('LOGOUT')
    }
  }
})
