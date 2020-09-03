---
title: 木易杨_Daily_155
date: 2020-09-03 19:39:00
tags:
---

# 第 155 题：求最终 left、right 的宽度
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
    flex: 1 2 500px;
    background: red;
  }
  .right {
    flex: 2 1 400px;
    background: blue;
  }
</style>
```

错误解： 因为子元素之和 400+500 = 900 > 父元素600
所以要按照flex-shrink来计算。
900 - 600 = 300
300/3 = 100
500 - 200== 300
400 - 100 = 300

正确解：
总权重 = （子元素宽度 * 子元素收缩系数）之和
溢出 = 子元素宽度之和 - 父元素之和
子元素收缩比例 = 子元素宽度 * 子项收缩系数 / 总权重
收缩宽度= 溢出 * 子元素收缩比例。

总权重 = 500*2 + 400*1 = 1400
溢出 = 400 + 500 - 600 = 300
.left收缩比例 = 500*2/1400
.left收缩宽度 = 500*2*300/1400
.right收缩比例 = 400*1/1400
.right收缩宽度 = 300*400*1/1400 
最终.left宽度为 500 - 500*2*300/1400 = 285.71
.right宽度为 400 - 300*400*1/1400 = 314.29
以上结果进行过四舍五入。