#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import sys, getopt, datetime

img_path = ''

def run(argv):
    filePath = ''
    categories = ''
    tags = ''
    if len(argv) > 0:
        if argv[0] == '-g':
            try:
                opts, args = getopt.getopt(argv, "hgp:c:t:", ["filePath=", "categories=", "tags="])
            except getopt.GetoptError:
                print 'article.py -g -p <filePath> -c <categories> -t <tags>'
                sys.exit(2)
            for opt, arg in opts:
                if opt == '-h':
                    print 'article.py -g -p <filePath> -c <categories> -t <tags> -----------------生成文章\n' \
                          'article.py -s         -------------------------------------------------提交文章\n' \
                          'article.py -rm <fileName>         -------------------------------------删除文章'
                    sys.exit()
                elif opt == '-p':
                    filePath = arg
                    print 'filePath is ' + filePath
                elif opt == '-c':
                    categories = arg
                    print 'categories is ' + categories
                elif opt == '-t':
                    tags = arg
                    print 'tags is ' + tags
            genrate(filePath, categories, tags)
        elif (argv[0] == '-s') and len(argv) == 1:
            submit()
        elif (argv[0] == '-rm') and len(argv) == 2:
            delArticle(argv[1])
        else:
            print 'article.py -g -p <filePath> -c <categories> -t <tags> -----------------生成文章\n' \
                  'article.py -s         -------------------------------------------------提交文章\n' \
                  'article.py -rm <fileName>         -------------------------------------删除文章'
            sys.exit()

    else:
        print 'article.py -g -p <filePath> -c <categories> -t <tags> -----------------生成文章\n' \
              'article.py -s             ---------------------------------------------提交文章\n' \
              'article.py -rm <fileName>         -------------------------------------删除文章'
        sys.exit()

def genrate(filePath, categories, tags):
    # 文件预处理
    (fp, fn) = os.path.split(filePath)
    (shortName, extension) = os.path.splitext(fn)
    cates = categories.split(',')
    ts = tags.split(',')
    inputFile = open(filePath, 'r')
    os.popen('mkdir source/_posts/' + shortName)
    content = inputFile.read()
    urls = re.findall('(' + img_path + '(.+?\.(png|jpg|jpeg)))', content, re.S)
    for url in urls:
        os.popen('cp ' + url[0].replace(' ', '\\ ') + ' source/_posts/' + shortName)
    content = content.replace(img_path, shortName + '/')
    outputFile = open('source/_posts/' + fn, 'wb')

    # 插入<!--more-->
    more_index = 0
    more_count = 0
    for c in content:
        more_index += 1
        if c == '\n':
            more_count += 1
            if more_count == 8:
                break

    print more_index
    content_list = list(content)
    content_list.insert(more_index, '\n<!--more-->\n')
    content = "".join(content_list)

    # 写文章头部信息
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    head = '---\n' + 'title: ' + shortName + '\ndate: '
    head = head + now + '\n'
    head = head + 'tags:\n'
    for t in ts:
        tinfo = '- ' + t + '\n'
        head += tinfo
    head = head + 'categories:\n'
    for c in cates:
        cinfo = '- ' + c + '\n'
        head += cinfo
    head = head + '---\n'
    outputFile.write(head)

    # 写入新文件
    outputFile.write(content)
    inputFile.close()
    outputFile.close()

def submit():
    os.popen('git checkout -b hexo')
    os.system('hexo d -g')
    os.popen('git add .')
    os.popen('git commit -m "updated"')
    os.popen('git push origin hexo')

def delArticle(fileName):
    os.popen('rm -rf source/_posts/' + fileName + '*')

if __name__ == '__main__':
    img_path = '/Users/xiongzhigang/Library/Application Support/typora-user-images/'
    run(sys.argv[1:])
