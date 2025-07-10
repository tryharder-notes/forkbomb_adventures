import pwn

def concat_set(check_cards):
    
    _set = [[], [], [], []] #0 - h, 1 - s, 2 - d, 3 - c
    
    for i in range(0, len(check_cards), 2):
            
        if check_cards[i + 1] == 'h':
            
            _set[0].append(int(check_cards[i]))
            
        elif check_cards[i + 1] == 's':
            
            _set[1].append(int(check_cards[i]))
            
        elif check_cards[i + 1] == 'd':
            
            _set[2].append(int(check_cards[i]))
            
        elif check_cards[i + 1] == 'c':
            
            _set[3].append(int(check_cards[i]))
            
    return _set
    
    
def concat_rank(check_cards):
    
    ranks = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    
    for i in range(0, len(check_cards), 2):
        
        ranks[int(check_cards[i]) - 1].append(int(check_cards[i]))
    
    return ranks


def royal_flush(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    _set = concat_set(check_cards)
            
    for i in range(len(_set)):
        
        if set(_set[i]) == {10, 11, 12, 13, 14}:
            
            print(f'{name}: Royal Flush (8)')
            
            return True
            
    return False
    
    
def straight_flush(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    _set = concat_set(check_cards)
    
    for i in range(len(_set)):
        
        count = 1
        
        _set[i] = sorted(_set[i])
        
        i1 = 0
        
        while True:
            
            if len(_set[i]) > 0:
            
                if _set[i].count(_set[i][i1]) > 1:
                    
                    _set[i].remove(_set[i][i1])
                
            i1 = i1 + 1
    
            if i1 >= len(_set[i]):
                break
        
        for i1 in range(len(_set[i]) - 1):
            
            if int(_set[i][i1 + 1]) - int(_set[i][i1]) == 1:
                
                count = count + 1
                
            else:
                
                count = 1
                
            if count == 5:
                
                print(f'{name}: Straight Flush (7)')
            
                return True
            
    return False
        
        
def quads(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    ranks = concat_rank(check_cards)
    
    for i in range(len(ranks)):
        
        if len(ranks[i]) >= 4:
            
            print(f'{name}: Quads (6)')
            
            return True
            
    return False
    
    
def full_house(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    ranks = concat_rank(check_cards)
    
    set = 0
    
    pair = 0
    
    for i in range(len(ranks)):
        
        if len(ranks[i]) == 3:
            
            set = 1
            
        if len(ranks[i]) == 2:
            
            pair = 1
            
    if set == 1 and pair == 1:
        
        print(f'{name}: Full House (5)')
        
        return True
        
    else:
        
        return False

    
def flush(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    _set = concat_set(check_cards)
    
    for i in range(len(_set)):
        
        if len(_set[i]) == 5:
            
            print(f'{name}: Flush (4)')
            
            return True
            
    return False
    
def straight(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    for i in range(0, len(check_cards), 2):
        
        combo.append(int(check_cards[i]))
        
    combo = sorted(combo)
        
    count = 1
        
    i = 0
        
    while True:
            
        if combo.count(combo[i]) > 1:    
            combo.remove(combo[i])
                
        i = i + 1
    
        if i >= len(combo):
            break
        
    for i in range(len(combo) - 1):
            
        if int(combo[i + 1]) - int(combo[i]) == 1:
                
            count = count + 1
                
        else:
                
            count = 1
                
        if count == 5:
            
            print(f'{name}: Straight (3)')
            
            return True
            
    return False
    
def three_of_a_kind(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    ranks = concat_rank(check_cards)
    
    for i in range(len(ranks)):
        
        if len(ranks[i]) == 3:
            
            print(f'{name}: Three of a kind (2)')
            
            return True
            
    return False
    
def two_pairs(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    ranks = concat_rank(check_cards)
    
    pairs_count = 0
    
    for i in range(len(ranks)):
        
        if len(ranks[i]) >= 2:
            
            pairs_count = pairs_count + 1
            
    if pairs_count == 2:
        
        print(f'{name}: Two pairs (1)')
        
        return True
        
    else:
        
        return False
    
def one_pair(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    ranks = concat_rank(check_cards)
    
    pairs_count = 0
    
    for i in range(len(ranks)):
        
        if len(ranks[i]) == 2:
            
            pairs_count = pairs_count + 1
            
    if pairs_count == 1:
        
        print(f'{name}: One Pair(0)')
        
        return True
        
    else:
        
        return False
    
def high_card(name, player_cards, table_cards):
    
    check_cards = table_cards + player_cards
    
    combo = list()
    
    _set = concat_set(check_cards)
    

def check_combo(name, player_cards, table_cards):
    
    points = 0
    
    if straight_flush(name, player_cards, table_cards) == True:
        
        points = 9
        return points
    
    elif royal_flush(name, player_cards, table_cards) == True:
        
        points = 8
        return points
    
    elif quads(name, player_cards, table_cards) == True:
        
        points = 7
        return points
    
    elif full_house(name, player_cards, table_cards) == True:
        
        points = 6
        return points
    
    elif flush(name, player_cards, table_cards) == True:
        
        points = 5
        return points
    
    elif straight(name, player_cards, table_cards) == True:
        
        points = 4
        return points
    
    elif three_of_a_kind(name, player_cards, table_cards) == True:
        
        points = 3
        return points
    
    elif two_pairs(name, player_cards, table_cards) == True:
        
        points = 2
        return points
    
    elif one_pair(name, player_cards, table_cards) == True:
        
        points = 1
        return points
        
    else:
        
        points = 0
        return points

    

def main():
    
    
    r = pwn.remote('109.233.56.90', 11546)
    
    r.sendline('CLIENT_HELLO')
    
    print(r.recvline().decode().strip())
    
    flag = 0
    
    while True:
        
        r.sendline('START_GAME')
        
        print(r.recvline().decode().strip())
        print(r.recvline().decode().strip())
        print(r.recvline().decode().strip())
        print(r.recvline().decode().strip())
        
        if flag == 1:
            break
        turn = 1
        
        while True:
    
            r.sendline('GET_GAME_STATE')
            
            state = r.recvline().decode().strip()
            
            cards = state.split(' ')
            print(cards)
            
            if cards[-2] == '0' and cards[-3] == '0':
                break
            
            balance = int(cards[-7])
                        
            cards = ' '.join(cards[2:-7])
            
            cards = cards.split(' ')
            
            my_cards = cards[0:4]
            bot_1_cards = cards[4:8]
            bot_2_cards = cards[8:12]
            table_cards = cards[12:]
            
            #print(f'My cards: {my_cards}')
            #print(f'Bot 1 cards: {bot_1_cards}')
            #print(f'Bot 2 cards: {bot_2_cards}')
            #print(f'Table cards: {table_cards}')
            
            my_points = check_combo('You', my_cards, table_cards)
            bot_1_points = check_combo('Bot 1', bot_1_cards, table_cards)
            bot_2_points = check_combo('Bot 2', bot_2_cards, table_cards)
            
            if turn != 3:
            
                if my_points > bot_1_points and my_points > bot_2_points:
                    
                    r.sendline('BET 1')
                    
                    while True:
                        line = r.recvline(timeout=2).decode().strip()
                        print(line)
                        
                        if not line:
                            break

                    
                else:
                    
                    r.sendline('BET 0')
                    while True:
                        line = r.recvline(timeout=2).decode().strip()
                        print(line)
                        
                        if not line:
                            break
                    
            else:
                
                if my_points > bot_1_points and my_points > bot_2_points:
                    
                    r.sendline('BET 1')
                    
                    while True:
                        line = r.recvline(timeout=2).decode().strip()
                        print(line)
                        
                        if not line:
                            break

                    
                else:
                    
                    
                    r.sendline('BET 0')
                    while True:
                        line = r.recvline(timeout=2).decode().strip()
                        print(line)
                        
                        if not line:
                            break
            
            if turn >= 3:
                
                break
                
            if balance > 500:
            
                r.sendline('GET_FLAG')
                print(r.recvline().decode().strip())
                r.sendline('BYE BYE')
                flag = 1
                break
            
            turn = turn + 1
            
        
    
    
if __name__ == "__main__":
    main()
    
    
