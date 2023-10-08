import cv2
from PySide6 import QtCore, QtWidgets
from moviepy.editor import VideoFileClip

def play_video(video_path):
    # 使用moviepy打开视频
    video_clip = VideoFileClip(video_path)
    duration = video_clip.duration  # 视频总时长（秒）
    fps = video_clip.fps  # 视频帧率

    app = QtWidgets.QApplication()

    window = QtWidgets.QWidget()
    window.setWindowTitle("Video")
    window.setFixedSize(800, 600)

    label = QtWidgets.QLabel("Hello", window)
    label.move(100, 300)
    window.show()

    app.exec()




    # # 使用OpenCV创建视频窗口
    # cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Video", 800, 600)
    #
    # # 逐帧播放视频
    # for t in range(int(duration * fps)):
    #     frame = video_clip.get_frame(t / fps)  # 获取指定时刻的帧
    #     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 转换颜色通道
    #     cv2.imshow("Video", frame)  # 显示帧
    #
    #     # 更新进度条
    #     progress = (t / (duration * fps)) * 100
    #
    #     if cv2.waitKey(33) & 0xFF == ord('q'):  # 按q退出
    #         break
    #
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    # "C:/Users/Icecider/Videos/Desktop/test.mp4"
    video_path = "C:/Users/Icecider/Videos/Desktop/test.mp4"  # 替换为你的视频文件路径
    play_video(video_path)
