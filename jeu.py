import pyxel

class App :
    def __init__(self) :
        pyxel.init(256, 192)
        pyxel.load("textures.pyxres")
        #################################
        
        self.menu = Menu()
        self.player1 = Player(8, 136, "right", 1)
        self.player2 = Player(240, 136, "left", 2)
        self.firelist = []


        #################################
        pyxel.run(self.update, self.draw)
    
    def update(self) :
        if self.menu.power :
            if pyxel.btnp(pyxel.KEY_RETURN) :
                self.menu.toggle()

        elif self.player1.win or self.player2.win:
            if pyxel.btnp(pyxel.KEY_RETURN) :
                self.menu.toggle()
                self.player1 = Player(8, 136, "right", 1)
                self.player2 = Player(240, 136, "left", 2)

        else : 
            self.player1.interactions()
            self.player2.interactions()

            if self.player1.life <= 0 :
                self.player2.win = True
            
            if self.player2.life <= 0 :
                self.player1.win = True

            if pyxel.btnp(pyxel.KEY_SPACE) and self.player1.mag.amount > 0 and self.player1.mag.loaded :
                self.firelist.append(Fire(self.player1.x, self.player1.y, self.player1.direction, 1))
                self.player1.mag.amount -= 1
            
            if pyxel.btnp(pyxel.KEY_L) and self.player2.mag.amount > 0 and self.player2.mag.loaded :
                self.firelist.append(Fire(self.player2.x, self.player2.y, self.player2.direction, 2))
                self.player2.mag.amount -= 1
            
            self.player1.mag.changing(1)
            self.player2.mag.changing(2)

            for fire in self.firelist :
                if (fire.x > 264) or (fire.x < -8) : 
                    self.firelist.remove(fire)
                
                elif ((fire.x+7 >= self.player1.x and fire.x <= self.player1.x+8) and (fire.y >= self.player1.y-5 and fire.y <= self.player1.y+8)) and fire.who != 1:
                    self.player1.life -= 1
                    self.player1.x, self.player1.y = 8, 136
                    self.player2.x, self.player2.y = 240, 136
                    self.player1.mag.amount = 10
                    self.player2.mag.amount = 10
                    self.firelist = []
                   
                elif ((fire.x+7 >= self.player2.x and fire.x <= self.player2.x+8) and (fire.y >= self.player2.y-5 and fire.y <= self.player2.y+8)) and fire.who != 2:
                    self.player2.life -= 1
                    self.player2.x, self.player2.y = 240, 136
                    self.player1.x, self.player1.y = 8, 136
                    self.player1.mag.amount = 10
                    self.player2.mag.amount = 10
                    self.firelist = []
                
                fire.move()


    def draw(self) :
        if self.menu.power :
            self.menu.draw()
        
        elif self.player1.win :
            pyxel.bltm(0, 0, 2, 0, 0, 256, 192)
            if pyxel.frame_count % 40 == 0 :
                col = 6
            else :
                col = 1
            pyxel.text(16, 158, "\nPRESS ENTER\n TO PLAY AGAIN", col)
            pyxel.text(180, 158, "\n PRESS ESC\nTO QUIT", col)
        
        elif self.player2.win :
            pyxel.bltm(0, 0, 3, 0, 0, 256, 192)
            if pyxel.frame_count % 40 == 0 :
                col = 6
            else :
                col = 1
            pyxel.text(16, 158, "\nPRESS ENTER\n TO PLAY AGAIN", col)
            pyxel.text(180, 158, "\n PRESS ESC\nTO QUIT", col)
        
        else :
            pyxel.bltm(0, 0, 0, 0, 0, 256, 192)
            
            self.player1.draw()
            self.player1.drawLife()
            self.player1.drawMag()
            
            self.player2.draw()
            self.player2.drawLife()
            self.player2.drawMag()

            for fire in self.firelist :
                fire.draw()

