# Predicting the Success of NFL Wide Receivers Based on their College Careers Using Classification Models
Consolidated 2014-2023 NCAA and NFL player data from csv files into a SQLite database. Performed data cleaning, feature selection, data standardization, and dimensionality reduction on receiving data from the wide receiver position to run 7 different classification models to see if a successful season in the NFL can be predicted by a wide receiver player based on their college performance.

## Files:

**Tech used:** Python, SQLite, Microsoft Excel

**csv2SQL.py**: There is a CSV file for each NFL and NCAA season receiving data in the raw_data folder. This file consoldates all CSVs into a SQLite database that is then placed in the raw_data folder.

**dataProcessing.py**: Performs SQL query from the database to extract wide receiver data, which is then cleaned and prcessed before exporting them into the final_data folder as two CSVs, one for the input data (data.csv) and the other for the classification labels (labels.csv).

**Classification.ipynb**: A Jupypter notebook where all the classification models are trained and tested using the cleaned data in the final_data folder.

**Report.pdf**

*The raw_data folder is not included in this public repo because it includes propriety data from PFF.

