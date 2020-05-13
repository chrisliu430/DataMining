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
        self.points = 2
        self.minPoints = 20
    def Inverting(self):
        for x in range (self.height):
            for y in range (self.width):
                if (self.imgArr[y, x]):
                    self.imgArr[y, x] = 0
                else:
                    self.imgArr[y, x] = 1
    def Clustering(self):
        pass
    def ToRGBArray(self):
        for k in range (1, self.points):
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            for x in range (self.height):
                for y in range (self.width):
                    if (self.imgArr[y, x] == k):
                        self.cimgArr[y, x, 0] = r
                        self.cimgArr[y, x, 1] = g
                        self.cimgArr[y, x, 2] = b
                    else:
                        self.cimgArr[y, x, 0] = 255
                        self.cimgArr[y, x, 1] = 255
                        self.cimgArr[y, x, 2] = 255
    def StorageIamge(self):
        cimg = Image.fromarray(self.cimgArr.astype('uint8')).convert('RGB')
        cimg.save("convert.bmp")
        pass

if __name__ == "__main__":
    ds = DBSCAN("./test.bmp")
    ds.Inverting()
    ds.Clustering()
    ds.ToRGBArray()
    ds.StorageIamge()