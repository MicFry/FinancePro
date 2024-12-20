import math
from cmu_graphics import *
class Chart():
    def __init__(self, name, testData, topLeftX, topLeftY, bottomRightX, bottomRightY, tickCount, tickSize):
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.bottomRightX = self.bottomRightX-25
        self.name = name
        self.numChartPoints = 100
        self.overallData = testData
        self.testData = []
        self.timestamps = []
        self.loadPriceData()
        self.fontSize = 10
        self.tickCount = tickCount
        self.tickSize = tickSize
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.lengthX = abs(self.topLeftX-self.bottomRightX)
        self.lengthY = abs(self.topLeftY- self.bottomRightY)
        self.nameFont = int(self.lengthY*0.05)
        self.bottomLeftX = self.topLeftX
        self.bottomLeftY = self.topLeftY + self.lengthY + self.nameFont
        self.minAxis = 0
        self.maxAxis = 100
        self.axisIncrement = 0
        self.loadAxis()
        self.endLine = True
        self.maxLine = True
        self.minLine = True
        self.fontSizeY = self.fontSize
    def loadPriceData(self):
        timestamps = []
        for b in range(0, len(self.overallData), int((len(self.overallData)-1)/self.numChartPoints)):
            self.testData.append(self.overallData[b][1])
            if b%math.floor((app.numChartPoints+1)/app.tickCount) == 0:
                self.timestamps.append(self.overallData[b][0].strftime('%Y-%m-%d'))
    def loadAxis(self):
        self.minAxis = int(0.98 * min(self.testData))
        delta = 0.02 * min(self.testData)
        self.maxAxis = int(max(self.testData) + delta)
        self.axisIncrement = (self.maxAxis - self.minAxis)/self.tickCount
    def draw(self):
        drawLabel(self.name, self.topLeftX+self.lengthX/2, self.topLeftY+self.nameFont/2, size = self.nameFont)
        self.drawAxis()
        self.drawPoints()
    def drawAxis(self):
        drawLine(self.bottomLeftX, self.bottomLeftY, self.bottomLeftX + self.lengthX, self.bottomLeftY)
        drawLine(self.bottomLeftX, self.bottomLeftY, self.bottomLeftX, self.bottomLeftY - self.lengthY)
        for i in range(self.tickCount):
            drawLabel("{:.2f}".format(self.minAxis + i * self.axisIncrement), self.bottomLeftX - self.tickSize - self.fontSize-7, self.bottomLeftY - (i+1)*self.lengthY/self.tickCount, size = self.fontSize)
            drawLine(self.bottomLeftX + self.tickSize, self.bottomLeftY - (i+1)*self.lengthY/self.tickCount, self.bottomLeftX - self.tickSize, self.bottomLeftY - (i+1)*self.lengthY/self.tickCount)
        for i in range(self.tickCount):
            drawLabel(self.timestamps[i], self.bottomLeftX + (i+1) * int(self.lengthX/self.tickCount), self.bottomLeftY + self.tickSize + 7, size = self.fontSize)
            drawLine(self.bottomLeftX + (i+1) * int(self.lengthX/self.tickCount), self.bottomLeftY + self.tickSize, self.bottomLeftX + (i+1) * int(self.lengthX/self.tickCount), self.bottomLeftY - self.tickSize)
    def drawPoints(self):
        for i in range(len(self.getPoints())):
            if i != 0:
                f = 'gray'
                if self.getPoints()[i-1][1] - self.getPoints()[i][1] > 0:
                    f = 'green'
                if self.getPoints()[i-1][1] - self.getPoints()[i][1] < 0:
                    f = 'red'
                drawLine(self.getPoints()[i-1][0], self.getPoints()[i-1][1], self.getPoints()[i][0], self.getPoints()[i][1], fill = f)
            #drawCircle(self.getPoints()[i][0], self.getPoints()[i][1], 2)
            if self.getPoints()[i][1] == self.maxPoints(self.getPoints()):
                f2 = 'red'
                maxX = len(self.getPoints())-1
                if self.maxLine:
                    drawLine(self.getPoints()[maxX][0], self.getPoints()[i][1], self.getPoints()[0][0], self.getPoints()[i][1], lineWidth = 2, dashes = True, fill = f2)
                    drawLabel("{:.2f}".format(self.testData[i]), self.getPoints()[maxX][0] + 22, self.getPoints()[i][1], size = 10, fill = f2)
            elif self.getPoints()[i][1] == self.minPoints(self.getPoints()):
                f2 = 'green'
                maxX = len(self.getPoints())-1
                if self.minLine:
                    drawLine(self.getPoints()[maxX][0], self.getPoints()[i][1], self.getPoints()[0][0], self.getPoints()[i][1], lineWidth = 2, dashes = True, fill = f2)
                    drawLabel("{:.2f}".format(self.testData[i]), self.getPoints()[maxX][0] + 22, self.getPoints()[i][1], size = 10, fill = f2)
            elif i == len(self.getPoints())-1:
                f2 = 'orange'
                if self.endLine:
                    drawLine(self.getPoints()[i][0], self.getPoints()[i][1], self.getPoints()[0][0], self.getPoints()[i][1], lineWidth = 2, dashes = True, fill = f2)
                    drawLabel("{:.2f}".format(self.testData[i]), self.getPoints()[i][0] + 22, self.getPoints()[i][1], size = 10, fill = f2)
    def maxPoints(self, p):
        max = 0
        for i in p:
            if i[1] > max:
                max = i[1]
        return max
    def minPoints(self, p):
        min = 100000
        for i in p:
            if i[1] < min:
                min = i[1]
        return min
    def getPoints(self):
        L = self.testData
        result = []
        for i in range(len(L)):
            x = self.bottomLeftX + i * self.lengthX/(len(self.testData)-1)
            y = self.bottomLeftY-(self.lengthY*(self.testData[i]-self.minAxis)/(self.maxAxis - self.minAxis))
            result.append((x, y))
        return result
    def inBounds(self, x, y):
        return x >= self.bottomLeftX and x <= (self.bottomLeftX + self.lengthX) and y <= self.bottomLeftY and y >= (self.bottomLeftY - self.lengthY)
    def yScale(self):
        maxY = max(self.testData)
        return 0.9 * self.lengthY/maxY