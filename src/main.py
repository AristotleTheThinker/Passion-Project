import numpy as np
from scipy.io import loadmat
import os
import matplotlib.pyplot as plt
import time

def input_sigmoid(x):
    if x > 128:
        return 1
    else:
        return 0

current_dir = os.path.dirname(__file__)  # Src/
mat_path = os.path.join(current_dir, '../Data/matlab/emnist-letters.mat')

digits_mat = loadmat(mat_path)

data = digits_mat['dataset']

# Training data
train_images = data['train'][0, 0]['images'][0, 0]
train_labels = data['train'][0, 0]['labels'][0, 0]

# Testing data
test_images = data['test'][0, 0]['images'][0, 0]
test_labels = data['test'][0, 0]['labels'][0, 0]

# Reshape images to 28x28
train_images = train_images.reshape((-1, 28, 28)).astype(np.uint8)
test_images = test_images.reshape((-1, 28, 28)).astype(np.uint8)

#Rotate the images
train_images = np.transpose(train_images, (0, 2, 1))
test_images = np.transpose(test_images, (0, 2, 1))

input_layer_size = 784 #input of a 28x28 grid

layer2_size = 64 #second layer has 64 neurons, can change

layer3_size = 64 #third layer has 64 neurons, can change

output_layer_size = 36 #outputs a number or character

input_neurons = []

layer2_neurons = []

input_to2connections = []

layer3_neurons = []

layer2to3connections = []

output_layer_neurons = []

layer3to_output_connections = []

train_image_1 = train_images[0]

class Neuron:
    def __init__(self, val, bias):
        self.val = val
        self.bias = bias

    def set_val(self, new_val):
        self.val = new_val

    def add_to_val(self, add_val):
        self.val += add_val

class Connection: #connection has a weight, bias, and is connected to 2 neurons
    def __init__(self, weight, neuron_in, neuron_out):
        self.weight = weight
        self.neuron_in = neuron_in
        self.neuron_out = neuron_out

    def set_weight(self, new_weight):
        self.weight = new_weight

    def set_bias(self, new_bias):
        self.bias = new_bias

#Creates input neuron objects
for i in range(input_layer_size):
    instance = Neuron(0, 0)
    input_neurons.append(instance)

#Creates layer2 neuron objects
for i in range(layer2_size):
    instance = Neuron(0, np.random.uniform(-0.01, 0.01))
    layer2_neurons.append(instance)

#Creates input_to2 connections
for neuron_in in input_neurons:
    for neuron_out in layer2_neurons:
        instance = Connection(np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
        input_to2connections.append(instance)

#Creates layer3 neuron objects
for i in range(layer3_size):
    instance = Neuron(0, np.random.uniform(-0.01, 0.01))
    layer3_neurons.append(instance)

#Creates layer2to3connections
for neuron_in in layer2_neurons:
    for neuron_out in layer3_neurons:
        instance = Connection(np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
        layer2to3connections.append(instance)

#Creates output layer neurons
for i in range(output_layer_size):
    instance = Neuron(0, np.random.uniform(-0.01, 0.01))
    output_layer_neurons.append(instance)

#Creates layer3to_output_connections
for neuron_in in layer3_neurons:
    for neuron_out in output_layer_neurons:
        instance = Connection(np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
        layer3to_output_connections.append(instance)

neurons = [input_neurons, layer2_neurons, layer3_neurons, output_layer_neurons]

connections = [input_to2connections, layer2to3connections, layer3to_output_connections]

def fill_inputs():
    #Fills input neurons with data
    for i in range(len(train_image_1)):
        for j in range(len(train_image_1[i])):
            input_neurons[28*i+j].set_val(input_sigmoid(train_image_1[i][j]))

def calculate_neuron_vals(arr, arr2):
    for connection in arr:
        input = connection.neuron_in.val
        weight = connection.weight
        output = input * weight
        connection.neuron_out.add_val(output)

    for neuron in arr2:
        neuron.add_to_val(neuron.bias)

def propagate_forward():
    #calculates the output of the first layer to each neuron in the second layer
    calculate_neuron_vals(input_to2connections, layer2_neurons)
    
    calculate_neuron_vals(layer2to3connections, layer3_neurons)

    calculate_neuron_vals(layer3to_output_connections, output_layer_neurons)

