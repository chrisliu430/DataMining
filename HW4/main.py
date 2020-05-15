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
        self.pointsArr = [0, 0]
        self.pointVal = 2

    def Inverting(self):
        for x in range (self.height):
            for y in range (self.width):
                if (self.imgArr[y, x]):
                    self.imgArr[y, x] = 0
                else:
                    self.imgArr[y, x] = 1

    def Clustering(self):
        # Pixel equal 1 is image pixel not background pixel
        for x in range (self.height):
            for y in range (self.width):
                if (self.imgArr[y, x] == 1):
                    self.edgeExist = self.CheckPointExist(y, x, 3)
                    if (self.edgeExist == 0):
                        self.imgArr[y, x] = 0
        for x in range (self.height):
            for y in range (self.width):
                if (self.imgArr[y, x] == 1):
                    self.edgeVal = self.CheckPointEdge(y, x, 10)
                    if (self.edgeVal == 0):
                        self.valImg[y, x] = self.pointVal
                        self.pointVal += 1
                        self.pointsArr.append(1)
                    else:
                        self.valImg[y, x] = self.edgeVal
                        self.pointsArr[self.edgeVal] += 1
                else:
                    self.valImg[y, x] = -1

    def ToRGBArray(self):
        print(self.pointVal)
        for val in range (2, len(self.pointsArr)):
            self.judge = False
            r = random.randint(1,255)
            g= random.randint(1,255)
            b = random.randint(1,255)
            if (self.pointsArr[val] < 10):
                self.judge = True
            for x in range (self.height):
                for y in range (self.width):
                    if (self.valImg[y, x] == -1 or (self.judge == True and self.valImg[y, x] == val)):
                        self.cimgArr[y, x, 0] = 255
                        self.cimgArr[y, x, 1] = 255
                        self.cimgArr[y, x, 2] = 255
                    elif (self.valImg[y, x] == val):
                        self.cimgArr[y, x, 0] = r
                        self.cimgArr[y, x, 1] = g
                        self.cimgArr[y, x, 2] = b

    def StorageIamge(self):
        cimg = Image.fromarray(self.cimgArr.astype('uint8')).convert('RGB')
        cimg.save("convert.bmp")
        
    def CheckPointEdge(self, startY, startX, radis):
        self.val = 0
        for y in range (startY - radis, startY + radis + 1):
            for x in range (startX - radis, startX + radis + 1):
                if (x < 0 or y < 0 or x >= self.height or y >= self.width):
                    break
                if (self.valImg[y, x] != -1):
                    self.val = self.valImg[y, x]
                    break
            if (self.val != 0):
                break
        return self.val

    def CheckPointExist(self, startY, startX, radis):
        self.val = 0
        for y in range (startY - radis, startY + radis + 1):
            for x in range (startX - radis, startX + radis + 1):
                if (x < 0 or y < 0 or x >= self.height or y >= self.width):
                    break
                if (self.imgArr[y, x] != 0 and x != startX and y != startY):
                    self.val = 1
                    break
            if (self.val):
                break
        return self.val

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp")
    ds.Inverting()
    ds.Clustering()
    ds.ToRGBArray()
    ds.StorageIamge()