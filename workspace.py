# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   06/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================

"""
Description:
This module is the workspace for the simulation environment where:
    - paths and directories can be defined
    - experiments can be performed
    - measurement results can be saved
    - results can be evaluated
"""


# %% Experiment: Testing

import os
from swarmy.experiment import Experiment

# ----- generate measurement results file -----
measFolderPath = os.getcwd() + "\\measurements\\"
captFolderPath = os.getcwd() + "\\capture\\"

exp1 = Experiment()

measFilePath = exp1.run(10, 1, measFolderPath, captFolderPath, [-60, True])
