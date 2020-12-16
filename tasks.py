import os

import luigi

from util import get_config
from jupyter_notebook import JupyterNotebookTask

repo_path = get_config('paths', 'parkinsons-luigi-notebook')
notebooks_path = os.path.join(repo_path, 'notebooks')
output_path = os.path.join(repo_path, 'output')


class PrepareData(JupyterNotebookTask):
    """
    A notebook that produces synthetic classification data.
    """
    notebook_path = os.path.join(notebooks_path, 'prepare_data.ipynb')
    kernel_name = 'luigi_tutorial_py3'
    timeout = 60

    def output(self):
        return luigi.LocalTarget(os.path.join(
            output_path, 'model_ready_data.csv')
        )


class FitModel(JupyterNotebookTask):
    """
    A notebook that fits a Random Forest classifier.
    """
    notebook_path = os.path.join(notebooks_path, 'fit_model.ipynb')
    kernel_name = 'luigi_tutorial_py3'

    n_estimators = luigi.Parameter(
        default=200
    )

    criterion = luigi.Parameter(
        default='gini'
    )

    max_features = luigi.Parameter(
        default=50
    )

    def requires(self):
        return PrepareData()

    def output(self):
        return luigi.LocalTarget(os.path.join(
            output_path,
            'model_fit.pkl'
        ))


class ProducePlot(JupyterNotebookTask):
    """
    A notebook that produces a visualization about the Random Forest
    classifier fit.
    """
    notebook_path = luigi.Parameter(
        default=os.path.join(notebooks_path, 'produce_plot.ipynb')
    )

    kernel_name = luigi.Parameter(
        default='luigi_tutorial_py3'
    )

    n_estimators = luigi.Parameter(
        default=200
    )

    criterion = luigi.Parameter(
        default='gini'
    )

    max_features = luigi.Parameter(
        default=50
    )

    def requires(self):
        return {
            'data': PrepareData(),
            'model': FitModel(
                n_estimators=self.n_estimators,
                criterion=self.criterion,
                max_features=self.max_features
            )
        }

    def output(self):
        return luigi.LocalTarget(os.path.join(
            output_path,
            'importances_plot.png'
        ))


class XGBPredict(JupyterNotebookTask):
    """
    A notebook that produces a visualization about the Random Forest
    classifier fit.
    """
    notebook_path = os.path.join(notebooks_path, 'parkinsons_detection.ipynb')
    kernel_name = 'luigi_tutorial_py3'
    timeout = 60

    def output(self):
        return luigi.LocalTarget(
            os.path.join(output_path, 'xgb_predict_score.txt')
        )
