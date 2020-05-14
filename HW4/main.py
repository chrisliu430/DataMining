from PIL import Image
import numpy as np
import random

class DBSCAN():
    def __init__(self, fileName):
        self.fileName = fileName
        self.img = Image.open(fileName)
        self.imgArr = np.array(self.img)
        self.width, self.height = np.shape(self.imgArr)
        self.cimgArr = np.full((self.width, self.height, 3), 0)
        self.valImg = np.full((self.width, self.height), 0)
        self.stack = []
        self.pointPos = [-1, -1]
        self.pointVal = 2
        self.distance = 0
    def Inverting(self):
        for x in range (self.height):
            for y in range (self.width):
                if (self.imgArr[y, x]):
                    self.imgArr[y, x] = 0
                else:
                    self.imgArr[y, x] = 1
    def Clustering(self):
        for x in range (self.height):
            for y in range (self.width):
                if (self.imgArr[y, x] == 1):
                    returnVal = self.CheckPointValue(y, x)
                    if (returnVal == 0 and self.CheckPointFact(y, x) == 1):
                        self.valImg[y, x] = -1
                    elif (returnVal == 0):
                        self.valImg[y, x] = self.pointVal
                        self.pointVal += 1
                    else:
                        self.valImg[y, x] = returnVal
    def ToRGBArray(self):
        print(self.pointVal)
        for k in range (2, self.pointVal + 1):
            r = random.randint(1, 255)
            g = random.randint(1, 255)
            b = random.randint(1, 255)
            for x in range (self.height):
                for y in range (self.width):
                    if (self.valImg[y, x] == k):
                        self.cimgArr[y, x, 0] = r
                        self.cimgArr[y, x, 1] = g
                        self.cimgArr[y, x, 2] = b
                    elif (self.valImg[y, x] == -1):
                        self.cimgArr[y, x, 0] = 255
                        self.cimgArr[y, x, 1] = 255
                        self.cimgArr[y, x, 2] = 255
                    elif (self.valImg[y, x] == 0):
                        self.cimgArr[y, x, 0] = 255
                        self.cimgArr[y, x, 1] = 255
                        self.cimgArr[y, x, 2] = 255
    def StorageIamge(self):
        cimg = Image.fromarray(self.cimgArr.astype('uint8')).convert('RGB')
        cimg.save("convert.bmp")
    def CheckPointValue(self, startY, startX):
        self.val = 0
        if (self.valImg[startY - 1, startX - 1] != 0):
            self.val = self.valImg[startY - 1, startX - 1]
        elif (self.valImg[startY - 1, startX] != 0):
            self.val = self.valImg[startY - 1, startX]
        elif (self.valImg[startY - 1, startX + 1] != 0):
            self.val = self.valImg[startY - 1, startX + 1]
        elif (self.valImg[startY, startX - 1] != 0):
            self.val = self.valImg[startY, startX - 1]
        elif (self.valImg[startY, startX + 1] != 0):
            self.val = self.valImg[startY, startX + 1]
        elif (self.valImg[startY + 1, startX - 1] != 0):
            self.val = self.valImg[startY + 1, startX - 1]
        elif (self.valImg[startY + 1, startX] != 0):
            self.val = self.valImg[startY + 1, startX]
        elif (self.valImg[startY + 1, startX + 1] != 0):
            self.val = self.valImg[startY + 1, startX + 1]
        return self.val
    def CheckPointFact(self, startY, startX):
        self.val = 1
        if (self.imgArr[startY - 1, startX - 1] == 1):
            self.val = 0
        elif (self.imgArr[startY - 1, startX] == 1):
            self.val = 0
        elif (self.imgArr[startY - 1, startX + 1] == 1):
            self.val = 0
        elif (self.imgArr[startY, startX - 1] == 1):
            self.val = 0
        elif (self.imgArr[startY, startX + 1] == 1):
            self.val = 0
        elif (self.imgArr[startY + 1, startX - 1] == 1):
            self.val = 0
        elif (self.imgArr[startY + 1, startX] == 1):
            self.val = 0
        elif (self.imgArr[startY + 1, startX + 1] == 1):
            self.val = 0
        return self.val

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp")
    ds.Inverting()
    ds.Clustering()
    ds.ToRGBArray()
    ds.StorageIamge()