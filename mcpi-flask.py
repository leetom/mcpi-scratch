#-*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import Response
import mcpi.minecraft as minecraft
from mcpi.codecraft import Codecraft
from mcpi.minecraftstuff import *
from mcpi.pixeltext import PixelText
import mcpi.block as block
import urlparse, urllib, argparse
import logging
import os
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)

server_url = 'http://www.codepku.com'
# server_url = 'http://platform.codepku.dev'

class Handler:
    def __init__(self, mc):
        self.mc = mc

    def __call__(self):
        pass

    @classmethod #类方法
    def setBlock(self, params, mc = None):
        print ('setblock: {0}'.format(params))
        x = int(params[0])
        y = int(params[1])
        z = int(params[2])
        blockType = int(params[3])
        blockData = int(params[4])
        if (params[5] == 'rel'): # set the block relative to the player
            playerPos = mc.player.getTilePos()
            #playerPos = minecraft.Vec3(int(playerPos.x), int(playerPos.y), int(playerPos.z))
            x += playerPos.x
            y += playerPos.y
            z += playerPos.z
        if (blockData == -1): # sure these is a more pythonesque way of doing this
            mc.setBlock(x, y, z, blockType)
        else:
            mc.setBlock(x, y, z, blockType, blockData)
        return ''

    @classmethod #类方法
    def setBlocks(self, params, mc = None): # doesn't support metadata
        log.info('invoke setBlocks with params: {} {} {} {} {} {} {} {}'.format(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
        if (int(params[7]) == -1): # sure these is a more pythonesque way of doing this
            log.debug('invoking without data')
            mc.setBlocks(int(params[0]), int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5]), int(params[6]))
        else:
            log.debug('invoking with data')
            mc.setBlocks(int(params[0]), int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5]), int(params[6]), int(params[7]))
        return ''

    @classmethod #类方法
    def setPlayerPos(self, params, mc = None): # doesn't support metadata
        log.info('invoke setPlayerPos with params: {} {} {}'.format(params[0], params[1], params[2]))
        mc.player.setPos(int(params[0]), int(params[1]), int(params[2]))
        return ''

    # implementation of Bresenham's Line Algorithm to rasterise the points in a line between two endpoints
    # algorithm taken from: http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
    # note: y refers to usual cartesian x,y coords. Not the minecraft coords where y is the veritical axis
    @classmethod #类方法
    def getLinePoints(self, x1, y1, x2, y2, mc = None):
        points = []
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points

    # calls getLine to rasterise a line between two points, the last param is the vertical axis.
    # eg: x1,z1,x2,z2,y in minecraft coordinates
    # then plots the line using setBlock
    @classmethod #类方法
    def setLine(self, params, mc = None):
        log.info('invoke setLine with params: {} {} {} {} {}'.format(params[0], params[1], params[2], params[3], params[4], params[5]))
        log.debug(params)
        x1 = int(params[0])
        y1 = int(params[1])
        z1 = int(params[2])
        x2 = int(params[3])
        y2 = int(params[4])
        z2 = int(params[5])
        blockType = int(params[6])
        blockData = int(params[7])
        mcDraw = MinecraftDrawing(mc)

        mcDraw.drawLine(x1, y1, z1, x2, y2, z2, blockType, blockData)
        return ''


    # builds a circle using Bresenham's circle algorithm (also known as a midpoint circle algorithm)
    # plots using setBlock
    @classmethod #类方法
    def setCircle(self, params, mc = None, H = False):
        log.info('invoke setCircle with params: {} {} {} {} {}'.format(params[0], params[1], params[2], params[3], params[4]))
        log.debug(params)
        x = int(params[0])
        y = int(params[1])
        z = int(params[2])
        r = int(params[3])
        blockType = int(params[4])
        blockData = int(params[5])
        log.info("draw circle")
        mcDraw = MinecraftDrawing(mc)

        if(H):
            mcDraw.drawHorizontalCircle(x, y, z, r, blockType, blockData)
        else:
            mcDraw.drawCircle(x, y, z, r, blockType, blockData)

        return ''

    # builds a circle using Bresenham's circle algorithm (also known as a midpoint circle algorithm)
    # plots using setBlock
    @classmethod #类方法
    def setHCircle(self, params, mc = None):
        self.setCircle(params, mc, True)
        return ''

    @classmethod #类方法
    def setSphere(self, params, mc = None):
        log.info('invoke setCircle with params: {} {} {} {} {}'.format(params[0], params[1], params[2], params[3], params[4]))
        log.debug(params)
        x = int(params[0])
        y = int(params[1])
        z = int(params[2])
        r = int(params[3])
        blockType = int(params[4])
        blockData = int(params[5])
        log.info("draw circle")
        mcDraw = MinecraftDrawing(mc)

        mcDraw.drawSphere(x, y, z, r, blockType, blockData)

        return ''

    @classmethod
    def setText(self, params, mc = None):
        txt = unicode(str(params[0]))
        log.info('create text ' + txt)
        x = int(params[1])
        y = int(params[2])
        z = int(params[3])
        blockType = int(params[4])
        blockData = int(params[5])

        pt = PixelText(txt)

        pixeltext = pt.getPixelList()
        for ch in xrange(len(txt)):
            if(txt[ch] != ' '): #跳过空格
                for yi in xrange(12):
                    for xi in xrange(12):
                        pos_x = x + 13 * ch + xi
                        pos_y = y + (12 - yi)
                        pos_z = z
                        if(pixeltext[ch][yi * 12 + xi] == '1'):
                            mc.setBlock(pos_x, pos_y, pos_z, blockType, blockData)
                        else:
                            mc.setBlock(pos_x, pos_y, pos_z, block.AIR.id)
        return ''

    @classmethod #类方法
    def postToChat(self, params, mc = None):
        log.info('post to chat: %s', urllib.unquote(params[0]))
        mc.postToChat(urllib.unquote(params[0]))
        return ''

    @classmethod #类方法
    def playerPosToChat(self, params, mc = None):
        log.info('playerPos to chat')
        playerPos = mc.player.getTilePos()
        log.debug(playerPos)
        #playerPos = minecraft.Vec3(int(playerPos.x), int(playerPos.y), int(playerPos.z))
        log.debug(playerPos)
        posStr = ("x {0} y {1} z {2}".format(str(playerPos.x), str(playerPos.y), str(playerPos.z)))
        log.debug(posStr)
        mc.postToChat(urllib.unquote(posStr))
        return ''

    @classmethod #类方法
    def cross_domain(self, params):
        # not needed for offline editor, only online webeditor
        log.info('need to return cross_domain.xml') # needed for scratch Flash issues
        return ''

    @classmethod #类方法
    def reset_all(self, params):
        log.info('trying to reset')
        return ''

    @classmethod #类方法
    def getPlayerPos(self, params, mc = None): # doesn't support metadata
        log.info('invoke getPlayerPos: {}'.format(params[0]))
        playerPos = mc.player.getPos()
        #Using your players position
        # - the players position is an x,y,z coordinate of floats (e.g. 23.59,12.00,-45.32)
        # - in order to use the players position in other commands we need integers (e.g. 23,12,-45)
        # - so round the players position
        # - the Vec3 object is part of the minecraft class library
        playerPos = minecraft.Vec3(int(playerPos.x), int(playerPos.y), int(playerPos.z))
        log.debug(playerPos)
        # I'm sure theres a more pythony way to get at the vector elements but...
        coord = params[0];
        coordVal = 0;
        if (coord == 'x'):
            coordVal = playerPos.x
        if (coord == 'y'):
            coordVal = playerPos.y
        if (coord == 'z'):
            coordVal = playerPos.z
        return str(coordVal)

    # getBlock calls getBlockWithData function
    # currently only returns the id and not the data
    # TODO: refactor to return data also
    @classmethod #类方法
    def getBlock(self, params, mc = None):
        log.info ('getBlock: {0}'.format(params))
        x = int(params[0])
        y = int(params[1])
        z = int(params[2])
        if (params[3] == 'rel'): # set the block relative to the player
            playerPos = mc.player.getTilePos()
            x += playerPos.x
            y += playerPos.y
            z += playerPos.z
        blockData = mc.getBlockWithData(x, y, z)
        log.info ('blockData: %s', blockData)
        return str(blockData.id)

    # pollBlockHits calls pollBlockHits function
    # currently only returns the first block in the period between polls
    # requires that polling is enabled to check
    # TODO: refactor to return multiple blocks
    @classmethod #类方法
    def pollBlockHits(self, params, mc = None):
        log.info ('pollBlockHits: {0}'.format(params))
        blockHits = mc.events.pollBlockHits()
        log.info ('blockHits: %s', blockHits)
        if blockHits:
            return str(1)
        return str(0)

    # from original version for scratch2 (offline)
    # currently unused
    @classmethod #类方法
    def pollEvents(self, params, mc = None):
        global pollInc, pollLimit, prevPosStr
        pollInc += 1
        log.debug('poll: {} {}'.format(pollInc, prevPosStr))
        if (prevPosStr != "") and (pollInc % pollLimit != 0):
            log.debug("don't call mc")
            return prevPosStr
        log.debug("call mc")
        playerPos = mc.player.getPos()
        #Using your players position
        # - the players position is an x,y,z coordinate of floats (e.g. 23.59,12.00,-45.32)
        # - in order to use the players position in other commands we need integers (e.g. 23,12,-45)
        # - so round the players position
        # - the Vec3 object is part of the minecraft class library
        playerPos = minecraft.Vec3(int(playerPos.x), int(playerPos.y), int(playerPos.z))
        posStr = ("playerPos/x {0}\r\nplayerPos/y {1}\r\nplayerPos/z {2}".format(str(playerPos.x), str(playerPos.y), str(playerPos.z)))
        # posStr = ("{0}".format(str(playerPos.x)))
        log.debug(playerPos)
        return posStr

    @staticmethod  
    def checkReady(username):
        #判断用户是否已经加入MC服务器
        #查找该用户的mc对象
        global mc_host, mc_port, mc_list
        if (username in mc_list):
            try:
                #用户是否还在游戏中。
                mc_list[username].getPlayerEntityId(username)
                return "true"
            except:
                del mc_list[username]
                return "false"
        else:
            #log.debug("config: {}, {}, {}".format(mc_host, mc_port, username))
            try:
                mc_temp = Codecraft(mc_host, mc_port, username)
                mc_list[username] = mc_temp
                return "true"
            except:
                log.error(mc_host + str(mc_port))
                log.error('all users: {}'.format(mc_list))
                log.error("User {0} has not join mc server{1} with port {2}:".format(username, mc_host, mc_port))
                return "false"


