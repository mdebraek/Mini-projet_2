import math
import random

import radio
import microbit

#definitions of functions
def get_message() -> str:
    """Wait and return a message from another micro bit
    
    Returns
    -------
    messages: message sent by another micro bit(str)
    """
    message=None
    while message == None:
        microbit.sleep(250)
        message=radio.receive()
        
    return message
def generate_board(size):
    """ generate the map, the wall, the position of the pkayer and the cat
    Parameters
    ----------
    size: size of the board (int)
    
    Returns
    -------
    wall: the list of the position of all walls(list)
    player: the list of the position of the player(list)
    cat: the list of the position of the cat(list)
    """
    #wall coordonate virtual
    wall = [[1,1],[2,1],[3,1],[7,1],[2,3],[2,4],[5,3],[6,3],[7,3],[8,3],[1,7],[1,8],[5,6],[6,6],[7,6],[6,7],[6,8],[6,9],[9,8],[9,9]]
    player = [1, 1]
    cat = [1, 1]
    while player in wall:
        player = [random.randint(0,size-1), random.randint(0,size-1)]
    while cat in wall and cat in player:
        cat = [random.randint(0,size-1), random.randint(0,size-1)]  
    return wall, player, cat
def get_local_view(wall, player, cat):
    """get local view for the gamepad 5 x 5 view of the player
    Parameters
    ----------
    wall: list of all walls position (list)
    player: list of the position x y of the player (list)
    cat: list of the position x y of the cat (list)

    Returns
    -------
    map: 25 letters for the 5 x 5 map (w for wall, p for player, c for cat, v for void)(str)
    """
    map=str()
    for x in range(player[0]-2, player[0]+3):
        for y in range(player[1]-2, player[1]+3):
            if [x, y] in wall:
                map+="w"
            elif [x, y] in player:
                map+="p"
            elif [x, y] in cat:
                map+="c"
            else:
                map+="v"
    print(map)
    return map
def move_cat(cat: list, wall: list):
    """Make the cat move
    Parameters
    ----------
    cat : the position x y of the cat(list)
    wall : the position x y of all walls on the map(list)
    
    Return
    ------
    Result: the result is that the cat moved.
    The cat can moved up,down,right,left or not moved
    """
    number = random.randint(1,5)
    if number == 1 and not [cat[0], cat[1]+1] in wall:
        cat[1]+1 #up
    elif number ==2 and not [cat[0], cat[1]-1] in wall:
        cat[1] -1 #down
    elif number == 3 and not [cat[0]+1, cat[1]] in wall:
        cat[0] +1 #right
    elif number == 4 and not [cat[0], cat[0]-1] in wall:
        cat[0] -1 #left
    return cat
    
def cat_hint(player, cat):
  """
  This function show a arrow on the console screen depending on the position of the player and the wherethe cat is in function of the player.
  Parameters
  ----------
  player:the position x y of the cat (list)
  cat: the position x y of the cat (list)
  Returns
  -------
  Return: the result is an arrow which is print on the screen of the console
  """
  microbit.display.clear()
  if player[1]==cat[1]:
      if cat[0] > player[0]: #show east
        microbit.display.show(microbit.Image.ARROW_E)
      else:
        #show west
        microbit.display.show(microbit.Image.ARROW_W)
  elif cat[0]==player[0]:
      if cat[1]> player[1]: #show north
        microbit.display.show(microbit.Image.ARROW_N)
      else:
        #show south
        microbit.display.show(microbit.Image.ARROW_S)
  elif cat[0]>player[0] and cat[1]>player[1]:
       microbit.display.show(microbit.Image.ARROW_SE)
  elif cat[0]<player[0] and cat[1]>player[1]:
      microbit.display.show(microbit.Image.ARROW_SW)
  elif cat[0]>player[0] and cat[1]<player[1]:
      microbit.display.show(microbit.Image.ARROW_NE)
  else:
      microbit.display.show(microbit.Image.ARROW_NW)
      
def move_player(order: str, player: list, wall: list, size: int):
    """Make the player move
    Parameters
    ----------
    order: the direction send (str)
    player : the position x y of the player (list)
    wall : the position x y of all wall on the map (list)
    size : size of the map(int)
    
    Return
    ------
    Result: the result is that the player moved.
    The player can moved up, down, left, right or not moved
    check if the player have the right to move (no wall, still in map)
    return the new position of the player
    """
    if order == "left" and [player[0]-1, player[1]] not in wall and player[0]-1>=0:
        player[0] -=1
    elif order ==  "right" and [player[0]+1, player[1]] not in wall and player[0]+1<size:
        player[0] +=1
    elif order == "up" and [player[0], player[1]+1] not in wall and player[1]+1<size:
        player[1] +=1           
    elif order == "down" and [player[0], player[1]-1] not in wall and player[1]-1>=0:
        player[1] -=1
    return player
def check_win(player, cat):
    """Check if the player win
    Parameters
    ----------
    player: the position x y of the player (list)
    cat: the position x y of the cat (list)
    
    Return
    ------
    Result: the result is that the player win or not
    """
    if player == cat:
        return True
    else:
        return False
#settings
group_id = int(20)
size = int(10)

#setup radio to receive/send messages
radio.on()
radio.config(group=group_id)

#create board an place cat + player
wall, player, cat = generate_board(size)

#send local view of the board to gamepad
local_view=get_local_view(wall, player, cat)
radio.send(local_view)

#loop until game is over
game_is_over = False
while not game_is_over:
    #show hint
    cat_hint(player, cat)
    
    #wait until gamepad send an order
    order = get_message()
    #execute order (move player)
    player = move_player(order, player, wall, size)
    
    #send local view of the board to gamepad
    local_view=get_local_view(wall, player, cat)
    radio.send(local_view)
    
    #check if game is over
    game_is_over = check_win(player, cat)
    
    if not game_is_over:
        #wait a few secondes and clear screen
        microbit.sleep(2000)
        microbit.display.clear()
        
        #update position of the cat
        cat = move_cat(cat, wall)
        
#tell that the game is over
microbit.display.scroll("You win !!! :D", delay=100)
