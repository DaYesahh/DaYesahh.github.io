---
title: Promise
date: 2019-04-15 13:06:06
tags:
- Promise
categories:
- es6
---

异步编程，是一个容器，里面保存着某个未来才会结束的事件（通常是一个异步操作），是**对象**，获取异步操作的消息。

其特点如下：

- 对象的状态不受外界影响。`Promise`对象代表一个**异步操作**，有三种状态：`pending(进行中)`、`fulfilled()已成功`和`rejected(已失败)`。注意：其状态只要异步操作才会使其改变！参考其名字！
- 状态一旦改变，就不会再变，任何时候都可以得到这个结果。`Promise`对象状态改变，两种可能：从`pending`变为`fulfilled`和从`pending`变为`rejected`。只要这两种情况发生，状态便凝固了，不会再改变！这时称为`resolved(已定型)`。如果改变已经发生，即使再对`Promise`对象添加回调函数，也会立即得到这个结果。

<!--more-->
- 日常使用为了方便：`resolved`统一指`fulfilled`状态，不包含`rejected`状态。
- 缺点：
  + 无法取消`Promise`
  + 如果未设置回调函数，其内部抛出的错误，不会反应到外部。
  + 当处于`pending`状态时，无法得到目前进展到哪一阶段。

## `Promise`语法

```javascript
// Promise实例化的时候，接收一个函数作参数，而函数有两个参数：resolve、reject。resolve是将**Promise对象**，从未完成变为成功。而reject是从未完成变为失败。
const promise = new Promise(function(resolve, reject) {
  // ... some code

  if (/* 异步操作成功 */){
    resolve(value);
  } else {
    reject(error);
  }
});
```

- 关于`then`：

  ```javascript
  // Promise实例生成以后，Promise参数函数中的状态函数，执行以后是否成功，会调用then
  promise.then(function(value){
      // success
      // promise对象状态变为resolved时调用
  },function(error){
      // failure
      // promise对象状态变为rejected时调用
  })
  ```

- promise实例作为另一个promise实例的参数

  ```javascript
  const p1 = new Promise(function (resolve, reject) {
    setTimeout(() => reject(new Error('fail')), 3000)
  })
  
  const p2 = new Promise(function (resolve, reject) {
    setTimeout(() => resolve(p1), 1000)
  })
  
  p2
    .then(result => console.log(result))
    .catch(error => console.log(error))
  // Error: fail
  // 此时p2的状态由p1决定
  ```

  - 调用`resolve`或`reject`并不会终结`Promise`参数的执行。

## `Promsie.prototype.then()`

```javascript
Promsie实例的then方法，是定义在原型对象Promise.prototype上的。
```

- then可以开启链式写法，前一个then方法将返回结果作为参数（如果该参数是一个Promise对象，则后一个回调函数会等待该Promise对象状态改变再调用）传入第二个回调函数。

## `Promise.prototype.catch()`

是`.then(null,rejection)`或`.then(undefined,rejection)`的别名。

```javascript
getJSON('/posts.json').then(function(posts) {
  // ...
}).catch(function(error) {
  // 处理 getJSON 和 前一个回调函数运行时发生的错误
  console.log('发生错误！', error);
});
// 返回一个Promise对象，如果该对象状态变为resolved，则会调用then方法指定的回调函数，如果抛出错误，则状态会变为rejected，就会调用catch方法指定的回调函数来处理。
// 实际像是then的参数只保留resolved，将rejected放在外面。最好不要给then设置两个参数，用catch即可。
```

- promise会吃掉错误

## `Promise.prototype.finally()`

不管`Promise`对象最后状态如何，都会执行的操作。

- **不接受任何参数！**，无法确定其前面的`Promise`的状态时`fulfilled`还是`rejected`。应执行与状态无关的，不依赖于`Promise`的执行结果

- 本质是`then`的特例。

  ```javascript
  // resolve 的值是 undefined
  Promise.resolve(2).then(() => {}, () => {})
  
  // resolve 的值是 2
  Promise.resolve(2).finally(() => {})
  
  // reject 的值是 undefined
  Promise.reject(3).then(() => {}, () => {})
  
  // reject 的值是 3
  Promise.reject(3).finally(() => {})
  
  ```

## `Promsie.all()`

`Promise.all`方法用于将多个 Promise 实例，包装成一个新的 Promise 实例。

- （`Promise.all`方法的参数可以不是数组，但必须具有 Iterator 接口，且返回的每个成员都是 Promise 实例。）

`p`的状态由`p1`、`p2`、`p3`决定，分成两种情况。

