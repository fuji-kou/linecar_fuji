import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #ソケット作成
    # IPアドレスとポートを指定
    s.bind(('127.0.0.1', 50007))
    # 1 接続（実際は２）
    s.listen(1)
    # connection するまで待つ
    while True:
        # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
        conn, addr = s.accept()
        with conn:
            while True:
                # データを受け取る
                data = conn.recv(1024)
                if not data:
                    break
                print('data : {}, addr: {}'.format(data, addr))
                # クライアントにデータを返す(b -> byte でないといけない)
                conn.sendall(b'Received: ' + data)