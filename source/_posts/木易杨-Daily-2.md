---
title: 木易杨-Daily-2
date: 2020-11-03 20:00:39
tags:
---

# 第 148 题：['1', '2', '3'].map(parseInt) what & why ?
答案是 `[ 1, NaN, NaN ]`
map中的方法是function(item, index, arr){}
在此处换成parseInt的话，传给parseInt的参数是item和index
而parseInt本身接收两个参数parseInt(string, radix)string为元素，radix为解析的基数
parseInt('1', 0) //radix为0时，且string参数不以“0x”和“0”开头时，按照10为基数处理。这个时候返回1
parseInt('2', 1) //基数为1（1进制）表示的数中，最大值小于2，所以无法解析，返回NaN
parseInt('3', 2) //基数为2（2进制）表示的数中，最大值小于3，所以无法解析，返回NaN

