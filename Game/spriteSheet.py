import pygame

def diviser_sprite_sheet(sprite_sheet, largeur_frame, hauteur_frame):
    frames = []
    largeur_total, hauteur_total = sprite_sheet.get_size()
    print(sprite_sheet.get_size())
    colonnes = largeur_total // largeur_frame
    lignes = hauteur_total // hauteur_frame

    for ligne in range(lignes):
        for colonne in range(colonnes):
            x = colonne * largeur_frame
            y = ligne * hauteur_frame
            frame_surface = pygame.Surface((largeur_frame, hauteur_frame))
            frame_surface.blit(sprite_sheet, (0, 0), (x, y, largeur_frame, hauteur_frame))
            frame_surface.set_colorkey((0, 0, 0))  # Supprimer le fond (noir)
            frames.append(frame_surface)

    return frames