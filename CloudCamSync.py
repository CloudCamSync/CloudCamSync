from bypy import ByPy  # 百度网盘第三方API 开源地址：https://github.com/houtianze/bypy
import onedrivesdk  # OneDrive SDK
import os
import cv2
import time
import threading
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import py7zr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 配置
Networkdisk = [1, 2, 3]  # 选择网盘 ([1] 百度网盘；[2] Google Drive；[3] OneDrive；可以同时选择多个网盘)
Cameras = [
    {'name': 'camera1', 'NVRurl': 'URL_1'},  # 配置第一个摄像头
    {'name': 'camera2', 'NVRurl': 'URL_2'},  # 配置第二个摄像头
    {'name': 'camera3', 'NVRurl': 'URL_3'},  # 配置第三个摄像头
    {'name': 'camera4', 'NVRurl': 'URL_4'},  # 配置第四个摄像头
    {'name': 'camera5', 'NVRurl': 'URL_5'},  # 配置第五个摄像头
    {'name': 'camera6', 'NVRurl': 'URL_6'}   # 配置第六个摄像头
]
videopath = '/Camera/'  # 本地文件路径                                           
videotime = 1  # 录制视频时长（分钟，范围：1-1000）
Updisk_motion = True  # 是否上传检测到运动的录像到网盘？（True 上传；False 不上传）
Updisk_full = True  # 是否上传全部录像到网盘？（True 上传；False 不上传）                   #CameraNVR(https://github.com/topak47/CameraNVR)
deletevd_motion = True  # 是否保留检测到运动的本地录像？（True 删除；False 保留）
deletevd_full = True  # 是否保留全部录像的本地文件？（True 删除；False 保留）
motion_frame_interval = 3  # 背景减除帧间隔
motion_duration_threshold = 5  # 活动持续时间阈值（秒）
Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB）
upload_threshold = 500  # 视频上传总大小阈值（GB）
encrypt_videos = True  # 是否加密视频（True 加密；False 不加密）
encryption_password = "your-password"  # 用户自定义的加密密码
use_email_alerts = True  # 是否启用邮件提醒
smtp_server = "smtp.example.com"  # SMTP服务器地址
smtp_port = 587  # SMTP服务器端口
email_sender = "sender@example.com"  # 发送方邮箱地址
email_receiver = "receiver@example.com"  # 接收方邮箱地址
email_password = "your-email-password"  # 发送方邮箱密码
use_status_report = True  # 是否启用摄像头状态报告
status_report_interval = 3600  # 状态报告发送间隔时间（秒）

