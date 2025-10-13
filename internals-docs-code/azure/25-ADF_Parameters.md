## Parameters in Azure Data Factory

Paramters are external values that can be passed into pipelines, datasets and linked services. The value cannot be changed inside a pipeline.

Variables are internal values set inside a pipeline that can be changed using Set Variable or Append Variable Activity.

### Steps to Parameterize a Pipeline

1. Source Dataset - Set Parameter for ```relativeURL```

![alt text](https://snipboard.io/chnHDu.jpg)

2. Source Dataset - Define the Paramter in Connections

![alt text](https://snipboard.io/k7RX49.jpg)

3. Sink Dataset - Parameterize File Name

![alt text](https://snipboard.io/krVp81.jpg)

![alt text](https://snipboard.io/ZPq25X.jpg)

![alt text](https://snipboard.io/D4RdFE.jpg)

4. Pipeline Parameterization - Add two variables

![alt text](https://snipboard.io/5x0Cas.jpg)

5. Pipeline Paramterization - Pass the variables to the activity

![alt text](https://snipboard.io/NIGRs6.jpg)

It asks us to pass relativeURL paramter which we do via the variables defined above.

![alt text](https://snipboard.io/whgrDO.jpg)

Similarly for the sink as well.

