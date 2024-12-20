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
                microbit.display.set_pixel(x, y, 2)
            elif game_map[x][y]=="p":
                microbit.display.set_pixel(x, y, 7)
            elif game_map[x][y]=="c":
                microbit.display.set_pixel(x, y, 9)
def get_direction():
    """return the direction of the gamepad
    Returns
    -------
    direction: direction up, down, left, right (str)
    """
    x_strength = microbit.accelerometer.get_x()
    y_strength = microbit.accelerometer.get_y()
    deadzone=100   # to only capture the player's intentional movements.
    direction=str()
    if abs(x_strength)>deadzone or abs(y_strength)>deadzone:
        if abs(x_strength)>abs(y_strength):
            if x_strength>0:
                direction="right"
            else:
                direction="left"
        else:
            if y_strength>0:
                direction="up"
            else:  
                direction="down"
    if direction == str():
        direction="none"
    return direction
                
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
    radio.send(get_direction())
