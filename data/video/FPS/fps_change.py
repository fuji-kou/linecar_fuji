import cv2
import datetime as dt

# 動画を読み込み、FPSを変更して別名で保存する関数
def m_speed_change(path_in, path_out, scale_factor):
    # 動画読み込みの設定
    movie = cv2.VideoCapture(path_in)

    # 動画ファイル保存用の設定
    fps = int(movie.get(cv2.CAP_PROP_FPS))                                  # 元動画のFPSを取得
    fps_new = int(fps * scale_factor)                                       # 動画保存時のFPSはスケールファクターをかける
    w = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))                            # 動画の横幅を取得
    h = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))                           # 動画の縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')                     # 動画保存時のfourcc設定（mp4用）
    now = dt.datetime.now()
    time = now.strftime('%Y_%m%d_%H%M_%S')
    video = cv2.VideoWriter(path_out + 'fpschange_{}.mp4'.format(time), fourcc, fps_new, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

    # ファイルからフレームを1枚ずつ取得して動画処理後に保存する
    while True:
        ret, frame = movie.read()        # フレームを取得
        #video.write(frame)               # 動画を保存する
        # フレームが取得できない場合はループを抜ける
        if not ret:
            break
    # 撮影用オブジェクトとウィンドウの解放
    movie.release()
    return

path_in = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\video\\" + 'video_20201127_1824_08.mp4'          # 元動画のパス
path_out = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\data\\video\\FPS\\"                                # 保存する動画のパス
scale_factor = 0.6              # FPSにかけるスケールファクター
#color_flag = True               # カラー動画はTrue, グレースケール動画はFalse

# 動画の再生速度を変更する関数を実行
m_speed_change(path_in, path_out, scale_factor)