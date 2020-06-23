from PIL import Image
import numpy as np
import random
import math

class DBSCAN():
    def __init__(self, fileName, radis, less):
        self.img = Image.open(fileName)
        self.radis = radis
        self.less = less
        # --- Image
        self.width, self.height = self.img.size
        self.imgArr = np.array(self.img)
        self.valImgArr = np.full((self.height, self.width), -1)
        self.newImgArr = np.full((self.height, self.width, 3), -1)
        # --- Image Value
        self.value = 1
        self.valArr = [0]

    def Start(self):
        self.Scan()
        self.VerifyPass()
        self.TransToRGB()
        print(self.value)

    def CreateNewImage(self, fileName):
        cimg = Image.fromarray(self.newImgArr.astype('uint8')).convert('RGB')
        cimg.save(fileName)

    # --- Hiding Layer
    def CalculateRadis(self, y, x, targetY, targetX):
        return int(math.sqrt(math.pow((y - targetY), 2) + math.pow((x - targetX), 2)))
    
    def Scan(self):
        for y in range (self.height):
            for x in range (self.width):
                checkValue = self.ScanNearValue(y, x)
                if (self.imgArr[y, x]):
                    self.valImgArr[y, x] = 0
                elif (not(self.imgArr[y, x]) and self.valImgArr[y, x] == -1 and checkValue == -1):
                    self.valImgArr[y, x] = self.value
                    self.valArr.append(1)
                    self.RecursionPassLine(y, x + 1, self.value)
                    self.RecursionPassPoint(y + 1, x, self.value)
                    self.value += 1
                elif (not(self.imgArr[y, x]) and self.valImgArr[y, x] == -1 and checkValue != -1):
                    self.valImgArr[y, x] = checkValue
                    self.valArr[checkValue] += 1
                    self.RecursionPassLine(y, x + 1, checkValue)
                    self.RecursionPassPoint(y + 1, x, checkValue)
    
    def RecursionPassPoint(self, y, x, val):
        if (not(self.imgArr[y, x])):
            self.valImgArr[y, x] = val
            self.valArr[val] += 1
            self.RecursionPassPoint(y, x - 1, val)
        else:
            return
    
    def RecursionPassLine(self, y, x, val):
        if (not(self.imgArr[y, x])):
            self.valImgArr[y, x] = val
            self.valArr[val] += 1
            self.RecursionPassPoint(y, x, val)
            self.RecursionPassLine(y - 1, x, val)
        else:
            return

    def ScanNearValue(self, centerY, centerX):
        rVal = -1
        for y in range (centerY - self.radis, centerY + self.radis + 1):
            for x in range (centerX - self.radis, centerX + self.radis + 1):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width or self.CalculateRadis(centerY, centerX, y, x) > self.radis):
                    continue
                elif (self.CalculateRadis(centerY, centerX, y, x) <= self.radis and self.valImgArr[y, x] != -1 and self.valImgArr[y, x] != 0):
                    rVal = self.valImgArr[y, x]
                    break
            if (rVal != -1):
                break
        return rVal

    def VerifyPass(self):
        for clearVal in range (1, self.value):
            if (self.valArr[clearVal] < self.less):
                self.ClearNoPassPoint(clearVal)
                self.valArr[clearVal] = 0

    def ClearNoPassPoint(self, cVal):
        for y in range (self.height):
            for x in range (self.width):
                if (self.valImgArr[y, x] == cVal):
                    self.valImgArr[y, x] = 0
    
    def TransToRGB(self):
        for y in range (self.height):
            for x in range (self.width):
                if (self.valImgArr[y, x] == 0):
                    for cir in range (3):
                        self.newImgArr[y, x, cir] = 255
        for pVal in range (1, self.value):
            if (self.valArr[pVal] != 0):
                self.Render(pVal, random.randint(1,255), random.randint(1,255), random.randint(1,255))

    def Render(self, val, r, g, b):
        for y in range (self.height):
            for x in range (self.width):
                if (self.valImgArr[y, x] == val):
                    self.newImgArr[y, x, 0] = r
                    self.newImgArr[y, x, 1] = g
                    self.newImgArr[y, x, 2] = b
    # --- --- ---

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp", 1, 5)
    ds.Start()
    ds.CreateNewImage("./convert_1_5.bmp")