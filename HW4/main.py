from PIL import Image
import numpy as np
import random

class DBSCAN():
    def __init__(self, fileName):
        self.img = Image.open(fileName)
        self.imgArr = np.array(self.img)
        self.width, self.height = self.img.size
        self.valImg = np.full((self.height, self.width), -1)
        self.cImgArr = np.full((self.height, self.width, 3), -1)
        self.valuesArr = [0]
        self.pointVal = 1

    def Start(self):
        self.Inverting()
        self.RemovePoints()
        self.Clustering()
        self.ToRGBArray()

    def CreateNewImage(self, newName):
        cimg = Image.fromarray(self.cImgArr.astype('uint8')).convert('RGB')
        cimg.save(newName)
    
    # Hiding Layer ---
    def Inverting(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x]):
                    self.imgArr[y, x] = False
                else:
                    self.imgArr[y, x] = True

    def RemovePoints(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x] and not(self.ScanNearPoints(y, x, 3))):
                    self.imgArr[y, x] = 0

    def Clustering(self):
        for y in range (self.height):
            for x in range (self.width):
                if (not(self.imgArr[y, x])):
                    self.valImg[y, x] = 0
                elif (self.imgArr[y, x] and self.valImg[y, x] == -1):
                    rVal = self.CatchNearPointsValue(y, x, 7)
                    if (not(rVal)):
                        self.valImg[y, x] = self.pointVal
                        self.valuesArr.append(1)
                        self.pointVal += 1
                        self.RecursionNearPoints(y + 1, x, 13, self.pointVal - 1)
                    else:
                        self.valImg[y, x] = rVal
                        self.valuesArr[rVal] += 1
                        self.RecursionNearPoints(y + 1, x, 13, self.pointVal - 1)

    def RecursionNearPoints(self, centerY, centerX, redis, value):
        for x in range (centerX - redis, centerX + redis + 1):
            if (x < 0 or x >= self.width):
                break
            if (self.imgArr[centerY, x] and self.valImg[centerY, x] == -1):
                self.valImg[centerY, x] = value
                self.valuesArr[value] += 1
                self.RecursionNearPoints(centerY + 1, x, redis, value)
        
    def ScanNearPoints(self, centerY, centerX, redis):
        exist = False
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                if (self.imgArr[y, x] and y != centerY and x != centerX):
                    exist = True
                    break
            if (exist):
                break
        return exist
    
    def CatchNearPointsValue(self, centerY, centerX, redis):
        rVal = 0
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                if (self.valImg[y, x] != -1 and self.valImg[y, x] != 0):
                    rVal = self.valImg[y, x]
                    break
            if (rVal):
                break
        return rVal

    def ToRGBArray(self):
        print(len(self.valuesArr))
        for sVal in range (1, len(self.valuesArr)):
            judge = False
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
            if (self.valuesArr[sVal] < 10):
                judge = True
            for y in range (self.height):
                for x in range (self.width):
                    if (self.valImg[y, x] == 0 or (self.valImg[y, x] == sVal and judge)):
                        self.cImgArr[y, x, 0] = 255
                        self.cImgArr[y, x, 1] = 255
                        self.cImgArr[y, x, 2] = 255
                    elif (self.valImg[y, x] == sVal):
                        self.cImgArr[y, x, 0] = r
                        self.cImgArr[y, x, 1] = g
                        self.cImgArr[y, x, 2] = b

    # For Test
    def GaryImage(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x] == 0):
                    self.cImgArr[y, x, 0] = 255
                    self.cImgArr[y, x, 1] = 255
                    self.cImgArr[y, x, 2] = 255
                if (self.imgArr[y, x] == 1):
                    self.cImgArr[y, x, 0] = 128
                    self.cImgArr[y, x, 1] = 128
                    self.cImgArr[y, x, 2] = 128
    # ---

    # --- --- ---

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp")
    ds.Start()
    ds.CreateNewImage("./convert.bmp")
    # ds = DBSCAN("./test2.bmp")
    # ds.Start()
    # ds.CreateNewImage("./convert2.bmp")