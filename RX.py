import pyb

lens = [0,0,0,0,0,0]
ch_up = [0,0,0,0,0,0]
ch_up_set = [0,0,0,0,0,0]
ch_pin = ( pyb.Pin.board.Y5,pyb.Pin.board.Y6,pyb.Pin.board.Y7,pyb.Pin.board.Y8  )


#ch_min = [ 1000,1000,1000,1000,1000,1000 ]
#ch_max = [ 2000,2000,2000,2000,2000,2000 ]
ch_min = 1050
ch_max = 1880

des_min = [ -45,0,-45,-45,0,0 ]
des_max = [ 45,180,45,45,1,1 ]
ch_des = [0.,0.,0.,0.,0.,0.]
fresh = False

def init():
    pyb.ExtInt( pyb.Pin.board.Y5, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, intCH1)
    pyb.ExtInt( pyb.Pin.board.Y6, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, intCH2)
    pyb.ExtInt( pyb.Pin.board.Y7, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, intCH3)
    pyb.ExtInt( pyb.Pin.board.Y8, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, intCH4)

def test():
    while True:
        #print('tick')
        print_rx()
        pyb.delay(500)


def intCH1(line):
    global ch_up
    ch_up[0] = pyb.micros()

def intCH2(line):
    global ch_up
    ch_up[1] = pyb.micros()

def intCH3(line):
    global ch_up,lens,ch_des
    ch_up[2] = pyb.micros()

def intCH4(line):
    global ch_up,ch_up_set,fresh
    if pin( ch_pin[3]  ):
        ch_up[3] = pyb.micros()
    else:
        ch_up[4] = pyb.micros()
        for i in range(5):
            ch_up_set[i] = ch_up[i]
        fresh = True

def get_rx():
    global fresh
    if fresh:
        calc_rx()
        fresh = False
    else:
        print('not fresh')
    return ch_des

def print_rx():
    for v in get_rx()[:-2]:
        print("%.2f" % v, end=' ')
    print()

def calc_rx():
    global fresh
    for i in range(4):
        lens[i] = ch_up_set[i + 1] - ch_up_set[i]
        #print(lens[i],end=' ')
    #print()

    for i in range(4):
        ch_des[i] = (lens[i]-ch_min) * ( des_max[i] - des_min[i] ) / (ch_max - ch_min) + des_min[i]

    fresh = False

def pin(board):
    return pyb.Pin(board).value()

init()

if __name__ == '__main__':
    test()