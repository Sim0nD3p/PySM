import sys

import OpenGL.arrays.ctypesparameters
from PyQt6.QtCore import Qt, QSize, QRect, QPoint
import PyQt6
from PyQt6.QtCore import Qt
from PySide2.QtWidgets import QOpenGLWidget
from PyQt6.QtOpenGL import QOpenGLPaintDevice, QOpenGLWindow
from PyQt6 import QtOpenGL
from PyQt6 import QtOpenGLWidgets
import numpy as np
from OpenGL.arrays import vbo
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen, QPixmap, QPainterPath, QPaintDevice, QOpenGLContext
from OpenGL.GLU import *
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from layout.openGL.shapes.triangle import Triangle
from OpenGL.GLUT import *
import OpenGL.GLU
# https://nrotella.github.io/journal/first-steps-python-qt-opengl.html#pyopengl

# solution is QOpenGLWidget
# https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtopenglwidgets/qopenglwidget.html?highlight=qopenglwidget#QOpenGLWidget
# uses OpenGL in a Qt widget

class Rect:
    def __init__(self):
        print('rect init')
        self.vao = gl.glGenVertexArrays(1, '&firstvao')
        gl.glBindVertexArray(self.vao)

        vertices = [
            [0.5, 0.5],
            [-0.5, 0.5],
            [0.5, -0.5],
            [-0.5, -0.5]
        ]
        data_array = [
            [0, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0]
        ]
        vertices = np.array(vertices, dtype=np.float32)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)







class Test(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()


    def create_shader(self):
        vertex_src = "in vec3 position; in vec3 color; out vec3 newColor; void main() { gl_Position = vec4(position,\
         1.0); newColor = color; }"
        fragment_src = "in vec3 newColor; out vec4 outColor; void main() { outColor = vec4(newColor, 1.0f); }"
        vertex_src = "in vec2 position; void main(){ gl_position = vec4(position, 0.0, 1.0); }"
        fragment_src = "out vec4 outColor; void main(){ outColor = vec4(1.0, 1.0, 1.0, 1.0); }"
        vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
        shader = compileProgram(vertex_shader, fragment_shader)
        print('done creating shader')
        return shader



    def initializeGL(self):
        # we can start to use OpenGL context
        print('initialize GL')
        self.shader = self.create_shader()
        # glutInit()
        # glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

    def draw_rect(self, x, y, width, height):
        glBegin(GL_QUADS)
        glVertex(x, y)
        glVertex(x + width, y)
        glVertex(x + width, y + height)
        glVertex(x, y + height)
        glEnd()


    def paintGL(self):
        print('paint GL')
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glUseProgram(self.shader)

        # refresh 2d
        glViewport(0, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


        glColor3f(0.0, 0.0, 1.0)
        self.draw_rect(50, 50, 100, 100)




        rectangle = Rect()
        gl.glBindVertexArray(rectangle.vao)

        position = gl.glGetAttribLocation(self.shader, 'position')
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(self.shader, 'color')
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # glClearColor(0.0, 1.0, 0.0, 1.0)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # gl.glDrawArrays(GL_TRIANGLES, 0, )

class Test_old(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__()
        print('yessir?')
        QtOpenGLWidgets.QOpenGLWidget.__init__(self, parent)

        # gl.glUseProgram(self.shader)

    def create_shader(self, vertex_file_path, fragment_file_path):
        with open(vertex_file_path, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_file_path, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(        # has to be within active OpenGl context
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        return shader


    def initializeGL(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.shader = self.create_shader("shaders/vertex.txt", "shaders/fragment.txt")
        gl.glUseProgram(self.shader)

    def resizeGL(self, w: int, h: int):
        gl.glViewport(0, 0, w, h)
        # gl.glMatrixMode(gl.GL_PROJECTION)
        # gl.glLoadIdentity()
        # aspect = w / float(h)
        # GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        # gl.glMatrixMode(gl.GL_MODELVIEW)
        # self.initGeometry()

    def initGeometry(self):
        self.cubeVtxArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]]
        )
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray, (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]]
        )
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray, (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4]
        )



    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glUseProgram(self.shader)
        triangle = Triangle()
        gl.glBindVertexArray(triangle.vao)
        gl.glDrawArrays(GL_TRIANGLES, 0, triangle.vertex_count)

        """
        # tutorial 1
        gl.glPushMatrix()  # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -50.0)  # third, translate cube to specified depth
        gl.glScale(20.0, 20.0, 20.0)  # second, scale cube
        gl.glTranslate(-0.5, -0.5, -0.5)  # first, translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()  # restore the previous modelview matrix
        """





