import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import pygame,sys, os
import re     #za splitanje po više znakova
pygame.init() #instalira i učitava sve pygame module


#Definiranje displaya
WIDTH, HEIGHT = 1280, 768
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Odabir naboja u prostoru")

#Slike
Checkbox_nes = pygame.image.load(os.path.join("Assets", "CheckboxNestisnuto.png")).convert_alpha()
Checkbox_hover = pygame.image.load(os.path.join("Assets", "Checkboxhover.png")).convert_alpha()
Checkbox_stis = pygame.image.load(os.path.join("Assets", "CheckboxStisnuto.png")).convert_alpha()

#Play_score
LINIJA_SCORE_PISANJE = pygame.image.load(os.path.join("Assets", "linija_za_pisanje.png")).convert_alpha()
LINIJA_SCORE_PISANJE = pygame.transform.scale(LINIJA_SCORE_PISANJE, (LINIJA_SCORE_PISANJE.get_width()/1.5, LINIJA_SCORE_PISANJE.get_height()//2))

LINIJA_SCORE_PRAZNINA = pygame.image.load(os.path.join("Assets", "linija_za_pisanje_praznina.png")).convert_alpha()
linija_key_index = 0
linija_playscore_animacija_lista = [LINIJA_SCORE_PISANJE,LINIJA_SCORE_PRAZNINA]
linija_playscore_surf = linija_playscore_animacija_lista[linija_key_index]

#Clock
clock = pygame.time.Clock()
FPS = 60 

#SIMULACIJA
k = 9*pow(10,9) #Nm^2C^-2 Coulombova konstanta

class Button:
    def __init__(self, text_input, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, position):
        #rectangle ispod teksta
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color = rectangle_color, rectangle_hovering_color
        #tekst u gumbu
        self.text_input = text_input
        self.font = pygame.font.Font(None, text_size)
        self.text_surface = self.font.render(text_input, True, text_color)
        self.text_rectangle = self.text_surface.get_rect(center = self.rectangle.center)
        self.player_number = 0

    def update(self, screen):       ##Crta na screen
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)

    def provjeraSudara(self, mouse_position):
        if mouse_position[0] in range(self.rectangle.left, self.rectangle.right) and mouse_position[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        return False
    
    def changeButtonColor(self):
        self.rectangle_color = self.rectangle_hovering_color

class Checkbox:
    def __init__(self, x, y, caption_input, caption_color, checkbox_nes, checkbox_hover, checkbox_stis):
        self.font_size = 35
        self.checked = False
        self.nes_slika = pygame.transform.scale_by(checkbox_nes,0.20)
        self.hover_slika = pygame.transform.scale_by(checkbox_hover,0.20)
        self.stis_slika = pygame.transform.scale_by(checkbox_stis,0.20)
        self.poz = (x, y)
        self.caption_input = caption_input
        self.caption_color = caption_color

        self.checkbox_rect = self.nes_slika.get_rect(topleft = self.poz)

        self.font = pygame.font.Font(None, self.font_size)
        


    def provjeraSudara(self, pozicija_misa):
        if pozicija_misa[0] in range(self.checkbox_rect.left, self.checkbox_rect.right) and pozicija_misa[1] in range(self.checkbox_rect.top, self.checkbox_rect.bottom):
            return True
        return False
    
    def crtanje(self, pozicija_misa):
        #Prvo napravi tekst ispred checkboxa i nacrtaj ga
        self.caption_surf = self.font.render(self.caption_input, True, self.caption_color)
        w,h = self.font.size(self.caption_input)
        self.caption_pos = (self.poz[0] - (w+w/8), self.poz[1] + self.nes_slika.get_height()/5)
        SCREEN.blit(self.caption_surf, self.caption_pos)

        #Onda crtaj checkbox
        if pozicija_misa[0] in range(self.checkbox_rect.left, self.checkbox_rect.right) and pozicija_misa[1] in range(self.checkbox_rect.top, self.checkbox_rect.bottom) and self.checked == False:
            SCREEN.blit(self.hover_slika, self.poz)
        elif self.checked == True:
            SCREEN.blit(self.stis_slika, self.checkbox_rect)
        else:
            SCREEN.blit(self.nes_slika, self.checkbox_rect)
        
class InputBox:
    def __init__(self, caption_input, caption_color, caption_size, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, rectangle_selected_color, position):
        #rectangle ispod teksta
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color, self.rectangle_selected_color = rectangle_color, rectangle_hovering_color, rectangle_selected_color
        self.poz = position
        #caption 
        self.caption_input = caption_input
        self.caption_color = caption_color
        self.capt_font = pygame.font.Font(None, caption_size)

        #tekst u inboxu
        self.text_input = ""
        self.text_color = text_color
        self.text_font = pygame.font.Font(None, text_size)
        self.text_surface = self.text_font.render(self.text_input, True, self.text_color)
        self.text_rectangle = self.text_surface.get_rect(center = self.rectangle.center)
        self.selektiran = False
    
    def Upisivanje(self,event_unicode):
        self.text_input += event_unicode

    def update(self, screen):       
        #Prvo napravi tekst ispred checkboxa i nacrtaj ga
        self.caption_surf = self.capt_font.render(self.caption_input, True, self.caption_color)
        caption_width, caption_height = self.capt_font.size(self.caption_input)
        capt_x = self.rectangle.left - caption_width - 10
        capt_y = self.rectangle.centery - caption_height / 2
        self.caption_pos = (capt_x, capt_y)
        screen.blit(self.caption_surf, self.caption_pos)

        pygame.draw.rect(screen, self.rectangle_color, self.rectangle,2)
        self.text_surface = self.text_font.render(self.text_input, True, self.text_color)
        self.text_rectangle = self.text_surface.get_rect(center = self.rectangle.center)
        screen.blit(self.text_surface, self.text_rectangle)

    def provjeraSudara(self, mouse_position):
        if mouse_position[0] in range(self.rectangle.left, self.rectangle.right) and mouse_position[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        return False
    
    def changeInboxHoverColor(self):
        self.rectangle_color = self.rectangle_hovering_color
    
    def changeInboxSelectedColor(self):
        self.rectangle_color = self.rectangle_selected_color


class Naboj:
    def __init__(self,poz,predznak,naboj,er = 1): 
        self.q = naboj
        self.predznak = predznak
        self.lok = poz
        self.er = er    #Relativna permitivnost sredstva

    def distance(self,X,Y):
        return np.sqrt((X - self.lok[0])**2 + (Y - self.lok[1])**2)         #vrati matrix udaljenosti točaka u prostoru od naboja
    
    def vektori_distance(self,X,Y):
        if self.predznak == "+":                                            
            distance_vektori = (X-self.lok[0], Y-self.lok[1])               #tuple s dva araya, prvi su "i" koor vektora, drugi su "j" koor vektora
        elif self.predznak == "-":                                          #ako je minus onda promjeni orijentaciju vektora
            distance_vektori = (-(X-self.lok[0]), -(Y-self.lok[1]))
        return distance_vektori
    
    def jedinični_distanca_vekSmjera(self,distance, distance_vektori):      # vrati array jediničnih vektora za svaku točku
        dist_jed_X = np.where(distance != 0, distance_vektori[0] / np.where(distance != 0, distance, 1), 0) 
        dist_jed_Y = np.where(distance != 0, distance_vektori[1] / np.where(distance != 0, distance, 1), 0) #pomoću where onemogućujemo dijeljnje s 0
        distanca_jedinični = np.stack((dist_jed_X, dist_jed_Y), axis=0)
        return distanca_jedinični

    def elPolje(self, distance):                                            #vrati se array jakosti el polja u svim točkama
        elpolje = np.where(distance != 0, (k/self.er) * self.q / (np.where(distance != 0, distance/100, 1))**2, 0)         
        return elpolje
        
    
    def vektori_elPolja(self, elPolje, jedinične_distance):                 #vrati se array vektora el polja u svim točkama
        return elPolje*jedinične_distance
    
    def __repr__(self):
        return f"Naboj na koordinatai {self.lok}"

class Prostor:
    def __init__(self, er=1):  
        self.size = 601
        self.x = np.linspace(-300, 300, self.size)
        self.y = np.linspace(300, -300, self.size)      
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.er = er

    def ukupnoPolje(self,lista_vektorskih_E):                                                       #vrati array ukupne jakosti el polja po točkama
        vektorski_E_po_točki = 0
        for vek_lista in lista_vektorskih_E:
            vektorski_E_po_točki += vek_lista
        jakost_E_po_točki = np.sqrt(vektorski_E_po_točki[0]**2 + vektorski_E_po_točki[1]**2)        
        return jakost_E_po_točki

def simulacija(Lista_koordinata_naboja, lista_predznaka_naboja, Lista_naboja_naboja,er):    
    #100 j.d. = 1 m, odnosno 100px = 1m 

    lista_naboja = []
    prostor = Prostor(er)
    for pozicija,predznak,naboj_vr in zip(Lista_koordinata_naboja, lista_predznaka_naboja, Lista_naboja_naboja):  #isti index u svakoj listi odnosi se na istu česticu
        naboj = Naboj(pozicija, predznak, naboj_vr, prostor.er)
        lista_naboja.append(naboj)

    
    lista_E_vek = []
    for naboj in lista_naboja:

        #Udljenost i vektor smjera
        distance = naboj.distance(prostor.X, prostor.Y)
        vektori_distanci = naboj.vektori_distance(prostor.X, prostor.Y)
        jedinične_distance = naboj.jedinični_distanca_vekSmjera(distance, vektori_distanci)

        ##Električno polje
        jakost_E_za_naboj = naboj.elPolje(distance)
        vektori_E_za_naboj = naboj.vektori_elPolja(jakost_E_za_naboj, jedinične_distance)
        
        lista_E_vek.append(vektori_E_za_naboj)

    jakost_el_polja_u_prostoru = prostor.ukupnoPolje(lista_E_vek)

    
    plt.figure(figsize=(8, 6))                              
    vmin = np.max(jakost_el_polja_u_prostoru)/(1e+4)
    vmax=  np.max(jakost_el_polja_u_prostoru)

    norm = colors.LogNorm(vmin,vmax)     
    plt.imshow(jakost_el_polja_u_prostoru, cmap='viridis', origin='upper', norm=norm, extent=(-3, 3, -3, 3), interpolation='bicubic', aspect='equal') 
    plt.colorbar(label='Jakost električnog polja (N/C)')
    plt.xlabel('Udaljenost (m)')
    plt.ylabel('Udaljenost (m)')
    plt.title('Električno polje')
    plt.grid(False)
    plt.show()


def main():
    Kružići_lista = []                  #lista s koordinatama za crtanje u pygameu
    Kružići_lista_zaSimulaciju = []     #lista s koordinatama za crtanje u simulaciji
    Predznaci = []
    Naboji = []

    Kružići_lista_X_Y = []
    Kružići_lista_zaSimulaciju_X_Y = []
    Predznaci_X_Y = []
    Naboji_X_Y = []


    Running = True
    
    #Fontovi 
    naslov_font = pygame.font.Font(None, 50)
    izbriši_font = pygame.font.Font(None, 25)
    mouse_poz_font = pygame.font.Font(None, 25)
    uputa_naboj_font = pygame.font.Font(None, 25)
    opis_naboja_font = pygame.font.Font(None, 25)

    #boje
    lg_blue = (173,216,230)
    dr_gray = (105,105,105)
    blue_okvir_inboxa = (0,162,232)

    #Dimenzije
    prostor_dimenzije = (600,600)   #dimenzije prostora gdje se pikne elektron
    Top_right_zaProstor = (WIDTH//2-prostor_dimenzije[0]//2,HEIGHT//2-prostor_dimenzije[1]//2)       #centar ekrana - 300
    Centar = (WIDTH//2, HEIGHT//2)
    
    CBOXES = []
    INBOXES = []

    #Elementi na zaslonu
    ZASEBNO_CBOX = Checkbox(210, 150, "Zasebno", "black", Checkbox_nes, Checkbox_hover, Checkbox_stis)
    KVADRAT_CBOX = Checkbox(210, 200, "Kvadrat", "black", Checkbox_nes, Checkbox_hover, Checkbox_stis)
    KRUŽNICA_CBOX = Checkbox(210, 250, "Kružnica", "black", Checkbox_nes, Checkbox_hover, Checkbox_stis)
    KRUŽNICA_INBOX = InputBox("Upiši broj", "dark gray", 28, 40, "black", (100, 35), "black", "gray", blue_okvir_inboxa, (195, 320))

    X_INBOX = InputBox("X:", "black", 28, 40, "black", (80, 35), "black", "gray", blue_okvir_inboxa, (120, 600))
    Y_INBOX = InputBox("Y:", "black", 28, 40, "black", (80, 35), "black", "gray", blue_okvir_inboxa, (240, 600))

    PREDZNAK_CBOX = Checkbox(1180, 150, "Predznak: +", "black", Checkbox_nes, Checkbox_hover, Checkbox_stis)
    NABOJ_INBOX = InputBox("Upiši jačinu naboja", "black", 30,  40, "black", (100, 35), "black", "gray", blue_okvir_inboxa, (1210, 225))
    NABOJ_INBOX.text_input = "1"
    PERMITIVNOST_INBOX = InputBox("Relativna perm. sredstva", "black", 24,  40, "black", (100, 35), "black", "gray", blue_okvir_inboxa, (1210, 390)) 
    PERMITIVNOST_INBOX.text_input = "1"
    
    X_Y_INBOXES = [X_INBOX, Y_INBOX]
    CBOXES.append(ZASEBNO_CBOX)
    CBOXES.append(KVADRAT_CBOX)
    CBOXES.append(KRUŽNICA_CBOX)

    INBOXES.append(X_INBOX)
    INBOXES.append(Y_INBOX)
    INBOXES.append(KRUŽNICA_INBOX)
    INBOXES.append(NABOJ_INBOX)
    INBOXES.append(PERMITIVNOST_INBOX)
    
    
    
    while Running:
        SCREEN.fill('White')
        
        PRIHVATI_GUMB = Button("Prihvati", 40, "White", (115, 50), "#0A0A09", "#064719", (Centar[0], Centar[1]+340))
        POSTAVI_GUMB = Button("Postavi", 35, "White", (95, 45), "#0A0A09", "#064719", (180, 660))

        GUMBI = [PRIHVATI_GUMB,POSTAVI_GUMB]

        #Surfaceovi, rectovi i textovi
        naslov_surface = naslov_font.render("Klikni na polje za postavljanje naboja", True, "Black")
        naslov_rectangle = naslov_surface.get_rect(center = (WIDTH/2, 20))
        izbriši_surface = izbriši_font.render("Tipkom Backspace izbriši posljednje postavljeni naboj", True, dr_gray)
        izbriši_rectangle = izbriši_surface.get_rect(center = (WIDTH/2, 63))
        mouse_position = pygame.mouse.get_pos()
        mouse_position_prostora = (mouse_position[0]-(Centar[0]), -(mouse_position[1]-(Centar[1])))
        mouse_poz_surface = mouse_poz_font.render(f"{mouse_position_prostora}",True,"Black")
        mouse_poz_rect = mouse_poz_surface.get_rect(center = (WIDTH-100, 680))
        Prostor = pygame.Rect(Top_right_zaProstor[0], Top_right_zaProstor[1], prostor_dimenzije[0], prostor_dimenzije[1])


        uputa_naboj_tekst1 = "*ako želiš potenciju ili decimalni"
        uputa_naboj_tekst2 = "broj onda napiši BROJe+-n"
        uputa_naboj_tekst3 = "(= BROJ * 10^+-n )"
        uputa_naboj_tekst4 = "** naboj u [C]"
        uputa_naboj_tekstovi = [uputa_naboj_tekst1,uputa_naboj_tekst2,uputa_naboj_tekst3,uputa_naboj_tekst4]

        uput_perm_tekst1 = "*Upiši broj > 1"
        uputa_perm_tekst2 = "**Decimalni može s točkom"
        uput_perm_tekstovi = [uput_perm_tekst1,uputa_perm_tekst2]

        IspisUpute(uputa_naboj_tekstovi, "gray", uputa_naboj_font, (1110, 265), SCREEN, 0)
        IspisUpute(uput_perm_tekstovi, "gray", uputa_naboj_font, (1090, 425), SCREEN, 0)


        #Crtanje na ekran
        pygame.draw.rect(SCREEN,lg_blue,Prostor,2)  
        if Prostor.collidepoint(mouse_position):
                    SCREEN.blit(mouse_poz_surface,mouse_poz_rect)      #Ako je miš u prostoru, crtaj dolje desno koordinate
        
        SCREEN.blit(naslov_surface, naslov_rectangle)       
        SCREEN.blit(izbriši_surface, izbriši_rectangle)      

        for GUMB in GUMBI:
            if GUMB.provjeraSudara(mouse_position):    
                GUMB.changeButtonColor()               #Crtaj hover gumba
            GUMB.update(SCREEN)

        #Crtaj lijeve checkboxove
        for Cbox in CBOXES:
            Cbox.crtanje(mouse_position)               

        #Crtaj desni checkbox
        PREDZNAK_CBOX.crtanje(mouse_position)

        #Crtanje i promjene inboxa
        for inbox in INBOXES:     
            if inbox == KRUŽNICA_INBOX:         
                if KRUŽNICA_CBOX.checked == True:
                    crtanjeInboxa(inbox, mouse_position)
                else:
                    pass
            elif inbox in X_Y_INBOXES:
                crtanjeInboxa(inbox, mouse_position,X_Y_INBOXES)
            else:
                crtanjeInboxa(inbox, mouse_position)

        
        crtajNabojeUProstor(Kružići_lista,Predznaci,SCREEN)
        crtajOpisNaboja(Kružići_lista, Predznaci, Naboji, mouse_position, opis_naboja_font, SCREEN)
        
        
        #What if...
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                
                #Odselektiraj inbox
                if event.key == pygame.K_RETURN:                                           
                    for INBOX in INBOXES:      
                        if INBOX.selektiran == True:       
                            INBOX.selektiran = False       
                    if NABOJ_INBOX.text_input == "" and NABOJ_INBOX.selektiran == False:    
                        NABOJ_INBOX.text_input = "1"
                    if (PERMITIVNOST_INBOX.text_input == "" or float(PERMITIVNOST_INBOX.text_input)<1) and PERMITIVNOST_INBOX.selektiran == False:   
                        PERMITIVNOST_INBOX.text_input = "1"
                        
                            
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #Obriši zadnji znak ili zadnji naboj
                if event.key == pygame.K_BACKSPACE:                                         
                    for inbox in INBOXES:
                        if inbox.selektiran and len(inbox.text_input)>0:        
                            inbox.text_input = inbox.text_input[:-1]           
                            if inbox == NABOJ_INBOX and len(inbox.text_input) > 0 and (KRUŽNICA_CBOX.checked == True or KVADRAT_CBOX.checked == True):
                                Naboj_vrijednost = DobiNaboj(inbox)
                                Naboji = [Naboj_vrijednost for i in Naboji]                 ## napravi listu, s novim nabojem iz inboxa
                            elif inbox == KRUŽNICA_INBOX and len(inbox.text_input) > 0:     
                                br_naboja = int(inbox.text_input)
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = crtajKružnicu(br_naboja,Centar,PREDZNAK_CBOX.caption_input[-1], DobiNaboj(NABOJ_INBOX)) 
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = NadopuniListe_sX_Y_odnaprijed(Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji, Kružići_lista_X_Y, Kružići_lista_zaSimulaciju_X_Y, Predznaci_X_Y, Naboji_X_Y) 

                            elif inbox == KRUŽNICA_INBOX:                   
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = [], [], [], []
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = NadopuniListe_sX_Y_odnazad(Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji, Kružići_lista_X_Y, Kružići_lista_zaSimulaciju_X_Y, Predznaci_X_Y, Naboji_X_Y) 

                    if len(Kružići_lista)>0 and True not in [inbox.selektiran for inbox in INBOXES]:    
                        if Kružići_lista[-1] in Kružići_lista_X_Y:                                          #izbaci naboj iz X_Y lista
                            Kružići_lista_X_Y.remove(Kružići_lista[-1])
                            Predznaci_X_Y.remove(Predznaci[-1])
                            Naboji_X_Y.remove(Naboji[-1])
                        if Kružići_lista_zaSimulaciju[-1] in Kružići_lista_zaSimulaciju_X_Y:
                            Kružići_lista_zaSimulaciju_X_Y.remove(Kružići_lista_zaSimulaciju[-1])

                        Kružići_lista.pop()
                        Kružići_lista_zaSimulaciju.pop()
                        Predznaci.pop()
                        Naboji.pop()


                        
                
                #Upisivanje u inboxe
                if PERMITIVNOST_INBOX.selektiran == True and (event.unicode.isdigit() or (event.unicode == "." and "." not in PERMITIVNOST_INBOX.text_input)) and len(PERMITIVNOST_INBOX.text_input) < 6:
                    PERMITIVNOST_INBOX.Upisivanje(event.unicode)
                
                Naboj_tekst = NABOJ_INBOX.text_input
                Što_smije_u_nabInbox = NABOJ_INBOX.selektiran == True and (event.unicode.isdigit() or ((event.unicode == "e") and ("e" not in Naboj_tekst)) or ((event.unicode == "+" or event.unicode == "-") and (("e" in Naboj_tekst) and (("+" not in Naboj_tekst) and ("-" not in Naboj_tekst))))) and len(Naboj_tekst) <6  
                if Što_smije_u_nabInbox:    
                    if NABOJ_INBOX.text_input == "" and (event.unicode == "0" or event.unicode == "e"):      
                        pass
                    else:
                        NABOJ_INBOX.Upisivanje(event.unicode) 
                        if KRUŽNICA_CBOX.checked == True or KVADRAT_CBOX.checked == True:   
                            Naboj_vrijednost = DobiNaboj(NABOJ_INBOX)
                            Naboji = [Naboj_vrijednost for i in Naboji]    
                          
                
                if KRUŽNICA_INBOX.selektiran == True and event.unicode.isdigit() and len(KRUŽNICA_INBOX.text_input) <5: 
                    KRUŽNICA_INBOX.Upisivanje(event.unicode) 
                    br_naboja = int(KRUŽNICA_INBOX.text_input)
                    Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = crtajKružnicu(br_naboja,Centar,PREDZNAK_CBOX.caption_input[-1], DobiNaboj(NABOJ_INBOX)) 
                    Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = NadopuniListe_sX_Y_odnaprijed(Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji, Kružići_lista_X_Y, Kružići_lista_zaSimulaciju_X_Y, Predznaci_X_Y, Naboji_X_Y) 

                    
                    
                    
                  
                
                for x_y_inbox in X_Y_INBOXES:
                    if x_y_inbox.selektiran == True and (event.unicode.isdigit() or ((event.unicode == "+" or event.unicode == "-") and x_y_inbox.text_input=="")) and len(x_y_inbox.text_input) < 4:
                        x_y_inbox.Upisivanje(event.unicode)
                        if len(x_y_inbox.text_input) > 2 and (DobiKoordinatu(x_y_inbox) > 300 or DobiKoordinatu(x_y_inbox) <-300):
                            x_y_inbox.text_input = x_y_inbox.text_input[:-1]  

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Interakcije miša i inboxa
                for INBOX in INBOXES:       
                    if INBOX.provjeraSudara(mouse_position):       #ako je kliknut inbox i nije selektiran, selektiraj ga
                        if INBOX.selektiran == False:
                            for inbox in INBOXES:                  
                                inbox.selektiran = False
                            INBOX.selektiran = True
                    else:                                           #ako je kliknuto, a nesto drugo, odselektiraj (osim X i Y kako bi se kod njih mogao birati predznak)
                        if INBOX not in X_Y_INBOXES:
                            INBOX.selektiran = False
                            if (NABOJ_INBOX.text_input == "" or DobiNaboj(NABOJ_INBOX) < 1e-171  or DobiNaboj(NABOJ_INBOX) > 1e+140) and NABOJ_INBOX.selektiran == False:    
                                        NABOJ_INBOX.text_input = "1"
                            if (PERMITIVNOST_INBOX.text_input == "" or float(PERMITIVNOST_INBOX.text_input)<1) and PERMITIVNOST_INBOX.selektiran == False:    
                                PERMITIVNOST_INBOX.text_input = "1"

                #Interakcije miša i gumba       
                if POSTAVI_GUMB.provjeraSudara(mouse_position) and DobiKoordinatu(X_INBOX) != "Nemože" and DobiKoordinatu(Y_INBOX) != "Nemože":
                    x = DobiKoordinatu(X_INBOX)
                    y = DobiKoordinatu(Y_INBOX)
                    if (x,y) not in Kružići_lista_zaSimulaciju:
                        X_Y = pretvorbaProstorU_Ekran_Kružić(x,y,Centar)
                        Kružići_lista_X_Y.append((X_Y[0], X_Y[1]))
                        Kružići_lista_zaSimulaciju_X_Y.append((x,y))
                        Predznaci_X_Y.append(PREDZNAK_CBOX.caption_input[-1]) 
                        Naboji_X_Y.append(DobiNaboj(NABOJ_INBOX)) 
                        #defaultne liste nadopuni s listom iz X, Y kucica
                        Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = NadopuniListe_sX_Y_odnazad(Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji, Kružići_lista_X_Y, Kružići_lista_zaSimulaciju_X_Y, Predznaci_X_Y, Naboji_X_Y) 


                if PRIHVATI_GUMB.provjeraSudara(mouse_position) and len(Kružići_lista_zaSimulaciju)>0: 
                    pygame.quit()
                    er = float(PERMITIVNOST_INBOX.text_input)
                    simulacija(Kružići_lista_zaSimulaciju, Predznaci, Naboji, er)                ## NAPRAVI SIMULACIJU
                
                #Interakcija miša i checkboxova
                for CBOX in CBOXES:
                    if CBOX.provjeraSudara(mouse_position):         
                        if CBOX.checked == False and (True not in [cbox.checked for cbox in CBOXES]):               ##ako već nije upaljen ijedan checkbox
                            CBOX.checked = True                                                                     ##stavi ga na upaljeno
                            if CBOX == KVADRAT_CBOX:                
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = crtajKvadrat(Centar, PREDZNAK_CBOX.caption_input[-1],DobiNaboj(NABOJ_INBOX))
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = NadopuniListe_sX_Y_odnaprijed(Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji, Kružići_lista_X_Y, Kružići_lista_zaSimulaciju_X_Y, Predznaci_X_Y, Naboji_X_Y) 

                        else:
                            CBOX.checked = False                
                            if CBOX == KRUŽNICA_CBOX:  
                                KRUŽNICA_INBOX.selektiran = False 
                                KRUŽNICA_INBOX.text_input = ""
                            if True not in [cbox.checked for cbox in CBOXES]:   
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = [], [], [], []
                                Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji = NadopuniListe_sX_Y_odnazad(Kružići_lista, Kružići_lista_zaSimulaciju, Predznaci, Naboji, Kružići_lista_X_Y, Kružići_lista_zaSimulaciju_X_Y, Predznaci_X_Y, Naboji_X_Y) 

                if PREDZNAK_CBOX.provjeraSudara(mouse_position):
                    if PREDZNAK_CBOX.checked == False:
                        PREDZNAK_CBOX.checked = True
                        PREDZNAK_CBOX.caption_input = PREDZNAK_CBOX.caption_input.replace("+","-")
                        if (KRUŽNICA_CBOX.checked or KVADRAT_CBOX.checked) and True not in [inbox.selektiran for inbox in X_Y_INBOXES]:           ##ako se predznak mijenja usred, onda za kruznicu i kvadrat odma mijenjaj
                            Predznaci = ["-" for pred in Predznaci]
                    else:
                        PREDZNAK_CBOX.checked = False
                        PREDZNAK_CBOX.caption_input = PREDZNAK_CBOX.caption_input.replace("-","+")
                        if (KRUŽNICA_CBOX.checked or KVADRAT_CBOX.checked) and True not in [inbox.selektiran for inbox in X_Y_INBOXES]:           
                            Predznaci = ["+" for pred in Predznaci]
                    

                if ZASEBNO_CBOX.checked == True:
                    if Prostor.collidepoint(mouse_position):
                        p, n = crtajZasebno(mouse_position, Kružići_lista, mouse_position_prostora, Kružići_lista_zaSimulaciju, PREDZNAK_CBOX.caption_input[-1], DobiNaboj(NABOJ_INBOX))
                        Predznaci.append(p)
                        Naboji.append(n)
                
                
        try:                                ## Nakon kaj udje u simulaciju, pygame se ugasi, ali ne i sys, pa se on gasi tek kada se ugasi simulacija, tako da se running stavi na false
            pygame.display.update()
            clock.tick(FPS)   
        except:
            Running = False

def crtanjeInboxa(inbox, mouse_position, X_Y_INBOXES = []):
    if inbox.provjeraSudara(mouse_position):
        if inbox.selektiran == False:      
            inbox.changeInboxHoverColor()
    elif inbox.selektiran == True:         
        inbox.changeInboxSelectedColor() 
        if len(inbox.text_input) < 4 and inbox in X_Y_INBOXES:
            linija_playscore_animacija(inbox)  
        elif len(inbox.text_input) < 6 and inbox not in X_Y_INBOXES:
            
            linija_playscore_animacija(inbox)
    else:                                           
        inbox.rectangle_color = "black"
    inbox.update(SCREEN)
    
def IspisUpute(uputa_tekstovi, tekst_color, tekst_font, position, SCREEN, y_pomak):     #Ispisivanje upute_teksta na ekran
    for red in uputa_tekstovi:                                        
        uputa_surface = tekst_font.render(red, True, tekst_color)
        uputa_rectangle = uputa_surface.get_rect(center=(position[0], position[1] + y_pomak))
        SCREEN.blit(uputa_surface, uputa_rectangle)
        if uputa_tekstovi.index(red)>1:
            y_pomak += uputa_rectangle.height + 10     
        else:
            y_pomak += uputa_rectangle.height       



def crtajNabojeUProstor(Kružići_lista,Predznaci,SCREEN):  
    for kružić, predznak in zip(Kružići_lista,Predznaci):               
        if predznak == "+":                                                
            pygame.draw.circle(SCREEN,"red",kružić,4)
        else:                                                              
            pygame.draw.circle(SCREEN,"blue",kružić,4)     

def crtajOpisNaboja(Kružići_lista, Predznaci, Naboji, mouse_position, opis_font,  SCREEN):
    for kružić,naboj,predznak in zip(Kružići_lista,Naboji,Predznaci):       
        kružić_rect = pygame.Rect((kružić[0]-5,kružić[1]-5), (10,10))
        if kružić_rect.collidepoint(mouse_position):
            opis_surface = opis_font.render(f"{predznak} {naboj}", True, "Black")           #opis kružića je predznak + naboj
            opis_rectangle = opis_surface.get_rect(center = (kružić[0]-25, kružić[1]+15)) 
            SCREEN.blit(opis_surface,opis_rectangle)


def NadopuniListe_sX_Y_odnazad(Kružići_lista, Kružići_lista_zaSimulaciju, predznaci, naboji, Kružići_listaXY, Kružići_lista_zaSimulacijuXY, predznaciXY, nabojiXY):
    Kružići_lista.extend(Kružići_listaXY)
    Kružići_lista_zaSimulaciju.extend(Kružići_lista_zaSimulacijuXY)
    predznaci.extend(predznaciXY)
    naboji.extend(nabojiXY)
    return Kružići_lista, Kružići_lista_zaSimulaciju, predznaci, naboji

def NadopuniListe_sX_Y_odnaprijed(Kružići_lista, Kružići_lista_zaSimulaciju, predznaci, naboji, Kružići_listaXY, Kružići_lista_zaSimulacijuXY, predznaciXY, nabojiXY):
    Kružići_lista = Kružići_listaXY + Kružići_lista
    Kružići_lista_zaSimulaciju = Kružići_lista_zaSimulacijuXY + Kružići_lista_zaSimulaciju
    predznaci = predznaciXY + predznaci
    naboji = nabojiXY + naboji
    return Kružići_lista, Kružići_lista_zaSimulaciju, predznaci, naboji



def DobiKoordinatu(X_Y_INBOX):      #Čita X, Y inboxe
    try:
        if "+" in X_Y_INBOX.text_input:
            Broj = int(X_Y_INBOX.text_input.split("+")[1])
        elif "-" in X_Y_INBOX.text_input:
            Broj = -int(X_Y_INBOX.text_input.split("-")[1])
        else:
            Broj = int(X_Y_INBOX.text_input)
        return Broj
    except:
        return "Nemože"

def DobiNaboj(NABOJ_INBOX):         #Čita Naboj inbox
    if "e" in NABOJ_INBOX.text_input:      
        if "e" != NABOJ_INBOX.text_input[-1]:       #ako nakon e ima jos brojeva
            if NABOJ_INBOX.text_input[NABOJ_INBOX.text_input.index("e")+1].isdigit():   #ako je znak nakon e broj (gledamo kao da je poz predznak)
                Naboj_vrijednost = NABOJ_INBOX.text_input.split("e")   
                Naboj_vrijednost = int(Naboj_vrijednost[0]) * (10 ** int(Naboj_vrijednost[1]))
            
            elif NABOJ_INBOX.text_input[NABOJ_INBOX.text_input.index("e")+1] == "+":        #npr. 1e+1
                if NABOJ_INBOX.text_input[-1] == "+": 
                    Naboj_vrijednost = re.split('e|\+',NABOJ_INBOX.text_input)           
                    Naboj_vrijednost = int(Naboj_vrijednost[0]) * (10**1)                   
                else:
                    Naboj_vrijednost = re.split('e|\+',NABOJ_INBOX.text_input)          
                    Naboj_vrijednost = int(Naboj_vrijednost[0]) * (10 ** int(Naboj_vrijednost[2]))  # drugo mjesto u indexu jer je srednje ''
            
            elif NABOJ_INBOX.text_input[NABOJ_INBOX.text_input.index("e")+1] == "-":    #npr. 1e-1
                if NABOJ_INBOX.text_input[-1] == "-":
                    Naboj_vrijednost = re.split('e|\-',NABOJ_INBOX.text_input)          
                    Naboj_vrijednost = int(Naboj_vrijednost[0]) * (10 **-1)          
                else:
                    Naboj_vrijednost = re.split('e|\-',NABOJ_INBOX.text_input)          
                    Naboj_vrijednost = int(Naboj_vrijednost[0]) * (10 ** -int(Naboj_vrijednost[2]))  # drugo mjesto u indexu jer je srednje ''

        else:                                                           #ako nakon e nema vise brojeva
            Naboj_vrijednost = int(NABOJ_INBOX.text_input[-2]) * 10

        return float(Naboj_vrijednost)
    else:                                   
        return float(NABOJ_INBOX.text_input)

        
    t

def pretvorbaProstorU_Ekran_Kružić(x,y,Centar):
    return (x + Centar[0], -y+Centar[1])

def crtajZasebno(mouse_position, Kružići_lista, mouse_position_prostora, Kružići_lista_zaSimulaciju, predznak, naboj):
    Kružić = mouse_position
    Kružići_lista.append(Kružić)

    Kružić_prostor = mouse_position_prostora
    Kružići_lista_zaSimulaciju.append(Kružić_prostor)

    return predznak, naboj 

def crtajKružnicu(br_naboja, Centar, predznak, naboj, radijus=2):  #radijus u m
    predznak = predznak
    naboj = naboj

    Kružići_lista_zaSimulaciju = []
    Kružići_lista = []
    predznaci = []
    naboji = []
    radijus = radijus*100           ##*100, jer je 1m = 100px 
    kuteviNaboja = np.linspace(0, 2*np.pi, br_naboja, endpoint=False) #dakle kružnica ide od 0 do 2PI i sad on iz tog rangea uzima brE Naboja i daje im kut iz rangea, da su svi jednako udaljeni
    for kut in kuteviNaboja:
        predznaci.append(predznak)  
        naboji.append(naboj) 

        x = round(radijus * np.cos(kut),0)
        y = round(radijus * np.sin(kut),0)
        kružić = (x,y)      
        Kružići_lista_zaSimulaciju.append(kružić)

        kružić = pretvorbaProstorU_Ekran_Kružić(x,y,Centar)  
        Kružići_lista.append(kružić)
        

    return Kružići_lista, Kružići_lista_zaSimulaciju, predznaci, naboji

def crtajKvadrat(Centar, predznak, naboj, dulj_stranice = 3): #dulj_stranice je u m
    predznak = predznak
    naboj = naboj
    Kružići_lista_zaSimulaciju = []
    Kružići_lista = []
    predznaci = []
    naboji = []
    dulj_stranice = dulj_stranice*100           ##*100, jer je 1m = 100px

    br_naboja = 120          #-4 zapravo, jer će se 4 naboja ponovit, ali i izbrisat kasnije da nebudu duplikati
    br_naboja_po_strani = br_naboja//4
    točke_po_strani = np.round(np.linspace(-150, dulj_stranice//2, br_naboja_po_strani, endpoint=True),0) #gleda se jedna stranica i na nju se raspoređuje br_naboja jednako udaljenih
    točke_po_strani = točke_po_strani.tolist()
    
    x_koordinate = []
    y_koordinate = []
    
    # Dolje
    x_koordinate.extend(točke_po_strani)
    y_koordinate.extend([-dulj_stranice//2] * br_naboja_po_strani)

    # Desno
    x_koordinate.extend([dulj_stranice//2] * br_naboja_po_strani)
    y_koordinate.extend(točke_po_strani)

    # Gore
    točke_po_strani_obrnuto = točke_po_strani.copy()[::-1]
    x_koordinate.extend(točke_po_strani_obrnuto)
    y_koordinate.extend([dulj_stranice//2] * br_naboja_po_strani)

    # Lijevo 
    x_koordinate.extend([-dulj_stranice//2] * br_naboja_po_strani)
    y_koordinate.extend(točke_po_strani_obrnuto)
    
    np_lista_koor = np.column_stack((x_koordinate, y_koordinate))
    lista_koor_sim = np_lista_koor.tolist()

    #Mičem duple točke
    unique_list = []
    unique_set = set()
    for item in lista_koor_sim:
        if tuple(item) not in unique_set:
            unique_list.append(item)
            unique_set.add(tuple(item))          

    Kružići_lista_zaSimulaciju = unique_list         #u prostoru


    #sada svaku koordinatu iz np liste pretvaram u koordinatu SCREENA
    Kružići_lista_prostora = Kružići_lista_zaSimulaciju.copy()

    for koor in Kružići_lista_prostora:
        Kružići_lista_prostora[Kružići_lista_prostora.index(koor)] =  pretvorbaProstorU_Ekran_Kružić(koor[0], koor[1], Centar)
    Kružići_lista = Kružići_lista_prostora 

    predznaci = [predznak for i in range(len(Kružići_lista))]       ##napravi listu predznaka dugu kao i lista točaka 
    naboji = [naboj for i in range(len(Kružići_lista))]             ##napravi listu naboja dugu kao i lista točaka 
    return Kružići_lista, Kružići_lista_zaSimulaciju, predznaci, naboji


def linija_playscore_animacija(Inbox):
    global linija_key_index, linija_playscore_surf      
    linija_key_index += 0.03                            #što veći broj, brža animacija
    if linija_key_index >= len(linija_playscore_animacija_lista):
        linija_key_index = 0
    linija_playscore_surf = linija_playscore_animacija_lista[int(linija_key_index)]

    Trenutni_tekst_Inbox = Inbox.text_input
    if Trenutni_tekst_Inbox != "":      #Ako postoji teksta već
        kraj_riječi_x, kraj_riječi_y = Inbox.text_rectangle.midright   
        linija_playscore_rect = linija_playscore_surf.get_rect(midright = (kraj_riječi_x+5, kraj_riječi_y))  #Na kraj text recta stavi crtu
    else:                               #Ako je prazan inputbox
        linija_playscore_rect = linija_playscore_surf.get_rect(center = (Inbox.rectangle.center)) #centriraj liniju u sred boxa

    SCREEN.blit(linija_playscore_surf, linija_playscore_rect)

if __name__ == "__main__":
    main()




