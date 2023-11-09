### Lab3 TCP对等通信协议

#### 1.1 实验目的

    通过该实验了解和掌握与对等方通信的协议,实现与对等方的通信

#### 1.2 实验环境

* 语言工具: 基于Python语言实现
* 操作系统: Windows

#### 1.3 实验要求

    根据lab3.md文档和完成src/torrent/message框架代码,通过test_download测试

#### 2.1 TCP Peer wire protocol介绍

    对等协议促进了片段的交换。客户端必须维护它与远程对等方的每个连接的状态信息。

    流程解析:
    1. 开启和对等方的TCP连接
    2. 完成HandShake
        * 请求方发送握手信息(1+19+8+20+20)
        * 握手信息格式(0x13 + 'BitTorrent protocol' + 00000000 + info_hash + peer_id)
        * 解析回传的握手信息，确保info_hash匹配
    3. 发送和接受信息

#### 2.2 通信方式

    整个下载过程中要不断的交换信息。通信流程如下:
    在接受了peer的握手之后，会收到一条bitfield信息，它的payload是一串位数组（bitarray），也就是c里的bitmap。
    payload里比特的个数等于我们想要下载的文件被分成piece的总个数，每一个比特代表这个peer是否拥有这个piece。1代表现在和我们联系的peer有这个piece，只需要发送请求就能下载，0则代表它现在没有这个piece。
    每一个客户端和peer取得联系后的初始状态都是uninterested和choked。
    uninterested指的是我们并没有向peer请求数据的兴趣。
    choked指的是我们无法向peer请求任何数据。按字面意思形象地理解就是我们被peer掐住（choke）了，只有对面把手松开才能出声。
    因此在收到了bitfield之后，当务之急是向peer发送一条interested信息，只有这样对方才能松手（unchoke）。

* 信息格式 length id payload
* length: id和payload的总长度，单位为字节
* id: 用来识别不同类型的信息,长度为1字节
* payload: 可有可无，长度和内容由信息类型决定

消息详解:

* keep-alive: <len=0000> 保持活动状态
* choke: <len=0001><id=0> 阻塞
* unchoke: <len=0001><id=1> 不阻塞
* interested: <len=0001><id=2> 感兴趣
* not interested: <len=0001><id=3> 不感兴趣
* have: <len=0005><id=4><piece index> 拥有
* bitfield: <len=0001+X><id=5><bitfield>
* request: <len=0013><id=6><index><begin><length> 请求

#### 3.1 任务框架

    参见 src/torrent/message.py,完成多种Message信息的编解码



