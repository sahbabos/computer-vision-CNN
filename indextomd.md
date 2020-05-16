Image Classification & Semantic Segmentation
=================================================================

Sahba Bostanbakhsh

Part 1: Image Classification {#image-classification}
----------------------------

### Overview

In order to classify the Fasion-mnist dataset with good accuracy we need
a good model architecture!! the one example could be as simple as this :

-   INPUT -\> [CONV2D -\> RELU -\> MaxPool] -\> [CONV2D -\> RELU -\>
    MaxPool] -\> FC -\> RELU -\> FC -\> OUTPUT

For this model, cross-entropy loss is used for computing the loss, Adam
is used for optimization, and the model was trined over 10 epoches, the
total accuracy is about 91% to 92%.

After training and validating the model the loss/Accuracy vs \#samples
can be plotted.

![](plot_acc.png)

![](plot_loss.png)

From the plot above we can see some overfitting has occurred. This could
happen because of many reasons. For example, if we have alot of
parameters for training.

However we can reduce overfitting by improving our model or tunning the
hyperparameters.

### Results {#Results}

the modle prediction chart: .

![](percent.png)

the hardes class to classify is shirt! and the reason could be the
information gain from the pixels share same hyperparameters as other
classes:

The shirt class had the lowest accuracy for both the validation and test
set.

lets look at some correct (Green) and incorrect (Red) predictions done
by our model.

![](ankle%20boot.png) ![](ankle%20boot2.png) ![](inc%20ankle%20boot.png)
![](inc%20ankle%20boot2.png)

![](bag.png) ![](bag2.png) ![](inc%20bag.png) ![](inc%20bag2.png)

![](dress.png) ![](dress2.png) ![](inc%20dress.png)
![](inc%20dress2.png)

![](pullover.png) ![](pullover2.png) ![](inc%20pullover.png)
![](inc%20pullover2.png)

![](sandal.png) ![](sandal2.png) ![](inc%20sandal.png)
![](inc%20sandal2.png)

![](shirt.png) ![](shirt2.png) ![](inc%20shirt.png)
![](inc%20shirt2.png)

![](sneaker.png) ![](sneaker2.png) ![](inc%20sneaker.png)
![](inc%20sneaker2.png)

![](top.png) ![](top2.png) ![](inc%20top.png) ![](inc%20top2.png)

![](trouser.png) ![](trouser2.png) ![](inc%20trouser.png)
![](inc%20trouser2.png)

![](coat.png) ![](coat2.png) ![](inc%20coat.png) ![](inc%20coat2.png)

### Filters

Below, the 3x3 filters have been visualized.

![](filters_0.png) ![](filters_1.png) ![](filters_2.png)
![](filters_3.png) ![](filters_4.png) ![](filters_5.png)
![](filters_6.png) ![](filters_7.png)

![](filters_8.png) ![](filters_9.png) ![](filters_10.png)
![](filters_11.png) ![](filters_12.png) ![](filters_13.png)
![](filters_14.png) ![](filters_15.png)

![](filters_16.png) ![](filters_17.png) ![](filters_18.png)
![](filters_19.png) ![](filters_20.png) ![](filters_21.png)
![](filters_22.png) ![](filters_23.png)

![](filters_24.png) ![](filters_25.png) ![](filters_26.png)
![](filters_27.png) ![](filters_28.png) ![](filters_29.png)
![](filters_30.png) ![](filters_31.png)

Semantic Segmentation {#Semantic-Segmentation}
---------------------

### Overview

This part of the project is a bit harder to implement since it requires
downsampling and upsampling of an input image.

### Architecture

The layers used are below:

-   Conv2d(3,32, 3, stride=1, padding=1)
-   BatchNorm2d(32)
-   ReLU
-   MaxPool2d(2)
-   Conv2d(32,64, 3,stride=1, padding=1)
-   BatchNorm2d(32)
-   ReLU
-   MaxPool2d(2)
-   Conv2d(64,64,3, stride=1, padding=1)
-   BatchNorm2d(64)
-   ReLU
-   nn.ConvTranspose2d(64,64,2,stride=2, padding=0)
-   Conv2d(64,32,3, stride=1, padding=1)
-   BatchNorm2d(32)
-   ReLU
-   ConvTranspose2d(32, 32, 2, stride=2, padding=0)
-   Conv2d(32,self.n\_class, 3, stride=1, padding=1)

### Train Loss and Test Loss plot {#Train Loss and Test Loss plot}

The graph below shows the modle is overfitting.

![](plot_ap.png)

### AP: average-precision {#AP: average-precision}

The reported values for the average precision of the network are below.

    AP = 0.5432155628391006
    AP = 0.6932388379961033
    AP = 0.1567090498345968
    AP = 0.8025611932893545
    AP = 0.3401661294507566

### Results {#Results}

The sample image below illustrates how the net would classify the parts
in an image.

![](main3.png) ![](result3.png)

![](main4.png) ![](result4.png)

### What class does model classify correctly and incorrectly {#What class does model classify correctly and incorrectly:}

Model is good for classifing windows. Facade and others score better
than avrage but pillar and balcony have low AP score. Model is not good
to classify pillar and balcony
