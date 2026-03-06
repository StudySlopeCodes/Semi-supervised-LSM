1. Prerequisites
1.1 Software Requirements
ArcGIS Desktop / ArcGIS Pro​ (with a valid license for arcpy)
Python 3.5.2​ (must be the version compatible with your ArcGIS installation)
Required Python packages (install via pip):
pip install scikit-learn==0.20.4  # Version compatible with Python 3.5.2
pip install pandas==0.23.4
pip install numpy==1.15.4
pip install openpyxl
pip install matplotlib
1.2 Hardware Recommendations
CPU: Intel i7 5th generation or equivalent
RAM: 8 GB minimum
Disk Space: ~500 GB for data processing and output storage
1.3 Input Data
Place the following files in the project root directory:
CommnSuscep.py​ – Main script
SemiSuscep100.xlsx​ – Training dataset (contains landslide/non-landslide samples and conditioning factors)
test.xlsx​ – Independent test dataset for model validation
fig1.tif… fig8.tif​ – 8 raster maps of landslide conditioning factors (e.g., slope, curvature, lithology, etc.) covering the study area.
Note: File names must match the pattern fig1.tifthrough fig8.tif.
2. How to Run
2.1 Setup Environment
Ensure the Python environment is set to use ArcGIS’s built-in Python 3.5.2​ (usually located at `C:\Python35`or within the ArcGIS installation directory).
Install the required packages listed above in that environment.
2.2 Execute the Model
Run the main script from the command line (within the ArcGIS Python environment) or directly in an IDE configured with arcpy:
python CommnSuscep.py
2.3 What the Script Does
Training Phase:
Reads the training samples and factor values from SemiSuscep100.xlsx.
Trains a semi-supervised landslide susceptibility model using scikit-learnalgorithms (e.g., Self-Training, Label Spreading, or a custom ensemble).
Validation Phase:
Loads the independent test set from test.xlsx.
Evaluates model performance using metrics such as Accuracy, Precision, Recall, AUC, and outputs a validation report.
Prediction (Susceptibility Mapping) Phase:
Reads the 8 factor rasters (fig1.tif… fig8.tif) as predictors.
Applies the trained model to each pixel in the study area to compute landslide susceptibility.
Outputs a Landslide Susceptibility Index (LSI)​ raster (e.g., LSI_map.tif) with values ranging from 0 (low susceptibility) to 1 (high susceptibility).
3. Outputs
After successful execution, the following outputs will be generated in the project directory:
LSI_map.tif​ – Final landslide susceptibility map of the study area.
validation_report.txt​ – Text file containing performance metrics (Accuracy, AUC, etc.) based on the test dataset.
model.pkl​ (optional) – Saved trained model for future use.
4. Notes
The script is designed for ArcGIS/arcpy​ and therefore requires spatial data (rasters) to be in a format recognized by ArcGIS (e.g., .tif, .img).
Ensure that all input rasters (fig1.tif…fig8.tif) have the same extent, cell size, and coordinate system.
If you encounter arcpyimport errors, verify that your Python environment is the one installed with ArcGIS.
5. Contact
For code access, technical questions, or collaboration inquiries, please contact:
Dr. Zhiyong Fu​
Email: fuzhiyong@whu.edu.cn
Institution: Wuhan University
6. License
This code is provided for academic and research purposes. Please cite the associated publication if you use this code in your work.
