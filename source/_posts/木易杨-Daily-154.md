---
layout: posts
title: 木易杨-Daily-154
date: 2020-09-11 19:57:02
tags:
---

## 第 154 题：弹性盒子中 flex: 0 1 auto 表示什么意思

答：
- flex 属性的含义是：用于指弹性子元素如何分配空间。
- flex：flex-grow flex-shrink flex-basis
  + flex-grow: 容器大于子元素的时候，子元素如何扩展
  + flex-shrink: 容器小于子元素的时候，子元素如何收缩
  + flex-basis: 子元素在被放入容器之前的大小，它与width作用强弱对比如下：flex-basis(limited by minWidth and maxWidth) > width
- 所以意思是，当容器宽度多的时候，不会扩大。而宽度不够的时候，会等比缩小。且如果设置了宽度，则为width的值，如果没设置宽度，则为实际内容。