import pygame

pygame.mixer.init()
pygame.mixer.music.stop()
pygame.mixer.music.set_volume(1.0) # Установить громкость на максимум
pygame.mixer.music.load('audio.mp3')
pygame.mixer.music.play()
input()