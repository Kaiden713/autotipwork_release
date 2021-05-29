# Stable and Public Version of Autotipwork
Automated tip conditioning program for Omicron scanning tunneling microscope. Aimed to obtain STM tips in good condition for scanning tunneling spectroscopy on Au(111).

## Authors
* Shenkai Wang, Junmian Zhu, Raymond Blackwell, and Felix R. Fischer
* A paper describing the methods used in this program is published here https://pubs.acs.org/doi/10.1021/acs.jpca.0c10731. If you find this program useful, we would greatly appreciate it if you can cite this paper in your publications.
* A provisional patent has been applied for the methods used in this program.

## Usage
### On Local STM Computer
* Download all the files in this repository in a local folder.
* Change the remotepath and installpath in `STM.py` to the directory for RemoteAccess_API.dll and Matrix program folder, respectively.
* To see if your Matrix environment (RemoteAccess_API.dll file) is 32 bit or 64 bit, run `test_connection.py` on a 32 bit or 64 bit python IDLE. The code should only be able to run in one version. The Matrix environment can be 32 bit even if your windows 64 bit.
* The machine learning model in this repository is for 32 bit Matrix environment. If your Matrix environment is 64 bit, run `didv_training_ada.py` to train the machine learning model locally.
* Before running this program, make sure that the STM can obtain good topographic images and can obtain STS point spectra. The STM tips need to be manually conditioned for topographic images.
* In the Matrix software, make sure the Z channel is always saved. The program will automatically save the Aux2 channel for STS point spectra. You also need to manually set the ZRamp (poking) parameters (recommended parameters: poke depth 2 nm, ramp rate 1 nm/s) and STS parameters (recommended parameters: bias range -2 V to 2 V, points collected 1024, stay 90 ms on each point, lock-in amplifier time constant: 30 ms). The bias range for STS point spectra needs to be larger than -1.5 V to 2 V. If other time constants are used, change the waiting time in `auto_tipwork_main.py` or `autotipworkui.py` accordingly.
* Run `auto_tipwork_main.py` or `autotipworkui.py`.

### Python Packages Required
* numpy, scipy, matplotlib, sklearn, joblib
* Can be run directly in Anaconda

## UC Berkeley's Copyright and Disclaimer Notice
* Copyright ©2021. The Regents of the University of California (Regents). All Rights Reserved. Permission to use, copy, modify, and distribute this software and its documentation for educational, research, and not-for-profit purposes, without fee and without a signed licensing agreement, is hereby granted, provided that the above copyright notice, this paragraph and the following two paragraphs appear in all copies, modifications, and distributions. Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue, Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu, http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
