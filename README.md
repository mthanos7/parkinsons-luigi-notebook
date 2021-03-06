# parkinsons-luigi-notebook

## Abstract
Parkinson' disease is a progressive disorder of the central nervous system affecting movement and inducing tremors and stiffness. It's a neurodegenerative disorder affecting dopamine-producing neurons in the brain and is estimated to affect 1 percent of the global population over the age of 50. It is chronic, and currently has no cure.

This project’s goal is to develop a scalable, organized, modular and reusable pipeline to execute analyses on data surrounding Parkinson’s disease. To accomplish this, a combination of Git, Jupyter and Luigi is used; this particular project utilizes the ability to use Luigi to turn Python notebooks into Luigi tasks to create the pipeline. While the exploration of this project focuses on Parkinson’s disease, the hope is that the pipeline structure will be easily repeatable in being able to execute different notebook based workflows.

## Setting up your environment

Make sure that Python is installed on your machine. On Mac, install it using homebrew with:
```bash
brew install python3
```

Clone this repository:
```bash
git clone git@github.com:mthanos7/parkinsons-luigi-notebook.git
```

cd to the root of the new repository, parkinsons-luigi-notebook.git and install packages with pipenv:
```bash
pipenv install
```
or
```bash
pipenv install -r requirements .txt
```

Run the setup.py file:
```bash
python setup.py
```

Follow the instructions that appear on the Terminal screen to set some environment variables for the project in your ~/.bash_profile or ~.zshrc. In particular, you will be asked to add something like this:
```bash
export PYTHONPATH=$PYTHONPATH:/Users/mthanos7/Git/parkinsons-luigi-notebook
export LUIGI_CONFIG_PATH=/Users/mthanos7/Git/parkinsons-luigi-notebook/luigi/luigi.conf
```

cd into the project repository and you're all set!

## Executing the notebooks into Luigi tasks using the JupyterNotebookClass
Configure a Python 3 Jupyter kernel which we will name luigi_notebook_py3. You can do this by executing:
```bash
python -m ipykernel install --user --name luigi_notebook_py3
```

Trigger the pipeline using the following command for producing a feature importance plot based on a random forest classification (this runs the Random Forest model with 50 trees using information gain/entropy as the splitting criterion, and limits to 3 the number of randomly sampled features that are used to determine the splits),
```bash
luigi --module tasks ProducePlot --n-estimators 50 --criterion entropy --max-features 3
```

and for generating an accuracy score based on XGBoost,
```bash
luigi --module tasks XGBPredict
```

## Technology overview
#### Pipeline
- Git(hub) (for version control)
- Jupyter (for notebook based data analysis)
- Luigi (to execute notebook based tasks)
- AWS (to download the data file)
- cookiecutter (to set up directory)
- pipenv (to isolate project in a virtual environment)

#### Analysis
- sklearn (RandomForestClassifier)
- XGBoost
- numpy
- pandas
- matplotlib
- pickle

# Pipeline overview
### Notebooks (.ipynb)
- prepare_data.ipynb: Notebook that cleans and organizes the dataset to be model-ready depending on intended analysis.
- fit_model.ipynb: Fits the model to the data (random forest classifier in this project).
- produce_plot.ipynb: Generates an output (a feature importance graph for this project).
- parkinsons_detection.ipynb: Self contained notebook workflow that uses XGBoost to detect the presence of onset Parkinson's disease.

### Luigi tasks (tasks.py)
- PrepareData: outputs a CSV file named model_ready_data.csv with the model-ready data that we use to train the RandomForest classifier.
- FitModel: add some parameters that are used in the notebook to control how we fit the Random Forest.
- ProducePlot: Runs the random forest model and generates a feature importance plot.
- XGBPredict: Runs the parkinsons_detection.ipynb notebook that contains the entire workflow based on XGBoost and writes to a xgb_predict_score.txt file.

### Output
- model_ready_data.csv: Output CSV of the model-ready data. 
- model_fit.pkl: Saved .pkl model using pickle.
- importances_plot.png: Output feature importance plot.
- xgb_predict_score.txt: Output .txt of printed accuracy score with XGBoost

