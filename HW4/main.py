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
                elif (self.imgArr[y, x]):
                    self.valImg[y, x] = self.pointVal
                    self.valuesArr.append(1)
                    self.pointVal += 1
                    self.RecursionNearPoints(y + 1, x, 3, self.pointVal - 1)

    def RecursionNearPoints(self, centerY, cencterX, redis, value):
        for x in range (cencterX - redis, cencterX + redis + 1):
            if (self.imgArr[centerY, x]):
                self.valImg[centerY, x] = value
                self.valuesArr[value] += 1
                self.RecursionNearPoints(centerY + 1, x, redis, value)
                return

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

    def ToRGBArray(self):
        print(self.valuesArr[1])
        print(self.pointVal)

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