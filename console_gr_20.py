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
    Returns
    -------
    wall: the list of the position of all walls(list)
    player: the list of the position of the player(list)
    cat: the list of the position of the cat(list)
    """
    #wall coordonate virtual
    wall = [[1,1],[2,1],[3,1],[7,1],[2,3],[2,4],[5,3],[6,3],[7,3],[8,3],[1,7],[1,8],[5,6],[6,6],[7,6],[6,7],[6,8],[6,9],[9,8],[9,9]]
    player = []
    cat = []
    while player in wall:
        player = [randint(0,size), randint(0,size)]
    while cat in wall and cat in player:
        cat = [randint(0,size), randint(0,size)]
          
    return wall, player, cat
def get_local_view(wall, player, cat):
    """get local view for the gamepad 5 x 5 view of the player

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
    return map
#settings
group_id = 20
size = 10

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
    
    #wait until gamepad send an order
    order = get_message()
    #execute order (move player)
    
    #send local view of the board to gamepad
    local_view=get_local_view(wall, player, cat)
    radio.send(local_view)
    
    #check if game is over
    game_is_over=True
    
    if not game_is_over:
        #wait a few secondes and clear screen
        microbit.sleep(2000)
        microbit.display.clear()
        
        #update position of the cat
        
#tell that the game is over
microbit.display.scroll("Vous avez gagné !!! :D", delay=100)
