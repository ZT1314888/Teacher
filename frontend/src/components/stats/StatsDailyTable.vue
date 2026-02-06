<template>
  <section class="stats-panel">
    <div class="panel-header">
      <div>
        <h3 class="panel-title">近 7 天预约趋势</h3>
        <p class="panel-subtitle">按天查看预约量与状态分布</p>
      </div>
    </div>

    <div v-if="loading" class="panel-loading">
      <div v-for="idx in 6" :key="idx" class="loading-line"></div>
    </div>

    <el-alert
      v-else-if="error"
      class="panel-alert"
      type="warning"
      :title="error"
      show-icon
      :closable="false"
    />

    <el-empty v-else-if="normalizedRows.length === 0" description="暂无近7天统计数据" />

    <el-table v-else :data="normalizedRows" stripe>
      <el-table-column label="日期" min-width="130">
        <template #default="{ row }">
          <span class="cell-date">{{ formatDate(row.date) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="total" label="总数" width="84" />
      <el-table-column prop="approved" label="已通过" width="96" />
      <el-table-column prop="rejected" label="已拒绝" width="96" />
      <el-table-column prop="cancelled" label="已取消" width="96" />
      <el-table-column prop="expired" label="已过期" width="96" />
      <el-table-column label="预约负载" min-width="160">
        <template #default="{ row }">
          <div class="load-track">
            <div class="load-fill" :style="{ width: `${getLoadPercent(row.total)}%` }"></div>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  rows: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const normalizedRows = computed(() =>
  props.rows.map((row) => ({
    date: row.date,
    total: Number(row.total || 0),
    approved: Number(row.approved || 0),
    rejected: Number(row.rejected || 0),
    cancelled: Number(row.cancelled || 0),
    expired: Number(row.expired || 0)
  }))
)

const maxTotal = computed(() => {
  const values = normalizedRows.value.map((item) => item.total)
  return Math.max(1, ...values)
})

const getLoadPercent = (value) => Math.round((Number(value || 0) / maxTotal.value) * 100)

const formatDate = (dateText) => {
  if (!dateText) return '--'
  const date = new Date(dateText)
  if (Number.isNaN(date.getTime())) return dateText
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${month}-${day} ${weekdays[date.getDay()]}`
}
</script>

<style scoped>
.stats-panel {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.panel-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.panel-subtitle {
  margin: 4px 0 0;
  font-size: 13px;
  color: #64748b;
}

.panel-loading {
  display: grid;
  gap: 10px;
}

.loading-line {
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(90deg, #f1f5f9 20%, #e2e8f0 45%, #f1f5f9 70%);
  background-size: 200% 100%;
  animation: shimmer 1.2s linear infinite;
}

.panel-alert {
  margin-bottom: 8px;
}

.cell-date {
  font-weight: 600;
  color: #334155;
}

.load-track {
  height: 8px;
  border-radius: 999px;
  background: #e2e8f0;
  overflow: hidden;
}

.load-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #14b8a6 0%, #0d9488 100%);
}

@keyframes shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}
</style>
