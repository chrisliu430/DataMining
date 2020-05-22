from PIL import Image
import numpy as np
import random
import math

class KMeans():
    def __init__(self, fileName, target):
        self.target = int(target)
        self.img = Image.open(fileName)
        self.imgArr = np.array(self.img)
        self.width, self.height = self.img.size
        self.cImgArr = np.full((self.height, self.width, 3), -1)
        # Processing ---
        self.coordinateArray = []
        self.passCoordinate = []
        self.judgeArray = []
        self.calArray = []
        self.countArray = []

    def Start(self):
        self.InitPoints()
        self.Clustering()

    def CreateImage(self, fileName = "Default.jpg"):
        for y in range (self.height):
            for x in range (self.width):
                self.cImgArr[y, x, 0] = self.coordinateArray[self.judgeArray[y * self.width + x]][0]
                self.cImgArr[y, x, 1] = self.coordinateArray[self.judgeArray[y * self.width + x]][1]
                self.cImgArr[y, x, 2] = self.coordinateArray[self.judgeArray[y * self.width + x]][2]
        cimg = Image.fromarray(self.cImgArr.astype('uint8')).convert('RGB')
        cimg.save(fileName)
    
    # Hiding Layer ---
    def InitPoints(self):
        for i in range (self.target):
            coordinate = [0, 0, 0]
            zerolist = [0, 0, 0]
            zerocoordinate = [0, 0, 0]
            self.calArray.append(zerolist)
            self.countArray.append(0)
            x = random.randint(0, 255)
            y = random.randint(0, 255)
            z = random.randint(0, 255)
            coordinate[0] = x
            coordinate[1] = y
            coordinate[2] = z
            self.coordinateArray.append(coordinate)
            self.passCoordinate.append(zerocoordinate)
        for y in range (self.height):
            for x in range (self.width):
                self.judgeArray.append(-1)

    def CheckFinishing(self):
        finish = True
        for lenN in range (self.target):
            for i in range (3):
                if (self.coordinateArray[lenN][i] != self.passCoordinate[lenN][i]):
                    finish = False
                    break
            if (not(finish)):
                break
        return finish
    
    def MoveToPass(self):
        for lenN in range (self.target):
            for i in range (3):
                self.passCoordinate[lenN][i] = self.coordinateArray[lenN][i]

    def Clustering(self):
        while (not(self.CheckFinishing())):
            self.MoveToPass()
            for y in range (self.height):
                for x in range (self.width):
                    self.judgeArray[y * self.width + x] = self.CalculateDistance(self.imgArr[y, x, 0], self.imgArr[y, x, 1], self.imgArr[y, x, 2])
                    self.CalculateTotalValueInPoint(self.judgeArray[y * self.width + x], self.imgArr[y, x, 0], self.imgArr[y, x, 1], self.imgArr[y, x, 2])
            self.CalculateNewCoordinate()

    def CalculateTotalValueInPoint(self, pos, x, y, z):
        self.calArray[pos][0] += x
        self.calArray[pos][1] += y
        self.calArray[pos][2] += z
        self.countArray[pos] += 1

    def CalculateNewCoordinate(self):
        for lenN in range (self.target):
            for i in range (3):
                if (self.countArray[lenN] != 0):
                    self.coordinateArray[lenN][i] = int(self.calArray[lenN][i] / self.countArray[lenN])
                else:
                    self.coordinateArray[lenN][i] = 0
        for lenN in range (self.target):
            for i in range (3):
                self.calArray[lenN][i] = 0
            self.countArray[lenN] = 0

    def CalculateDistance(self, calX, calY, calZ):
        calNum = 0
        minDistance = 9999999
        minPos = -1
        for i in range (self.target):
            calNum = (math.pow((self.coordinateArray[i][0] - calX), 2)
                    + math.pow((self.coordinateArray[i][1] - calY), 2)
                    + math.pow((self.coordinateArray[i][2] - calZ), 2))
            calNum = int(math.sqrt(calNum))
            minPos = i if minDistance > calNum else minPos
            minDistance = calNum if minDistance > calNum else minDistance
        return minPos
    # ---

if __name__ == "__main__":
    kms = KMeans("Demo1.jpg", 2)
    kms.Start()
    kms.CreateImage("Demo1_2_Convert.jpg")
    # kms = KMeans("Demo1.jpg", 4)
    # kms.Start()
    # kms.CreateImage("Demo1_4_Convert.jpg")
    # kms = KMeans("Demo1.jpg", 6)
    # kms.Start()
    # kms.CreateImage("Demo1_6_Convert.jpg")
    # kms = KMeans("Demo1.jpg", 8)
    # kms.Start()
    # kms.CreateImage("Demo2_8_Convert.jpg")
    # kms = KMeans("Demo2.jpg", 2)
    # kms.Start()
    # kms.CreateImage("Demo2_2_Convert.jpg")
    # kms = KMeans("Demo2.jpg", 4)
    # kms.Start()
    # kms.CreateImage("Demo2_4_Convert.jpg")
    # kms = KMeans("Demo2.jpg", 6)
    # kms.Start()
    # kms.CreateImage("Demo2_6_Convert.jpg")
    # kms = KMeans("Demo2.jpg", 8)
    # kms.Start()
    # kms.CreateImage("Demo2_8_Convert.jpg")