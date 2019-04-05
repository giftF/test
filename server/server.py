import socketserver
import threading
from time import sleep
import random

from base import Protocol
from Script.My_Redis import My_redis

import random

seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
sa = []
for i in range(8):
  sa.append(random.choice(seed))
code = ''.join(sa)

room = {
    'users': 'room%s' % code,
    'talk': 'talk%s' % code,
    'monster': 'monster%s' % code
}

# 初始化redis
MR = My_redis()
MR.set(room['users'], str([]))
MR.set(room['talk'], '')
MR.set(room['monster'], str([]))

ADDRESS = ('0.0.0.0', 8712)  # 绑定地址
g_conn_pool = []  # 连接池

userreadydict = {
    'Y': 'N',
    'N': 'Y'
}

usercount = 0

# 初始化user数据
class Conn:
    def __init__(self, conn):
        # 连接信息
        self.conn = conn
        self.user = {
            'x': None,
            'Y': None,
            'number': None,
            'name': None,
            'my': None,
            'troops': {},
            'isready': 'N',
            'race': 'Random',
            'Money': 1000,
        }

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.request.sendall("连接服务器成功!".encode(encoding='utf8'))
        self.request.settimeout(0.1)
        # 加入连接池
        conn = Conn(self.request)
        g_conn_pool.append(conn)

    def handle(self):
        while True:
            try:
                # 读取数据包
                bytes = self.request.recv(1024)
                # 切割数据包
                while True:
                    # 读取包长度
                    length_pck = int.from_bytes(bytes[:4], byteorder='little')
                    # 截取封包
                    pck = bytes[4:4 + length_pck]
                    # 删除已经读取的字节
                    bytes = bytes[4 + length_pck:]
                    # 把封包交给处理函数
                    self.pck_handler(pck)
                    # 如果bytes没数据了，就跳出循环
                    if len(bytes) == 0:
                        break
                    # print("客户端消息：", bytes.decode(encoding="utf8"))
            except Exception as e:  # 意外掉线
                err = e.args[0]
                if err == 'timed out':
                    pamras = {
                        'users': eval(MR.get(room['users'])),
                        'talk': MR.get(room['talk']),
                        'monster': eval(MR.get(room['monster']))
                    }
                    for u in pamras['users']:
                        if u['name'] == self.get_conn().user['name']:
                            u['my'] = 'Y'
                    ret = Protocol()
                    ret.add_str('games')
                    ret.add_str(str(pamras))
                    self.request.sendall(ret.get_pck_has_head())
                else:
                    print('用户可能掉线了')
                    break

    def finish(self):
        pass

    def get_conn(self):
        for conn in g_conn_pool:
            if conn.conn == self.request:
                return conn

    def new_role(self):
        # 告诉各个客户端有新玩家加入
        ret = Protocol()
        ret.add_str("newplayer")
        ret.add_int32(self.get_conn().x)
        ret.add_int32(self.get_conn().y)
        ret.add_str(self.get_conn().name)
        ret.add_str(self.get_conn().number)
        for r in g_conn_pool:
            if r != self.get_conn():
                ret.add_str('N')
                ret.add_str(self.get_conn().race)
                r.conn.sendall(ret.get_pck_has_head())

    def other_role(self):
        # 告诉当前玩家，其他玩家的信息
        for conn in g_conn_pool:
            ret = Protocol()
            ret.add_str("newplayer")
            ret.add_int32(conn.x)
            ret.add_int32(conn.y)
            ret.add_str(conn.name)
            ret.add_str(conn.number)
            # 本人返回1，非本人返回0
            if conn != self.get_conn():
                ret.add_str('N')
            else:
                ret.add_str('Y')
            ret.add_str(conn.race)
            self.request.sendall(ret.get_pck_has_head())

    def move_role(self):
        # 告诉各个客户端有玩家移动了
        ret = Protocol()
        ret.add_str("playermove")
        ret.add_int32(self.get_conn().x)
        ret.add_int32(self.get_conn().y)
        ret.add_str(self.get_conn().name)
        for r in g_conn_pool:
            if r != self.get_conn():
                r.conn.sendall(ret.get_pck_has_head())

    def pck_handler(self, pck):
        """
        解析数据包
        """
        global usercount
        p = Protocol(pck)
        pck_type = p.get_str()
        users = eval(MR.get(room['users']))
        talk = MR.get(room['talk'])

        print(users)

        if pck_type == "newuser":
            self.get_conn().user['name'] = '%s%s' % (p.get_str(), usercount)
            usercount += 1
            self.get_conn().user['number'] = len(g_conn_pool)
            users.append(self.get_conn().user)
            talk += '欢迎%s加入游戏！\n' % self.get_conn().user['name']
            MR.set(room['users'], str(users))
            MR.set(room['talk'], str(talk))
        elif pck_type == "change":
            pass
        elif pck_type == "ready":
            print('收到一个ready请求')
            user_name = p.get_str()
            user_number = int(user_name[-1])
            user_isready = userreadydict[p.get_str()]

            # print(user_name)
            # print(user_isready)

            for r in g_conn_pool:
                if r == self.get_conn() and r.user['name'] == user_name:
                    for u in users:
                        if u['name'] == user_name:
                            u['isready'] = user_isready
                            MR.set(room['users'], str(users))
                            print('修改成功')
                            break
                    break
        elif pck_type == "talk":
            pass
        elif pck_type == "out":
            pass
        elif pck_type == "move":
            pass
        elif pck_type == "build":
            pass
        elif pck_type == "up":
            pass

        if pck_type == 'newrole':
            self.get_conn().x = p.get_int32()
            self.get_conn().y = p.get_int32()
            self.get_conn().name = p.get_str()
            self.get_conn().number = len(g_conn_pool)
            self.get_conn().my = None
            self.new_role()  # 告诉当前服务器的其他玩家，有新玩家加入
            self.other_role()  # 告诉新加入的玩家，当前服务器的其他玩家信息
        elif pck_type == 'move':
            self.get_conn().x = p.get_int32()
            self.get_conn().y = p.get_int32()
            self.move_role()

    def remove(self):
        # 告诉各个客户端有玩家离线
        ret = Protocol()
        ret.add_str("logout")
        ret.add_str(self.get_conn().name)
        for r in g_conn_pool:
            if r != self.get_conn():
                r.conn.sendall(ret.get_pck_has_head())
        g_conn_pool.remove(self.get_conn())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    server = ThreadedTCPServer(ADDRESS, ThreadedTCPRequestHandler)
    # 新开一个线程运行服务端
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # 主线程逻辑
    while True:
        sleep(3)