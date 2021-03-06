# ENPM661

The script name is Project_Two.py
The packages imported in the code are numpy, sys, cv2, and datetime
-----------------------------------------------------------------------
Running the code:

1A. To run in Spyder IDE (preferred)---execute the script with the "Run" icon. 
	a. Tester MUST go into the code and manually key in the start and end points for the test. 
	b. START points: variable name TestCaseXY = [x,y], where x and y are the standard orientation coordinates from the obstacle map
	c. END points: variable name FinalStateXY = [x,y], where x and y are the standard orientation coordinates from the obstacle map
	d. TestCaseXY variable is defined on line 24 of the code, FinalStateXY is defined on line 34.


1B. To run in LINUX (not preferred)---execute the script with this command in the Linux terminal window:
	
	python3 Project_Two.py 

	a. Tester MUST go into the code and manually key in the start and end points for the test. 
	b. START points: variable name TestCaseXY = [x,y], where x and y are the standard oriented coordinates from the obstacle map
	c. END points: variable name FinalStateXY = [x,y], where x and y are the standard oriented coordinates from the obstacle map
	d. TestCaseXY variable is defined on line 24 of the code, FinalStateXY is defined on line 34.


2. The script should not take long to complete (<7 minutes), and some output info will be sent to the NodePath.txt file in the same directory as the script.
	a. General Note: Some informative msgs will print to the terminal window/Spyder command line when running the code. 
	b. In these msgs, "node" indicates the PIXEL x,y coordinates (Y coordinate is inverted in pixel coordinates) 

3. The script will run only one testcase at a time, and the NodePath.txt file with results will overwrite every time.

4. As a note, in the output NodePath.txt file, "Our road map" is the parent-child node map from initial to goal state. Nodes are stored as pixel coordinates, not standard x-y coordinates (only difference is the Y pixel coordinate will be inverted) 	 

5. The output video is called "Sweeping.mp4"


