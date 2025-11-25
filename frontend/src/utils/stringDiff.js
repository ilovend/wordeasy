/**
 * 字符串差异比较工具
 */

/**
 * 计算两个字符串的编辑距离并标记差异
 * @param {string} input - 用户输入
 * @param {string} correct - 正确答案
 * @returns {Array} 差异标记数组
 */
export function highlightDifferences(input, correct) {
  input = input.toLowerCase().trim()
  correct = correct.toLowerCase().trim()

  if (input === correct) {
    return [{ text: input, isCorrect: true }]
  }

  const result = []
  const maxLen = Math.max(input.length, correct.length)

  // 逐字符比较
  for (let i = 0; i < maxLen; i++) {
    const inputChar = input[i] || ''
    const correctChar = correct[i] || ''

    if (inputChar === correctChar && inputChar !== '') {
      // 相同字符
      if (result.length > 0 && result[result.length - 1].isCorrect) {
        result[result.length - 1].text += inputChar
      } else {
        result.push({ text: inputChar, isCorrect: true })
      }
    } else if (inputChar !== '') {
      // 错误字符（用户输入的）
      if (result.length > 0 && result[result.length - 1].isError) {
        result[result.length - 1].text += inputChar
      } else {
        result.push({ text: inputChar, isError: true })
      }
    } else {
      // 缺少字符（用户未输入）
      if (result.length > 0 && result[result.length - 1].isMissing) {
        result[result.length - 1].text += correctChar
      } else {
        result.push({ text: correctChar, isMissing: true })
      }
    }
  }

  return result
}

/**
 * 生成友好的错误提示
 * @param {string} input - 用户输入
 * @param {string} correct - 正确答案
 * @returns {string} 错误提示文本
 */
export function getErrorHint(input, correct) {
  input = input.toLowerCase().trim()
  correct = correct.toLowerCase().trim()

  if (input.length < correct.length) {
    return `提示：单词还缺少 ${correct.length - input.length} 个字母`
  } else if (input.length > correct.length) {
    return `提示：单词多了 ${input.length - correct.length} 个字母`
  } else {
    // 找出第一个不同的位置
    for (let i = 0; i < correct.length; i++) {
      if (input[i] !== correct[i]) {
        return `提示：第 ${i + 1} 个字母有误`
      }
    }
  }

  return '提示：请检查拼写'
}
