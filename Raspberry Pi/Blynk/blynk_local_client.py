import blynklib
import random

BLYNK_AUTH = 'AoQoa96Q5BolVXfrlreEnfbe8VdlDx-6'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"


# register handler for virtual pin V11 reading
@blynk.handle_event('read V1')
def read_virtual_pin_handler(pin):
    print(READ_PRINT_MSG.format(pin))
    blynk.virtual_write(pin, random.randint(0, 40))


###########################################################
# infinite loop that waits for event
###########################################################
if __name__ == "__main__":
	while True:
		blynk.run()