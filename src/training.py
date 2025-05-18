import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
import time
import os
import main
import pickle

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

let_nums = [[0 for i in range(2)] for j in range(26)]

def train(num):
    for i in range(num):
        neural_network.fill_inputs_create_target_array(train_images[i],train_labels[i][0])
        neural_network.propagate_forward()
        neural_network.backpropagation()
        if i%500 == 0:
            output_vals = [round(n.val, 2) for n in neural_network.output_layer_neurons]
            print("Pred:", np.argmax(output_vals), "Target:", train_labels[i][0]-1, "Out:", output_vals)
            print(i)
def dump(file_name):
    with open(file_name, "wb") as f:
        pickle.dump(neural_network, f)
    print("dumped")

def load(model):
    with open(model, "rb") as f:   
        return pickle.load(f)

def test(num):
    indices = np.arange(20800)
    np.random.shuffle(indices)
    correct = 0
    incorrect = 0
    for i in range(num):
        label_num = test_labels[indices[i]][0]
        target = label_num-1
        neural_network.fill_inputs_create_target_array(test_images[indices[i]], label_num)
        neural_network.propagate_forward()
        output = 0
        index = 0
        for neuron in neural_network.output_layer_neurons:
            if neuron.val > output:
                output = neuron.val
                index = neuron.position
        if index == target:
            correct += 1
            let_nums[target][0] += 1
        else:
            incorrect += 1
            let_nums[target][1] += 1

        if i%1000 == 0:
            print(i)

    print("Correct: " + str(correct))
    print("Incorrect: " + str(incorrect))
    print(str(correct/(correct+incorrect) * 100) + "%")
    for i, pair in enumerate(let_nums):
        print(chr(65+i) + ": " + str(round(pair[0]/(pair[0]+pair[1])*100,2)) + "%")

#neural_network = main.Neural_network()
#train(100000)
#dump("trained_model.pkl")
neural_network = load("trained_model_10000.pkl")
test(2000)