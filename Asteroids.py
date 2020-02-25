"""
File: Rocks.py
Original Author: Br. Burton
Designed to be completed by others

This program implements the Rocks game.
"""
import arcade
from random import randrange
from random import uniform
import math as m
from abc import abstractmethod
from abc import ABC
  
  
# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 30

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 15

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 5

#Function to check collisions for bullets and asteroids
def checkCollision(list1, list2, scoreList):
    newList1 = []
    newList2 = []
    removeListx = []
    removeListy = []
    for x in list1:
        for y in list2:
            xTest = y.point.x - y.radius <= x.point.x + x.radius and \
                    y.point.x + y.radius >= x.point.x - x.radius
            yTest = y.point.y - y.radius <= x.point.y + x.radius and \
                    y.point.y + y.radius >= x.point.y - x.radius
            if(xTest and yTest):
                if(x not in removeListx):
                    removeListx.append(x)
                if(y not in removeListy):
                    removeListy.append(y)
                    if(isinstance(x, Big)):
                        scoreList[0] += 100
                    elif(isinstance(x, Medium)):
                        scoreList[0] += 300
                    else:
                        scoreList[0] += 500
                newList1 += x.hit()
                newList2 += y.hit()
    for x in removeListx:
        list1.remove(x)
    for x in removeListy:
        list2.remove(x)
    list1 += newList1
    list2 += newList2

#Initiates the velocities for every object in the game
class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0

#Initiates the starting point of the asteroids in the game
class Point:
    def __init__(self):
        self.x = uniform(0,800)
        self.y = uniform(0,600)
        
#Parent class of Rock, Ship, and Bullet       
class FlyingObject:
    #Initail member function. Initializes the velocity, starting coordinate and speeds
    def __init__(self):
        self.velocity = Velocity()
        self.point = Point()
        self.angle = 0
    #Hit function to determine what happens if collision happens
    @abstractmethod
    def hit(self):
        pass
    #Moves the object from frame to frame based on the velocities
    def advance(self):
        self.point.x += self.velocity.dx
        self.point.y += self.velocity.dy
    #Checks for if object is offscreen, and wraps the object to the other side
    def wrap(self):
        if(self.point.x > SCREEN_WIDTH):
            self.point.x = 0
        if(self.point.x < 0):
            self.point.x = SCREEN_WIDTH
        if(self.point.y > SCREEN_HEIGHT):
            self.point.y = 0
        if(self.point.y < 0):
            self.point.y = SCREEN_HEIGHT

#Bullet class, used for when the ship fires
class Bullet(FlyingObject):
    #Initial member function
    def __init__(self, x, y, dx, dy, angle):
        super().__init__()
        self.point.x = x
        self.point.y = y
        self.velocity.dx = BULLET_SPEED * m.cos(m.radians(angle)) + dx
        self.velocity.dy = BULLET_SPEED * m.sin(m.radians(angle)) + dy
        self.angle = angle
        self.life = BULLET_LIFE
        self.radius = BULLET_RADIUS
    def hit(self):
        return []
    #Moves the bullet, also keeps track of how many frames the bullet is alive
    def advance(self):
        self.point.x += self.velocity.dx
        self.point.y += self.velocity.dy
        self.life += -1
    #Draw function, uploads the png, and draws it on the screen
    def draw(self):
        texture = arcade.load_texture("laser.png")
        
        arcade.draw_texture_rectangle(self.point.x, self.point.y, \
                                      texture.width, texture.height, \
                                      texture, self.angle)

#Ship class, keeps track of all the actions for the ship
class Ship(FlyingObject):
    #Initializes everything, changing coordinates to start at the center
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.point.x = SCREEN_WIDTH / 2
        self.point.y = SCREEN_HEIGHT / 2
        self.alive = True
        self.radius = SHIP_RADIUS
        self.texture = 'ship.png'
    #hit function that sets texture to None to make the ship disappear
    def hit(self):
        self.texture = None
        self.alive = False
    #Returns a bullet object to append to the list of bullets on the screen
    def fire(self):
        return Bullet(self.point.x, self.point.y, self.velocity.dx, \
                      self.velocity.dy, self.angle + 90)
    #Draws the ship based off of the member attribute texture
    def draw(self):
        texture = arcade.load_texture(self.texture)
        
        arcade.draw_texture_rectangle(self.point.x, self.point.y, \
                                      texture.width, texture.height, \
                                      texture, self.angle)
        
