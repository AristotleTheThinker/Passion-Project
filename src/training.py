import numpy as np
from scipy.io import loadmat
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

neural_network = main.Neural_network()

# neural_network.fill_inputs_create_target_array(train_images[0],train_labels[0][0])
# neural_network.propagate_forward()
# for i in range(20):
#     print(neural_network.layer3to_output_connections[i].weight)
# print("______")
# neural_network.backpropagation()
# for i in range(20):
#     print(neural_network.layer3to_output_connections[i].weight)


for i in range(len(train_images)):
    neural_network.fill_inputs_create_target_array(train_images[i],train_labels[i][0])
    neural_network.propagate_forward()
    neural_network.backpropagation()
    if i%1000 == 0:
        print(i)

with open("trained_model.pkl", "wb") as f:
    pickle.dump(neural_network, f)

print("dumped")

correct = 0
incorrect = 0
for i in range(len(test_images)):
    neural_network.fill_inputs_create_target_array(test_images[i], test_labels[i][0])
    neural_network.propagate_forward()
    output = 0
    index = 0
    for neuron in neural_network.output_layer_neurons:
        if neuron.val > output:
            output = neuron.val
            index = neuron.position
    if index == test_labels[i][0]-1:
        correct += 1
    else:
        incorrect += 1
        
    if i%1000 == 0:
        print(i)

print(correct)
print(incorrect)
print(correct/(correct+incorrect) * 100 + "%")

