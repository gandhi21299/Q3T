from operator import xor
import subprocess
import os
import threading
import time

class Server:
    def __init__(self, state0):
        self.state = '1'
        self.gameState = state0

    def update(self, action):
        '''
        args: action must be in (0,1,2)
        '''
        if action not in (0,1,2):
            return

        if action == 0:
            self.gameState = xor(self.gameState, 3)
        elif action == 1:
            self.gameState = xor(self.gameState, 7)
        elif action == 2:
            self.gameState = xor(self.gameState, 6)

    def __str__(self):
        binStr = ''
        val = self.gameState
        while val:
            binStr = str(val%2) + binStr
            val //= 2

        while len(binStr) < 3:
            binStr = '0'+binStr
        return binStr

# def prog1():
#     print('Running prog1()...')
#     os.chdir('/home/gandhi56/Desktop/prog1/')
#     cmd = './player'
#     subprocess.Popen(cmd, shell=True)

# def prog2():
#     print('Running prog2()...')
#     os.chdir('/home/gandhi56/Desktop/prog2/')
#     cmd = './player'
#     subprocess.Popen(cmd, shell=True)

if __name__ == '__main__':
    
    # multithreading implementation
    threadLock = threading.Lock()

    try:
        t1 = myThread(1, 'thread1', 1)
        t2 = myThread(1, 'thread2', 2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    except:
        print('threads failed to start.')

    while 1:
        pass
    
    # server = Server(0)
    # while True:
    #     move = input('> ')
    #     if move in '012':
    #         move = int(move)
    #     else:
    #         move = random.choose([0,1,2])
    #     server.update(move)

    #     print('State:'+str(server))