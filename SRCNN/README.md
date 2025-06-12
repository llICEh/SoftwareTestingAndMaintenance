


The SR-CNN project is consisted of three major parts.<br> 
1.generate_data.py is used for preprocess the data, where the original continuous time series are splited according to window size and  artificial outliers are injected in proportion. <br> 
`
python generate_data.py --data <dataset>
`<br> 
where dataset is the file name of data folder.If you want to change the default config, you can use the command line args:<br>
`
python generate_data.py -data <dataset> --window 256 --step 128
`<br> 
2.train.py is the network training module of SR-CNN. SR transformer is applied on each time-series before training.<br> 
`
python train.py -data <dataset>
`<br> 
3.evalue.py is the evaluation module.As mentioned in our paper, <br>
`
We evaluate our model from three aspects,accuracy,efficiency and generality.We use precision,recall and F1-score to indicate the  accuracy of our model.In real applications,the human operators do not care about the point-wise metrics. It is acceptable for an algorithm to trigger an alert for any point in a contiguous anomaly segment if the delay is not too long.Thus,we adopt the evaluation  strategy following[23].We mark the whole segment of continuous anomalies as a positive sample which means no matter how many anomalies have been detected in this segment,only one effective detection will be counted.If any point in ananomaly segment can be detected by the algorithm,and the delay of this point is no more than k from the start point of the anomaly segment, we say this segment is detected correctly.Thus,all points in this segment are treated as correct,and the points outside the anomaly segments are treated as normal. 
`<br>
we set different delays to verify whether a whole section of anomalies can be detected in time. For example,  When delay = 7, for an entire segment of anomaly, if the anomaly detector can issue an alarm at its first 7 points, it is considered that the entire segment of anomaly has been successfully detected, otherwise it is considered to have not been detected.<br> 
Run the code:<br>
`
python evalue.py -data <dataset>
`<br> 
