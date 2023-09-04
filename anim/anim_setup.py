def save_set():
    global names, lst
    fl = open('nigger.txt','w')
    for i in range(len(names)):
        msg = names[i]+',%3f,%3f' %(lst[i].rect.topleft[0],lst[i].rect.topleft[1])
        if not lst[i].target: msg+=',None'
        else:
            l = lst[i].target[:]
            msg+=',%3f,%3f' %(l[0],l[1])
        if not lst[i].son: msg+=',None'
        else:
            l = lst.index(lst[i].son)
            msg+=',%i' %(l)
        l = lst[i].mhook[:]
        msg+=',%3f,%3f,%3f' %(l[0],l[1],l[2])
        l = lst[i].hook[:]
        msg+=',%3f,%3f,%3f,%3f' %(l[0],l[1],l[2],l[3])
        msg+=',%3f' %(lst[i].angles)
        fl.write(msg)
        fl.write('\n')
    fl.close()
    print('saving sucsessfull... maybe... i hope...')

def open_set():
    global lst, names
    fl = open('nigger.txt','r')
    ls = fl.readlines()
    for i in ls:
        o = i.split(',')
        name = o.pop(0)
        names.append(name)
        lst.append(AnimClass(name))
        lst[-1].topleft = [float(o.pop(0)),float(o.pop(0))]
        if o[0] == 'None':
            lst[-1].target = None
            del o[0]
        else: lst[-1].target = [float(o.pop(0)),float(o.pop(0))]
        if o[0] == 'None':
            lst[-1].son = None
            del o[0]
        else: lst[-1].son = int(o.pop(0))
        lst[-1].mhook = [float(o.pop(0)),float(o.pop(0)),float(o.pop(0))]
        lst[-1].hook = [float(o.pop(0)),float(o.pop(0)),float(o.pop(0)),float(o.pop(0))]
        lst[-1].angles = float(o.pop(0))
    for i in lst:
        if i.son: i.son = lst[i.son]
    fl.close()

import pygame
from anim_module import *
from text import *
pygame.init()

##gab = [1000,600]
gab = [1000,800]
screen = pygame.display.set_mode(gab)
screen.fill([255,255,255])

##names = ['green_stick.png','blue_stick.png','red_stick.png']
pre_names = 'pre_legb,footb,legb,handb,pre_handb,armb,connect,pre_leg,body,head,foot,leg,hand,pre_hand,arm'
pre_names = pre_names.split(',')
names = []
for i in pre_names:
    names.append('%s%s%s' %('D:\\Desktop\\TheDog\\Boss\\',i,'.png'))
##grn = AnimClass('green_stick.png')
##bl = AnimClass('blue_stick.png')
##red = AnimClass('red_stick.png')

gen_obj = AnimClass('rect1.png')
##gen_obj = AnimClass('men/body.png')
gen_obj.rect.center = [(gab[0]-200)/2,gab[1]/2]
saving = False

lst = []
for i in names:
    lst.append(AnimClass(i))
##for i in ['b_leg','b_foot','leg','foot']:
##    lst.append(AnimClass('men/%s.png' %(i)))
##for i in ['arm','hand']:
##    lst.append(AnimClass('men/%s.png' %(i)))
    
names = []      #Uncommit to
lst = []        #upload file
open_set()      #'nigger.txt'

l = [0,4,6,7,13]
for i in l:
    lst[8].sons.append(lst[i])
l = [[429.030811425,304.213992614,92.0869154658,358],\
     [175.0,374.999926984,65.0,180,0],\
     [253.008798043,381.259887917,122.065556157,182],\
     [429.030811425,304.213992614,92.0869154658,358],\
     [175.0,374.999926984,65.0,180,0]]
for i in l:
    lst[8].hooks.append(i)

panel = PanelClass()
panel.lst = lst
rotating = False
item = None
item_num = 0
nn = None
mm = None
hh = None
change_mod = False
boost = 1
rotating_up = False
rotating_down = False