（1）只有`p1`、`p2`、`p3`的状态都变成`fulfilled`，`p`的状态才会变成`fulfilled`，此时`p1`、`p2`、`p3`的返回值组成一个数组，传递给`p`的回调函数。

（2）只要`p1`、`p2`、`p3`之中有一个被`rejected`，`p`的状态就变成`rejected`，此时第一个被`reject`的实例的返回值，会传递给`p`的回调函数。

```javascript
const p = Promise.all([p1, p2, p3]);
```

## `Promise.race()`

`Promise.race`方法同样是将多个 Promise 实例，包装成一个新的 Promise 实例。

```javascript
const p = Promise.race([p1, p2, p3]);
```

## `Promise.resolve()`

将现有对象转为 `Promise `对象

```javascript
const jsPromise = Promise.resolve($.ajax('/whatever.json'));

// 一
var pro = Promise.resolve('foo')
console.log(pro)
// 二
var pro1 = new Promise(resolve => resolve('foo'))
console.log(pro1)
// 一和二等价
```

### 参数区分

#### `Promise` 实例

不做任何修改、原封不动地返回这个实例。

#### `thenable`对象

`thenable`对象指的是具有`then`方法的对象，比如下面这个对象。

```javascript
let thenable = {
  then: function(resolve, reject) {
    resolve(42);
  }
};
```

`Promise.resolve`方法会将这个对象转为 Promise 对象，然后就立即执行`thenable`对象的`then`方法。

```javascript
let thenable = {
  then: function(resolve, reject) {
    resolve(42);
  }
};

let p1 = Promise.resolve(thenable);
p1.then(function(value) {
  console.log(value);  // 42
});

```

#### **参数不是具有then方法的对象，或不是对象**

```javascript
const p = Promise.resolve('Hello');

p.then(function (s){
  console.log(s)
});
// Hello
// 如果参数是一个原始值，或者是一个不具有then方法的对象，则Promise.resolve方法返回一个新的 Promise 对象，状态为resolved。
```

#### 不带有任何参数

`Promise.resolve()`方法允许调用时不带参数，直接返回一个`resolved`状态的 Promise 对象。

```javascript
const p = Promise.resolve();

p.then(function () {
  // ...
});
// 立即resolve()的 Promise 对象，是在本轮“事件循环”（event loop）的结束时执行，而不是在下一轮“事件循环”的开始时。
```

## `Promise.rejected()`

`Promise.reject(reason)`方法也会返回一个新的 Promise 实例，该实例的状态为`rejected`。

```javascript
const p = Promise.reject('出错了');
// 等同于
const p = new Promise((resolve, reject) => reject('出错了'))

p.then(null, function (s) {
  console.log(s)
});
// 出错了
```

## 应用

- 加载图片，当图片加载完成，promise状态发生变化。

  ```javascript
  const preloadImage = function(path){
      return new Promise(function(resolve,reject){
          const image = new Image();
          image.onload = resolve;
          image.onerror = reject;
          image.src = path;
      })
  }
  ```

- `Generator函数与Promise的结合`

  ```javascript
  ？？？？？？？？
  ```

- `Promise.try()`

   ```javascript
   如果不想区分同步函数还是异步操作，采用Promise来处理，不管是否包含异步（关于同步，可以选择同步变异步，也可以选择同步依旧是同步），均可用then来指定下一步流程，用catch方法处理f抛出的错误。
   // 同步变异步
   const f = () => console.log('now');
   Promise.resolve().then(f);
   console.log('next');
   // next
   // now
   ```

// 同步依旧为同步一
const f = () => console.log('now');
(async () => f())(); // 采用匿名函数和async
console.log('next');
// now
// next
// 异步为异步
const f = () => console.log('now');
(async () => f())().then();
console.log('next');

   ```



## 其他异步与promise的关系

### `setTimeout`

看如下代码：

​```javascript
const promise = new Promise(function (resolve, reject) {
  resolve('ok');
  setTimeout(function () { throw new Error('test') }, 0)
});
promise.then(function (value) { console.log(value) });
// ok
// error，说明setTimeour在promise结束以后执行。
   ```

如下代码：

```javascript
setTimeout(function () {
  console.log('three');
}, 0);

Promise.resolve().then(function () {
  console.log('two');
});

console.log('one');

// one
// two
// three
/*
上面代码中，setTimeout(fn, 0)在下一轮“事件循环”开始时执行，Promise.resolve()在本轮“事件循环”结束时执行，console.log('one')则是立即执行，因此最先输出。
*/
```

