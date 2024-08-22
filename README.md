# CloudCamSync

CloudCamSync是一款开源的监控视频自动备份工具，其有一部分代码来源于开源项目CameraNVR(https://github.com/topak47/CameraNVR)，支持将监控视频上传到多种云存储服务，包括百度网盘、Google Drive和OneDrive。该工具旨在为用户提供一个多功能、灵活的解决方案，帮助用户管理和备份监控摄像头的视频数据。该软件主要作用是省钱：（1）将实时产生的监控视频上传到云端，节省本地存储的费用（2）软件很小，可在任何支持python的环境中运行，节省设备的费用。


# 主要功能
1、多云存储支持：支持百度网盘、Google Drive和OneDrive，可以同时将视频备份到多个云存储服务中。  
2、多摄像头支持：支持最多6个摄像头的同时视频捕获和处理，可以满足大多数需求。  
3、运动检测及活动视频录制：可选的活动视频保存与上传功能。利用背景减除算法，检测到当活动时间大于用户定义的时间，判断此时为活动视频。开始录制视频，并将其分类存储。背景减除算法部分代码来源于开源项目CameraNVR。  
4、全时段录制：可选的支持全时段视频录制，无需依赖运动检测。  
5、视频加密：可选的7z格式视频加密功能，密码完全由用户自定义，保障视频文件的安全性。在节省费用的同时兼顾隐私保护。  
6、网盘空间管理：自动检测云盘剩余空间，及时删除旧视频以释放空间。网盘的空间管理功能的代码全部来源于开源项目CameraNVR。  
7、邮件提醒：用户可自行配置smtp邮件服务器，运动检测到活动视频可以触发邮件提醒，通知用户发生了摄像头捕捉的运动。当检测到活动视频时，用户可以收到包含活动视频时间和截图的邮件提醒。  
8、摄像头状态报告：可设置的时间，定期生成并发送摄像头状态报告，确保监控系统的正常运行。  
9、灵活的云盘上传和本地存储选项：用户可以根据需求选择视频的存储方式，包括上传到云盘、保存在本地，或者同时进行。视频存储可选择仅保存检测到的运动视频、全部视频，或两者兼有。具体细节如下：  
（1）定时录制视频：摄像头可设定为持续定时录制，不再依赖运动检测启动录像。  
（2）录像分类：检测到运动时，将视频保存至“motion”文件夹并重命名为包含“motion”字样的文件；全时段录制的视频则保存在“full”文件夹。  
（3）灵活上传策略：用户可以选择是否上传“motion”文件夹中的运动视频，或“full”文件夹中的全部录制视频。  
（4）灵活保留策略：用户可以选择是否保留本地的“motion”视频或“full”视频。  
10、动态文件夹命名和多线程处理：  
（1）日期文件夹：在本地和云盘中，文件夹结构自动生成，格式为 YYYY-MM-DD/摄像头名称/。  
（2）路径动态生成：在上传视频文件时，系统会动态生成当天日期和摄像头名称的文件夹路径。  
11、多线程处理：每个摄像头独立使用线程处理视频捕获和上传，确保高效运行。


#功能对比：CloudCamSync vs CameraNVR  
CloudCamSync相比于CameraNVR，提供了以下新增和改进的功能：

# 新增功能  
1、多云存储支持：除了CameraNVR支持的百度网盘和阿里云盘，CloudCamSync还支持Google Drive和OneDrive，提供更多的云存储选择。  
2、视频加密：CloudCamSync新增了视频加密功能，支持将视频文件压缩并加密为7z格式，以提高数据的安全性。  
3、邮件提醒功能：CloudCamSync引入了邮件提醒功能，可以在检测到运动视频时，自动向用户发送通知邮件，邮件内容为检测到运动视频的时间、运动视频的截图，提供更及时的安全提醒。即使选择视频文件加密也不会影响该功能正常运行。但是后续需要自己去云盘或本地输入自己设定的压缩包密码解密查看。  
4、摄像头状态报告：定期生成并发送摄像头状态报告，确保监控系统的正常运行，这在CameraNVR中并未实现。  
5、运动检测功能部分更新：用户可自定义检测到运动的时间，当活动时间大于用户定义的时间，判断此时为活动视频。  
6、视频的存储方式给了用户更多的自由选择。

# 删减功能  
1、阿里云盘支持：CloudCamSync中移除了对阿里云盘的支持，改为支持Google Drive和OneDrive。因为阿里云盘不支持上传加密压缩包。  
本地视频分类细化：虽然CloudCamSync仍然支持按运动检测和全时段录制进行视频分类，但对本地文件夹结构的管理有所简化，减少了对不同视频类别的细粒度控制。

#其他  
本软件优化了云存储的功能。软件的重点功能在云存储与同步功能。为突出软件的重点，将软件名更改为CloudCamSync。

作者声明：使用本软件时，用户必须遵守所在国的法律以及云盘供应商的规定。作者坚决反对任何利用该程序进行违法犯罪的行为，包括但不限于侵犯他人隐私。由于个人能力有限，本源码可能存在缺陷，无法保证其在所有环境下正常运行。请勿将其用于商业用途，对于因使用该源码导致的任何问题，作者概不负责，仅供学习和参考之用。特别注意：涉及隐私的视频请勿使用本源码进行处理，上传到网盘可能存在泄露风险！

感谢各位大佬的分享的参考源码：

https://github.com/topak47/CameraNVR

https://github.com/wfxzf/pyNvr

https://github.com/houtianze/bypy

https://github.com/foyoux/aligo



  

# 使用教程(以下为CloudCamSync的教程，有部分修改自CameraNVR作者所撰写的CameraNVR的使用教程。可供参考。)
[![监控视频，自动备份到百度网盘和阿里云盘！](https://res.cloudinary.com/marcomontalbano/image/upload/v1692928086/video_to_markdown/images/youtube--hWiwCpJyk0M-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://youtu.be/hWiwCpJyk0M "监控视频，自动备份到百度网盘和阿里云盘！")


# 安装教程

确保你已经安装了python3.0以上版本,可以通过下方命令查询是否安装。

*   执行命令：
 
        python3 --version

### 您需要安装以下依赖项：

#### 1，安装pip用于安装和管理Python软件包的命令行工具

*   执行命令：
 
        sudo apt-get install python3-pip


#### 2，安装bypy百度网盘库，用于百度网盘的文件上传和管理。

*   执行命令：
 
        pip3 install bypy
       
*   登录百度网盘获取cookie：
 
        bypy info
    
  登录网盘后，复制终端里的百度网盘地址到浏览器打开，登录后获取cookie，然后黏贴到终端窗口回车

#### 3，安装OpenCV库，用于视频捕获、处理和录制。您可以通过以下命令使用pip安装：

*   执行命令：
 
        pip3 install opencv-python


#### 4，下载git工具

*   执行命令：
 
        apt install git

#### 5，下载源码

*   执行命令：
 
        git clone https://github.com/CloudCamSync/CloudCamSync.git


修改CloudCamSync.py里面的配置：

* Networkdisk = [1]  # 选择网盘 ([1] 表示百度网盘；[2] 表示阿里云网盘；[1, 2]同时选择两个网盘)  
* Cameraname = 'videos'  # 摄像头名称，支持自定义  
* videopath = '/Camera/'  # 本地文件路径，支持自定义  
* NVRurl = '根据摄像头填写'  # 视频流URL ，根据你摄像头的NVR地址来填写  
* videotime = 1  # 录制视频时长（分钟，范围：1-1000）  
* Updisk = True  # 是否上传到网盘？（True 表示上传；False 表示不上传）  
* deletevd = True  # 上传后是否删除视频文件？（True 表示删除；False 表示保留）  
* motion_frame_interval = 3  # 背景减除帧间隔，表示只每隔3帧进行一次运动检测，这样做的目的是为了减少运动检测的频率，节省计算资源。  
* Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB），当网盘的剩余可用空间低于或等于这个阈值时，系统会删除最早上传的视频，以防止网盘的空间不足。  
* upload_threshold = 500  # 视频上传总大小阈值（GB），当视频累计上传到这个阈值后，开始自动检测网盘百度网盘和阿里云盘的空间容量是否足够，不够采取删除！  

# 配置
*Networkdisk = [1, 2, 3]  # 选择网盘 ([1] 百度网盘；[2] Google Drive；[3] OneDrive；可以同时选择多个网盘)  
*Cameras = [
    {'name': 'camera1', 'NVRurl': 'URL_1'},  # 配置第一个摄像头
    {'name': 'camera2', 'NVRurl': 'URL_2'},  # 配置第二个摄像头
    {'name': 'camera3', 'NVRurl': 'URL_3'},  # 配置第三个摄像头
    {'name': 'camera4', 'NVRurl': 'URL_4'},  # 配置第四个摄像头
    {'name': 'camera5', 'NVRurl': 'URL_5'},  # 配置第五个摄像头
    {'name': 'camera6', 'NVRurl': 'URL_6'}   # 配置第六个摄像头
]#摄像头名称，支持自定义  
*videopath = '/Camera/'  # 本地文件路径，支持自定义                                             
*videotime = 1  # 录制视频时长（分钟，范围：1-1000），支持自定义  
*Updisk_motion = True  # 是否上传检测到运动的录像到网盘？（True 上传；False 不上传），支持自定义  
*Updisk_full = True  # 是否上传全部录像到网盘？（True 上传；False 不上传），支持自定义                    
*deletevd_motion = True  # 是否保留检测到运动的本地录像？（True 删除；False 保留），支持自定义  
*deletevd_full = True  # 是否保留全部录像的本地文件？（True 删除；False 保留），支持自定义  
*motion_frame_interval = 3  # 背景减除帧间隔，支持自定义   
*motion_duration_threshold = 5  # 活动持续时间阈值（秒），支持自定义   
*Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB），支持自定义   
*upload_threshold = 500  # 视频上传总大小阈值（GB），支持自定义   
*encrypt_videos = True  # 是否加密视频（True 加密；False 不加密），支持自定义  
*encryption_password = "your-password"  # 用户自定义的加密密码，支持自定义  
*use_email_alerts = True  # 是否启用邮件提醒，支持自定义   
*smtp_server = "smtp.example.com"  # SMTP服务器地址，支持自定义   
*smtp_port = 587  # SMTP服务器端口，支持自定义   
*email_sender = "sender@example.com"  # 发送方邮箱地址，支持自定义   
*email_receiver = "receiver@example.com"  # 接收方邮箱地址，支持自定义   
*email_password = "your-email-password"  # 发送方邮箱密码，支持自定义    
*use_status_report = True  # 是否启用摄像头状态报告，支持自定义   
*status_report_interval = 3600  # 状态报告发送间隔时间（秒），支持自定义    


#### 6，运行测试

*  执行命令：
 
        python3 CloudCamSync.py

 运行后可登录云盘！测试没问题后，ctrl+z退出运行

 #### 7，后台运行程序:

*  执行命令：
 
        nohup python3 CloudCamSync.py > nohup.out 2>&1 &


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


