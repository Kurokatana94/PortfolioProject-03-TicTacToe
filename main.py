from random import *
import copy

isRunning = True

paper = [[' ',' ',' '],
         [' ',' ',' '],
         [' ',' ',' ']]

#ai logical functions
def random_move(s, session) -> list:
    placed = False
    while not placed:
        cord = (randint(0,2), randint(0,2))
        if session[cord[0]][cord[1]] == ' ':
            session[cord[0]][cord[1]] = s
            placed = True
    return session

def winning_move(s, session):
    if all(' ' == spot for row in session for spot in row):
        return False, None
    for row in session:
        if row.count(s) == 2:
            try:
                row[row.index(' ')] = s
                return True, session
            except ValueError:
                pass
    for c in range(len(session[0])):
        n = 0
        free_cord = None
        for row in session:
            if row[c] == s:
                n+=1
            if row[c] == ' ':
                free_cord = [session.index(row), c]
            if n == 2 and free_cord is not None:
                session[free_cord[0]][free_cord[1]] = s
                return True, session
    if session[1][1] == s:
        corners = [(0,0,2,2),(2,2,0,0),(0,2,2,0),(2,0,0,2)]
        for y1, x1, y2, x2 in corners:
            if session[y1][x1] == s:
                if session[y2][x2] == ' ':
                    session[y2][x2] = s
                    return True, session
    return False, None

def defensive_move(s, opp_s, session) -> tuple:
    if all(' ' == spot for row in session for spot in row):
        return False, None
    for row in session:
        if row.count(opp_s[s]) == 2:
            try:
                row[row.index(' ')] = s
                return True, session
            except ValueError:
                pass
    for c in range(len(session[0])):
        n = 0
        free_cord = None
        for row in session:
            if row[c] == opp_s[s]:
                n+=1
            if row[c] == ' ':
                free_cord = [session.index(row), c]
            if n == 2 and free_cord is not None:
                session[free_cord[0]][free_cord[1]] = s
                return True, session
    if session[1][1] == opp_s[s]:
        corners = [(0,0,2,2),(2,2,0,0),(0,2,2,0),(2,0,0,2)]
        for y1, x1, y2, x2 in corners:
            if session[y1][x1] == opp_s[s]:
                if session[y2][x2] == ' ':
                    session[y2][x2] = s
                    return True, session
    return False, None

def offensive_move(s, opp_s, session) -> tuple:
    if session[1][1] == ' ':
        session[1][1] = s
        return True, session
    for row in session[0:3:2]:
        if row[0] == ' ':
            session[session.index(row)][0] = s
            return True, session
        elif row[2] == ' ':
            session[session.index(row)][2] = s
            return True, session
    return False, None

def ai_turn(s: str, session: list):
    opponent_s = {'x': 'o', 'o': 'x'}
    paper_visual(session)
    print('ai')
    turn_move = winning_move(s, session)
    if turn_move[0]:
        print('winning')
        return turn_move[1]
    turn_move = defensive_move(s, opponent_s, session)
    if turn_move[0]:
        print('defense')
        return turn_move[1]
    turn_move = offensive_move(s, opponent_s, session)
    if turn_move[0]:
        print('offense')
        return turn_move[1]
    print('random')
    return random_move(s, session)

def paper_visual(session: list):
    print(f"  1 2 3 \n"
          f"1 {session[0][0].upper()}|{session[0][1].upper()}|{session[0][2].upper()} \n"
          f" -------\n"
          f"2 {session[1][0].upper()}|{session[1][1].upper()}|{session[1][2].upper()} \n"
          f" -------\n"
          f"3 {session[2][0].upper()}|{session[2][1].upper()}|{session[2][2].upper()} \n")

# 's' stands for symbol
def p_turn(s: str, session: list):
    while True:
        paper_visual(session)
        try:
            cords = [int(cor.strip())-1 for cor in ''.join(input(f'Player {s.upper()}\n'
                                                                 f'Please input the y x coordinates, as digits, of your next move:\n').split())]
            print(cords)
            if len(cords) == 2 and all(0 <= n <= 2 for n in cords):
                if session[cords[0]][cords[1]] == ' ':
                    session[cords[0]][cords[1]] = s
                    return session
                print("The selected location wasn't empty")
            print('Please try again')
        except ValueError:
            print('Please type only digits')

#All this could be done using range(3) or checking the 3 columns/rows, but I like to practice for possibles future larger projects. Diagonals thou, have to be more hard-coded
#Returns bool True if GameOver, False if not. Returns winner symbol if there's a winner or None if draw
def check_if_over(session: list) -> tuple:
    for row in session:
        if all(s == row[0] and s != ' ' for s in row):
            return True, row[0]
    for c in range(len(session[0])):
        if all(session[0][c] == row[c] and row[c] != ' ' for row in session):
            return True, session[0][c]
    if all(session[1][1] == s and s != ' ' for s in [session[0][0], session[2][2]]) or \
       all(session[1][1] == s and s != ' ' for s in [session[0][2], session[2][0]]):
        return True, session[1][1]
    if all(' ' not in row for row in session):
        return True, None
    return False, None

def game(mode):
    game_session = copy.deepcopy(paper)
    game_over = False
    player_symbol = None
    while not game_over:
        if not player_symbol:
            player_symbol = input('Do you want to play with X or O?\n').lower()
        if player_symbol == 'x':
            game_session = p_turn('x', game_session)
            #Checks if game is over before the second player tries a move
            if not check_if_over(game_session)[0]:
                if mode == '1':
                    game_session = ai_turn('o', game_session)
                else:
                    game_session = p_turn('o', game_session)
        elif player_symbol == 'o':
            if mode == '1':
                game_session = ai_turn('x', game_session)
            else:
                game_session = p_turn('x', game_session)
            #Checks if game is over before the second player tries a move
            if not check_if_over(game_session)[0]:
                game_session = p_turn('o', game_session)
        else:
            player_symbol = None
            print('Wrong input, try again.')

        #Checking winning condition
        game_result = check_if_over(game_session)
        if game_result[0]:
            if game_result[1] is not None:
                paper_visual(game_session)
                print(f'Game Over!\n'
                      f'The Winner is Player {game_result[1].upper()}')
            else:
                paper_visual(game_session)
                print('Game Over!\n'
                      'It\'s a draw!')
            game_over = True
            input('Press enter to continue...')

while isRunning:
    game_mode = input("Type \'1\' if you want to play solo-mode\n"
                    "Type \'2\' if you want to play duo-mode\n"
                    "Type \'0\' to exit\n")
    if game_mode == '1' or game_mode == '2':
        game(game_mode)
        [print('\n') for _ in range(20)]
    elif game_mode == '0':
        isRunning = False
        break
    else:
        print("The wrong command was typed, please try again")