#Rock class, the parent class of Big, Medium, and Small
class Rock(FlyingObject):
    #Initiates the member data. Not used here, but will help with Child classes
    def __init__(self):
        super().__init__()
    #Each Child class has this function, so it is an abstract method
    @abstractmethod
    def hit(self):
        pass
    #Each Child class has this function, so it is an abstract method
    @abstractmethod
    def advance(self):
        pass
    #Each Child class has this function, so it is an abstract method
    @abstractmethod
    def draw(self):
        pass

#Big class, used at the beginning of the game
class Big(Rock):
    #Initializes the member attributes to be used
    def __init__(self):
        super().__init__()
        self.angle = randrange(0, 359)
        self.velocity.dx = BIG_ROCK_SPEED * m.cos(m.radians(self.angle))
        self.velocity.dy = BIG_ROCK_SPEED * m.sin(m.radians(self.angle))
        self.radius = BIG_ROCK_RADIUS
    #When hit, adds a list of two medium objects and a small object
    def hit(self):
        newList = [Medium(self.point.x, self.point.y, -1, self.angle), \
                   Medium(self.point.x, self.point.y, 1, self.angle), \
                   Small(self.point.x, self.point.y, 1, True, 0, self.angle)]
        return newList
    #Moves object from frame to frame based on velocity
    def advance(self):
        self.point.x += self.velocity.dx
        self.point.y += self.velocity.dy
        self.angle += BIG_ROCK_SPIN
        self.radius = BIG_ROCK_RADIUS
    #Draw function, uploads the png, and draws it on the screen  
    def draw(self):
        texture = arcade.load_texture("big.png")
        arcade.draw_texture_rectangle(self.point.x, self.point.y, \
                                      self.radius * 2, self.radius * 2, \
                                      texture, self.angle)

#Medium class, used only when a bullet collides with a Big object
class Medium(Rock):
    #Initializes the member attributes to be used
    def __init__(self, x, y, direction, angle):
        super().__init__()
        self.point.x = x
        self.point.y = y
        self.angle = angle
        self.velocity.dx = BIG_ROCK_SPEED * m.cos(m.radians(angle))
        self.velocity.dy = (BIG_ROCK_SPEED + 2 * direction) * m.sin(m.radians(angle))
        self.radius = MEDIUM_ROCK_RADIUS
    #When hit, adds a list of two small objects
    def hit(self):
        velocity = m.sqrt(self.velocity.dx**2 + self.velocity.dy**2)
        newList = [Small(self.point.x, self.point.y, -1, False, velocity, \
                         self.angle), \
                   Small(self.point.x, self.point.y, 1, False, velocity, \
                         self.angle)]
        return newList
    #Moves object from frame to frame based on velocity
    def advance(self):
        self.point.x += self.velocity.dx
        self.point.y += self.velocity.dy
        self.angle += MEDIUM_ROCK_SPIN
        self.radius = MEDIUM_ROCK_RADIUS
    #Draw function, uploads the png, and draws it on the screen
    def draw(self):
        texture = arcade.load_texture("medium.png")
        
        arcade.draw_texture_rectangle(self.point.x, self.point.y, \
                                      texture.width, texture.height,\
                                      texture, self.angle)

