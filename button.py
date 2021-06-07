class Button:

    max_x = 8
    max_y = 8

    def __init__( self, x, y ):
        self._x = x
        self._y = y

    def __repr__(self):
        return f"{self.x}:{self.y}"

    def in_range(self):
        return self.x >= 0 and self.x < self.max_x and self.y >= 0 and self.y < self.max_y

    @property
    def x( self ):
        return self._x
    
    @x.setter
    def x( self, value ):
        self._x = value

    @property
    def y( self ):
        return self._y
    
    @y.setter
    def y( self, value ):
        self._y = value