import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
import time
import os
import main
import pickle

class Training:
    def __init__(self, neural_network):
        self.neural_network = neural_network

        self.current_dir = os.path.dirname(__file__)  # Src/
        self.mat_path = os.path.join(self.current_dir, '../data/matlab/emnist-letters.mat')

        self.digits_mat = loadmat(self.mat_path)

        self.data = self.digits_mat['dataset']

        # Training data
        self.train_images = self.data['train'][0, 0]['images'][0, 0]
        self.train_labels = self.data['train'][0, 0]['labels'][0, 0]

        # Reshape images to 28x28
        self.train_images = self.train_images.reshape((-1, 28, 28)).astype(np.uint8)

        #Rotate the images
        self.train_images = np.transpose(self.train_images, (0, 2, 1))

    def train(self, num):
        for i in range(num):
            self.neural_network.fill_inputs(self.train_images[i])
            self.neural_network.create_target_array(self.train_labels[i][0])
            self.neural_network.propagate_forward()
            self.neural_network.backpropagation()
            if i%500 == 0:
                output_vals = [round(n.val, 2) for n in self.neural_network.output_layer_neurons]
                print("Pred:", np.argmax(output_vals), "Target:", self.train_labels[i][0]-1, "Out:", output_vals)
                print(i)

    def dump(self, file_name):
        with open(file_name, "wb") as f:
            pickle.dump(self.neural_network, f)
        print("dumped")

class Testing:

    def __init__(self, neural_network):
        self.neural_network = neural_network

        #Import Dataset
        self.current_dir = os.path.dirname(__file__)  # Src/
        self.mat_path = os.path.join(self.current_dir, '../data/matlab/emnist-letters.mat')

        self.digits_mat = loadmat(self.mat_path)

        self.data = self.digits_mat['dataset']

        # Testing data
        self.test_images = self.data['test'][0, 0]['images'][0, 0]
        self.test_labels = self.data['test'][0, 0]['labels'][0, 0]

        # Reshape images to 28x28
        self.test_images = self.test_images.reshape((-1, 28, 28)).astype(np.uint8)

        #Rotate the images
        self.test_images = np.transpose(self.test_images, (0, 2, 1))

        self.let_nums = [[0 for i in range(2)] for j in range(26)]

    @staticmethod
    def load(model):
        with open(model, "rb") as f:   
            return pickle.load(f)

    def test(self, num):
        indices = np.arange(20800)
        np.random.shuffle(indices)
        correct = 0
        incorrect = 0
        for i in range(num):
            label_num = self.test_labels[indices[i]][0]
            target = label_num-1
            self.neural_network.fill_inputs(self.test_images[indices[i]])
            self.neural_network.create_target_array(label_num)
            self.neural_network.propagate_forward()
            max_prob = 0
            output = 0
            for neuron in self.neural_network.output_layer_neurons:
                if neuron.val > max_prob:
                    max_prob = neuron.val
                    output = neuron.position
            if output == target:
                correct += 1
                self.let_nums[target][0] += 1
            else:
                incorrect += 1
                self.let_nums[target][1] += 1

            if i%1000 == 0:
                print(i)

        print("Correct: " + str(correct))
        print("Incorrect: " + str(incorrect))
        result = ""
        result += (str(round(correct/(correct+incorrect) * 100,2)) + "%")
        print(result)
        for i, pair in enumerate(self.let_nums):
            result += "\n" + (chr(65+i) + ": " + str(round(pair[0]/(pair[0]+pair[1])*100,2)) + "%")
        print(result)
        return result

    @staticmethod
    def dump(file_name, result):
        with open(file_name, "wb") as f:
            pickle.dump(result, f)
        print("dumped")

    def attempt(self, image):
        self.neural_network.fill_inputs(image)
        self.neural_network.propagate_forward()
        max_prob = 0
        output = 0
        for neuron in self.neural_network.output_layer_neurons:
            if neuron.val > max_prob:
                max_prob = neuron.val
                output = neuron.position
        return output


# neural_network_train = main.Neural_network()
# training = Training(neural_network_train)
# training.train(1000)
# training.dump("models/trained_model.pkl")


# model_name = "trained_model_0.05-128-128.pkl"
# neural_network_test = Testing.load("models/" + model_name)
# testing = Testing(neural_network_test)
# result = testing.test(3000)
# Testing.dump('analysis/' + model_name, result)