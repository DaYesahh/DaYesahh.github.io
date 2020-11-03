---
title: React_JSX
date: 2020-09-02 19:30:25
tags:
---

# JSX
JSX是JS的扩展语言，特点是既可以写JS，也可以写Html，而且不用以字符串的方式写。
例如：
```javascript
function getGreeting(user) {
  if (user) {
    return <h1>Hello, {formatName(user)}!</h1>;  }
  return <h1>Hello, Stranger.</h1>;}
```

## 关于JSX的三个大问题
### JSX的本质是什么，它和js之间到底是什么关系？

- 模板语法的一种
- JSX是JS的一种语法扩展，它和模板语言很接近，但是它充分具备JS的能力。
- JSX是如何生效的呢？
  + JSX会被编译为React.createElement(), React.createElement()将返回一个叫做“React Element”的JS对象。编译是通过Babel来完成的。
  + React.createElement(标签名, 属性, 子元素)
- JSX使用最熟悉的类HTML标签语法来创建虚拟DOM，降低学习成本，提升研发效率与研发体验。
#### React.createElement源码
```javascript
export function createElement(type[节点类型，div啥的], config[属性对象对象], children[子元素]) {
  // propName 变量用于储存后面需要用到的元素属性
  let propName;
  // props 变量用于储存元素属性的键值对集合
  const props = {};
  // key ref self source 均为React的属性，此处不深究
  let key = null;
  let ref = null;
  let self = null;
  let source = null;

  // config对象中存储的是元素的属性
  if (config != null) {
    // 进来之后做的第一件事，是依次对ref key self 和source属性赋值
    if (hasValidRef(config)) {
      ref = config.ref;
    }
    // 此处将key值字符串化
    // 按照Ref 以此类推
    // 接着就是要把config里面的属性都一个一个挪到props这个之前声明好多对象里面
    for (propName in config) {
      if{
        // 筛选出可以提进props对象的属性
        hasOwnProperty.call(config, propName) &&/ 
        !RESERVED_PROPS.hasOwnProperty(propName)
        props[propName] = config[propName];
      }
    }
  }
  // childrenLength 指的是当前元素的子元素的个数，减去的2是type和config两个参数占用的长度
  const childrenLenght = arguments.length - 2;
  // 如果抛去type和config，就只剩一个参数，一般意味着文本节点出现了
  if (childrenLength === 1){
    // 添加到props
  } else if (childrenLength > 1) {
    // 把子元素推进数组里
    // 添加到props中
  }
  // 处理defaultProps
  // defaultProps推到props
}
// 最后返回一个调用ReactElement执行方法，并传入刚才处理过的参数
return ReactElement(
  type,
  key,
  ref,
  self,
  source,
  RectCurrentOwner.current,
  props,
)

// 1、React.createElement
// 2、二次处理key、ref、self、source四个属性值
// 3、遍历config，筛出可以提进props里的属性
// 4、提取子元素，推入childArray数组
// 5、格式化defaultProps

```
开发者=》react.createElement => ReactElement =》 ReactDOM.render()
```javascript
const ReactElement = function (  type,key,ref,self,source,RectCurrentOwner,current,props) {
 const element = {
   // REACT_ELEMENT_TYPE是一个常量，用来标识该对象是一个ReactElement
   $$ typeof:REACT_ELEMENT_TYPE,
   // 内置属性赋值
   // 组装，然后返回给React.createElement
 }
}
ReactDOM.render(
  // 需要渲染的元素(ReactElement)
  element,
  // 元素挂载的目标容器（一个真实DOM，确实存在的）
  contanier,
  // 回调函数，可选参数，可以用来处理渲染的结束后的逻辑
  [callback]
)
```

## React15 React16 生命周期
### 虚拟DOM生命流
组件初始化 =》 render方法 =》生成虚拟DOM =》 ReactDOM.render方法 =》 真实DOM
组件更新 =》 render方法 =》 生成新的虚拟DOM =》 diff算法 =》定位出两次虚拟DOM的差异
React允许开发者基于单向数据流的原则，完成组件间的通信，而组件间的通信，又将改变通信双方某一方内部的数据，进而对渲染结果构成影响。

