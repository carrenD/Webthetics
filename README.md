## Webthetics: Quantifying Webpage Aesthetics with Deep Learning
by Qi Dou, Sam Zheng*, Samuel Sun, and Pheng-Ann Heng </br>
conducted when Qi and Samuel were doing internship at Siemens Corporate Research, Princeton, US.

### Introduction

As web has become the most popular media to attract users and customers worldwide, webpage aesthetics plays an increasingly important role for engaging users online and impacting their user experience. We present a novel method using deep learning to automatically compute and quantify webpage aesthetics. Our deep neural network, named as Webthetics, which is trained from the collected user rating data, can extract representative features from raw webpages and quantify their aesthetics. To improve the model performance, we propose to transfer the knowledge from image style recognition task into our network. We have validated that our method significantly outperforms previous method using hand-crafted features such as colorfulness and complexity. Moreover, empirical experiments show that our network is sensitive to important design factors including layout, balance, content information and spatial frequency. These promising results indicate that our method can serve as an effective and efficient means for providing objective aesthetics evaluation during the design process.

### Requirements
We make this implementation as light-weighted and Windows environment friendly, so that it can be easily executable at a designer PC with minumum gpu and system requirements.

### Usage

- exp_prepare.py </br>
prepare the data of webpage screenshots and user aesthetics ratings, and collect the webpage--userrating pairs </br> 
need to first download the resources released by Reinecke et al. we also put our downloaded reosurces in the data folder </br>

- webthetics.prototxt </br>
the convolutional neural network model as listed in Table 1 in the paper </br>
The model folder has the trained network

- test_eva.py </br>
for testing the webthetics model, to predict the aesthetics rating score for a webpage screenshot.

- occlusion.py </br>
for generating the manipulated webpages for empirical study towards design factors </br>
test these images to observe how these damage of design influence the automated aesthetics quanfitication.


