---
title: Selection
date: 2020-09-02 19:29:27
tags:
---

通过做文本的复制粘贴了解到这个属性，通过该机制操作选中的文本。
参考MDN：https://developer.mozilla.org/zh-CN/docs/Web/API/Window/getSelection
描述比较简单。

## 获取选中的文本
### selection 对象
const selection = window.getSelection();或者document.getSelection();
### 文本
- MDN上写的是`selection.toString()`即可。这样拿的话，可以保留换行等一些符号，因为在某些网站中，会把换行处理成`<br>`，这样就拿可以保留来。
- 如果通过下面这种方式拿，换行符会消失。
  ```javascript
  window.getSelection().getRangeAt(0).cloneContents().textContent
  ```

## 删除选中的文本
-   
  ```javascript
  window.getSelection().getRangeAt(0).deleteContents()
  ```