### 生命周期的本质
React组件内部的生命周期方法，LifeCircel的render，是组件的灵魂，其他方法是躯干。
渲染工作流：组件数据改变到组件实际更新的过程。
React15的生命周期流程：
挂载阶段：组件初始化渲染，只发生一次
- constructor()，对this.state初始化
- componentWillMount()
在执行过程中，不会操作真实dom，只是把需要渲染的内容返回出来
- render
在渲染结束后被处罚，真实DOM已经挂载到页面上，可以对真实DOM操作
- componentDidMount()
更新阶段
- componentWillReceiveProps(nextProps) // 父组件触发的更新
 + 不是props的变化触发的，而是父组件的变化触发的
- shouldComponentUpdate(nextProps, nextState) // 组件自身更新
 + React组件会根据此方法的返回值，来决定是否执行该方法之后的生命周期，进而决定是否对组件进行re-render
- componentWillUpdate()
- componentDidUpdate()


- render()
组件卸载阶段
- componentWillUnmount()

### react16 生命周期
先看react16.3生命周期 react16.4后又有微调
mounting阶段：
constructor()
getDerivedStateFromProps(props[父组件的props], state[本组件的state
]) // 废弃了compoenentWillMount，是废弃不是被代替
- 使用props来派生/更新state
- 直接从命名层面约束了它的用途
- 在更新和挂载两个阶段都会出现
- 是静态方法，不依赖组件实例而存在，访问不到this
- 得返回一个对象格式的返回值，需要用这个返回值来更新组件的state，不更新就返回null，不是覆盖式更新，而是针对某个属性的定向更新，不会替换原来的state，而是更新，也就是添加
render() react 16之前render方法必须返回元素，现在可以返回元素数组和字符串
componentDidMount()

更新阶段 
getDerivedStateFromProps()
shouldComponentUpdate()
render()
getSnapshotBeforeUpdate(prevProps, prevState) // 代替了compoenentWillUpdate
- 会作为第三个参数给到componenetDidUpdate()
- 在真实DOM更新之前，在render之后执行
- 同时获得更新前真实DOM和更新前后的state&props信息

compoenentDidUpdate()
react16.4和react16.3更新流程不一致，getDerivedStateFromProps 任何更新流程都会触发，而3只有父组件的触发才会走该生命周期。
为啥要用getDerivedStateFromProps？
- getDerivedStateFromProps是作为试图代替compoenentWillReceiveProps的APT而出现的
- getDerivedStateFromProps 不能喝compoenentWillReceiveProps划等号
- getDerivedStateFromProps 现在只能做基础props更新state

卸载阶段
没变

## Fiber架构
是对React16对React核心算法的一次重写
Fiber会使原本同步的渲染过程变成异步的
- 将大的更新任务拆分成许多个小任务
- 可以被打断的异步渲染模式
- 但这个“打断”是有原则的，根据“能否被打断”这一标准，React 16 的生命周期被划分为了 render 和 commit 两个阶段，而 commit 阶段又被细分为了 pre-commit 和 commit。每个阶段所涵盖的生命周期如下图所示：
- render 阶段在执行过程中允许被打断，而 commit 阶段则总是同步执行的。
- render 阶段是允许暂停、终止和重启的。当一个任务执行到一半被打断后，下一次渲染线程抢回主动权时，这个任务被重启的形式是“重复执行一遍整个任务”而非“接着上次执行到的那行代码往下走”。这就导致 render 阶段的生命周期都是有可能被重复执行的。
- React 16 改造生命周期的主要动机是为了配合 Fiber 架构带来的异步渲染机制
- React 团队精益求精，针对生命周期中长期被滥用的部分推行了具有强制性的最佳实践。这一系列的工作做下来，首先是确保了 Fiber 机制下数据和视图的安全性，同时也确保了生命周期方法的行为更加纯粹、可控、可预测。

