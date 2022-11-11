class Player:
    name = 'Player'

    def __init__(self): #self자리에 my를 넣어도 됨. self는 객체 그 자기자신일 뿐이다.
        self.x = 100

    def where(self):
        print(self.x)

player = Player()
player.where()

print(Player.name)
print(player.name)

#Player.where()
#Player.where는 self가필요함
Player.where(player)
#(player)은 self로 연결됨.