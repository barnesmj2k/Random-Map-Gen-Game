import numpy as np
import random
from PIL import Image, ImageEnhance

class Noise():

    def __init__(self, x, y):
        self.vector = [np.random.uniform(0,200) for _ in range(0, (x+1) * (y+1) * 2)]
        self.num_col = x

    def generateNoise(type, x, y):

        # if (type == "gaussian"):
        #     noise = [int(np.random.normal(0, 200)) for _ in range (0,(x*y))]
        noise = [0 for _ in range(x*y)]
        forest = [(56, 82, 55),(94, 76, 66)] # green, brown
        beach = [(255, 230, 161),(156, 238, 255)] # yellow, blue
        hell = [(87, 5, 5),(0,0,0)] # red, black
        bw   = [(255,255,255),(0,0,0)]
        if (type == "beach"):
            noise = [random.choice(beach) for _ in range (0,(x*y))]
        elif (type == "forest"):
            noise = [random.choice(forest) for _ in range (0,(x*y))]
        elif (type == "hell"):
            noise = [random.choice(hell) for _ in range (0,(x*y))]
        elif (type == "bw"):
            noise = [random.choice(bw) for _ in range (0,(x*y))]
        elif (type == "log"):
            noise = [int(np.random.logistic(0, 200)) for _ in range (0,(x*y))]
        elif (type == "uniform"):
            noise = [int(np.random.uniform(0, 200)) for _ in range (0,(x*y))]
        else:
            raise ValueError("invalid noise type specified")
        return noise
    
    def mapify(img):
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(40)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(40)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(40)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.5)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)

        return img
    
    def makeImage(width, height, type, scalar):
        gen = Noise.generateNoise(type, width//scalar, height//scalar)
        img = Image.new("RGB",(width//scalar, height//scalar))
        #data = list(range(0, 256, 5)) * 104
        nWidth = img.width * (scalar * 3)
        nHeight = img.height * (scalar * 3)

        nSize = (nWidth, nHeight)
        img.putdata(gen)
        img = img.resize(nSize)
        img = img.resize(nSize)
        img = Noise.mapify(img)
        img.save('mapbw.png')

        mapImage = Noise.makeMapFromBW()

    def makeMapFromBW():
        im1 = Image.open("mapbw.png").convert("L")
        iData = list(im1.getdata())
        width = im1.width
        size = (width,width)
        wh = len(iData)

        sand = [(90,80,61) for _ in range(0,100)] # sand yellow
        sand.append((100,100,255)) # blue specs
        sand.append((50,50,50)) # dark gray specs

        water = [(26,38,65) for _ in range(0,25)]
        water.append((255,255,255)) #blue and white

        # print(iData)
        mData = [0 for _ in range(wh)]
        for i in range(0,wh):
            if (iData[i] == 0):
                mData[i] = random.choice(sand)
            elif (iData[i] == 255):
                mData[i] = random.choice(water)

        im2 = Image.new("RGB",size)
        im2.putdata(mData)
        im2.save('mapColor.png')



def main():
    type = "bw"
    # type = input("Enter noise type: ")
    # samples = 90000
    width = 5
    height = 5

    gen = Noise.generateNoise(type, width, height)
    # print(gen)
    # rgbNoise = [(val,val,val) for row in gen for val in row]

    img = Image.new("RGB",(width, height))
    #data = list(range(0, 256, 5)) * 104
    nWidth = img.width * 100
    nHeight = img.height * 100

    nSize = (nWidth, nHeight)
    img.putdata(gen)
    img = img.resize(nSize)
    
    img = Noise.mapify(img)
    Noise.makeMapFromBW()
    

    # img = Image.new("L", (104, 104))  # single band 
    # newdata = list(range(0, 256, 4)) * 104
    # img.putdata(newdata) 
    # img.show() 
main()
    