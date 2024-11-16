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

#settings
group_id = 20
size = 10

#setup radio to receive/send messages
radio.on()
radio.config(group=group_id)

#create board an place cat + player

#send local view of the board to gamepad
local_view="test"
radio.send(local_view)

#loop until game is over
game_is_over = False
while not game_is_over:
    #show hint
    
    #wait until gamepad send an order
    order = get_message()
    #execute order (move player)
    
    #send local view of the board to gamepad
    local_view="test"
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