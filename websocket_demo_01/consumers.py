from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        # 接收URL传来的参数
        group = self.scope['url_route']['kwargs'].get('group')
        print("有人来连接了")
        # 接受客户端连接
        self.accept()
        # self.send(text_data='欢迎来到聊天室!')
        # 当前用户加入到 group 群里。
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        print("接收到数据:".format(group), message)
        text = message['text']
        print("接收到客户端数据:", text)
        # for conn in CONN_LIST:
        #     conn.send(text_data=text)
        # 执行xxx_000方法去实现给用户群里的每个用户发送消息
        async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_message_for_each_user', 'message': message})

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        # 当前用户退出群组
        print("有人断开连接了:", message)
        # CONN_LIST.remove(self)
        # raise StopConsumer()
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)

    # 自定义方法用于处理收到信息后，发给群组中每个成员的信息
    def send_message_for_each_user(self, message):
        self.send(text_data=message['message']['text'])
