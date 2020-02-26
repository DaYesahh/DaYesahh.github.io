---
title: WebWorker
date: 2019-02-03 12:03:42
tags:
- WebWorker
categories:
- js
---


- 前面在《js异步执行如何工作的》一文中简单提到，因为js是单线程的，在如今这种高密度的计算中，显然有些吃力。于是，浏览器积极发展多线程，来弥补js单线程的不足。而Web Worker就是其中一种机制。
既然是一种多线程机制，那么它是怎么工作的呢？
- 简单的说，Web Worker是运行在后台的。为什么这么说？js是一种单线程机制，那么其就有一个主线程。而主线程可以创建Worker线程，将一些任务分配给后者运行。那跟人家主线程相比，Web Worker可不就是运行在后台。
- 更巧妙的是，Worker是独立于其他脚本的，不会影响页面的性能，跟主线程互不干扰。除了两者之间进行消息沟通。
- 互不干扰的意思是不会被主线程上的活动给打断，比如主线程要进行用户点击、提交表单等等。不是不会进行通信的意思哦。

<!--more-->
## 使用注意点
- 同源限制
 + 分配给Worker线程运行的脚本文件，必须与主线程的脚本文件同源
- DOM限制
 + Worker线程所在的全局对象(self)，与主线程的(根据宿主环境不同而不同)不同，无法读取主线程所在网页的DOM对象，也无法使用document、window（既然无法使用window，也就无法使用全局变量和全局函数，因为这些都是挂载到window对象上的）、parent这些对象。但是，Worker线程可以使用navigator对象和location对象。
 + 上句进一步复习了全局对象不仅仅是window
- 通信联系
 + Worker线程和主线程不在同一个上下文环境，他们不能直接通信，必须通过消息完成。
 + 上句进一步复习了上下文环境与作用域的不同。
- 脚本限制
 + worker线程不能执行alert()方法和confirm()方法，但可以使用XMLHttpRequest对象发出AJAX请求、使用SetTimeout(),setInterval()之类的函数
