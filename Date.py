class Date():
    days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    months = {1: 'January', 2: 'Feburary', 3: 'March', 4: 
    'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    def __init__(self, month, day, year):
        self.day = day
        self.month = month
        self.year = year
        self.handleLeapYear()
    def addTime(self, day, month, year):
        curr = self.day + day
        while(curr >= self.days[self.month]):
            curr -= self.days[self.month]
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
                self.handleLeapYear()
        self.day = curr
        self.month+= month
        while(self.month > 12):
            self.month -= 12
            self.year += 1
            self.handleLeapYear()
        self.year += year
        self.handleLeapYear()
    def backTime(self, day, month, year):
        newDate = Date(self.month, self.day, self.year)
        newDate.year -= year
        newDate.handleLeapYear()
        newDate.month -= month
        while(newDate.month <= 0):
            if newDate.month == 0:
                newDate.month = 12
                newDate.year -= 1
                newDate.handleLeapYear()
            elif newDate.month < -12:
                newDate.month += 12
                newDate.year -= 1
                newDate.handleLeapYear()
            else:
                newDate.month = newDate.month %12
                newDate.year -= 1
                newDate.handleLeapYear()
        newDate.day -= day
        while(newDate.day <= 0):
            if newDate.month > 1:
                newDate.day += newDate.days[newDate.month-1]
                newDate.month -= 1
            else:
                newDate.year -= 1
                newDate.month = 12
                newDate.day = newDate.days[newDate.month]
            
        return newDate
    def handleLeapYear(self):
        if (self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)):
            self.days[2] = 29
        else:
            self.days[2] = 28
    def __repr__(self):
        return f'{self.months[self.month]} {self.day}, {self.year}'
    def getDateFormat(self):
        y = self.year
        m = str(self.month).zfill(2)
        d = str(self.day).zfill(2)
        return f'{y}-{m}-{d}'
    def __eq__(self, other):
        return isinstance(other, Date) and self.year == other.year and self.day == other.day and self.month == other.month
    def __lt__(self, other):
        if not isinstance(other, Date):
            return True
        if other.year < self.year:
            return False
        if self.year < other.year:
            return True
        if other.month < self.month:
            return False
        if self.month < other.month:
            return True
        if other.day < self.day:
            return False
        return True