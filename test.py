from mcpi.minecraft import *
from mcpi.codecraft import *
import time
import sys
import os

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

mc = Codecraft('10.0.0.5', 4711, 'leetom')

while(True):
    try:
	print mc.getPlayerEntityId('leetom')
    except:
        print "not found"
    time.sleep(1)
