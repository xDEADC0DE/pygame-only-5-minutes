import pygame
import random


class Ennemi:
	def __init__(self, taille, largeur, hauteur, cible_x, cible_y, vitesse):
		self.taille = taille
		self.vitesse = vitesse

		# position de départ aléatoire, au bord de l’écran
		random.seed()

		if(bool(random.getrandbits(1))):
			if(bool(random.getrandbits(1))):
				self.x = random.randrange(0,largeur)
				self.y = 0
			else:
				self.x = random.randrange(0,largeur)
				self.y = hauteur - 10
		else:
			if(bool(random.getrandbits(1))):
				self.x = 0
				self.y = random.randrange(0,hauteur)
			else:
				self.x = largeur -10
				self.y = random.randrange(0,hauteur)

		#self.x, self.y = 450,0

		# avec des Vector2
		self.pos = pygame.math.Vector2(self.x, self.y)
		self.cible = pygame.math.Vector2(cible_x, cible_y)
		self.dir = pygame.math.Vector2(self.cible - self.pos).normalize()
		#print('pos : ' + str(self.pos)) 
		#print('cible : ' + str(self.cible)) 
		#print('dir : ' + str(self.dir))  

		self.rect = pygame.Rect(self.x,self.y,taille,taille)

	def move(self):
		self.pos += self.dir * self.vitesse
		self.rect.x = round(self.pos.x)
		self.rect.y = round(self.pos.y)
		#print('pos rect : {:},{:}'.format(self.rect.x, self.rect.y)) 
