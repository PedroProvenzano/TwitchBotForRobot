from twitchio.ext import commands
from pyfirmata import Arduino, util, SERVO, STRING_DATA
from time import sleep
from dotenv import load_dotenv
load_dotenv()    
import os
board = Arduino('COM3')
sleep(5)
board.digital[3].mode = SERVO


def servo(posicion1, posicion2):
    board.digital[3].write(posicion1)
    sleep(1)
    board.digital[3].write(posicion2)
def wake_up():
    #para prender el led write 1 y para apagar 0
    board.digital[11].write(1)
    board.digital[12].write(1)
    sleep(1)
    board.digital[11].write(0)
    board.digital[12].write(0)
    sleep(1)
    board.digital[11].write(1)
    board.digital[12].write(1)
def go_to_sleep():
    board.digital[11].write(0)
    board.digital[12].write(0)
def speak(text):
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(text))
def sound(note):
    if len(note) == 3:
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("8"+note+"f"))
    else:
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("8"+note))
wake_up()



class Bot(commands.Bot):  

    isMuted = False
    isSleeping = False

    def __init__(self):
        super().__init__(irc_token=os.getenv("IRC_TOKEN"), client_id=os.getenv("CLIENT_ID"), nick=os.getenv("NICK"), prefix='!',
                         initial_channels=[os.getenv("INITIAL_CHANNELS")])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    # Commands use a decorator...
    @commands.command(name='hola')
    async def my_command(self, ctx):
        servo(150, 0)
        if not self.isMuted:
            sound("740f")
            sound("784f")
        speak('Hola,')
        speak(f'     {ctx.author.name}!')
        sleep(10)
        speak("...")
        speak(" ")
    
    @commands.command(name='dormite')
    async def sleep_command(self, ctx):
        if not self.isSleeping:
            speak('Buenas noches..')
            speak(" ")
            self.isSleeping = True
            if not self.isMuted:
                sound("523f")
                sleep(0.5)
                sound("349f")
            sleep(3)
            go_to_sleep()
            speak('Zzz...')
            speak(" ")
        else:
            speak("Ya estoy")
            speak("durmiendo...")
            sleep(10)
            speak('Zzz...')
            speak(" ")
    
    @commands.command(name='despertate')
    async def wake_up_command(self, ctx):
        if self.isSleeping:
            wake_up()
            speak(f'Buenos dias..')
            speak(" ")
            self.isSleeping = False
            if not self.isMuted:
                sound("349f")
                sound("523f")
        else:
            speak("No estoy")
            speak("durmiendo...")
            sleep(10)
            speak("...")
            speak(" ")

    @commands.command(name='mute')
    async def mute(self, ctx):
        if ctx.author.is_mod and not self.isMuted:
            self.isMuted = True
        elif ctx.author.is_mod and self.isMuted:
            self.isMuted = False

bot = Bot()
bot.run()