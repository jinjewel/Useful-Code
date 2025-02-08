# 틱 텍 톡 게임
# 게임순서 결정, 보드 그리기, 플레이어 '수' 놓기, AI '수' 놓기, 승자체크 모듈
# 플레이어 승리, AI 승리, 무승부 확인 모듈

import random 
import sys

# 게임순서 결정 모듈
def choosePlayer():
    print('선공 결정을 위해 O, X를 입력)')
    print('O : AI, X : 플레이어')
    while True:
        str_ch = input('입력 : ')
        chosen = str_ch.upper()
        if chosen != 'O' and chosen !='X' : #영문자 O,X가 아닌 경우 다시 입력
            print('영문자 O 또는 X를 다시 입력하세요.')
            continue
        elif chosen == 'O': #AI가 선공
            return 'O','X'
        elif chosen == 'X': #Palyer가 선공
            return 'X','O'

# 보드 그리기 모듈
def drawingBoard(screen):
    print()
    print('───────────────────────')
    print(' '+screen[6]+' '+'│'+' '+screen[7]+' '+'│'+' '+screen[8]) 
    print('───────────────────────')
    print(' '+screen[3]+' '+'│'+' '+screen[4]+' '+'│'+' '+screen[5])
    print('───────────────────────')
    print(' '+screen[0]+' '+'│'+' '+screen[1]+' '+'│'+' '+screen[2])
    print('───────────────────────')
    print() 

# 플레이어 '수' 놓기 모듈
def putPlayerStone(screen, mark):
    while True:
        print('>> 돌 위치 선택 : ',end='')
        position = input()
        if position not in ['1', '2', '3', '4', '5' ,'6' ,'7' ,'8', '9'] : # 1~ 9 숫자만 가능
            continue
        if screen[int(position)-1] != '': # 이미 수가 놓여 있다면..
            continue
        else :
            break 
    screen[int(position)-1] = mark #player의 ‘수’ 놓기
    return screen

# AI '수' 놓기 모듈
def putAIStone (screen, player, AI): 
    AI_willPut_here=[] #AI가 놓을 위치

    #플레이어가 ‘수’를 놓은 위치를 확인
    Put_player = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,9):
        if player == screen[i]:
            Put_player[i] = True

    #컴퓨터가 놓아서 승리할 수 있는 위치가 있는지 확인
    Put_AI = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,9):
        if AI == screen[i]:
            Put_AI[i] = True

    #컴퓨터의 돌이 가로로 2개 이상 놓였는지 확인
    hIdx = 8
    while hIdx >= 2:
        #한 쪽에 쏠려 놓인 경우 
        if Put_AI[hIdx -1]==True: #가운데
            if Put_AI [hIdx -1-1] == True: #왼쪽
                AI_willPut_here.append(hIdx -1+1)
            elif Put_player[hIdx -1+1] == True: #오른쪽
                AI_willPut_here.append(hIdx -1-1)
        #양쪽에 놓인 경우
        elif Put_AI[hIdx -1-1] == True and Put_AI[hIdx -1+1] == True:
            AI_willPut_here.append(hIdx -1)
        hIdx -= 3

    #컴퓨터의 돌이 세로로 2개 이상 놓였는지 확인
    vIdx = 4
    while vIdx <= 6:
        # 한쪽에 쏠려 놓인경우.
        if Put_AI[vIdx -1] == True: #가운데 돌이 놓인 경우
            if Put_AI[vIdx-1+3] == True: #위쪽에 돌이 놓인 경우
                AI_willPut_here.append(vIdx -1-3)
            elif Put_AI[vIdx -1-3] == True: #아래쪽에 돌이 놓인 경우
                AI_willPut_here.append(vIdx -1+3)
        #양쪽에 놓인 경우
        elif Put_AI[vIdx -1+3] == True and Put_AI[vIdx -1-3] == True:
            AI_willPut_here.append(vIdx -1)
        vIdx += 1

    #컴퓨터의 돌이 대각선으로 2개 이상 놓였는지 확인
    if Put_AI[5-1] == True: #5번에 돌이 놓인 경우
        if Put_AI[7-1] == True:
            AI_willPut_here.append(3-1)
        elif Put_AI[3-1] == True:
            AI_willPut_here.append(7-1)
        elif Put_AI[9-1] == True:
            AI_willPut_here.append(1-1)
        elif Put_AI[1-1] == True:
            AI_willPut_here.append(9-1)
    if Put_AI[7-1] == True and Put_AI[3-1] == True:
        AI_willPut_here.append(5-1)
    if Put_AI[9-1] == True and Put_AI[1-1] == True:
        AI_willPut_here.append(5-1)

    # '수'를 놓을 자리 선택
    for i in range(0,len(AI_willPut_here)):
        if screen[AI_willPut_here[i]] == '' :
            screen[AI_willPut_here[i]] = AI
            return screen
    
    #수를 놓을 자리를 못 찾은 경우 랜덤하게 지정
    for i in range(0,9):
        if screen[i]=='':
            AI_willPut_here.append(i)
    
    available = []
    for i in range(0,len(AI_willPut_here)):
        if screen[AI_willPut_here[i]] == '' :
            available.append(AI_willPut_here[i])
    available = random.choice(available)
    screen[int(available)] = AI
    return screen

