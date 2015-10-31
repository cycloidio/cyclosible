from ws4redis.subscriber import RedisSubscriber


class WebSocketSubscriber(RedisSubscriber):
    def __init__(self, connection):
        self._subscription = None
        super(WebSocketSubscriber, self).__init__(connection)

    def send_persited_messages(self, websocket):
        """
        This method is called immediately after a websocket is openend by the client, so that
        persisted messages can be sent back to the client upon connection.
        """
        for channel in self._subscription.channels:
            task_id = channel.split(':')[2]
            task_channel = ':'.join(['tasks', task_id])
            logs = self._connection.lrange(task_channel, 0, -1)[:-1]
            for log in logs:
                websocket.send(log)

            message = self._connection.get(channel)
            if message:
                websocket.send(message)
