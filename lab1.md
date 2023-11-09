### Lab1 解析torrent文件

#### 1.1 实验目的
    通过该实验了解和掌握.torrent文件的编码格式，能够正确解析和加密Bencode格式

#### 1.2 实验环境
   * 语言工具: 基于Python语言实现
   * 操作系统: Windows

#### 1.3 实验要求
    根据lab1.md文档和完成src/torrent/bencoding.py框架代码,通过test/test_bencoding.py的测试

#### 2.1 torrent文件介绍
    要实现下载文件的功能，我们得知道需要下载的文件是什么，以及去哪儿才能找到拥有数据的用户（Peer）。这些信息一般都能在.torrent文件（也就是大家俗称的种子文件）里找到。.torrent文件的信息存储用的Bencode的编码。因此想要读取有用的内容，首先要做的就是解析.torrent文件。

#### 2.2 Bencode 编码格式介绍
    Bencode并不复杂,它只支持四种类型，分别是字符串（String），整数（Integer），串列（List）以及字典表（Dictionary），本质上和JSON一样。

*  整数
    * 编码方式: i[num]e。以i标志开始,e标志结束,将数插在中间
    * 示例: i3e 表示整数“3”
    * 示例：i-3e 表示整数“-3”
*  字符串
   *  编码方式: num:string。 长度 冒号 字符串
   *  示例：4：spam 表示字符串“spam”
   *  示例：0：表示空字符串 “”
*  列表
   *  编码方式:l [bencode value] e 列表是一个递归定义类型,以l开始,以e结束
   *  示例：l4：spam4：egge 表示两个字符串的列表：[ “spam”， “eggs” ]
   *  示例：le 表示空列表：[]
*  字典
   *  编码方式: d[bencoded string][bencoded element]e。初始 d 和尾随 e 是开始分隔符和结束分隔符。请注意，密钥必须是编码的字符串。这些值可以是任何编码类型，包括整数、字符串、列表和其他字典。键必须是字符串，并按排序顺序显示（排序为原始字符串，而不是字母数字）。应使用二进制比较来比较字符串，而不是使用特定于区域性的“自然”比较来比较字符串。
   *  示例：d3：cow3：moo4：spam4：eggse 表示字典 { “cow” => “moo”， “spam” => “eggs” }
   *  示例：d4：spaml1：a1：bee 表示字典 { “spam” => [ “a”， “b” ] }
   *  示例：d9：publisher3：bob17：publisher-webpage15：www.example.com18：publisher.location4：homee 表示 { “publisher” => “bob”， “publisher-webpage” => “www.example.com”， “publisher.location” => “home” }
   *  示例：de 表示空字典 {}

#### 3.1 任务框架
    参见 src/torrent/bencoding.py



