import matplotlib.pyplot as plt 
import matplotlib.image as mgimg
from matplotlib import animation
import numpy as np
from scipy.ndimage import convolve

# 
CAFrames = []
CASize = 100
updates = 100
snowFallChance = 0.2 # occurs as normal varb < threshold
snowFallFequency = 10
speed = 1
temp = 0.2 # represents melting chance
meltFreq = 1
CLUMPRANGE = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]])



fig = plt.figure()


# Makes 'new snowfall' 
def makeSnowFall():
    rands = np.random.rand(CASize,CASize)
    rands[rands < snowFallChance] = 1 # snow falls if lower than chance
    return(rands)

def clump(snowCA,clumpRange = CLUMPRANGE):
    return(convolve(snowCA,clumpRange, mode = 'constant'))

def melt(snowCA):
    rands = np.random.rand(CASize,CASize)
    meltChance = np.arange(1/CASize,1+1/CASize,1/CASize)
    rands[rands < snowFallChance/2] = 2 # "big snow" at half snow chance
    snowCA[(snowCA*rands)>temp] = 0 # 'melts' if randoms are lower than expected value
    return(snowCA)

#loops through available png:s
def runCA():
    pastFrame = np.zeros((CASize,CASize))
    for i in range(updates):
        curFrame = pastFrame
        if i%snowFallFequency == 0: 
            randSnowFall = makeSnowFall()
            curFrame = pastFrame + randSnowFall
        if i%meltFreq == 0:
            curFrame = melt(curFrame)
        nextFrame = np.roll(melt(curFrame),1, axis = 0) # applies flow, and also melts
        nextFrame[nextFrame >= 1] = 1
        imgplot = plt.imshow(nextFrame, cmap="binary_r") # makes image simply
        pastFrame = nextFrame # advances time

        # I hate that I need a global variable, but okay
        CAFrames.append([imgplot])


runCA()

my_anim = animation.ArtistAnimation(fig, CAFrames, interval=10, blit=True, repeat_delay=1000) # makes the animation using matplotlib
my_anim.save("animation.gif") #doesnt want to use ffmpeg for some reason, hence the gif extension

plt.show()