<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="label">教室类型</label>
          <el-select
            :model-value="modelValue.classroom_type"
            class="w-full filter-control"
            placeholder="全部"
            clearable
            size="large"
            :disabled="classroomTypeLocked"
            @update:model-value="onFieldChange('classroom_type', $event || '')"
          >
            <el-option label="普通教室" value="lecture" />
            <el-option label="实验室" value="lab" />
            <el-option label="多媒体教室" value="multimedia" />
            <el-option label="会议室" value="conference" />
            <el-option label="艺术室" value="art" />
          </el-select>
        </div>

        <div>
          <label class="label">楼栋</label>
          <el-input
            :model-value="modelValue.building"
            class="w-full filter-control"
            size="large"
            placeholder="输入楼栋"
            clearable
            @update:model-value="onFieldChange('building', $event || '')"
          />
        </div>

        <div>
          <label class="label">容量</label>
          <el-select
            :model-value="modelValue.capacity"
            class="w-full filter-control"
            placeholder="全部"
            clearable
            size="large"
            @update:model-value="onFieldChange('capacity', $event || '')"
          >
            <el-option label="30人以下" value="30" />
            <el-option label="30-50人" value="50" />
            <el-option label="50-100人" value="100" />
            <el-option label="100人以上" value="101" />
          </el-select>
        </div>

        <div>
          <label class="label">搜索教室</label>
          <el-input
            :model-value="modelValue.search"
            class="w-full filter-control"
            size="large"
            placeholder="输入教室编号或名称"
            clearable
            @update:model-value="onFieldChange('search', $event || '')"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>

      <div class="flex space-x-3 mt-4">
        <button type="button" class="btn-primary" @click="$emit('search')">查询</button>
        <button type="button" class="btn-secondary" @click="$emit('reset')">重置</button>
      </div>

      <p v-if="classroomTypeLocked" class="lock-tip mt-3">
        当前为课程预约场景，教室类型已按课程要求锁定。
      </p>
    </div>
  </div>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  classroomTypeLocked: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'search', 'reset'])

const onFieldChange = (key, value) => {
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: value
  })
}
</script>

<style scoped>
.filter-control :deep(.el-input__wrapper) {
  min-height: 44px;
}

.lock-tip {
  color: #0f766e;
  font-size: 13px;
}
</style>
