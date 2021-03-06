import glfw
from OpenGL.GL import *

# abstraction for glfw
KEY_W = glfw.KEY_W
KEY_A = glfw.KEY_A
KEY_S = glfw.KEY_S
KEY_D = glfw.KEY_D
KEY_Q = glfw.KEY_Q
KEY_E = glfw.KEY_E
KEY_ESC = glfw.KEY_ESCAPE
KEY_SPACE = glfw.KEY_SPACE
KEY_ENTER = glfw.KEY_ENTER
KEY_1 = glfw.KEY_1
KEY_2 = glfw.KEY_2
KEY_3 = glfw.KEY_3
KEY_UP = glfw.KEY_UP
KEY_DOWN = glfw.KEY_DOWN
KEY_LEFT = glfw.KEY_LEFT
KEY_RIGHT = glfw.KEY_RIGHT


class InputManager:

    def __init__(self):
        self.Keys = [False] * 1024
    # set glfw key call back
    def key_callback(self, window, key, scancode, action, mode):

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, GL_TRUE)

        if 0 <= key < 1024:
            # print(key)
            if action == glfw.PRESS:
                self.Keys[key] = True
            elif action == glfw.RELEASE:
                self.Keys[key] = False

    def SetCallback(self, window):
        glfw.set_key_callback(window, self.key_callback)

    def getKeys(self):
        return self.Keys

    # returns key values for the specified string
    @staticmethod
    def key_string_to_glfw(keystr):

        if keystr == "A":
            return KEY_A
        elif keystr == "W":
            return KEY_W
        elif keystr == "D":
            return KEY_D
        elif keystr == "S":
            return KEY_S
        elif keystr == "Q":
            return KEY_Q
        elif keystr == "E":
            return KEY_E
        elif keystr == "ESC":
            return KEY_ESC
        elif keystr == "SPACE":
            return KEY_SPACE
        elif keystr == "ENTER":
            return KEY_ENTER
        elif keystr == "1":
            return KEY_1
        elif keystr == "2":
            return KEY_2
        elif keystr == "3":
            return KEY_3
        elif keystr == "UP":
            return KEY_UP
        elif keystr == "DOWN":
            return KEY_DOWN
        elif keystr == "LEFT":
            return KEY_LEFT
        elif keystr == "RIGHT":
            return KEY_RIGHT

    def cursorPositionCallback(self, window, xPos, yPos):
        print("XPos:" + str(xPos) + " YPos:" + str(yPos))
