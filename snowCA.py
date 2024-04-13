import matplotlib.pyplot as plt 
import matplotlib.image as mgimg
from matplotlib import animation
import numpy as np
from scipy.ndimage import convolve

# TO DO:
# ADD SLIDERS AND ALLOW THE SIMULATION TO JUST RUN ALWAYS
# ADD EVOLUTION TO EVOLVE TO BEST "DESIRED CONVOLUTION"

CAFrames = []
CASize = 100
UPDATES = 1000
SNOWFALLCHANCE = 1 # occurs as normal varb < threshold
SNOWFALLSPACE = [3,CASize]
MELTCHANCE = 0.1 # turn this into a real function one day
SPEED = 1 
DIR = 0 # 0 is horz

# # Turn this on to turn it into a sideways flame!
# CLUMPRANGE = np.array([[0.1, 0.2, 0.1],
#                        [0.2, 0.3, 0.2],
#                        [0.1, 0.2, 0.1]])
# SNOWFALLSPACE = [CASize,3] 
# DIR = 1

CLUMPRANGE = np.array([[0.1, 0.1, 0.1],
                       [0.1, 1, 0.1],
                       [0.1, 0.1, 0.1]])

fig = plt.figure()



def clump(snowCA,clumpRange = CLUMPRANGE):
    return(convolve(snowCA,clumpRange, mode = 'constant'))

def melt(snowCA):
    meltAtElevation = np.arange(0,CASize)/CASize*MELTCHANCE # Given by a linear change from 0 to melt chance
    meltAtElevation = meltAtElevation.reshape((CASize,1)) # This and above line could be precomped
    randomChances = np.random.rand(CASize,CASize)
    snowCA = np.greater(randomChances*snowCA,meltAtElevation).astype(int)
    return(snowCA)

#loops through available png:s
def runCA(info = 0):
    score = 0
    pastFrame = np.zeros((CASize,CASize))
    for i in range(UPDATES):
        # CLUMPRANGE = np.random.uniform(0,0.5,(3,3))*2 #This is a fun idea, but it just makes little spheres
        curFrame = pastFrame
        curFrame[0:SNOWFALLSPACE[0],0:SNOWFALLSPACE[1]] = np.random.rand(SNOWFALLSPACE[0],SNOWFALLSPACE[1]) < SNOWFALLCHANCE # makes snow fall in region at chance LOWER than given
        curFrame = convolve(curFrame,CLUMPRANGE) # clumps up the snow in the CLUMPRANGE neighbourhood as perscribed
        imgplot = plt.imshow(curFrame, cmap="binary_r") # makes image simply
        nextFrame = np.roll(melt(curFrame),SPEED, axis = DIR) # applies flow, and also melts
        pastFrame = nextFrame # advances time
        score += np.cumsum(curFrame)
        # I hate that I need a global variable, but okay
        CAFrames.append([imgplot])
    return(score)


runCA()

my_anim = animation.ArtistAnimation(fig, CAFrames, interval=10, blit=True, repeat_delay=1000) # makes the animation using matplotlib
my_anim.save("animation.gif") #doesnt want to use ffmpeg for some reason, hence the gif extension

plt.show()