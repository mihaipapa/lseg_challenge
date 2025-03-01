# lseg_challenge

This is my implementation of the LSEG technical challenge.

The logic of the implementation is in the stock_price_predictor.py file, where I created the 2 API functions that were
necessary for the task, and, also, some helping functions to make the code a bit tidier.

The folder structure is:
- all the input files are grouped in the input_folders directory, with a folder for each stock exchange
- the output files will be placed in the output_folders directory, with the same folder structure as the input

All the folders were designed with relative paths, as manually changing the path everytime you change the machine
is too much work.

The code was (I hope) pretty well explained with comments.  

I want to mention that the code was tested on both windows and WSL, so if you have any issues, please message the recruiter :).

The code can be run by going to the code folder, installing the requirements with:  
pip install -r requirements.txt  
or just  
pip install pandas  
and then just doing: python stock_price_predictor.py <number_of_files>.  

Because of the argparse library, running the script with arguments other than 1 and 2 should prompt you an error.

There were not that many areas of the code that needed exception handling, only the read part which could yield an
IOError, so most of my exception handling was this and a large try except that covers all the code.

As the logic was pretty simple, it COULD have been implemented with base python data structures, but
I chose to use pandas as I thought that was a good tool for the job and in my working experience, I used it 
rarely.

Things I would do in the future:
- add a Dockerfile that installs all the requirements and could be easier to run without installing dependencies and virtual environments on the local machine
- adding some logging to the code, it was a little overkill for the 5 input files
- maybe taking a course on pandas to use it more efficiently :)
- if the code would get stuffier, grouping functions in other files would be more helpful
- better heuristics for the prediction
