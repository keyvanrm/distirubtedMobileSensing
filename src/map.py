import math

class Map:
    def __init__(self, lat_up, lat_down, long_left, long_right, x_grid):
        self.lat_up = lat_up
        self.lat_down = lat_down
        self.long_left = long_left
        self.long_right = long_right
        self.x_grid = x_grid
        self.set_y_grid()
        self.y_grid = 0
        self.dx = 0.0
        self.dy = 0.0

    def set_y_grid(self):
        x_length = Map.get_distance(self.lat_down, self.long_right, self.lat_down, self.long_left)
        y_length = Map.get_distance(self.lat_down, self.long_right, self.lat_up, self.long_right)
        self.y_grid = math.ceil(self.x_grid*y_length/x_length)
        self.dx = x_length/self.x_grid
        self.dy = y_length/self.y_grid

    @staticmethod
    def get_distance(lat1, long1, lat2, long2):
        r = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_l = math.radians(long2-long1)
        delta_p = phi2-phi1
        a = math.sin(delta_p/2)*math.sin(delta_p/2) + \
            math.cos(phi1)*math.cos(phi2) * \
            math.sin(delta_l/2)*math.sin(delta_l/2)
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return r*c

    def get_coordinates(self, lat, longt):
        x = Map.get_distance(lat, longt, lat, self.long_left)
        y = Map.get_distance(lat, longt, self.lat_down, longt)
        xg = math.trunc(x/self.dx)
        yg = math.trunc(y/self.dy)
        return [xg, yg]
