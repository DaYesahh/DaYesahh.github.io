---
layout: posts
title: 木易杨-Daily-160
date: 2020-09-08 19:41:53
tags:
---

# 第 160 题：输出以下代码运行结果，为什么？如果希望每隔 1s 输出一个结果，应该如何改造？注意不可改动 square 方法

```javascript
const list = [1, 2, 3]
const square = num => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(num * num)
    }, 1000)
  })
}

function test() {
  list.forEach(async x=> {
    const res = await square(x)
    console.log(res)
  })
}
test()
```

## 答案
```javascript
const list = [1, 2, 3]
const square = num => {
  return new Promise((resolve, reject) => {
	//  console.log(new Date().getSeconds())
    setTimeout(() => {
		console.log(new Date().getSeconds())
      resolve(num * num)
    }, 1000)
  })
}

async function test() {
	for (let item of list) {
         const res = await square(item)
         console.log(res)	
	}
}
test()

```

解释：
因为forEach是默认请求并发发起的，所以不能阻塞。可以吧forEach换掉，换成for of或者普通的for循环。
具体参考官网：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach
其中解释道：‘除了抛出异常以外，没有办法中止或跳出 forEach() 循环。如果你需要中止或跳出循环，forEach() 方法不是应当使用的工具。’