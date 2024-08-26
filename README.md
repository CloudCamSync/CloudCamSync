# CloudCamSync--开源的监控视频云盘自动备份工具，支持在Windows上将摄像头录像自动加密保存到云盘（百度云盘）中

#CloudCamSync 是一款开源的监控视频自动备份工具，支持将监控视频上传到云存储服务（百度网盘）。该工具旨在为用户提供一个多功能、灵活的解决方案，帮助用户管理和备份监控摄像头的视频数据。在如今的智能家居时代，许多家庭和企业依赖摄像头来进行监控，而这些摄像头通常会将视频数据存储到品牌自带的云盘上。然而，这些云盘服务通常按月收费，且限制较多，使得长期使用成本较高且灵活性不足。为了解决这些问题，结合Windows操作系统，我们推出了一款创新的产品——CloudCamSync。

#CloudCamSync是一款开源的监控视频自动备份工具，支持将监控视频上传到云存储服务（百度网盘）。该工具旨在为用户提供一个多功能、灵活的解决方案，帮助用户管理和备份监控摄像头的视频数据。该软件主要作用是省钱：（1）将实时产生的监控视频上传到云端，节省本地存储的费用（2）软件很小，可在任何支持python的环境中运行，节省设备的费用。这是专门针对Windows系统进行优化的软件，可在Windows中运行，支持将摄像头录像自动加密保存到云盘（百度云盘）中。

# CloudCamSync 主要功能
1、云存储支持：支持百度网盘，可以同时将视频备份到多云存储服务中。  
2、全时段录制：支持全时段视频录制，无需依赖运动检测。上传的每段时间的时间长度可自定义。  
3、视频加密：可选的7z格式视频加密功能，密码完全由用户自定义，保障视频文件的安全性。在节省费用的同时兼顾隐私保护。  
4、网盘空间管理：自动检测云盘剩余空间，及时删除旧视频以释放空间。网盘的空间管理功能的代码全部来源于开源项目CameraNVR。  
5、灵活的云盘上传和本地存储选项：用户可以根据需求选择视频的存储方式，包括上传到云盘、保存在本地，或者同时进行。
6、路径动态生成：在上传视频文件时，系统会动态生成当天日期和摄像头名称的文件夹路径。  
7、多线程处理：每个摄像头独立使用线程处理视频捕获和上传，确保高效运行。
8、视频文件的格式为MP4。

作者声明：使用本软件时，用户必须遵守所在国的法律以及云盘供应商的规定。由于个人能力有限，本源码可能存在缺陷，无法保证其在所有环境下正常运行。请勿将其用于商业用途，对于因使用该源码导致的任何问题，作者概不负责，仅供学习和参考之用。特别注意：涉及隐私的视频请勿使用本源码进行处理，上传到网盘可能存在泄露风险！

感谢各位大佬的分享的参考源码：

https://github.com/topak47/CameraNVR

https://github.com/wfxzf/pyNvr

https://github.com/houtianze/bypy



# 使用教程(以下为CloudCamSync的使用教程)


# 安装教程

在Windows上下载python安装包，安装python。确保你已经安装了python3.0以上版本,可以通过下方命令查询是否安装。

*   执行命令：
 
        python

### 您需要安装以下依赖项：

#### 1，安装pip用于安装和管理Python软件包的命令行工具

*   一般来说，Windows的python包中已经包含pip包，不需要再安装，可在cmd窗口中输入pip进行查询：
 
        pip

  如果返回大量配置参数，说明pip已经安装成功。
#### 2，安装bypy百度网盘库，用于百度网盘的文件上传和管理。

*   执行命令：
 
        pip install bypy
       
*   查看已经安装的pip包：
 
        pip list

*   登录百度网盘获取cookie：
 
        python -m bypy info
    
  登录网盘后，复制终端里的百度网盘地址到浏览器打开，登录后获取cookie，然后黏贴到终端窗口回车

#### 3，安装OpenCV库，用于视频捕获、处理和录制。您可以通过以下命令使用pip安装：

*   执行命令：
 
        pip install opencv-python

#### 4，安装py7zr库，用于7zip压缩包加密。您可以通过以下命令使用pip安装：

*   执行命令：
 
        pip install py7zr

#### 5，下载程序，并放入任意文件夹，右键点击该程序，以txt格式查看程序代码。

修改CloudCamSync-Windows.py里面的配置：

* Cameraname = 'videos'  # 摄像头名称，支持自定义  
* videopath = '/Camera/'  # 本地文件路径，支持自定义  
* NVRurl = '根据摄像头填写'  # 视频流URL ，根据你摄像头的NVR地址来填写  
* videotime = 1  # 录制视频时长（分钟，范围：1-1000）  
* Updisk = True  # 是否上传到网盘？（True 表示上传；False 表示不上传）  
* deletevd = True  # 上传后是否删除视频文件？（True 表示删除；False 表示保留）  
* Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB），当网盘的剩余可用空间低于或等于这个阈值时，系统会删除最早上传的视频，以防止网盘的空间不足。  
* upload_threshold = 500  # 视频上传总大小阈值（GB），当视频累计上传到这个阈值后，开始自动检测网盘百度网盘和阿里云盘的空间容量是否足够，不够采取删除！  

