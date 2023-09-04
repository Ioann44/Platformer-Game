import pygame, module_editor
pygame.init()

# width, height = raw_input('Enter gabarits: ').split(',')
# width, height = int(width), int(height)

gabarits = width, height = 25, 18
place = module_editor.PlaceClass(gabarits)
screen = pygame.display.set_mode([width*30,height*30])
surface = pygame.surface.Surface([30,30])

surface.fill([255,255,0])
image_block = surface.convert()
surface.fill([0,200,0])
image_spawn = surface.convert()

clock = pygame.time.Clock()
activate = False
delete = False
# spawn = False
mouse = [0,0]

going = True
while going:
    clock.tick(120)
    # print(clock.get_fps())
    screen.fill([150,200,255])
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            going = False
        elif e.type == pygame.MOUSEMOTION:
            mouse = e.pos
        elif e.type == pygame.MOUSEBUTTONDOWN:
            activate = True
        elif e.type == pygame.MOUSEBUTTONUP:
            activate = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                going = False
            elif e.key == pygame.K_q:
                delete = True
            elif e.key == pygame.K_s:
                # spawn = True
                place.change_spawn(mouse)
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_q:
                delete = False
            # elif e.key == pygame.K_s:
            #     spawn = False

    if delete:
        place.del_block(mouse)
    # elif spawn:
    #     place.change_spawn(mouse)
    elif activate:
        place.add_block(mouse)
    x, y = 0, 0
    for a in place.level:
        for b in a:
            if b == 'o':
                screen.blit(image_block, [x,y])
            elif b == 'x':
                screen.blit(image_spawn, [x,y])
            x += 30
        x = 0
        y += 30
    pygame.display.flip()
    
pygame.quit()
place.view()