from gettext import install
import numpy as np

input_layer_size = 784 #input of a 28x28 grid

layer2_size = 128 #second layer has 128 neurons, can change

layer3_size = 128

output_layer_size = 36 #outputs a number or character

input_neurons = []

layer2_neurons = []

layer1to2connections = []

layer3_neurons = []

layer2to3connections = []

output_layer_neurons = []

layer3to_output_connections = []

class neuron:
    def __init__(self, val):
        self.val = val

    def set_val(self, new_val):
        self.val = new_val

class connection: #connection has a weight, bias, and is connected to 2 neurons
    def __init__(self, weight, bias, neuron_in, neuron_out):
        self.weight = weight
        self.bias = bias
        self.neuron_in = neuron_in
        self.neuron_out = neuron_out

    def set_weight(self, new_weight):
        self.weight = new_weight

    def set_bias(self, new_bias):
        self.bias = new_bias

for i in range(input_layer_size):
    instance = neuron(0)
    input_neurons.append(instance)

for i in range(layer2_size):
    instance = neuron(0)
    layer2_neurons.append(instance)

for neuron_in in input_neurons:
    for neuron_out in layer2_neurons:
        instance = connection(np.random.uniform(-0.01, 0.01), np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
        layer1to2connections.append(instance)

for i in range(layer3_size):
    instance = neuron(0)
    layer3_neurons.append(instance)

for neuron_in in layer2_neurons:
    for neuron_out in layer3_neurons:
        instance = connection(np.random.uniform(-0.01, 0.01), np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
        layer2to3connections.append(instance)

for i in range(output_layer_size):
    instance = neuron(0)
    output_layer_neurons.append(instance)

for neuron_in in layer3_neurons:
    for neuron_out in output_layer_neurons:
        instance = connection(np.random.uniform(-0.01, 0.01), np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
        layer3to_output_connections.append(instance)

neurons = [input_neurons, layer2_neurons, layer3_neurons, output_layer_neurons]

connections = [layer1to2connections, layer2to3connections, layer3to_output_connections]

for layer in neurons:
    for neuron in layer:
        print(neuron.val)
