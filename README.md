## Webthetics: Quantifying Webpage Aesthetics with Deep Learning
by Qi Dou, Sam Zheng*, Samuel Sun, and Pheng-Ann Heng </br>
conducted when Qi and Samuel were doing internship at Siemens Corporate Research, Princeton, US.

### Introduction

As web has become the most popular media to attract users and customers worldwide, webpage aesthetics plays an increasingly important role for engaging users online and impacting their user experience. We present a novel method using deep learning to automatically compute and quantify webpage aesthetics. Our deep neural network, named as Webthetics, which is trained from the collected user rating data, can extract representative features from raw webpages and quantify their aesthetics. To improve the model performance, we propose to transfer the knowledge from image style recognition task into our network. We have validated that our method significantly outperforms previous method using hand-crafted features such as colorfulness and complexity. Moreover, empirical experiments show that our network is sensitive to important design factors including layout, balance, content information and spatial frequency. These promising results indicate that our method can serve as an effective and efficient means for providing objective aesthetics evaluation during the design process.

### Requirement
We make this implementation as light-weighted and Windows environment friendly, so that it can be easily executable at a designer PC with minumum GPU and system requirements.

### Usage

- Prepare the data of webpage screenshots and user aesthetics ratings </br>
download the resources released by Reinecke et al, which we also put in the data folder. </br>
use the exp_prepare.py as preprocessing to collect the webpage--userRating pairs </br>
