![Example of CNN layer activation visualization](https://raw.githubusercontent.com/andropar/cnnvis/master/example.png)

# CNN layer activation visualization

This is a simple example of how to visualize the activations of a convolutional neural network layer. The example uses the AlexNet network, displaying the feature maps of all convolutional layers, and the activations of the fully connected layers when the model is fed a live stream of your laptop camera! You can start the visualization by first installing the required packages in a virtual environment of your choice, and then running the script:

``` bash
$ pip install -r requirements.txt
$ python real_time_cnnvis.py
```