- 文件限制
 + Worker线程无法读取本地文件，即不能打开本机的文件系统(file://)，它所加载的脚本，必须来自网络

## 分类
- 专用线程`dedicated web worker`--简称为`Worker`
 + 只能被创建它的页面访问，也会随着当前页面的关闭而结束
- 共享线程`shared web worker`--简称为`SharedWorker`
 + 线程如其名，会被多个页面访问。

## 基本用法
### 主线程处的用法
- 新建一个Worker线程：`var worker = new Worker('work.js')`
 + 前面提到，Worker()读取的文件要来自网络。如果没有下载成功，Worker也会失败
 + Worker()读取的文件就是其所要执行的任务
- 主线程向Worker发送消息
 + ```javascript
    worker.postMessage('hello world') // 传递字符串举例
    worker.postMessage({method:'echo',args:['Work']}) // 传递对象举例
    ```

+ 主线程向`Worker`传递的数据类型可以是各种数据类型，甚至是二进制数据 

+ 主线程通过`onmessage`指定监听函数，接收子线程发回来的消息

    ```javascript
     worker.onmessage = function (event){
     	console.log('Received message' + event.data) //可以打印看看还有什么其他属性
     	dosomething() // 推荐的编程方式
     }
     function dosomething(){
     	// 执行任务
     	worker.postMessage('Work done')
     }
    ```
- 关闭`Worker`
 + `worker.terminate()`

### Worker线程处的用法

- Worker线程内需要一个监听函数，监听message事件

 ```javascript
// self表示子线程自身，即子线程的全局对象
 self.addEventListener('message', function(e){
 	self.postMessage('You said:'+ e.data)
 })
 ```
 + 除了使用self.addEventListener()指定监听函数，也可以使用self.onmesssage指定。
 + 监听函数的参数是一个事件对象，它的data属性包含主线程发来的数据
 + self.postMessage()方法用来向主线程发送消息
 + 举例：
  ```javascript
  self.addEventListener('message', function(e){
  	var data = e.data
  	switch(data.cmd){
  		case 'start':
  		  self.postMessage('Worker started:' + data.msg)
  		  break;
  		case 'stop':
  		  self.postMessage('Worker stopped:' + data.msg)
  		  self.close() //这里是自己关闭自己
  		  break;
  		default:
  		  self.postMessage('unknow command:' + data.msg)    
  	}
  	},false)
  ```
 - Worker内部加载其他脚本
  + ```javascript
      importScripts('script1.js',...) //可以加载多个
      ```

+ 错误处理 

+ + 同上，无论是主线程中的Worker还是子线程Worker内部，当Worker发生错误的时候，均可以监听并且触发error事件
  ```javascript
  worker.onerror(function (event){
  	console.log([
       'ERROR:Line', e.lineno, 'in', e.filename,':',e.message
  		].join(''))
  	})
  	// 或者是如下：
  	worker.addEventListener('error', function (event){
  		// ...
  		})
  ```
 - 关于Worker的关闭事件
    上述提到了两种，一种是主线程关系Worker，一种是Worker自我关闭，分别是：
  + `worker.terminate()`
  + `self.close()`

### 数据通信
- 主线程与Worker之间的通信是拷贝关系，是传值而不是传地址。所以Worker对数据的修改不会影响到主线程，主线程只需要接收最终结果即可。
- 浏览器内部的运行机制是，先将通信内容串行化，然后把串行化的字符串发给worker，后者再将其还原
- 举例
  ```javascript
  var uInt8Array = new Uint8Array('aaa')
  worker.postMessage(uInt8Array)

  // Worker线程
  self.onmessage = function(e) {
  	var uInt8Array = e.data
  	// 接收以后返回拼接的字符串
  	postMessage('Inside worker.js: uInt8Array.toString() = ' + uInt8Array.toString());
    postMessage('Inside worker.js: uInt8Array.byteLength = ' + uInt8Array.byteLength);
  }
  ```
- 虽然也可以发送二进制数据，但是二进制数据会造成性能问题。详情如下
```javascript
// 比如，主线程向 Worker 发送一个500MB 文件，默认情况下浏览器会生成一个原文件的拷贝。为了解决这个问题，JavaScript 允许主线程把二进制数据直接转移给子线程，但是一旦转移，主线程就无法再使用这些二进制数据了，这是为了防止出现多个线程同时修改数据的麻烦局面。这种转移数据的方法，叫做Transferable Objects。这使得主线程可以快速把数据交给 Worker，对于影像处理、声音处理、3D 运算等就非常方便了，不会产生性能负担。
// 如果要直接转移数据的控制权，就要使用下面的写法。
worker.postMessage(arrayBuffer, [arrayBuffer]);

// 例子
var ab = new ArrayBuffer(1);
worker.postMessage(ab, [ab]);

```

### 加载同页面的Web Worker
腊月二十九依旧减肥快饿死了。
- 上述介绍了Worker加载一个单独的js文件`var worker = new Worker('a.js')`，但是也可以加载与主线程在同一网页的代码段
- 请直接看举例：
```javascript
<!DOCTYPE html>
  <body>
    <script id="worker" type="app/worker">
      addEventListener('message', function () {
        postMessage('some message');
      }, false);
    </script>
  </body>
</html>
// 注意这里的type,
var blob = new Blob([document.querySelector('#worker').textContent])
var url = window.URL.createObjectURL(blob)
var worker = new Worker(url)

worker.onmessage = function (e){
	// dosomething
}
//上面代码中，先将嵌入网页的脚本代码，转成一个二进制对象，然后为这个二进制对象生成 URL，再让 Worker 加载这个 URL。这样就做到了，主线程和 Worker 的代码都在同一个网页上面。
```

### 使用worker的建议
- 使用多少个1worker1？
 + 只要是线程必将耗费资源，那么开启多少个worker才合适呢？
 + 采用`navigator.hardwareConcurrency`，其表示机器支持的并行最大任务数
 + 还有一种动态监测`Worker`数量的方式：https://github.com/oftn-oswg/core-estimator。
- 优化`worker`与主线程通信开销
 + 前面提到数据通信是通过拷贝的方式，如果数据量大，消耗的时长也长。解决办法是：
  - 先通过`JSON.stringify`将对象序列化，接收之后再用`JSON.parse`还原。
  - 因为：`stringify `+ 传递字符串的耗时 < 传递对象的耗时
  ```javascript
  // 操作像素
    var imageData = context.createImageData(img.width, img.height);
    var work = new Worker('./cal.js');
    var data = {
        data: imageData.data,
        width: imageData.width,
        height: imageData.height
    };
    // 将传递的参数转换成字符串
    work.postMessage(JSON.stringify(data));
  ```

## 参考
- http://www.ruanyifeng.com/blog/2018/07/web-worker.html
- https://www.cnblogs.com/wmhuang/p/6913468.html
