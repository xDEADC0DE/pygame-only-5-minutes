import pygame
import sys
from pathlib import Path
from ennemi import Ennemi

#TODO:nécessaire ?
#pygame.init()

# configuration Pygame
LARGEUR, HAUTEUR = 900, 500
TAILLE_PERSO = 50
TAILLE_ENNEMI = 10
TITRE = 'Only 5 minutes'
FPS = 60
FOLDER_ASSETS = Path.cwd() / 'assets'
IMAGE_FOND = pygame.transform.scale(pygame.image.load(FOLDER_ASSETS / 'space.jpg'), (LARGEUR,HAUTEUR))
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption(TITRE)
pygame.init()

IMAGE_PERSO = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(FOLDER_ASSETS / 'spaceship.png'), (TAILLE_PERSO,TAILLE_PERSO)), 90)
IMAGE_ENNEMI = pygame.transform.scale(pygame.image.load(FOLDER_ASSETS / 'ennemi.png'), (TAILLE_ENNEMI, TAILLE_ENNEMI))

#	events
#JAUNE_TOUCHE = pygame.USEREVENT + 1

#	sons
pygame.mixer.init()
SON_TOUCHE = pygame.mixer.Sound(FOLDER_ASSETS / 'Gun+Silencer.mp3')

#	polices
pygame.font.init()
POLICE_TIMER = pygame.font.SysFont('arial', 50)
POLICE_SCORE = pygame.font.SysFont('arial', 20)

# timer
clock = pygame.time.Clock()

# options du jeu
DEBUG = False
DUREE_JEU = 5 * 60 * 1000
COUT_TIR_S = 10
VITESSE = 5
COUT_TOUCHE_S = 25
VITESSE_ENNEMIS = 5

#TODO: revoir la gestion des variable locales et globales
temps_restant = DUREE_JEU

def draw(time, score, joueur, ennemis):
	screen.blit(IMAGE_FOND, (0,0))

	# timer
	texte_timer = POLICE_TIMER.render(time, 1, 'white')
	screen.blit(texte_timer, (LARGEUR - texte_timer.get_width()-20, 5))

	# score
	texte_score = POLICE_SCORE.render('score : {:d}'.format(int(score)), 1, 'white')
	screen.blit(texte_score, (10, 5))

	# joueur
	screen.blit(IMAGE_PERSO, (joueur.x,joueur.y))

	# ennemis
	for ennemi in ennemis:
		screen.blit(IMAGE_ENNEMI, (ennemi.rect.x, ennemi.rect.y))

	if DEBUG:
		pygame.draw.rect(screen, 'red', joueur, width=1)

	pygame.display.update()

def mouvement_joueur(keys_pressed, joueur):
	if keys_pressed[pygame.K_q] and joueur.x-VITESSE>0: # gauche
		joueur.x-=VITESSE
	if keys_pressed[pygame.K_d] and joueur.x+VITESSE+joueur.width<LARGEUR: # droite
		joueur.x+=VITESSE
	if keys_pressed[pygame.K_z] and joueur.y-VITESSE>0: # haut
		joueur.y-=VITESSE
	if keys_pressed[pygame.K_s] and joueur.y+VITESSE+joueur.height<HAUTEUR: # bas
		joueur.y+=VITESSE

def deplacer_ennemis(joueur, ennemis):
	for ennemi in ennemis:
		ennemi.move()
		if ennemi.rect.x > LARGEUR or ennemi.rect.x < 0 or ennemi.rect.y > HAUTEUR or ennemi.rect.y < 0:
			ennemis.remove(ennemi)
			if DEBUG:
				print('ennemi hors écran')

		if ennemi.rect.colliderect(joueur):
			joueur_touche()
			ennemis.remove(ennemi)
			

def joueur_touche():
	global temps_restant
	SON_TOUCHE.play()
	if DEBUG:
		print('joueur touché')
	#TODO: pas besoin de //FPS ici ?
	temps_restant -= COUT_TOUCHE_S*1000

def draw_end_screen(score):
	screen.blit(IMAGE_FOND, (0,0))
	texte_fin = POLICE_TIMER.render('**GAME OVER**', 1, 'white')
	screen.blit(texte_fin, (LARGEUR/2 - texte_fin.get_width()/2, HAUTEUR/2-40)) # centré

	texte_score = POLICE_SCORE.render('Score final : {:d}'.format(int(score)), 1, 'white')
	screen.blit(texte_score, (LARGEUR/2 - texte_score.get_width()/2, HAUTEUR/2+20)) # centré
	pygame.display.update()


def main():
	global temps_restant
	clock = pygame.time.Clock()
	jouer = True

	joueur = pygame.Rect(LARGEUR/2-TAILLE_PERSO/2,HAUTEUR/2-TAILLE_PERSO/2, TAILLE_PERSO,TAILLE_PERSO)
	#print('{:d},{:d}'.format(joueur.x, joueur.y)) 

	last_spawn = 0
	score = 0
	ennemis = []

	while jouer:
		clock.tick(FPS)

		now = pygame.time.get_ticks()

		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			#if event.type == pygame.KEYDOWN:
			#	if event.key == pygame.K_SPACE:
			#TODO: pause ?

		# Game logic : animations, enemy AI, etc.
		if now - last_spawn > 500:
			ennemis.append(Ennemi(TAILLE_ENNEMI, LARGEUR, HAUTEUR, joueur.x+TAILLE_PERSO/2, joueur.y+TAILLE_PERSO/2, VITESSE_ENNEMIS))
			last_spawn = now

		mouvement_joueur(keys_pressed, joueur)
		deplacer_ennemis(joueur, ennemis)

		# Visuals : draw()
		#TODO: quelle horreur…
		timer = '{:02d}:{:02d}'.format(int(temps_restant//1000//60), int(temps_restant//1000%60))
		draw(timer, score, joueur, ennemis)
		
		# Temps écoulé : fin du jeu
		temps_restant -= 1000//FPS
		score += 10/FPS
		if temps_restant < 0:
			jouer = False


	# End state
	while True:
		draw_end_screen(score)

		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	#TODO: what’s that?
	#pygame.display.flip()

if __name__ == "__main__":
	main()
