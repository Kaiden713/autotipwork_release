# Stable and Public Version of Autotipwork
automated tip conditioning program for Omicron scanning tunneling microscope

## Usage
### On Local STM Compter
* Download all the files in this repository in a local folder.
* Change the remotepath and installpath in `STM.py` to the directory for RemoteAccess_API.dll and Matrix program folder, respectively.
* Run `auto_tipwork_main.py` or `autotipworkui.py` in the IDLE. 
* The machine learning model in this repository is for 32 bit system. If you are running the program on 64 bit system, run `didv_training_ada.py` to train the machine learning model locally.
* To see if your Matrix environment (RemoteAccess_API.dll file) is 32 bit or 64 bit, run 'test_connection.py' on a 32 bit or 64 bit python IDLE separately. The code can only be run in one version.

### Python Packages Required
* numpy, scipy, matplotlib, sklearn, joblib
