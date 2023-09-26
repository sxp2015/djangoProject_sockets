from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        # 接收URL传来的参数
        group = self.scope['url_route']['kwargs'].get('group')
        # 接受客户端连接
        self.accept()
        # 当前用户加入到 group 群里。
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        group = self.scope['url_route'][' kwargs'].get('group')
        print("}群接收到数据:".format(group), message)
        # 执行xxx_000方法去实现给用户群里的每个用户发送消息
        async_to_sync(self.channel_layer.group_send)(group, {'type': 'xxx.ooo', 'message': message})
