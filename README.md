## Launching The Application  
The application is prepared as a Jupyter notebook containing the main UI generated using ipywidgets. Please follow the steps below to launch the application:  
1. Open the project repository in an IDE like Virtual Studio Code  
2. Install dependecies in requirements.txt (either into local environment or a created virtual environment)  
3. Run main UI in main.ipynb using a Python3 kernel. Development was done using Pythgon 3.12.7
4. The entry point of the tool is in main.ipynb, simply run all cells to generate the main UI. Restart the kernel as required to reset the state  
  
Note: If the cell runs but UI is not shown, try closing and relaunching your IDE.  
  
## Description of Application  
This tool was created to run Monte Carlo simulations for a single period newsvendor problem, allowiong the user to determine the optimal order quantity using simulation 
methods. The tool is split into three main sections:  
1. Instructions and Assumptions section providing guidance on how to use the application and detailing key assumptions made  
2. Control Panel / Input Parameters section where user keys in input variables to the Monte Carlo simulation. Relevant charts are generated using the respective button
widgets.  
3. Output section where output text and charts are displayed. The output area can be reset / cleared using the Clear Output Area button  
  
## Repository Structure  
1. main.ipynb - entry point / main jupyter notebook file to launch UI  
2. core.py - contains main Python class object to store data / state  
3. UI.py - holds all widget objects and charting functions  
4. UI_constants.py - holds constants used by UI.py  
5. README.md - contains instrutions on how to setup and use application  
6. requirements.txt - file containing required packages, use to setup virtual environment  

