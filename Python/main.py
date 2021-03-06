# -*- coding: utf-8 -*-
"""Copy of Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VoxEZTpYT0q-re2rYhDfivewzHnT0G-a
"""

pip install -U keras

from google.colab import drive
from pathlib import Path
import numpy as np
from matplotlib import pyplot
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import keras
import cv2
from keras.callbacks import TensorBoard
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.optimizers import Adam
import sys
import os
import time
from torch.utils.tensorboard import SummaryWriter
import png
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from colormap.colors import Color, hex2rgb
from sklearn.metrics import average_precision_score as ap_score
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm

from dataset import FacadeDataset

# we need to load the data I used keras API for simpification
# i could use kaggle since they already processed the csv file with labels for the dataset
(train_image, train_lable), (test_image, test_lable) = fashion_mnist.load_data()
#lets see how did we do so far:
print('Train: Image=%s, Lable=%s' % (train_image.shape, train_lable.shape))
print('Test: Image=%s, Lable=%s' % (test_image.shape, test_lable.shape))

# great we can see we loaded the images they are about 60k wow alot!
#also we can see we loaded a lable for each image they are one of the 10 lables
#now we need to normalized the images to the size 28*28 with channle 1 and pixle value [0,1]
#but lets write some fucntions to do thes jobs for use


#this loader will load the files and then normolizes

def loader():
  (train_image, train_lable), (test_image, test_lable) = fashion_mnist.load_data()
  train_image = train_image.reshape((train_image.shape[0], 28, 28, 1)).astype('float32')/ 255.0
  test_image = test_image.reshape((test_image.shape[0], 28, 28, 1)).astype('float32')/ 255.0

  #now we use one hot vector to do it makes it easier for classification

  train_lable = to_categorical(train_lable)
  test_lable =  to_categorical(test_lable)
  return train_image, train_lable, test_image, test_lable
#now we need to define a modle to train and predict with good accuracy
# INPUT -> [CONV -> RELU -> POOL] -> [CONV -> RELU -> POOL] -> FC -> RELU -> FC
def modle_definer():
  model = Sequential()
  model.add(Conv2D(32, (3,3), activation='relu', kernel_initializer='he_uniform', padding="same", input_shape=(28, 28, 1)))
  model.add(MaxPooling2D((2, 2)))
  model.add(Dropout(.2))
  model.add(Conv2D(64, (3,3), activation='relu', kernel_initializer='he_uniform', padding="same", input_shape=(28, 28, 1)))
  model.add(MaxPooling2D((2, 2)))
  model.add(Dropout(.25))
  model.add(Flatten())
  model.add(Dense(64, activation='relu', kernel_initializer='he_uniform'))
  model.add(Dense(10, activation='softmax'))
  model.summary()
  model.compile(loss='categorical_crossentropy', optimizer= 'adam', metrics=['accuracy'])
  return model

