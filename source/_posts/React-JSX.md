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