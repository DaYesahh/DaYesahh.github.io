---
title: 木易杨_Daliy_156
date: 2020-09-02 20:04:08
tags:
---

# 第 156 题：求最终 left、right 的宽度

```javascript
<div class="container">
    <div class="left"></div>
    <div class="right"></div>
</div>

<style>
  * {
    padding: 0;
    margin: 0;
  }
  .container {
    width: 600px;
    height: 300px;
    display: flex;
  }
  .left {
    flex: 1 2 300px;
    background: red;
  }
  .right {
    flex: 2 1 200px;
    background: blue;
  }
</style>
```

注：此题和 155 题 left、right 样式有些不同
因为300+200小于600，则flex-grow有效，需要计算剩余空间。而如果子元素的综合大于父元素时，需要使用flex-shrink来计算如果缩小。
剩余的空间：600 - (300 + 200) = 100。
子元素的 flex-grow 的值分别为 1，2， 剩余空间用3等分来分
100 / 3 = 33.3333333
所以 left = 300 + 1 * 33.33 = 333.33
right = 200 + 2 * 33.33 = 266.67