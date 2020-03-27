class User:
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.total = 0
    def show(self):
        print("Name: {}\nScore: {}\nTotal: {}".format(self.name,self.score,self.total))
    