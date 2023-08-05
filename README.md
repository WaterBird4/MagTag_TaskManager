# MagTag_TaskManager
Project to use the Adafruit MagTag as a Task Randomizer and Manager.


### Project Updates

#### Updated 5 Aug 2023
I am actively working on this project. 

One of the first challenges I faced was to determine which tasks should be included in the randomized data set.  I decided it would be best to use google sheets to store the data for now. I wrote a python script using google colab that takes data from a tasks spreadsheet and a results spreadsheet, performs some logic and then creates 3 separate spreadsheets for the 3 bins I divide the tasks into. In this part of the code I am most proud of how I solved the sub-tasks problem, where a task requires other tasks to be completed before it can be finished. 

The next step is to write the circuit python to pull the data from the spreadsheets onto the MagTag. My plan is to use 3 of the buttons to pick which bucket to select a random task. I have divided the tasks into 3 bins for how long it will take to complete the tasks. 

Once I can pull, display and interact with the data on the MagTag I will write the circuit python to send the results of whether I completed the task, skipped the task or didn't respond to the prompt to another google sheet. After I complete this I plan to use the MagTag Task Randomizer to help me with my tasks and to start gathering data for the machine learning model I plan to use in my next project.
