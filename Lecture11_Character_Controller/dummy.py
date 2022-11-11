class Star:
    name = 'Star' #클래스 변수임
    x = 100 #이것도 클래스 변수임

    def change():
        x = 200
        print('x is ', x)

        #스타라는 클래스안에 self를 안씀 change(self) X

print('x is ', Star.x) #클래스 안에 있는 변수를 액세스함.
Star.change() #클래스 안에 있는 함수를 호출함. 클래스 함수임.

#클래스는 객체를 만드는 틀임.
#파이썬은 함수나 변수를 그루핑(관리)할 수 있음.

star = Star() #생성자가 없는데 객체를 생성?? 근데 됨.
print(type(star))
print(star.x)
#비록 객체 변수로 액세스 했으나, 같은 이름의 클래스 변수가 우선임.

star.change() #Star.change(star)와 동일함.
#객체의 함수를 호출하면 저 star에 클래스를 찾음.(대문자 Star)
#5열의 change()에서 빈칸이므로 오류가 뜸.