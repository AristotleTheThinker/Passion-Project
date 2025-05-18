import numpy as np
from scipy.io import loadmat
import os
import matplotlib.pyplot as plt

class Neuron:
            def __init__(self, val, bias, index):
                self.val = val
                self.bias = bias
                self.position = index

            def set_val(self, new_val):
                self.val = new_val

            def add_to_val(self, add_val):
                self.val += add_val

            def update_bias(self, delta, learning_rate):
                self.bias += learning_rate * delta

class Connection: #connection has a weight, bias, and is connected to 2 neurons
            def __init__(self, weight, neuron_in, neuron_out):
                self.weight = weight
                self.neuron_in = neuron_in
                self.neuron_out = neuron_out

            def set_weight(self, new_weight):
                self.weight = new_weight

class Neural_network:

    def __init__(self):
        self.input_layer_size = 784 #input of a 28x28 grid

        self.layer2_size = 64 #second layer has 64 neurons, can change

        self.layer3_size = 64 #third layer has 64 neurons, can change

        self.output_layer_size = 26 #outputs a number or character

        self.learning_rate = 0.01

        self.input_neurons = []

        self.layer2_neurons = []

        self.input_to2connections = []

        self.layer3_neurons = []

        self.layer2to3connections = []

        self.output_layer_neurons = []

        self.layer3to_output_connections = []

        self.target_arr = []

        #Creates input neuron objects
        for i in range(self.input_layer_size):
            instance = Neuron(0, 0, i)
            self.input_neurons.append(instance)

        #Creates layer2 neuron objects
        for i in range(self.layer2_size):
            instance = Neuron(0, np.random.uniform(-0.01, 0.01), i)
            self.layer2_neurons.append(instance)

        #Creates input_to2 connections
        for neuron_in in self.input_neurons:
            for neuron_out in self.layer2_neurons:
                instance = Connection(np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
                self.input_to2connections.append(instance)

        #Creates layer3 neuron objects
        for i in range(self.layer3_size):
            instance = Neuron(0, np.random.uniform(-0.01, 0.01), i)
            self.layer3_neurons.append(instance)

        #Creates layer2to3connections
        for neuron_in in self.layer2_neurons:
            for neuron_out in self.layer3_neurons:
                instance = Connection(np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
                self.layer2to3connections.append(instance)

        #Creates output layer neurons
        for i in range(self.output_layer_size):
            instance = Neuron(0, np.random.uniform(-0.01, 0.01), i)
            self.output_layer_neurons.append(instance)

        #Creates layer3to_output_connections
        for neuron_in in self.layer3_neurons:
            for neuron_out in self.output_layer_neurons:
                instance = Connection(np.random.uniform(-0.01, 0.01), neuron_in, neuron_out)
                self.layer3to_output_connections.append(instance)

        neurons = [self.input_neurons, self.layer2_neurons, self.layer3_neurons, self.output_layer_neurons]

        connections = [self.input_to2connections, self.layer2to3connections, self.layer3to_output_connections]

    @staticmethod
    def input_sigmoid(x):
        if x > 128.0:
            return 1
        else:
            return 0
       
    @staticmethod    
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def der_relu(x):
        if x <= 0:
            return 0
        else:
            return 1
        
    def fill_inputs(self, image):
        #Fills input neurons with data
        for i in range(len(image)):
            for j in range(len(image[i])):
                self.input_neurons[28*i+j].set_val(self.input_sigmoid(image[i][j]))

    def create_target_array(self, label_num):
        self.target_arr = [0] * self.output_layer_size
        self.target_arr[label_num - 1] = 1

    def reset_neurons(self):
        for layer in [self.layer2_neurons, self.layer3_neurons, self.output_layer_neurons]:
            for neuron in layer:
                neuron.set_val(0)

    def calculate_neuron_vals(self, arr, arr2):
        for connection in arr:
            input = connection.neuron_in.val
            weight = connection.weight
            output = input * weight
            connection.neuron_out.add_to_val(output)

        for neuron in arr2:
            neuron.add_to_val(neuron.bias)
            neuron.set_val(self.relu(neuron.val))

    def propagate_forward(self):
        self.reset_neurons()

        #calculates the output of the first layer to each neuron in the second layer
        self.calculate_neuron_vals(self.input_to2connections, self.layer2_neurons)
        
        self.calculate_neuron_vals(self.layer2to3connections, self.layer3_neurons)

        self.calculate_neuron_vals(self.layer3to_output_connections, self.output_layer_neurons)

    @staticmethod
    def calculate_output_error(target, actual):
        return target - actual

    #Backpropagation
    def backpropagation(self):
        
        output_error = []

        layer3_error = []

        for i in range(len(self.layer3_neurons)):
            layer3_error.append(0)

        layer2_error = []

        for i in range(len(self.layer2_neurons)):
            layer2_error.append(0)

        #Output Errors
        for i in range(len(self.output_layer_neurons)):
            error = self.calculate_output_error(self.target_arr[i], self.output_layer_neurons[i].val)
            output_error.append(error)

        for i, neuron in enumerate(self.output_layer_neurons):
            neuron.update_bias(output_error[i], self.learning_rate)


        #Reset Layer3toOutput Weights + Get Layer 3 errors
        raw_layer3_error = [0.0] * self.layer3_size
        for connection in self.layer3to_output_connections:
            out_index = connection.neuron_out.position
            in_index = connection.neuron_in.position
            error = output_error[out_index]
            raw_layer3_error[in_index] += error * connection.weight
            connection.set_weight(connection.weight + self.learning_rate * error * connection.neuron_in.val)

        for i in range(self.layer3_size):
            layer3_error[i] = raw_layer3_error[i] * self.der_relu(self.layer3_neurons[i].val)

        for i, neuron in enumerate(self.layer3_neurons):
            neuron.update_bias(layer3_error[i], self.learning_rate)


        #Reset Layer2to3 Weights + Get Layer 2 errors
        raw_layer2_error = [0.0] * self.layer2_size
        for connection in self.layer2to3connections:
            out_index = connection.neuron_out.position
            in_index = connection.neuron_in.position
            error = layer3_error[out_index]
            raw_layer2_error[in_index] += error * connection.weight
            connection.set_weight(connection.weight + self.learning_rate * error * connection.neuron_in.val)

        for i in range(self.layer2_size):
            layer2_error[i] = raw_layer2_error[i] * self.der_relu(self.layer2_neurons[i].val)

        for i, neuron in enumerate(self.layer2_neurons):
            neuron.update_bias(layer2_error[i], self.learning_rate)


        #Reset InputTo2 Weights
        for connection in self.input_to2connections:
            out_index = connection.neuron_out.position
            error = layer2_error[out_index]
            connection.set_weight(connection.weight + self.learning_rate * error * connection.neuron_in.val)