#### 6，进入放置有该程序的文件夹，将文件管理器的地址修改为cmd，并按回车确定。在打开的任务栏中，您可以通过以下命令执行程序，运行测试：

*   执行命令：
 
        python CloudCamSync.py

 运行后可软件会提示上传的结果！测试没问题后，ctrl+z退出运行

 #### 7，后台运行程序:

*  执行命令：
 
        nohup python3 CloudCamSync.py > nohup.out 2>&1 &


# 多摄像头的配置方式
可以复制新建多个程序，每个程序内部自由配置路径、录像时间、摄像头NVRurl，更改不同的名字，如CloudCamSync1.py，CloudCamSync2.py。


# 常见NVR摄像头码流
国内网络摄像机的端口及RTSP地址
#### 1，海康威视
* 默认IP地址：192.168.1.64/DHCP 用户名admin 密码自己设
* 端口：“HTTP 端口”（默认为 80）、“RTSP 端口”（默认为 554）、“HTTPS 端 口”（默认 443）和“服务端口”（默认 8000），ONVIF端口 80。
* 主码流：rtsp://admin:12345@192.0.0.64:554/h264/ch1/main/av_stream
* 子码流：rtsp://admin:12345@192.0.0.64/mpeg4/ch1/sub/av_stream

#### 2，大华
* 默认IP地址：192.168.1.108 用户名/密码：admin/admin
* 端口：TCP 端口 37777/UDP 端口 37778/http 端口 80/RTSP 端口号默认为 554/HTTPs 443/ONVIF 功能默认为关闭，端口80
* RTSP地址：rtsp://username:password@ip:port/cam/realmonitor?channel=1&subtype=0

#### 3，雄迈/巨峰
* 默认IP地址：192.168.1.10 用户名admin 密码空
* 端口：TCP端口：34567 和 HTTP端口：80，onvif端口是8899
* RTSP地址：rtsp://10.6.3.57:554/user=admin&password=&channel=1&stream=0.sdp?

#### 4，天视通
* 默认IP地址：192.168.0.123 用户名admin 密码123456
* 端口：http端口80 数据端口8091 RTSP端口554 ONVIF端口 80
* RTSP地址：主码流地址:rtsp://192.168.0.123:554/mpeg4
* 子码流地址:rtsp://192.168.0.123:554/mpeg4cif
* 需要入密码的地址： 主码流 rtsp://admin:123456@192.168.0.123:554/mpeg4
* 子码流 rtsp://admin:123456@192.168.0.123:554/mpeg4cif

#### 5，中维/尚维
* 默认IP地址：DHCP 默认用户名admin 默认密码 空
* RTSP地址：rtsp://0.0.0.0:8554/live1.264（次码流）
* rtsp://0.0.0.0:8554/live0.264 (主码流)

#### 6，九安
* RTSP地址：rtsp://IP:port（website port）/ch0_0.264（主码流）
* rtsp://IP:port（website port）/ch0_1.264（子码流）

#### 7，技威/YOOSEE
* 默认IP地址：DHCP 用户名admin 密码123
* RTSP地址：主码流：rtsp://IPadr:554/onvif1
* 次码流：rtsp://IPadr:554/onvif2
* onvif端口是5000
* 设备发现的端口是3702

#### 8，V380
* 默认IP地址：DHCP 用户名admin 密码空/admin
* onvif端口8899
* RTSP地址：主码流rtsp://ip//live/ch00_1
* 子码流rtsp://ip//live/ch00_0

#### 9，宇视
* 默认IP地址： 192.168.0.13/DHCP 默认用户名 admin 和默认密码 123456
* 端口：HTTP 80/RTSP 554/HTTPS 110(443)/onvif端口 80
* RTSP地址：rtsp://用户名:密码@ip:端口号/video123 123对应3个码流

#### 10，天地伟业
* 默认IP地址：192.168.1.2 用户名“Admin”、密码“1111”
* onvif端口号“8080”
* RTSP地址：rtsp：//192.168.1.2

#### 11，巨龙/JVT
* 默认IP地址：192.168.1.88 默认用户名 admin 默认密码admin
* 主码流地址:rtsp://IP地址/av0_0
* 次码流地址:rtsp://IP地址/av0_1
* onvif端口 2000

#### 12，TP-Link/水星安防
* 默认IP地址：192.168.1.4   用户名“Admin”、密码“app里设置”
* 主码流地址:rtsp://user:password@ip:554/stream1
* 次码流地址:rtsp://user:password@ip:554/stream2