class Menu :
    def __init__(self) :
        self.power = True
    
    def draw(self) :
        pyxel.bltm(0, 0, 1, 0, 0, 256, 192)
        
        if pyxel.frame_count % 40 == 0 :
            col = 6
        else :
            col = 1
        pyxel.text(16, 158, "PLAYER 1 : \nWASD TO MOVE \nR TO CHANGE MAG\n SPACE TO SHOOT", col)
        pyxel.text(180, 158, " PLAYER 2 : \n ARROWS TO MOVE \n K TO CHANGE MAG\nL TO SHOOT", col)
        pyxel.text(107, 164, "ESC TO QUIT", 8-col)

    def toggle(self) :
        self.power = not self.power
    
class Player :
    def __init__(self, x:int, y:int, direction:str, skin:int) :
        self.x = x
        self.y = y
        self.life = 8
        self.win = False
        self.direction = direction
        self.costume = 0
        self.skin = skin
        self.jump = 0
        self.mag = Mag()
    
    def draw(self) :
        down_tile = pyxel.tilemap(0).pget((self.x+4)//8, (self.y+8)//8)
        if self.skin == 1 :    
            if down_tile != (0,0) :
                if self.direction == "left":
                    if self.costume in {0, 1, 2}: # le costume change en fonction de la valeur de coeff
                        pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, 0)
                    else :
                        pyxel.blt(self.x, self.y, 0, 16, 8, 8, 8, 0)
                
                elif self.direction == "right":
                    if self.costume in {0, 1, 2}: # le costume change en fonction de la valeur de coeff
                        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, 0)
                    else :
                        pyxel.blt(self.x, self.y, 0, 16, 0, 8, 8, 0)
                
            else:
                if self.direction == "left":
                    pyxel.blt(self.x,self.y,0,24,8,8,8,0)                
                elif self.direction == "right":
                    pyxel.blt(self.x,self.y,0,24,0,8,8,0)

        elif self.skin == 2 :
            if down_tile != (0,0) :
                if self.direction == "left":
                    if self.costume in {0, 1, 2}: # le costume change en fonction de la valeur de coeff
                        pyxel.blt(self.x, self.y, 0, 0, 56, 8, 8, 0)
                    else :
                        pyxel.blt(self.x, self.y, 0, 8, 56, 8, 8, 0)
                
                elif self.direction == "right":
                    if self.costume in {0, 1, 2}: # le costume change en fonction de la valeur de coeff
                        pyxel.blt(self.x, self.y, 0, 0, 48, 8, 8, 0)
                    else :
                        pyxel.blt(self.x, self.y, 0, 8, 48, 8, 8, 0)
                
            else:
                if self.direction == "left":
                    pyxel.blt(self.x, self.y ,0 ,16 ,56 ,8 ,8 ,0)                
                elif self.direction == "right":
                    pyxel.blt(self.x ,self.y ,0 ,16 ,48 ,8 ,8 ,0)

    def drawLife(self) :
        if self.skin == 1 :
            for i in range(self.life) :
                pyxel.blt(i*8+4, 4, 0, 32, 32, 8, 8, 0)
        elif self.skin == 2 :
            for i in range(self.life) :
                pyxel.blt(244-(i*8), 4, 0, 40, 32, 8, 8, 0)
    
    def drawMag(self) :
        if self.skin == 1 :
            if self.mag.loaded :
                pyxel.text(4, 16, str(self.mag.amount), 7)
            else :
                pyxel.text(4, 16, "LOADING...", 7)

        elif self.skin == 2 :
            if self.mag.loaded :
                pyxel.text(244, 16, str(self.mag.amount), 7)
            else :
                pyxel.text(216, 16, "LOADING...", 7)


    def interactions(self) :
        right_tile = pyxel.tilemap(0).pget((self.x+8)//8, (self.y+4)//8)
        left_tile = pyxel.tilemap(0).pget((self.x-1)//8, (self.y+4)//8)
        down_tile = pyxel.tilemap(0).pget((self.x+4)//8, (self.y+8)//8)
        down_down_tile = pyxel.tilemap(0).pget((self.x+4)//8, (self.y+16)//8)
        void_tile = (0, 0)

        if self.skin == 1 :
            #jump
            if pyxel.btnp(pyxel.KEY_W) and self.jump == 0 and down_tile != void_tile :
                self.jump =  25
            elif self.jump > 15 :
                self.jump -= 1
                self.y -= 3
            elif down_tile == void_tile :
                self.jump = 0
                self.y += 2
            #walking
            if pyxel.btnp(pyxel.KEY_A, hold=True, repeat=True) :
                self.direction = "left"
                if left_tile == void_tile and self.x > 0 :
                    self.x -= 2
                    self.costume = (self.costume+1)%6
            elif pyxel.btnp(pyxel.KEY_D, hold=True, repeat=True) :
                self.direction = "right"
                if right_tile == void_tile and self.x+8 < 256 :
                    self.x += 2
                    self.costume = (self.costume+1)%6
            #dash
            if pyxel.btnp(pyxel.KEY_S) and down_down_tile == void_tile:
                self.y += 8
        
        elif self.skin == 2 :
            #jump
            if pyxel.btnp(pyxel.KEY_UP) and self.jump == 0 and down_tile != void_tile :
                self.jump =  25
            elif self.jump > 15 :
                self.jump -= 1
                self.y -= 3
            elif down_tile == void_tile :
                self.jump = 0
                self.y += 2
            #walkingw
            if pyxel.btnp(pyxel.KEY_LEFT, hold=True, repeat=True) :
                self.direction = "left"
                if left_tile == void_tile and self.x > 0 :
                    self.x -= 2
                    self.costume = (self.costume+1)%6
            elif pyxel.btnp(pyxel.KEY_RIGHT, hold=True, repeat=True) :
                self.direction = "right"
                if right_tile == void_tile and self.x+8 < 256 :
                    self.x += 2
                    self.costume = (self.costume+1)%6
            #dash
            if pyxel.btnp(pyxel.KEY_DOWN) and down_down_tile == void_tile :
                self.y += 8
        
class Fire :
    def __init__(self, x, y, direction, who) :
        self.x = x
        self.y = y
        self.direction = direction
        self.who = who
    
    def move(self) :
        if self.direction == "right" :
            self.x += 2
        elif self.direction == "left" :
            self.x -= 2
    
    def draw(self) :
        if self.who == 2 :
            if self.direction == "right" :
                pyxel.blt(self.x, self.y, 0, 80, 1, 7, 5, 0)
            elif self.direction == "left" :
                pyxel.blt(self.x, self.y, 0, 89, 1, 7, 5, 0)
        elif self.who == 1 :
            if self.direction == "right" :
                pyxel.blt(self.x, self.y, 0, 80, 9, 7, 5, 0)
            elif self.direction == "left" :
                pyxel.blt(self.x, self.y, 0, 89, 9, 7, 5, 0)

class Mag :
    def __init__(self) :
        self.timeToLoad = 150
        self.amount = 10
        self.timer = self.timeToLoad
        self.loaded = True

    def changing(self, who) :
        if pyxel.btnp(pyxel.KEY_R) and who == 1:
            if self.timer == self.timeToLoad and self.amount < 10:
                self.loaded = False
            
        if self.loaded == False :
            if self.timer <= 0 :
                self.loaded = True
                self.timer = self.timeToLoad
                self.amount = 10
            else :
                self.timer -= 1

        if pyxel.btnp(pyxel.KEY_K) and who == 2:
            if self.timer == self.timeToLoad and self.amount < 10:
                self.loaded = False
            
        if self.loaded == False :
            if self.timer <= 0 :
                self.loaded = True
                self.timer = self.timeToLoad
                self.amount = 10
            else :
                self.timer -= 1

App()
