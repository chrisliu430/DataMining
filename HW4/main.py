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

    # Finish ---
    def Inverting(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x].any()):
                    self.imgArr[y, x] = False
                else:
                    self.imgArr[y, x] = True

    def RemovePoints(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.imgArr[y, x].any() and not(self.ScanNearPoints(y, x, 2))):
                    self.ClearNearPoints(y, x, 2)

    def ClearNearPoints(self, centerY, centerX, redis):
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                else:
                    self.imgArr[y, x] = 0

    def ScanNearPoints(self, centerY, centerX, redis):
        exist = False
        counter = 0
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                elif (y == centerY and x == centerX):
                    continue
                elif (self.imgArr[y, x].any()):
                    counter += 1
                if (counter > 8):
                    exist = True
                    break
            if (exist):
                break
        return exist
        
    def ToRGBArray(self):
        print(len(self.valuesArr))
        for sVal in range (1, len(self.valuesArr)):
            judge = False
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
            if (self.valuesArr[sVal] < 50):
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
    # Finish End

    def Clustering(self):
        for y in range (self.height):
            for x in range (self.width):
                if (not(self.imgArr[y, x].any())):
                    self.valImg[y, x] = 0
                elif (self.imgArr[y, x].any() and self.valImg[y, x] == -1):
                    rVal = self.GetNearPointsValue(y, x, 5)
                    if (not(rVal)):
                        rVal = self.pointVal
                        self.valImg[y, x] = rVal
                        self.valuesArr.append(1)
                        self.pointVal += 1
                    else:
                        self.valImg[y, x] = rVal
                        self.valuesArr[rVal] += 1
                    self.RecursionCircle(y + 1, x, 3, rVal)
    
    def RecursionCircle(self, centerY, centerX, redis, value):
        stepY = False
        for x in range (centerX - redis, centerX + redis + 1):
            if (centerY < 0 or centerY >= self.height or x < 0 or x >= self.width):
                break
            elif (self.imgArr[centerY, x].any() and self.valImg[centerY, x] == -1):
                stepY = True
                self.valImg[centerY, x] = value
                self.valuesArr[value] += 1
                self.RecursionSearchLine(centerY, x, redis, value)
            if (stepY):
                stepY = False
                self.RecursionCircle(centerY + 1, x, redis, value)

    def RecursionSearchLine(self, centerY, centerX, redis, value):
        for x in range (centerX - redis, centerX + redis + 1):
            if (centerY < 0 or centerY >= self.height or x < 0 or x >= self.width):
                break
            elif (self.imgArr[centerY, x].any() and self.valImg[centerY, x] == -1):
                self.valImg[centerY, x] = value
                self.valuesArr[value] += 1
                self.RecursionSearchLine(centerY, x, redis, value)
                
    def GetNearPointsValue(self, centerY, centerX, redis):
        rVal = 0
        for y in range (centerY, centerY - redis, -1):
            for x in range (centerX - redis, centerX + redis + 1):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                elif (self.valImg[y, x] != 0 and self.valImg[y, x] != -1):
                    rVal = self.valImg[y, x]
                    break
            if (rVal):
                break
        if (not(rVal)):
            for y in range (centerY, centerY + redis + 1):
                for x in range (centerX - redis, centerX + redis + 1):
                    if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                        break
                    elif (self.valImg[y, x] != 0 and self.valImg[y, x] != -1):
                        rVal = self.valImg[y, x]
                        break
                if (rVal):
                    break
        return rVal

    # --- --- ---

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp")
    ds.Start()
    ds.CreateNewImage("./convert.bmp")
    ds = DBSCAN("./test2.bmp")
    ds.Start()
    ds.CreateNewImage("./convert2.bmp")