mouse_loc = [0,0]
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
        elif e.type == pygame.MOUSEMOTION: mouse_loc = e.pos[:]
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if panel.collide_buttons(mouse_loc, 0):
                panel.add()
                panel.rectpoints.append(gen_obj.rect.topleft)
                panel.points[-1].append(pygame.transform.scale(screen,(250,150)))
            elif panel.collide_buttons(mouse_loc, 1):
                panel.delete()
            elif panel.collide_buttons(mouse_loc, 2):
                panel.gener_angles()
                saving = True
            #    print panel.save_file
                
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
            #    rotating = True
                pass
            elif e.key == pygame.K_u:
                save_set()
            elif e.key == pygame.K_LCTRL: boost = 5
            elif e.key == pygame.K_LSHIFT: boost = 0.1
            elif e.key == pygame.K_h:
                if item:
                    item.angles = 0
                    item.add_mhook(mouse_loc[:])
                    hh = item
            elif e.key == pygame.K_m:
                if item:
                    item.angles = 0
                    mm = item
            elif e.key == pygame.K_n:
                if item:
                    old_ang = item.angles
                    item.angles = 0
                    nn = item
            elif e.key == pygame.K_r:
                if item: item.angles = 0
            elif e.key == pygame.K_c:
                if change_mod: change_mod = False
                else: change_mod = True
            elif e.key == pygame.K_v:
                panel.gener_angles()
                saving = False
            elif e.key == pygame.K_z: gen_obj.rect.center = mouse_loc
            elif e.key == pygame.K_x: gen_obj.rect.center = [(gab[0]-200)/2,gab[1]/2]
            elif e.key == pygame.K_s:
                panel.save()
            #    for i in panel.save_file:
            #        print i
            elif e.key == pygame.K_UP: rotating_up = True
            elif e.key == pygame.K_DOWN: rotating_down = True
            elif e.key == pygame.K_LEFT: item_num -= 1
            elif e.key == pygame.K_RIGHT: item_num += 1
            elif e.key == pygame.K_LEFTBRACKET: panel.point_num -= 1
            elif e.key == pygame.K_RIGHTBRACKET: panel.point_num += 1
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
            #    rotating = False
                pass
            elif e.key == pygame.K_LCTRL: boost = 1
            elif e.key == pygame.K_LSHIFT: boost = 1
            elif e.key == pygame.K_h:
                if item:
                    if item == hh:
                        hh.add_mhook(mouse_loc[:])
                    else:
                        item.angles = 0
                        item.add_hook(mouse_loc[:])
                        item.son = hh
            elif e.key == pygame.K_m:
                if mm:
                    mm.son = None
            elif e.key == pygame.K_n:
                if nn:
                    nn.target = mouse_loc[:]
                    nn.angles = old_ang
            elif e.key == pygame.K_UP: rotating_up = False
            elif e.key == pygame.K_DOWN: rotating_down = False

    if change_mod:
        for i in lst:                     #Changing item
            if i.collide(mouse_loc):      #by mouse pos
                item = i
                break
            elif i == lst[-1]:
                item = None
    else:
        try: item_num = item_num % len(lst) #Changing item
        except: pass                        #by buttons
        item = lst[item_num]

    if item:
        if rotating_up:
            item.rotate(boost)
        elif rotating_down:
            item.rotate(-boost)

    if panel.msg:
        panel.save_file = [[]]
        gen_obj.rect.topleft = panel.rectpoints[0]
        for it_n in range(len(lst)):
            lst[it_n].rect.topleft = panel.points[0][0][it_n][1][:]
            lst[it_n].angles = panel.points[0][0][it_n][0]
            # panel.save_file[0].append([lst[it_n].angles,\
            #                         [(lst[it_n].rect.left-gen_obj.rect.left)/4.,\     #Tiny models
            #                         (lst[it_n].rect.top-gen_obj.rect.top)/4.]])
                                                                                        # Giant models
            panel.save_file[0].append([lst[it_n].angles,\
                                    [(lst[it_n].rect.left-gen_obj.rect.left)/2.,\
                                    (lst[it_n].rect.top-gen_obj.rect.top)/2.]])

        usls_num = -1
        print(panel.rectmsg)
        for i in panel.msg:
            usls_num += 1
            clock.tick(30)
            panel.save_file.append([])
            screen.fill([255,255,255])
            gen_obj.rect.left += panel.rectmsg[usls_num][0]
            gen_obj.rect.top += panel.rectmsg[usls_num][1]
            screen.blit(gen_obj.image, gen_obj.rect.topleft)
            for it_n in range(len(lst)):
                lst[it_n].rotate(i[it_n])
            for j in lst:
                j.update()
                screen.blit(j.nimage, j.rect.topleft)

                                                                #Forgotten "4"
                panel.save_file[-1].append([j.angles,\
                                        [(j.rect.left-gen_obj.rect.left)/4.,\
                                        (j.rect.top-gen_obj.rect.top)/4.]])
            pygame.display.flip()
        # print panel.save_file
        panel.msg = []
        if saving: panel.save() #print a list
    
    screen.fill([255,255,255])
    
    screen.blit(gen_obj.image, gen_obj.rect.topleft)
    for i in lst:
        i.update()
        screen.blit(i.nimage, i.rect.topleft)
    if item:
        pygame.draw.rect(screen,[0,0,0],item.rect,5)
    screen.blit(panel.image, [gab[0]-200,0])
    if panel.update():
        screen.blit(panel.points[panel.point_num][2],[gab[0]-195,80])
        blittext(screen, panel.point_num, [gab[0]-190,85], 30)
        blittext(screen, panel.points[panel.point_num][1], [gab[0]-190,105], 30)
    
    pygame.display.flip()
pygame.quit()
