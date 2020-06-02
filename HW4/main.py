from PIL import Image
import numpy as np
import random
import math

class DBSCAN():
    def __init__(self, fileName, minNumber, redis):
        self.img = Image.open(fileName)
        self.imgArr = np.array(self.img)
        self.width, self.height = self.img.size
        self.valImg = np.full((self.height, self.width), -1)
        self.cImgArr = np.full((self.height, self.width, 3), -1)
        self.valuesArr = [0]
        self.pointVal = 1
        self.minNumber = minNumber
        self.redis = redis

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
                if (self.imgArr[y, x].any() and not(self.ScanNearPoints(y, x, self.redis))):
                    self.imgArr[y, x] = 0

    def ScanNearPoints(self, centerY, centerX, redis):
        exist = False
        counter = 0
        distance = 0
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                distance = int(math.sqrt(math.pow((y - centerY), 2) + math.pow((x - centerX), 2)))
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                elif ((y == centerY and x == centerX) or (self.imgArr[y, x].any() and distance <= redis)):
                    counter += 1
                if (counter > 1):
                    exist = True
                    break
            if (exist):
                break
        return exist

    def ClearNearPoints(self, centerY, centerX, redis):
        only = True
        distance = 0
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                distance = int(math.sqrt(math.pow((y - centerY), 2) + math.pow((x - centerX), 2)))
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                elif (y == centerY and x == centerX):
                    continue
                elif (distance <= redis):
                    only = False
        if (only):
            self.imgArr[centerY, centerX] = 0

    def ToRGBArray(self):
        print(len(self.valuesArr))
        for sVal in range (1, len(self.valuesArr)):
            judge = False
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
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

    def CheckPassMinNumber(self, centerY, centerX, redis):
        passStatus = False
        counter = 0
        distance = 0
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                distance = int(math.sqrt(math.pow((y - centerY), 2) + math.pow((x - centerX), 2)))
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                elif ((y == centerY and x == centerX) or (self.imgArr[y, x].any() and distance <= redis)):
                    counter += 1
                if (counter >= self.minNumber):
                    passStatus = True
                    break
            if (passStatus):
                break
        return passStatus

    def ChangePassYAxisValue(self, centerY, centerX, redis, value):
        distance = 0
        for y in range (centerY, centerY - redis - 1, -1):
            distance = int(math.sqrt(math.pow((y - centerY), 2)))
            if (y < 0 or y >= self.height or centerX < 0 or centerX >= self.width):
                break
            elif (y == centerY):
                continue
            elif (self.imgArr[y, centerX].any() and distance <= redis):
                self.valImg[y, centerX] = value
                self.ChangePassYAxisValue(y, centerX, redis, value)
                self.ChangePassXAxisValue(y, centerX, redis, value)
            else:
                return

    def ChangePassXAxisValue(self, centerY, centerX, redis, value):
        distance = 0
        for x in range (centerX, centerX - redis - 1, -1):
            distance = int(math.sqrt(math.pow((x - centerX), 2)))
            if (centerY < 0 or centerY >= self.height or x < 0 or x >= self.width):
                break
            elif (x == centerX):
                continue
            elif (self.imgArr[centerY, x].any() and distance <= redis):
                self.valImg[centerY, x] = value
                self.ChangePassXAxisValue(centerY, x, redis, value)
            else:
                return

    def Clustering(self):
        for y in range (self.height):
            for x in range (self.width):
                if (not(self.imgArr[y, x].any())):
                    self.valImg[y, x] = 0
                elif (self.imgArr[y, x].any()):
                    if (self.CheckPassMinNumber(y, x, self.redis)):
                        rVal = self.GetNearPointsValue(y, x, self.redis)
                        if (rVal == 0):
                            rVal = self.pointVal
                            self.valImg[y, x] = rVal
                            self.valuesArr.append(1)
                            self.pointVal += 1
                        else:
                            self.valImg[y, x] = rVal
                            self.valuesArr[rVal] += 1
                    else:
                        rVal = self.GetNearPointsValue(y, x, self.redis)
                        if (rVal == 0):
                            self.valImg[y, x] = 0
                        else:
                            self.valImg[y, x] = rVal
                        self.ChangePassYAxisValue(y, x, self.redis, rVal)
                    self.ChangePassXAxisValue(y, x, self.redis, rVal)

    def GetNearPointsValue(self, centerY, centerX, redis):
        rVal = 0
        distance = 0
        for y in range (centerY - redis, centerY + redis + 1):
            for x in range (centerX - redis, centerX + redis + 1):
                distance = int(math.sqrt(math.pow((y - centerY), 2) + math.pow((x - centerX), 2)))
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    break
                elif (self.valImg[y, x] != 0 and self.valImg[y, x] != -1 and distance <= redis):
                    rVal = self.valImg[y, x]
                    break
            if (rVal):
                break
        return rVal

    # --- --- ---

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp", 5, 1)
    ds.Start()
    ds.CreateNewImage("./convert_1_5.bmp")
    # ds = DBSCAN("./test.bmp", 7, 1)
    # ds.Start()
    # ds.CreateNewImage("./convert_1_7.bmp")
    # ds = DBSCAN("./test.bmp", 5, 3)
    # ds.Start()
    # ds.CreateNewImage("./convert_3_5.bmp")
    # ds = DBSCAN("./test.bmp", 35, 5)
    # ds.Start()
    # ds.CreateNewImage("./convert_5_35.bmp")
    # ---
    # ds = DBSCAN("./test2.bmp", 5, 1)
    # ds.Start()
    # ds.CreateNewImage("./convert2_1_5.bmp")
    # ds = DBSCAN("./test2.bmp", 7, 1)
    # ds.Start()
    # ds.CreateNewImage("./convert2_1_7.bmp")
    # ds = DBSCAN("./test2.bmp", 5, 3)
    # ds.Start()
    # ds.CreateNewImage("./convert2_3_5.bmp")
    # ds = DBSCAN("./test2.bmp", 35, 5)
    # ds.Start()
    # ds.CreateNewImage("./convert2_5_35.bmp")