def classifi():
  #load the data
  x,y,t_x,t_y = loader()
  #define the model
  model = modle_definer()
  H = model.fit(x, y, validation_split=0.2, batch_size=32, epochs=10)
  # now we can visualize modle and see the prediction
  lables = ['top', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt', 'sneaker', 'bag', 'ankle boot']
  prediction = model.predict(t_x)
  print("Network evaluation....")
  print(classification_report(t_y.argmax(axis=1), prediction.argmax(axis=1), target_names=lables))
  print(H.history.keys())
  plt.style.use("ggplot")
  plt.figure()
  plt.plot(np.arange(0, 10), H.history["accuracy"], label="train_acc")
  plt.plot(np.arange(0, 10), H.history["val_accuracy"], label="val_acc")
  plt.title("Training Loss and Accuracy on Dataset")
  plt.xlabel("Train on 48000 samples, validate on 12000 samples")
  plt.ylabel("Accuracy")
  plt.legend(loc="lower left")
  plt.savefig("plot_acc.png")
  plt.figure()
  plt.plot(np.arange(0, 10), H.history["loss"], label="train_loss")
  plt.plot(np.arange(0, 10), H.history["val_loss"], label="val_loss")
  plt.title("Training Loss and Accuracy on Dataset")
  plt.xlabel("Train on 48000 samples, validate on 12000 samples")
  plt.ylabel("Lossy")
  plt.legend(loc="lower left")
  plt.savefig("plot_loss.png")
  plt.figure()
  filter_1, biases_1 = model.layers[0].get_weights()
  f_1_min, f_1_max = filter_1.min(), filter_1.max()
  filter_1 = (filter_1 - f_1_min) / (f_1_max - f_1_min)
  index = 1
  for i in range(32):
      fil_1 = filter_1[:,:,:,i]
      pyplot.imshow(fil_1[:, :, 0], cmap='gray')
      pyplot.savefig('filters/filter_' + str(i) + '.png')
## code below is for visualization of the data I saved it in the colab but the address might be diffrent 
##so if you run it might get an error
# now lets visualize correctness of the modle



# for i in np.random.choice(np.arange(0,len(t_y)), size= (300,)):
#   pred_test = model.predict(t_x[np.newaxis, i])
#   pred_arg = pred_test.argmax(axis=1)
#   lables_test = lables[pred_arg[0]]
#   image = (t_x[i]*255).astype("uint8")
#   if pred_arg[0] == np.argmax(t_y[i]):
#     color = (0,150,0)
#     cor = True
#   else:
#     color = (0,0,200)
#     cor = False



#   image = cv2.merge([image] * 3)
#   image = cv2.resize(image, (100,100))
#   cv2.putText(image, lables_test, (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.50, color, 2)
#   if cor:
#     if lables_test == 'top':
#       cv2.imwrite("cor/top" + str(i) + ".png", image)
#     if lables_test == 'trouser':
#       cv2.imwrite("cor/trouser" + str(i) + ".png", image)
#     if lables_test == 'pullover':
#       cv2.imwrite("cor/pullover" + str(i) + ".png", image)
#     if lables_test == 'dress':
#       cv2.imwrite("cor/dress" + str(i) + ".png", image)
#     if lables_test == 'coat':
#       cv2.imwrite("cor/coat" + str(i) + ".png", image)
#     if lables_test == 'sandal':
#       cv2.imwrite("cor/sandal" + str(i) + ".png", image)
#     if lables_test == 'shirt':
#       cv2.imwrite("cor/shirt" + str(i) + ".png", image)
#     if lables_test == 'sneaker':
#       cv2.imwrite("cor/sneaker" + str(i) + ".png", image)
#     if lables_test == 'bag':
#       cv2.imwrite("cor/bag" + str(i) + ".png", image)
#     if lables_test == 'ankle boot':
#       cv2.imwrite("cor/ankle" + str(i) + ".png", image)
#   else:
#     test_inc.append(image)
#     cv2.imwrite("inc/image_" + str(i) + ".png", image)
#     if lables_test == 'trouser':
#       cv2.imwrite("tro_inc/image_" + str(i) + ".png", image)

# for i in range(len(test_cor)):
#   cv2.imwrite("cor/image_" + str(i) + ".png", test_cor[i])
# for i in range(len(test_inc)):
#   cv2.imwrite("inc/image_" + str(i) + ".png", test_inc[i])

# for i in range(len(tro_cor)):
#   cv2.imwrite("tro_cor/image_" + str(i) + ".png", tro_cor[i])
# for i in range(len(tro_inc)):
#   cv2.imwrite("tro_inc/image_" + str(i) + ".png", tro_inc[i])

classifi()

#!unzip part2.zip
#!rm -rf part2/
#!mv "part2/train.py" "/content"

!pip3 install -r requirements.txt

import os
import time
from torch.utils.tensorboard import SummaryWriter
import cv2
import matplotlib.pyplot as plt
import numpy as np
import png
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from colormap.colors import Color, hex2rgb
from sklearn.metrics import average_precision_score as ap_score
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm

from dataset import FacadeDataset

N_CLASS=5

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.n_class = N_CLASS
        self.layers = nn.Sequential(
            #########################################
            ###        TODO: Add more layers      ###
            #########################################


            nn.Conv2d(3,32, 3, stride=1, padding=1),
            nn.BatchNorm2d(32, eps=1e-3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            

            nn.Conv2d(32,64, 3,stride=1, padding=1),
            nn.BatchNorm2d(64, eps=1e-3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(64,64,3, stride=1, padding=1),
            nn.BatchNorm2d(64, eps=1e-3),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64,64,2,stride=2, padding=0),
            
            nn.Conv2d(64,32,3, stride=1, padding=1),
            nn.BatchNorm2d(32, eps=1e-3),            
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(32, 32, 2, stride=2, padding=0),
            nn.Conv2d(32,self.n_class, 3, stride=1, padding=1)
            

        )

    def forward(self, x):
        x = self.layers(x)
        return x


def save_label(label, path):
    '''
    Function for ploting labels.
    '''
    colormap = [
        '#000000',
        '#0080FF',
        '#80FF80',
        '#FF8000',
        '#FF0000',
    ]
    assert(np.max(label)<len(colormap))
    colors = [hex2rgb(color, normalise=False) for color in colormap]
    w = png.Writer(label.shape[1], label.shape[0], palette=colors, bitdepth=4)
    with open(path, 'wb') as f:
        w.write(f, label)

def train(trainloader, net, criterion, optimizer, device, epoch):
    '''
    Function for training.
    '''
    batch_loss = []
    tota_loss = []
    start = time.time()
    running_loss = 0.0
    net = net.train()
    for images, labels in tqdm(trainloader):
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        output = net(images)
        loss = criterion(output, labels)
        batch_loss.append(loss.item())
        loss.backward()
        optimizer.step()
        running_loss = loss.item()
    end = time.time()
    print('[epoch %d] loss: %.3f elapsed time %.3f' %
          (epoch, running_loss, end-start))
    return batch_loss

def test(testloader, net, criterion, device):
    '''
    Function for testing.
    '''
    batch_loss = []
    losses = 0.
    cnt = 0
    with torch.no_grad():
        net = net.eval()
        for images, labels in tqdm(testloader):
            images = images.to(device)
            labels = labels.to(device)
            output = net(images)
            loss = criterion(output, labels)
            batch_loss.append(loss.item())
            losses += loss.item()
            cnt += 1
    print(losses / cnt)
    return batch_loss, (losses/cnt)


def cal_AP(testloader, net, criterion, device):
    '''
    Calculate Average Precision
    '''
    losses = 0.
    cnt = 0
    with torch.no_grad():
        net = net.eval()
        preds = [[] for _ in range(5)]
        heatmaps = [[] for _ in range(5)]
        for images, labels in tqdm(testloader):
            images = images.to(device)
            labels = labels.to(device)
            output = net(images).cpu().numpy()
            for c in range(5):
                preds[c].append(output[:, c].reshape(-1))
                heatmaps[c].append(labels[:, c].cpu().numpy().reshape(-1))

        aps = []
        for c in range(5):
            preds[c] = np.concatenate(preds[c])
            heatmaps[c] = np.concatenate(heatmaps[c])
            if heatmaps[c].max() == 0:
                ap = float('nan')
            else:
                ap = ap_score(heatmaps[c], preds[c])
                aps.append(ap)
            print("AP = {}".format(ap))

    # print(losses / cnt)
    return None


def get_result(testloader, net, device, folder='output_train'):
    result = []
    cnt = 1
    with torch.no_grad():
        net = net.eval()
        cnt = 0
        for images, labels in tqdm(testloader):
            images = images.to(device)
            labels = labels.to(device)
            output = net(images)[0].cpu().numpy()
            c, h, w = output.shape
            assert(c == N_CLASS)
            y = np.zeros((h,w)).astype('uint8')
            for i in range(N_CLASS):
                mask = output[i]>0.5
                y[mask] = i
            gt = labels.cpu().data.numpy().squeeze(0).astype('uint8')
            save_label(y, './{}/y{}.png'.format(folder, cnt))
            save_label(gt, './{}/gt{}.png'.format(folder, cnt))
            plt.imsave(
                './{}/x{}.png'.format(folder, cnt),
                ((images[0].cpu().data.numpy()+1)*128).astype(np.uint8).transpose(1,2,0))

            cnt += 1

def main():
    ###### For part 1 uncomment the classifi() function!!########
    #classifi()




    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # TODO change data_range to include all train/evaluation/test data.
    # TODO adjust batch_size.
    train_data = FacadeDataset(flag='train', data_range=(0,725), onehot=False)
    train_loader = DataLoader(train_data, batch_size=1)

    train_val =  FacadeDataset(flag='train', data_range=(725,906), onehot=False)
    train_val_loader = DataLoader(train_val, batch_size=1)
    
    test_data = FacadeDataset(flag='test_dev', data_range=(0,114), onehot=False)
    test_loader = DataLoader(test_data, batch_size=1)
    ap_data = FacadeDataset(flag='test_dev', data_range=(0,114), onehot=True)
    ap_loader = DataLoader(ap_data, batch_size=1)
    name = 'starter_net'
    net = Net().to(device)
    criterion = nn.CrossEntropyLoss() #TODO decide loss
    optimizer = torch.optim.Adam(net.parameters(), 1e-3, weight_decay=1e-5)

    print('\nStart training')
    train_loss = []
    test_loss = []
    for epoch in range(20): #TODO decide epochs
        print('-----------------Epoch = %d-----------------' % (epoch+1))
        batch_loss = train(train_loader, net, criterion, optimizer, device, epoch+1)
        # TODO create your evaluation set, load the evaluation set and test on evaluation set
        evaluation_loader = train_val_loader
        test_batch,_ = test(evaluation_loader, net, criterion, device)
        result_eval = get_result(evaluation_loader, net, device, folder='output_test')
        train_loss.append(np.mean(batch_loss))
        test_loss.append(np.mean(test_batch))
    plt.figure()
    plt.plot(np.arange(0, 20), train_loss, label="train_loss")
    plt.plot(np.arange(0, 20), test_loss, label="test_loss")
    plt.title("Training Loss and Accuracy on Dataset")
    plt.xlabel("20 epoches")
    plt.ylabel("Lossy")
    plt.legend(loc="lower left")
    plt.savefig("plot_loss.png")

    print('\nFinished Training, Testing on test set')
    test(test_loader, net, criterion, device)
    print('\nGenerating Unlabeled Result')
    result = get_result(test_loader, net, device, folder='output_train')

    torch.save(net.state_dict(), './models/model_{}.pth'.format(name))


    cal_AP(ap_loader, net, criterion, device)

if __name__ == "__main__":
    main()