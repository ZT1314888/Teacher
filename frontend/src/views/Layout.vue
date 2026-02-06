<template>
  <div class="layout-container">
    <AppHeader
      :user="user"
      :role-text="roleText"
      :unread-count="unreadCount"
      @command="handleCommand"
      @notifications="handleNotifications"
    />

    <div class="layout-body">
      <SidebarNav :user-role="user?.role" />
      <main class="layout-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import SidebarNav from '@/components/layout/SidebarNav.vue'
import { getNotifications } from '@/api/notification'

const store = useStore()
const router = useRouter()
const route = useRoute()
const unreadCount = ref(0)
let pollTimer = null
let notificationChangedHandler = null

const user = computed(() => store.state.user)

const roleText = computed(() => {
  const roleMap = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return roleMap[user.value?.role] || ''
})

const handleCommand = (command) => {
  if (command === 'logout') {
    store.dispatch('logout')
    router.push('/login')
    return
  }

  if (command === 'profile') {
    router.push('/profile')
    return
  }

  if (command === 'settings') {
    router.push('/change-password')
  }
}

const fetchUnreadNotifications = async () => {
  try {
    const data = await getNotifications()
    const rows = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])
    unreadCount.value = rows.filter((item) => !item.is_read).length
  } catch (error) {
    unreadCount.value = 0
  }
}

const handleNotifications = () => {
  router.push('/announcements')
}

watch(
  () => route.path,
  async () => {
    await fetchUnreadNotifications()
  },
  { immediate: true }
)

onMounted(() => {
  notificationChangedHandler = () => {
    fetchUnreadNotifications()
  }
  window.addEventListener('notification:changed', notificationChangedHandler)
  window.addEventListener('focus', notificationChangedHandler)

  pollTimer = window.setInterval(() => {
    fetchUnreadNotifications()
  }, 10000)
})

onUnmounted(() => {
  if (notificationChangedHandler) {
    window.removeEventListener('notification:changed', notificationChangedHandler)
    window.removeEventListener('focus', notificationChangedHandler)
    notificationChangedHandler = null
  }
  if (pollTimer) {
    window.clearInterval(pollTimer)
    pollTimer = null
  }
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100%;
  min-width: 0;
}

.layout-body {
  display: flex;
  height: calc(100vh - 64px);
  min-width: 0;
}

.layout-main {
  flex: 1;
  min-width: 0;
  background-color: #f9fafb;
  padding: 24px;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
