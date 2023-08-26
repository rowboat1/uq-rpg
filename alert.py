from constants import font

class Alert:
    def __init__(self, message, colour, expiry, location):
        self.message = message
        self.colour = colour
        self.expiry = expiry
        self.location = location
        self.yincrement = 0.5
    
    def draw(self, surface):
        alert_text = font.render(self.message, True, self.colour)
        surface.blit(
            alert_text, (self.location[0], self.location[1])
        )

    def update(self):
        self.expiry -= 1
        self.location = (self.location[0], self.location[1]-self.yincrement)

    def should_be_dead(self):
        return (self.expiry<1)