# 승자체크 모듈
def checkWinner(screen,player,AI): # 플래이어 승리 확인
    #플레이어가 돌을 놓은 위치를 확인
    playerPut = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,9):
        if player == screen[i]:
            playerPut[i] = True
      
    #AI가 돌을 놓은 위치를 확인
    AIPut = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,9):
        if AI == screen[i]:
            AIPut[i] = True  
      
    # 플레이어 세로 확인
    vIdx = 7
    while vIdx <=9:
        if playerPut[vIdx-1]==True and playerPut[vIdx-1-3]==True and playerPut[vIdx-1-6]==True :
            playerWin(screen)
            return True
        vIdx+=1

    # AI 세로 확인
    vIdx = 7
    while vIdx <=9:
        if AIPut[vIdx-1]==True and AIPut[vIdx-1-3]==True and AIPut[vIdx-1-6]==True :
            AIWin(screen)
            return True
        vIdx+=1

    # 플레이어 가로 확인
    hIdx = 7
    while hIdx >=1:
        if playerPut[hIdx-1]==True and playerPut[hIdx-1+1]==True and playerPut[hIdx-1+2]==True :
            playerWin(screen)
            return True 
        hIdx-=3
    
    # AI 가로 확인
    hIdx = 7
    while hIdx >=1:
        if AIPut[hIdx-1]==True and AIPut[hIdx-1+1]==True and AIPut[hIdx-1+2]==True :
            AIWin(screen)
            return True 
        hIdx-=3    
    
    # 플레이어 대각선 확인
    if playerPut[7-1]==True and playerPut[5-1]==True and playerPut[3-1]==True :
        playerWin(screen)
        return True 
    elif playerPut[9-1]==True and playerPut[5-1]==True and playerPut[1-1]==True :
        playerWin(screen)
        return True

    # AI 대각선 확인
    if AIPut[7-1]==True and AIPut[5-1]==True and AIPut[3-1]==True :
        AIWin(screen)
        return True 
    elif AIPut[9-1]==True and AIPut[5-1]==True and AIPut[1-1]==True :
        AIWin(screen)
        return True

    # 무승부 확인
    for i in range(0,9):
        if screen[i]=='':
            break
        elif i==8:
            draw(screen) 
            return True

def playerWin(screen):
    drawingBoard(gameScreen) # 보드 그리기
    print("플레이어가 이겼습니다.!!")
    sys.exit()
    
def AIWin(screen):
    drawingBoard(gameScreen) # 보드 그리기
    print("AI가 이겼습니다.!!")
    sys.exit()
    
def draw(screen):
    drawingBoard(gameScreen) # 보드 그리기
    print("무승부입니다.!!")
    sys.exit()
    
# 메인
if __name__ == "__main__": 
    while True:
        gameScreen = ['', '', '', '', '' ,'' ,'' ,'', ''] 
        player, AI = choosePlayer() # 게임순서 결정하기
        drawingBoard(gameScreen) # 보드 그리기
 
        if player =='O': # AI가 선공을 하는 경우
            while True:
                putAIStone(gameScreen, player, AI) # AI 플레이
                checkWinner(gameScreen, player, AI) #승패결정
                drawingBoard(gameScreen) #보드 그리기                
 
                gameScreen = putPlayerStone(gameScreen, player) #먼저 수를 놓는다.
                checkWinner(gameScreen,player,AI) #승패결정
                drawingBoard(gameScreen) # 보드 그리기
 
        if player =='X': # 플레이어가 선공을 하는 경우
            while True: #사용자 플레이
                gameScreen = putPlayerStone(gameScreen, player) #먼저 수를 놓는다.
                checkWinner(gameScreen,player,AI) #승패결정
                drawingBoard(gameScreen) # 보드 그리기
                
                putAIStone(gameScreen, player, AI) # AI 플레이
                checkWinner(gameScreen, player, AI) #승패결정
                drawingBoard(gameScreen) #보드 그리기