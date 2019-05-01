
# No assert

class default:
    THRESHOLD = 1
    ENENERGY = 2
    INENERGY = -3
    K_ADD = 2

NEURONTYPEEN = 0
NEURONTYPEIN = 1

class Neuron:
    class Connect:
        def __init__(self,k,t,to):
            self.k = k
            self.t = t
            self.to = to
            self.actpacks = []
            self.backpacks = []

        def tick(self):
            for actpack in self.actpacks:
                actpack.left_t -= 1
                if actpack.left_t <= 0:
                    self.to.receiveact(self,actpack)
            for backpack in self.backpacks:
                backpack.left_t -= 1
                if backpack.left_t <= 0:
                    self.to.receiveback(self,backpacks)


    class ActPack:
        def __init__(self,add_value,left_t):
            self.add_value = add_value
            self.left_t = left_t


    class BackPack:
        def __init__(self,left_t):      # 这里后端神经元不影响权值变化
            self.left_t = left_t


    def __init__(self,neurontype):
        self.type = neurontype
        self.value = False
        self._ = 0  # 没办法……
        self.connects = []

        self.THRESHOLD = default.THRESHOLD
        self.ENERGY = {NEURONTYPEEN:default.ENENERGY, NEURONTYPEIN:default.INENERGY}[neurontype]
        self.K_ADD = default.K_ADD

    def sendact(self):
        _sum_k = sum([connect.k**2 for connect in self.to])     # 【增加较大权值的作用】
        for connect in self.connects:
            add_value = self.ENERGY*(connect.k**2/_sum_k)
            connect.sendpacks.append(Neuron.ActPack(add_value,connect.t))

    def receiveact(self,connect,pack):
        self._ += pack.add_value

    def sendback(self):
        for connect in self.connects:
            connect.backpacks.append(Neuron.BackPack(connect.t))

    def receiveback(self,connect,pack):
        if self.value:
            connect.k += k_ADD


def EN():return Neuron(NEURONTYPEEN)
def IN():return Neuron(NEURONTYPEIN)

class Group:
    def __init__(self,neurons):
        self.neurons = neurons

    def evo(self):
        for neuron in self.neurons:
            if neuron.value == True:
                neuron.sendact()
            for connect in neuron.connects:
                connect.tick()
        for neuron in self.neurons:
            neuron.value = neuron._ >= neuron.THRESHOLD
            neuron._ = 0





