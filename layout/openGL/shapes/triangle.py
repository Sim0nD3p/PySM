from OpenGL import GLU as glu, GL as gl
import numpy as np
from OpenGL.GL import *

class Triangle:
    def __init__(self):
        self.vertices = (
            -0.5, -0.5, 0, 1, 0, 0,
            0.5, -0.5, 0, 0, 1, 0,
            0, 0.5, 0, 0, 0, 1
        )
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vertex_count = 3

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def destroy(self):
        gl.glDeleteVertexArrays(1, (self.vao,))
        gl.glDeleteBuffers(1, (self.vbo,))


