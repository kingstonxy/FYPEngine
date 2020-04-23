import numpy
import glm
import _ctypes
from OpenGL.GL import *
from OpenGL.GLUT import *

#                         x   y    color        tx   ty   ti
sampleQuad = numpy.array([0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1,
                          1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1,
                          0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1,

                          0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1,
                          1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1,
                          1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1], dtype="f")


class BatchRenderer:
    def __init__(self):
        self.Shader = None
        self.VAO = GLuint(0)
        self.VBO = GLuint(0)
        self.Objects = []
        self.MaxObjects = 100
        self.MaxObjectsVertex = self.MaxObjects * 6
        self.Textures = []
        self.MaxTexture = 30
        self.TextureIndex = 0
        self.BatchHead = 0
        self.BufferSize = numpy.size(sampleQuad) * self.MaxObjects * 4

    def AddObject(self, position, size, rotation, grid, selected):
        return

    def Start(self):
        self.Shader.Compile()
        self.Shader.UseProgram()

        glGenVertexArrays(1, self.VAO)
        glGenBuffers(1, self.VBO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.BufferSize, ctypes.c_void_p(0), GL_DYNAMIC_DRAW)

        glBindVertexArray(self.VAO)
        # position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8, ctypes.c_void_p(0))
        # color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8,
                              ctypes.c_void_p(2 * ctypes.sizeof(GLfloat)))
        # tex
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8,
                              ctypes.c_void_p(5 * ctypes.sizeof(GLfloat)))
        # texID
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 8,
                              ctypes.c_void_p(7 * ctypes.sizeof(GLfloat)))

    def Render(self):
        count = 1
        CurrDrawArray = self.Objects[0]
        for obj in self.Objects[1:]:
            if count >= self.MaxObjects:
                break
            CurrDrawArray = numpy.append(CurrDrawArray, obj)
            count = count + 1

        self.Textures[0].BindTexture()
        sizeOfData = numpy.size(CurrDrawArray) * 4
        glBufferSubData(GL_ARRAY_BUFFER, 0, sizeOfData, CurrDrawArray)

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, numpy.size(CurrDrawArray))
        glBindVertexArray(0)

    def Draw(self, texture, position, size, rotate, color, grid, selected, TexID):
        model = glm.fmat4(1.0)
        model = glm.translate(model, glm.vec3(position, 0.0))

        model = glm.translate(model, glm.vec3(0.5 * size.x, 0.5 * size.y, 0.0))
        model = glm.rotate(model, rotate, glm.vec3(0.0, 0.0, 1.0))
        model = glm.translate(model, glm.vec3(-0.5 * size.x, -0.5 * size.y, 0.0))

        model = glm.scale(model, glm.vec3(size, 1.0))

        glPos1 = model * glm.vec4(0.0, 1.0, 0.0, 1.0)
        glPos2 = model * glm.vec4(1.0, 0.0, 0.0, 1.0)
        glPos3 = model * glm.vec4(0.0, 0.0, 0.0, 1.0)
        glPos4 = model * glm.vec4(1.0, 1.0, 0.0, 1.0)

        # Pos                 color                            TexCoords                                    TexID
        vertices = numpy.array(
            [glPos1.x, glPos1.y, color.x, color.y, color.z, ((selected.x - 1) / grid.x), (selected.y / grid.y), TexID,
             glPos2.x, glPos2.y, color.x, color.y, color.z, (selected.x / grid.x), ((selected.y - 1) / grid.y), TexID,
             glPos3.x, glPos3.y, color.x, color.y, color.z, ((selected.x - 1) / grid.x), ((selected.y - 1) / grid.y),
             TexID,

             glPos1.x, glPos1.y, color.x, color.y, color.z, ((selected.x - 1) / grid.x), (selected.y / grid.y), TexID,
             glPos4.x, glPos4.y, color.x, color.y, color.z, (selected.x / grid.x), (selected.y / grid.y), TexID,
             glPos2.x, glPos2.y, color.x, color.y, color.z, (selected.x / grid.x), ((selected.y - 1) / grid.y), TexID],
            dtype="f")

        if self.TextureIndex >= self.MaxTexture:
            print("ERROR : Texture binding limit reached, currently set at : " + str(self.MaxTexture))
            return

        if (texture not in self.Textures) and (self.TextureIndex < self.MaxTexture):
            self.Textures.append(texture)
            self.TextureIndex = self.TextureIndex + 1

        self.Objects.append(vertices)

    def Flush(self):
        return

    def End(self):
        return