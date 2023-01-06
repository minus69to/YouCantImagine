import sys
import pygame

from subprocess import call
pygame.init()

class CallPy(object):
    def __init__(self, path='learningSprite.py'):
        self.path = path
    def call_python_file(self):
        call(["Python3", "{}", format(self.path)])

cp=CallPy()
cp.call_python_file()