from operator import xor

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

class Player:
    def __init__(self):
        pass

if __name__ == '__main__':
    
    server = Server(0)
    while True:
        move = input('> ')
        if move in '012':
            move = int(move)
        else:
            move = random.choose([0,1,2])
        server.update(move)

        print('State:'+str(server))