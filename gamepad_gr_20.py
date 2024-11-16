import radio
import microbit

# definition of functions
def get_message() -> str:
    """Wait and return a message from another micro bit
    
    Returns
    -------
    message: message sent by another micro bit(str)
    """
    message = None
    while message==None:
        microbit.sleep(250)
        message = radio.receive()
    return message

def show_map(local_view):
    """show the map on the gamepad
    """
    game_map = []#conversion de la map 
    for i in range(5):
        temp = []
        for j in range(5):
            temp.append(local_view[i*5+j])
        game_map.append(temp)
    for x in range(5):#affichage de la map 
        for y in range(5):
            if game_map[x][y]=="w":
                microbit.display.set_pixel(x, y, 3)
            elif game_map[x][y]=="p":
                microbit.display.set_pixel(x, y, 9)
            elif game_map[x][y]=="c":
                microbit.display.set_pixel(x, y, 9)
                
#settings
group_id = 20

#setup radio to receive/send messages
radio.on()
radio.config(group = group_id)

#loop forever (until micro bit is switched off)
while True:
    #get local view of the board
    local_view = get_message()

    #clear screen
    microbit.display.clear()

    #show local view of the board
    show_map(local_view)

    #wait for button A to be pressed 
    while not microbit.button_a.is_pressed():
        microbit.sleep(50)

    #send current direction
    
    x_strength = accelerometer.get_x()
    y_strength = accelerometer.get_y()
    
    if abs(x_strength)-1000>abs(y_strength)-1000:
        if x_strength>-1000:
            direction="up"
        else:
            direction="down"
    else:
        if y_strength>-1000:
            direction="right"
        else:  
            direction="left"
    radio.send(direction)
