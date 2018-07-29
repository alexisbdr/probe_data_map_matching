class Node():
    latitude=0#A
    longitude=0#B

    def __init__(self, data):
        self.latitude=float(data.split("/")[0])
        self.longitude=float(data.split("/")[1])

