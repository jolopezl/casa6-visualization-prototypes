# casa6-visualization-prototypes
A collection of prototypes for data visualization in CASA6

# Dependencies
```
python3.6 -m venv casa6
source casa6/bin/activate
pip install --index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatools
pip install --index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatasks
pip install dash
pip install dash-bootstrap-components
pip install pandas
pip install jupyterlab
pip install jupyter-dash
pip install bokeh
```
Additionally, you need some CASA data (see: https://open-bitbucket.nrao.edu/projects/CASA/repos/casa-data/browse), but you can download a small sample:
```
wget https://bulk.cv.nrao.edu/almadata/public/working/sis14_twhya_calibrated_flagged.ms.tar
tar -xvf sis14_twhya_calibrated_flagged.ms.tar
```
For the dash application, you can paste the path to this MS in the application text box. For the Bokeh application, you must change the code a little bit the let the application where to look at (see lines 20-21 in `bokeh/app.py`).

# Run applications
To run the Dash application:
```
python dash/app.py
```
To run the Bokeh application: 
```
python -m bokeh serve bokeh/app.py
```