# 初始化 OneDrive 客户端
def init_onedrive_client():
    client_id = 'your-client-id'  # 替换为你的客户端ID
    client_secret = 'your-client-secret'  # 替换为你的客户端机密
    redirect_uri = 'http://localhost:8080/'  # 替换为你的重定向URI

    client = onedrivesdk.get_default_client(client_id=client_id, scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite'])

    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    # 打印 URL 并在浏览器中访问以授权应用程序
    print("请在浏览器中访问以下 URL 并登录授权：\n{0}".format(auth_url))

    # 获取授权码
    code = input('输入浏览器中提供的代码：')

    client.auth_provider.authenticate(code, redirect_uri, client_secret)

    return client

# 初始化 Google Drive 客户端
def init_google_drive_client():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

# 获取文件上传的总大小
def get_uploaded_size():
    total_size = 0
    for root, dirs, files in os.walk(videopath):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
    return total_size

def bysync(file, path, i, deletevd):
    if i >= 3:
        print(file + " 上传错误，请检查网络、网盘账户和路径。")
        return
    time.sleep(10)
    print(file + " 正在上传到百度网盘......")
    bp = ByPy()
    code = bp.upload(file, '/' + path + '/', ondup='overwrite')  # 使用覆盖上传方式
    if code == 0:
        if deletevd:
            os.remove(file)
        print(file + " 上传成功！")
    else:
        i += 1
        print(file + " 重试次数: " + str(i))
        bysync(file, path, i, deletevd)                            #开源地址https://github.com/topak47/CameraNVR

def google_drive_sync(file, path, i, deletevd, service):
    if i >= 3:
        print(file + " 上传错误，请检查网络、网盘账户和路径。")
        return
    time.sleep(10)
    print(file + " 正在上传到 Google Drive......")
    
    try:
        # 在云盘中创建日期文件夹
        folder_name = path.split('/')[0]
        camera_folder_name = path.split('/')[1]
        
        # 查找或创建文件夹
        def get_folder_id(folder_name, parent_id=None):
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            results = service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
                if parent_id:
                    file_metadata['parents'] = [parent_id]
                folder = service.files().create(body=file_metadata, fields='id').execute()
                return folder.get('id')
            else:
                return items[0]['id']

        root_folder_id = get_folder_id(folder_name)
        camera_folder_id = get_folder_id(camera_folder_name, root_folder_id)

        file_metadata = {'name': os.path.basename(file), 'parents': [camera_folder_id]}
        media = MediaFileUpload(file, mimetype='video/avi')
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        if deletevd:
            os.remove(file)
        print(file + " 上传成功！")
    except Exception as e:
        print(e)
        i += 1
        print(file + " 重试次数: " + str(i))
        google_drive_sync(file, path, i, deletevd, service)       #开源地址https://github.com/topak47/CameraNVR

def onedrive_sync(file, path, i, deletevd, client):
    if i >= 3:
        print(file + " 上传错误，请检查网络、网盘账户和路径。")
        return
    time.sleep(10)
    print(file + " 正在上传到 OneDrive......")
    
    try:
        # 在云盘中创建日期文件夹
        folder_name = path.split('/')[0]
        camera_folder_name = path.split('/')[1]
        
        root_folder = client.item(drive='me', id='root').children[folder_name].get()
        if not root_folder:
            root_folder = client.item(drive='me', id='root').children[folder_name].create_folder().post()

        camera_folder = client.item(drive='me', id=root_folder.id).children[camera_folder_name].get()
        if not camera_folder:
            camera_folder = client.item(drive='me', id=root_folder.id).children[camera_folder_name].create_folder().post()

        client.item(drive='me', id=camera_folder.id).children[file].upload(file).post()

        if deletevd:
            os.remove(file)
        print(file + " 上传成功！")
    except Exception as e:
        print(e)
        i += 1
        print(file + " 重试次数: " + str(i))
        onedrive_sync(file, path, i, deletevd, client)

# 7z加密函数
def encrypt_and_compress_file(file_path, password):
    compressed_file_path = file_path + '.7z'
    with py7zr.SevenZipFile(compressed_file_path, 'w', password=password) as archive:
        archive.write(file_path, arcname=os.path.basename(file_path))
    return compressed_file_path

# 邮件发送函数
def send_email(subject, body, image_path=None):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if image_path:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(img)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
        print("邮件已发送。")
    except Exception as e:
        print(f"邮件发送失败：{e}")

def capture(camera, videopath, videotime, Updisk_motion, Updisk_full, deletevd_motion, deletevd_full, Networkdisk, Networkdisk_space_threshold, upload_threshold, onedrive_client, google_drive_client, encrypt_videos, encryption_password, motion_duration_threshold):
    Cameraname = camera['name']
    NVRurl = camera['NVRurl']

    try:
        print(f"正在捕获摄像头 {Cameraname} 的视频流...")
        cap = cv2.VideoCapture(NVRurl)
    except:
        print(f"无法捕获摄像头 {Cameraname} 的视频流，请检查URL或网络连接。")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps >= 30:
        fps = 30
    elif fps <= 0:
        fps = 15
    print("fps: " + str(fps))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("视频尺寸: " + str(size))

    # 获取当天日期
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    # 本地保存路径
    motion_videopath = os.path.join(videopath, today_date, Cameraname, "motion")
    full_videopath = os.path.join(videopath, today_date, Cameraname, "full")

    if not os.path.exists(motion_videopath):
        try:
            os.makedirs(motion_videopath)
        except:
            print("请手动创建运动录像文件夹")
            return

    if not os.path.exists(full_videopath):
        try:
            os.makedirs(full_videopath)
        except:
            print("请手动创建全部录像文件夹")
            return

    # 初始化视频上传总大小变量
    video_total_size = 0

    bg_subtractor = cv2.createBackgroundSubtractorKNN()
    frame_counter = 0
    motion_start_time = None
    motion_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1

        fg_mask = bg_subtractor.apply(frame)
        motion_pixels = cv2.countNonZero(fg_mask)

        # 开始录制全时段视频
        full_video_filename = os.path.join(full_videopath, str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + '_full.avi')
        full_out = cv2.VideoWriter(full_video_filename, fourcc, fps, size)

        start_time = time.time()

        while time.time() - start_time < videotime * 60:
            ret, frame = cap.read()
            if not ret:
                break

            fg_mask = bg_subtractor.apply(frame)
            motion_pixels = cv2.countNonZero(fg_mask)

            if motion_pixels > 3000:                                         #CameraNVR开源地址https://github.com/topak47/CameraNVR
                if motion_start_time is None:
                    motion_start_time = time.time()
                elif time.time() - motion_start_time >= motion_duration_threshold:
                    motion_detected = True
            else:
                motion_start_time = None

            full_out.write(frame)

        full_out.release()

        # 如果检测到运动并且持续超过阈值，保存到运动录像文件夹
        if motion_detected:
            motion_video_filename = os.path.join(motion_videopath, str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + '_motion.avi')
            os.rename(full_video_filename, motion_video_filename)
            if encrypt_videos:
                motion_video_filename = encrypt_and_compress_file(motion_video_filename, encryption_password)
            if Updisk_motion:
                for disk in Networkdisk:
                    upload_path = f"{today_date}/{Cameraname}/motion"
                    if disk == 1:
                        sync = threading.Thread(target=bysync, args=(motion_video_filename, upload_path, 0, deletevd_motion))
                    elif disk == 2:
                        sync = threading.Thread(target=google_drive_sync, args=(motion_video_filename, upload_path, 0, deletevd_motion, google_drive_client))
                    elif disk == 3:
                        sync = threading.Thread(target=onedrive_sync, args=(motion_video_filename, upload_path, 0, deletevd_motion, onedrive_client))
                    sync.start()

            # 邮件提醒
            if use_email_alerts:
                image_filename = os.path.join(motion_videopath, str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + '_snapshot.jpg')
                cv2.imwrite(image_filename, frame)
                subject = f"运动检测提醒 - {Cameraname} - {today_date}"
                body = f"检测到运动视频，时间：{today_date}，摄像头：{Cameraname}"
                send_email(subject, body, image_filename)

        if Updisk_full:
            if encrypt_videos:
                full_video_filename = encrypt_and_compress_file(full_video_filename, encryption_password)
            for disk in Networkdisk:
                upload_path = f"{today_date}/{Cameraname}/full"
                if disk == 1:
                    sync = threading.Thread(target=bysync, args=(full_video_filename, upload_path, 0, deletevd_full))
                elif disk == 2:
                    sync = threading.Thread(target=google_drive_sync, args=(full_video_filename, upload_path, 0, deletevd_full, google_drive_client))
                elif disk == 3:
                    sync = threading.Thread(target=onedrive_sync, args=(full_video_filename, upload_path, 0, deletevd_full, onedrive_client))
                sync.start()

        video_total_size += os.path.getsize(full_video_filename)  # 更新视频总大小
        if video_total_size >= upload_threshold * (1024 * 1024 * 1024):
            check_and_delete_earlier_videos()  # 检测网盘空间并删除早期视频    #CameraNVR开源地址https://github.com/topak47/CameraNVR

    cv2.destroyAllWindows()
    cap.release()

def send_status_report(Cameras):
    report_content = "摄像头状态报告：\n\n"
    for camera in Cameras:
        report_content += f"摄像头: {camera['name']}\n"
        report_content += f"视频流 URL: {camera['NVRurl']}\n"
        report_content += "状态: 正常\n"  # 在实际应用中，这里可以通过更多的逻辑来判断摄像头状态
        report_content += "\n"

    subject = "摄像头状态报告"
    send_email(subject, report_content)

def status_report_thread(Cameras, interval):
    while True:
        if use_status_report:
            send_status_report(Cameras)
        time.sleep(interval)

if __name__ == '__main__':
    # 初始化 OneDrive 和 Google Drive 客户端
    onedrive_client = None
    google_drive_client = None

    if 3 in Networkdisk:
        onedrive_client = init_onedrive_client()
    if 2 in Networkdisk:
        google_drive_client = init_google_drive_client()

    # 启动摄像头状态报告线程
    if use_status_report:
        status_thread = threading.Thread(target=status_report_thread, args=(Cameras, status_report_interval))
        status_thread.daemon = True  # 设为守护线程
        status_thread.start()

    # 为每个摄像头启动一个线程进行视频捕获和处理
    threads = []
    for camera in Cameras:
        t = threading.Thread(target=capture, args=(camera, videopath, videotime, Updisk_motion, Updisk_full, deletevd_motion, deletevd_full, Networkdisk, Networkdisk_space_threshold, upload_threshold, onedrive_client, google_drive_client, encrypt_videos, encryption_password, motion_duration_threshold))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
