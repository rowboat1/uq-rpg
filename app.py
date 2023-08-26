import pygame

main_s = pygame.display.set_mode((1600, 900))
pygame.font.init()
font = pygame.font.Font(None, 30)

if __name__ == "__main__":
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        main_s.fill("black")
        mp = pygame.mouse.get_pos()
        loc = font.render(str(mp), True, "red")
        
        pygame.draw.polygon(main_s, "green", 
            [
                (100, 800), 
                (100, 600), 
                (400, 200), 
                (1200, 200), 
                (1500, 600),
                (1500, 800)
            ]
        )
        pygame.draw.polygon(main_s, (212, 191, 142), [
            (775, 200),
            (825, 200),
            (825, 800),
            (775, 800)
        ])
        main_s.blit(loc, mp)
        pygame.display.flip()  