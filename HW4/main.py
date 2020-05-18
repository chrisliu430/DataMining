from PIL import Image
import numpy as np
import random

class DBSCAN():
    def __init__(self, fileName):
        self.fileName = fileName
        self.img = Image.open(fileName)
        self.imgArr = np.array(self.img)
        self.height, self.width = np.shape(self.imgArr)
        self.cimgArr = np.full((self.height, self.width, 3), 0)
        self.valImg = np.full((self.height, self.width), 0)
        self.valuesArr = [0, 0]
        self.pointVal = 2

    def inverting(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x]):
                    self.imgArr[y, x] = 0
                else:
                    self.imgArr[y, x] = 1
    
    def clustering(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x]):
                    pointIsExist = self.discretecheck(y, x, 3)
                    if (not(pointIsExist)):
                        self.imgArr[y, x] = 0
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x]):
                    value = self.scanpointsvalue(y, x, 10)
                    if (value == 0):
                        self.valImg[y, x] = self.pointVal
                        self.pointVal += 1
                        self.valuesArr.append(1)
                    else:
                        self.valImg[y, x] = value
                        self.valuesArr[value] += 1
                else:
                    self.valImg[y, x] = -1
      
    def toRGBarray(self):
        print(self.pointVal)
        for val in range (2, len(self.valuesArr)):
            r = random.randint(1, 255)
            g = random.randint(1, 255)
            b = random.randint(1, 255)
            if (self.valuesArr[val] < 10):
                r = g = b = -1
            for y in range (self.height):
                for x in range (self.width):
                    if (self.valImg[y, x] == -1):
                        self.cimgArr[y, x, 0] = 255
                        self.cimgArr[y, x, 1] = 255
                        self.cimgArr[y, x, 2] = 255
                    if (self.valImg[y, x] == val):
                        self.cimgArr[y, x, 0] = r
                        self.cimgArr[y, x, 1] = g
                        self.cimgArr[y, x, 2] = b

    def storageimage(self):
        cimg = Image.fromarray(self.cimgArr.astype('uint8')).convert('RGB')
        cimg.save("convert.bmp")

    # --- SCAN
    def discretecheck(self, startY, startX, redis):
        judge = False
        for y in range (startY - redis, startY + redis + 1):
            for x in range (startX - redis, startX + redis + 1):
                if (y < 0 or x < 0 or x >= self.width or y >= self.height):
                    break
                if (self.imgArr[y, x] != 0 and x != startX and y != startY):
                    judge = True
            if (judge):
                break
        return judge

    def scanpointsvalue(self, startY, startX, redis):
        value = 0
        for y in range (startY - redis, startY + redis + 1):
            for x in range (startX - redis, startX + redis + 1):
                if (x < 0 or y < 0 or x >= self.width or y >= self.height):
                    break
                if (self.valImg[y, x] != -1):
                    value = self.valImg[y, x]
                    break
            if (value != 0):
                break
        return value
    # ---
    
if __name__ == "__main__":
    ds = DBSCAN("./test.bmp")
    ds.inverting()
    ds.clustering()
    ds.toRGBarray()
    ds.storageimage()