#Small class, used when a bullet collides with a Big object or a Medium object
class Small(Rock):
    #Initializes the member attributes to be used,
    #direction based on previous object hit(Big or Medium)
    def __init__(self, x, y, direction, bigCheck, velocity, angle):
        super().__init__()
        self.point.x = x
        self.point.y = y
        self.angle = angle
        if(bigCheck):
            self.velocity.dx = (BIG_ROCK_SPEED + 5) * m.cos(m.radians(angle))
            self.velocity.dy = BIG_ROCK_SPEED * m.sin(m.radians(angle))
        else:
            self.velocity.dx = (velocity + 1.5 * direction) * m.cos(m.radians(angle))
            self.velocity.dy = (velocity + 1.5 * direction) * m.sin(m.radians(angle))
        self.radius = SMALL_ROCK_RADIUS
    #When hit, returns an empty list
    def hit(self):
        return []
    #Moves object from frame to frame based on velocity
    def advance(self):
        self.point.x += self.velocity.dx
        self.point.y += self.velocity.dy
        self.angle += MEDIUM_ROCK_SPIN
    #Draw function, uploads the png, and draws it on the screen
    def draw(self):
        texture = arcade.load_texture("small.png")
        
        arcade.draw_texture_rectangle(self.point.x, self.point.y, \
                                      texture.width, texture.height, texture,\
                                      self.angle)

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes
    """
    
    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.lRocks = [Big(), Big(), Big(), Big(), Big()]
        self.lLazers = []
        self.ship = Ship()
        self.title_screen = True
        self.secret = False
        self.text_counter = 0
        self.score = [0]

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        Also, includes boolean for a title screen and a score screen
        """

        # clear the screen to begin drawing
        arcade.start_render()
        
        
        # TODO: draw each object
        for x in self.lRocks:
                x.draw()
        #You win screen
        if(self.ship.alive):
            if(self.title_screen):
                arcade.draw_text("Asteroids!", 315, 400, arcade.color.YELLOW, 30)
                sTexture = arcade.load_texture('ship.png')
        
                if(self.text_counter % 60 >= 0 and self.text_counter % 60 <= 30):
                    arcade.draw_text("Press Enter to Play", 335, 300, arcade.color.YELLOW, 12)
                arcade.draw_texture_rectangle(390, 200, sTexture.width, sTexture.height, sTexture)
                #Shhhhhhh it's a secret ;)
                if(self.secret):
                    arcade.draw_text("Made by Nicolaas Gartside!", 270, 100, arcade.color.YELLOW, 18)
            else:
                arcade.draw_text("Score: {}".format(self.score[0]), 20, 570, arcade.color.YELLOW, 12)
                self.ship.draw()
        
            for x in self.lLazers:
                x.draw()
        #Game over screen
        else:
            arcade.draw_text("Game", 315, 400, arcade.color.YELLOW, 50)
            arcade.draw_text("Over!", 316, 300, arcade.color.YELLOW, 50)
            if(self.text_counter % 60 >= 0 and self.text_counter % 60 <= 30):
                arcade.draw_text("Final Score: {}".format(self.score[0]), 290, 200, arcade.color.YELLOW, 30)
        if(self.lRocks == []):
            arcade.draw_text("You", 320, 400, arcade.color.YELLOW, 50)
            arcade.draw_text("Win!!", 315, 300, arcade.color.YELLOW, 50)
            arcade.draw_text("Congratulations!", 155, 200, arcade.color.YELLOW, 55)
            if(self.text_counter % 60 >= 0 and self.text_counter % 60 <= 30):
                arcade.draw_text("Final Score: {}".format(self.score[0]), 250, 100, arcade.color.YELLOW, 30)
            
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        self.ship.advance()
        self.ship.wrap()
        ship = self.ship
        for x in self.lRocks:
                x.wrap()
                x.advance()
                
        if(self.title_screen):
            self.text_counter += 1
        else:
            for x in self.lLazers:
                x.wrap()
                x.advance()
                if(x.life <= 0):
                    self.lLazers.remove(x)
            for x in self.lRocks:
                xTest = ship.point.x - ship.radius <= x.point.x + x.radius and \
                         ship.point.x + ship.radius >= x.point.x - x.radius
                yTest = ship.point.y - ship.radius <= x.point.y + x.radius and \
                           ship.point.y + ship.radius >= x.point.y - x.radius
                if(xTest and yTest):
                   self.ship.hit()
        if(self.lRocks == [] or self.ship.alive == False):
            self.text_counter += 1
        

        # TODO: Check for collisions
        checkCollision(self.lRocks, self.lLazers, self.score)
    
        ship = self.ship
                    
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if(self.title_screen == False):
            if arcade.key.LEFT in self.held_keys:
                self.ship.angle += SHIP_TURN_AMOUNT

            if arcade.key.RIGHT in self.held_keys:
                self.ship.angle += -SHIP_TURN_AMOUNT

            if arcade.key.UP in self.held_keys:
                self.ship.velocity.dx += m.cos(m.radians(self.ship.angle + 90))
                self.ship.velocity.dy += m.sin(m.radians(self.ship.angle + 90))

        if arcade.key.DOWN in self.held_keys:
            self.ship.velocity.dx = 0
            self.ship.velocity.dy = 0

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                if(self.title_screen == False):
                    self.lLazers.append(self.ship.fire())
                
        if key == arcade.key.ENTER:
            self.title_screen = False
        
        if key == arcade.key.N:
            self.secret = True

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()