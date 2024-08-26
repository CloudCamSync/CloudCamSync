# 引用模块
from bypy import ByPy     # 百度网盘第三方API  开源地址：https://github.com/houtianze/bypy
import os
import cv2
import time
import threading
import py7zr  # 7zip压缩库

# 配置
Cameraname = 'videos111'  # 摄像头名称
videopath = 'N:'  # 本地文件路径
NVRurl = 'rtsp://admin:MMTESM@192.168.0.109:554/h264/ch1/main/av_stream'  # 视频流URL 
videotime = 1  # 录制视频时长（分钟，范围：1-1000）
Updisk = True  # 是否上传到网盘？（True 表示上传；False 表示不上传）
deletevd = True  # 上传后是否删除视频文件？（True 表示删除；False 表示保留）
Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB）
upload_threshold = 500  # 视频上传总大小阈值（GB）


# 获取文件上传的总大小
def get_uploaded_size():
    total_size = 0
    for root, dirs, files in os.walk(videopath):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
    return total_size

# 压缩并加密文件
def compress_and_encrypt(file, password):
    compressed_file = file + '.7z'
    with py7zr.SevenZipFile(compressed_file, 'w', password=password) as archive:
        archive.write(file, os.path.basename(file))
    return compressed_file

# 百度云盘同步函数
def bysync(file, path, i, deletevd, password):
    if i >= 3:
        print(file + " 上传错误，请检查网络、网盘账户和路径。")
        return

    # 根据是否有密码决定是否加密
    if password:
        file_to_upload = compress_and_encrypt(file, password)
    else:
        file_to_upload = file
    
    time.sleep(10)
    print(file_to_upload + " 正在上传到百度网盘......")
    bp = ByPy()
    code = bp.upload(file_to_upload, '/' + path + '/', ondup='overwrite')  # 使用覆盖上传方式
    if code == 0:
        if deletevd:
            os.remove(file)
            if password:
                os.remove(file_to_upload)
        print(file_to_upload + " 上传成功！")
    else:
        i += 1
        print(file_to_upload + " 重试次数: " + str(i))
        bysync(file, path, i, deletevd, password)

def capture(NVRurl, Cameraname, videopath, videotime, Updisk, deletevd, Networkdisk_space_threshold, upload_threshold, password):
    try:
        print("****")
        cap = cv2.VideoCapture(NVRurl)
        print("****")
    except:
        print("无法捕获视频流，请检查URL或网络连接。")
        return

    # 使用摄像头的最高FPS
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps <= 0:
        fps = 15  # 如果无法获取FPS，则设置为15
    print("摄像头FPS: " + str(fps))

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("视频尺寸: " + str(size))

    # 设置视频保存路径
    videopath = os.path.join(videopath, Cameraname)
    if not os.path.exists(videopath):
        try:
            os.makedirs(videopath)
        except:
            print("请手动创建文件夹")
            return

    # 初始化视频上传总大小变量
    video_total_size = 0

    # 检测网盘空间并删除早期上传的视频文件
    def check_and_delete_earlier_videos():
        nonlocal video_total_size
        if Updisk and video_total_size > 0:  # 确保文件非空才进行上传判断
            uploaded_size = get_uploaded_size() / (1024 * 1024 * 1024)  # 转换为GB单位
            if uploaded_size > Networkdisk_space_threshold:
                print("上传视频总大小达到 {}GB，开始检查网盘剩余空间...".format(uploaded_size))
                bp = ByPy()
                space_info = bp.info()
                free_space = space_info['free'] / (1024 * 1024 * 1024)  # 转换为GB单位
                print("网盘剩余空间为 {}GB".format(free_space))
                if free_space < Networkdisk_space_threshold:
                    print("网盘剩余空间不足 {}GB，开始删除早期上传的视频文件...".format(Networkdisk_space_threshold))
                    # 删除早期上传的视频文件
                    files_to_delete = os.listdir(videopath)
                    files_to_delete.sort()
                    for file in files_to_delete:
                        file_path = os.path.join(videopath, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print("已删除文件：", file)
                    print("删除早期视频文件完成。")
        video_total_size = 0  # 清零视频总大小，为下一轮上传准备

    while True:
        cu_videopath = os.path.join(videopath, str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + '.mp4')
        
        # 设置为MP4格式
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(cu_videopath, fourcc, fps, size)

        start_time = time.time()

        while time.time() - start_time < videotime * 60:
            ret, frame = cap.read()
            if not ret:
                break

            out.write(frame)

        out.release()

        if Updisk:
            sync = threading.Thread(target=bysync, args=(cu_videopath, Cameraname, 0, deletevd, password))
            sync.start()

        video_total_size += os.path.getsize(cu_videopath)  # 更新视频总大小
        if video_total_size >= upload_threshold * (1024 * 1024 * 1024):
            check_and_delete_earlier_videos()  # 检测网盘空间并删除早期视频

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    zip_password = input("请输入压缩包密码（留空则不加密）：")
    capture(NVRurl, Cameraname, videopath, videotime, Updisk, deletevd, Networkdisk_space_threshold, upload_threshold, zip_password)
