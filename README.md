# rankEvaluations
A simple Python script to rank items on the basis of evaluations.
This scripts performs a ranking of evaluations expressed in an ordinal scale.

	Requirements for version 2: Python 2.7, scipy, ranking and mx packages. 
        Requirements for version 3: Python 3, scipy, numpy, datetime and ranking 
	Input options: 
		-h :: to display this help
		-i :: to specify the input file
		-d :: to set the debug mode ON (default is OFF)
		
	Inputs: The script takes in input a CSV with header which represents ordinal evaluations on n items (from 1, lowest to m, highest value; n must be >=3); 
	Outputs: According to single evaluations and corresponding rankings, the script provides a global ranking for the items.
	
	Released under the Creative Commons License 2015 by F Cabitza. Version 3 ported by Gioele Brancaleoni
