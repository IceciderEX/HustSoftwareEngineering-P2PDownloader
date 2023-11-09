### Lab4 解析磁力链接并转换为torrent文件

#### 1.1 实验目的

    1. 通过该实验了解和掌握magnetlink的格式，以及其与torrent文件的关系
    2. 对磁力链接进行转换，获取对应的.torrent文件。

#### 1.2 实验环境

* 语言工具: 基于Python语言实现
* 操作系统: Windows

#### 1.3 实验要求

    1. 根据lab4.md文档和完成src/magnetlink/MagnetlinkParser.py框架代码,通过test/test_magnetlink_parser.py的测试

#### 2.1 磁力链接介绍

磁力链接是一个字符串，它包含了该磁力链接对应文件的info_hash, display_name, trackers等等信息，这些信息实际上与.torrent文件中包含的相关信息是一样的，只是磁力链接相较于.torrent文件是一个更加直观的字符串。它实际起到的作用与.torrent文件是类似的。因此，可以实现磁力链接与.torrent文件的相互转换。

#### 2.2 磁力链接格式介绍

  磁力链接的格式通常为"magnet:?xt=urn:btih:哈希值(info_hash)&dn=文件名(display_name)&tr=Tracker(服务器地址)"。其中，xt表示链接类型，urn:btih表示文件哈希值，dn表示文件名，tr表示Tracker服务器地址。

* 详细信息可以参考[wiki百科]([Magnethttps://en.wikipedia.org/wiki/Magnet_URI_scheme)

#### 2.3 解析磁力链接，封装到类

    实现MagnetlinkParser类中的给定接口,完成磁力链接正则表达式的编写与解析磁力链接的任务，并封装到Magnetlink类。

#### 2.4 实现磁力链接到.torrent文件的转换

要想通过磁力链接下载文件，大部分磁力链接只包含文件的info_hash，所以本质上还是要通过此info_hash得到该磁力链接对应的.torrent文件，才能进一步得到piece_length，trackers等等信息。
因为我们并没有如同种子文件服务器拥有的相关数据，所以，要将磁力链接转换为.torrent文件，只能通过调用网络上的API完成。在本项目中，我们选择向一个在线磁力链接转换.torrent文件的网站发送HTTP Request，并接收该网站返回的Response（.torrent)文件，以实现磁力链接到.torrent文件的转换。
	

#### 3.1 任务框架

    参见 src/magnetlink/MagenetlinkParser.py
    由于.torrent向磁力链接的转换类似，不要求读者自己独立完成