Readme file for the 318 project

Execution steps:

1. The program requires the follow packages/libraries to be installed:
	1. numpy
	2. pandas
	3. The scikit packages (SVC, OneVsRestClassifier, DecisionTreeClassifier)
	which should be installed if you can run the SVC model
	if not, please look at scikit-learn.org/stable/install.html for details
	4. install python pillow:
	http://pillow.readthedocs.io/en/3.4.x/installation.html


2. Please have the katkam images uncompressed before running the program
We are using the original katkam images provided at:
https://courses.cs.sfu.ca/2017su-cmpt-318-d1/pages/ProjectWeatherKatkam

3. Please also uncompresss the weather.zip file, which is provided at:
https://courses.cs.sfu.ca/2017su-cmpt-318-d1/pages/ProjectWeatherWeather

4. after decompression, make sure you have the following folders in the same
directory as weather_predict.py:
	1. katkam-scaled
	2. yvr-weather

5. you can then run the program by executing the command on terminal:
python3 weather_predict.py ./yvr-weather ./katkam-scaled output.csv
Where the output.csv is the file name argument for the output file

After the program finishes running, you should be able to see the accuracy score
on the terminal, and a output.csv file, which contains the observed weather condition
and the predicted weather condition

Running time:
Using the lab's computer, it takes about 2 to 3 minutes for the program to finish executing
Please wait for a few minutes for the program to finish execution

