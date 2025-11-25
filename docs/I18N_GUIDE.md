# WordEasy 国际化 (i18n) 指南

## 概述

WordEasy 项目已集成 Vue I18n 实现多语言支持，目前支持中文和英文两种语言。

## 已完成的工作

### 1. 安装和配置
- ✅ 安装了 `vue-i18n` 包
- ✅ 创建了 `src/i18n.js` 配置文件
- ✅ 在 `main.js` 中注册了 i18n 插件
- ✅ 创建了语言文件存储目录 `src/locales/`

### 2. 语言文件
- ✅ `src/locales/zh.json` - 中文翻译
- ✅ `src/locales/en.json` - 英文翻译

所有用户界面文本都已提取并组织到这两个文件中。

### 3. 已更新的组件
- ✅ Home.vue - 首页（完全国际化）
- ✅ Settings.vue - 设置页面（添加了语言切换功能）

### 4. 语言切换功能
在设置页面新增了语言切换选项：
- 🇨🇳 中文
- 🇬🇧 English

语言设置会自动保存到 localStorage，页面刷新后保持选择。

## 使用方法

### 在模板中使用

```vue
<template>
  <!-- 基本用法 -->
  <h1>{{ $t('home.title') }}</h1>
  
  <!-- 带参数的翻译 -->
  <p>{{ $t('game.review.count', { count: reviewCount }) }}</p>
  
  <!-- 在属性中使用 -->
  <button :title="$t('common.save')">保存</button>
</template>
```

### 在 script setup 中使用

```vue
<script setup>
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

// 使用翻译
const message = t('common.success')

// 切换语言
function changeLanguage(lang) {
  locale.value = lang
  localStorage.setItem('wordeasy_locale', lang)
}
</script>
```

### 在 JavaScript 中使用 confirm/alert

```javascript
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

if (confirm(t('settings.confirm.reset'))) {
  // 执行操作
}
```

## 需要完成的组件国际化

以下组件仍需要将硬编码的中文替换为 `$t()` 调用：

### 高优先级
1. **SpellGame.vue** - 游戏核心组件
   - 难度选择界面
   - 学习模式界面
   - 游戏进行界面
   - 结果界面
   - 所有提示和反馈文本

2. **SpeedChallenge.vue** - 速拼挑战
   - 开始界面
   - 游戏界面
   - 结果界面

3. **Review.vue** - 复习模式
   - 复习计划说明
   - 模式选择卡片

4. **WordList.vue** - 词库管理
   - 上传界面
   - 统计信息
   - 错词本
   - 待复习单词列表

### 中优先级
5. **LoadingSpinner.vue** - 加载提示
6. Toast 和其他工具函数中的文本

## 翻译键命名规范

语言文件采用层级结构组织：

```json
{
  "模块名": {
    "子模块": {
      "键名": "翻译文本"
    }
  }
}
```

例如：
- `home.title` - 首页标题
- `game.difficulty.easy` - 游戏难度-简单
- `settings.sound.enable` - 设置-音效-启用

## 添加新翻译

1. 在 `src/locales/zh.json` 和 `src/locales/en.json` 中添加键值对
2. 在组件中使用 `$t('your.translation.key')`
3. 确保两个语言文件都有相同的键

## 带参数的翻译

在语言文件中使用 `{变量名}` 占位符：

```json
{
  "game.review.count": "有 {count} 个单词需要复习"
}
```

在组件中传递参数：

```vue
{{ $t('game.review.count', { count: reviewCount }) }}
```

## 注意事项

1. **保持一致性**：确保中英文翻译键完全一致
2. **emoji 保留**：emoji 图标在两种语言中保持一致
3. **测试**：切换语言后测试所有功能是否正常
4. **格式化**：使用 `{参数}` 而不是字符串拼接

## 下一步工作

1. 逐个更新剩余的 Vue 组件
2. 更新 toast 等工具函数中的消息
3. 测试所有页面在两种语言下的显示效果
4. 考虑添加更多语言支持（如日语、韩语等）

## 示例：完整的组件国际化

参考 `Home.vue` 和 `Settings.vue` 的实现方式，它们已经完全国际化。

需要帮助时，可以查看这两个文件作为参考。
