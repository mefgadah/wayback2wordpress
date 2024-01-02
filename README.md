# wayback2wordpress
crawl your old blog in archive.org to your new blog
从archive.org获取你原来的博客内容，然后发布到你的新博客，如果新博客不实用WordPress，可以相应的去使用其他博客程序的API或者使用wordpress创建个账号再导出xml文件，大多数的博客程序应该都支持WordPress的导出格式。

This program is generated with ChatGPT.I modified some. Wayback website has access limitations so i add time.sleep(60)

You need modify *archive_url*,line**58-80** for your blog html selector

程序使用ChatGPT生成,你也可以自己修改提示词去生成

```
我多年前的wordpress网站 在Internet Archive有快照，使用python3 写一个程序帮我从Internet Archive 获取我当时的博客内容，并使用wordpress_xmlrpc库发布到我的新wordpress。我的wordpress网址首页是 blogurl = http://xxx.info，下面按照顺序去帮我写程序
1.访问https://web.archive.org/web/timemap/json?url=xxx.info&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=10000&_=1703940417831 会返回json格式 类似这样
<<
[
[
    "http://xxx.info/?p=1005",
    "text/html",
    "20120618121042",
    "20120618121042",
    "1",
    "1"
  ],
  [
    "http://xxx.info:80/",
    "text/html",
    "20101113233908",
    "20131011205549",
    "41",
    "31"
  ],
[
    "http://xxx.info/archives/939",
    "text/html",
    "20120625150038",
    "20120625150038",
    "1",
    "1"
  ]
]
>>
子列表第一项为所有url，你需要提取出类似这两种url http://xxx.info/archives/939, http://xxx.info/?p=1005，其中939,1005是blog_id,blog_id是纯数字,提取后的blog_ids去重并保存成一个类似这样的old2new.json文件{blog_id:0,blog_another_id:0}到程序当前目录
2.读取1中的json文件，获取值是0的blog_id，循环访问http://web.archive.org/web/http://xxx.info/archives/939 其中939换成blog_id，这样就得到每篇博客文章的备份网页
3.使用BeautifulSoup解析第2步中获取的网页内容，为了导出成WordPress备份格式 我们需要找3个内容title、date、content,存在2种可能性的网页。如果2种可能性都不是，直接跳过 写到old2new.json文件中对应blog_id的值为-1，并开始第下一个blog_id
第一种可能性：其中title的class是entry-title，date的class是published，网页上date的格式是这样的“2011 年 6 月 2 日 at 下午 1:45”，为了使用wordpress_xmlrpc发布你可能需要转化一下时间格式，content的class是entry-content
第二种可能性：其中title的class是corner，date的class是edit的子节点ul的第1个子节点li，网页上date的格式是这样的“19 十二月, 2010 -”，为了使用wordpress_xmlrpc发布你可能需要转化一下时间格式，content的id是post

4.将所有第三步获取的每篇博客文章的title、date、content，使用wordpress_xmlrpc发布到我新的wordpress，每发布成功1篇，记录返回的新blog_id,并写到old2new.json文件中对应blog_id的值
```
