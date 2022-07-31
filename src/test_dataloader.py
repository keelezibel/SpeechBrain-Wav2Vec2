from dataprep import prepare_data
from hyperpyyaml import load_hyperpyyaml

hparams_file = "../hparams/hyperparams.yaml"
# Load hyperparameters file with command-line overrides.
with open(hparams_file) as fin:
    hparams = load_hyperpyyaml(fin, None)
prepare_data("../data","../data/train.json","../data/valid.json","../data/test.json")