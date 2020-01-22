import argparse
import datetime
import os
import sys
import time


def _get_custom_parser(subdir: str) -> object:

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--subdir', default=subdir, help='Checkpoints directory')
    parser.add_argument('--validation', default=False, help='Perform Holdout-Validation for hyperparameter selection', action='store_true')
    parser.add_argument('--train', default=False, help='Train model on whole training data and save it', action='store_true')
    parser.add_argument('--test', default=False, help='Test saved model, in the specified subdir, on test bin', action='store_true')
    parser.add_argument('--batch_size', default=10, help='Number of sample for each training step',type=int)
    parser.add_argument('--num_epochs', default=50, help='Number of epochs before halting the training',type=int)
    parser.add_argument('--lr', default=1e-3, help='Learning rate coefficient',type=float)
    parser.add_argument('--sequence_type', default='protein', choices=['dna', 'protein'], help='Type of sequence to process in the model: "dna" or "protein"', type=str)
    parser.add_argument('--pretrained_model', help='Path where to find the weights of a pre-trained model', type=str, default=None)
    parser.add_argument('--network_parameters', default=None, help='File with neural network parameters, either json or yaml format', type=str)
    parser.add_argument('--load_network', default=None, help='Architecture\'s name. According to this a different model is loaded', type=str)
    parser.add_argument('--onehot_flag', default=False, help='If true, it encodes data by using one-hot encodin, otherwise embedding representation is used', action='store_true')
    parser.add_argument('--steps', default=None, help='Number of steps of training', type=int)
    parser.add_argument('--path_source_data', default='./data/bins_translated', help='Path that specifies the location of source datasets.', type=str)
    parser.add_argument('--create_spredsheet_report', default=False, help='Flag that allows to automatically generate a spredsheet-like report, when included esplicitly before running the program.', action='store_true')
    parser.add_argument('--experimental_mode', default=False, help='Flag that allows to run analysis tool in a experimental manner, when included esplicitly before running the program.', action='store_true')
 
    params = parser.parse_args()

    return params, parser

def get_parsed_params() -> dict:

    subdir: str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
    subdir_date: str = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d') 
    subdir_time: str = datetime.datetime.strftime(datetime.datetime.now(), '%H_%M_%S') 

    params, parser = _get_custom_parser(subdir)

    if params.subdir != subdir:
        params.subdir = \
            os.path.join(f"{params.subdir}", f"{subdir_date}", f"train_{subdir_time}")
    return params, parser