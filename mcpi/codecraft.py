# -*- coding:utf-8 -*-

from minecraft import *

class Codecraft(Minecraft):
 
    def __init__(self, address = "localhost", port = 4711, name = None):
        Minecraft.__init__(self, Connection(address, port))
        
        try:
            id = self.getPlayerEntityId(name)
            self.player = CmdPlayer(self.conn, name)
        except Exception:
            exit("Error: 没有此用户，请确认已经加入对应服务器")