cmds = {
    "poll" : Handler.pollEvents,
    "postToChat" : Handler.postToChat,
    "setBlock" : Handler.setBlock,
    "setBlocks" : Handler.setBlocks,
    "setPlayerPos" : Handler.setPlayerPos,
    "playerPosToChat" : Handler.playerPosToChat,
    "setLine" : Handler.setLine,
    "setCircle" : Handler.setCircle,
    "setHCircle" : Handler.setHCircle,
    "setSphere" : Handler.setSphere,
    "setText" : Handler.setText,
    "cross_domain.xml" : Handler.cross_domain,
    "reset_all" : Handler.reset_all,
    "getPlayerPos" : Handler.getPlayerPos,
    "getBlock" : Handler.getBlock,
    "pollBlockHit" : Handler.pollBlockHits,
    "checkReady": Handler.checkReady,
}

@app.route('/', methods = ['GET'])
def index():
    return "hello CodeCraft!\n"

@app.route('/<path:path>', methods = ['OPTIONS'])
def do_options(path):
    return "true"
@app.route('/<username>/checkReady/', methods = ['GET'])
def get_checkReady(username):
    return Handler.checkReady(username)


@app.route('/<path:path>', methods=['POST'])
def catch_all(path):
    cmdpath = []
    cmdpath = path.split('/')
    if(len(cmdpath) < 2):
        return "error"
    # return "-".join(cmdpath)
    username = urlparse.unquote(cmdpath[0])
    global mc
    global mc_list
    global mc_host
    global mc_port
    global cmds

    if(username in mc_list):      
        mc_temp = mc_list[username]
        handler = cmds[cmdpath[1]]
        log.info("run command for " + username)
        pollResp = str(handler(cmdpath[2:], mc_temp))
        return pollResp
    else:
        return "fail"
    return 'You want path: {}'.format(cmdpath)



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', server_url)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    # deal with the CORS issue
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add("Access-Control-Allow-Headers", "X-Requested-With, Content-type, X-CSRF-Token")
    return response

mc_list = {}    # list of mc object for each user, indexed by username
mc_host = 'localhost'
mc_port = 4711
web_host = '211.101.17.10'

if 'MCPI_MC_SERVER' in os.environ:
    mc_host = os.environ['MCPI_MC_SERVER']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mcpi-scratch is a Scratch2 extension helper app to allow Scratch programs to manipulate Minecraft through the Pi protocol')
    parser.add_argument('-m', action="store", dest="host", help="hostname/IP for the machine running Minecraft. Default is localhost")
    parser.add_argument('-l', action="store", dest="serve", help="the ip/hostname the web server is listening")

    args = parser.parse_args()

    if args.serve:
        web_host = args.serve


    try:
        if args.host:
            mc_host = args.host
            mc = minecraft.Minecraft.create(mc_host) #仅仅测试服务器是否启动。
        else:
            mc = minecraft.Minecraft.create()
    except:
        e = sys.exc_info()[0]
        log.exception('cannot connect to minecraft')
        sys.exit(0)

    app.debug = True
    app.run(web_host, 4715)
