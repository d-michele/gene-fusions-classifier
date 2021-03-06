import datetime
import json
import yaml
import logging
import os
import sys
import time

from pprint import pprint

from utils.parse_args_util import get_parsed_params
from utils.pipeline_analysis_util import run_pipeline
from utils.setup_analysis_environment_util import setup_analysis_environment

# =============================================================================================== #
# MAIN UTILS                                                                                      #
# =============================================================================================== #

def read_neural_network_params(cmd_line_params):
    if cmd_line_params.network_parameters is not None:
        network_params_path = cmd_line_params.network_parameters
    else:
        raise Exception('[ERROR] Please define a valid parameters\' filename')        
    
    # Parameters read from file
    network_params = get_neural_network_params_from_file(network_params_path)

    # It it exists, weights of a pre-trained model are loaded
    network_params['pretrained_model'] = cmd_line_params.pretrained_model
    return network_params

def get_neural_network_params_from_file(network_params_path: str) -> dict:
    result_dict: dict = None

    with open(network_params_path, "r") as f:
        if network_params_path.endswith('json'):
            result_dict = json.load(f)
        elif network_params_path.endswith('yaml'):
            result_dict = yaml.load(f)
    return result_dict

def run_test_decorator(a_test):
    def wrapper_function(a_dict):
        flag_test_passed: bool = True 
        try:
            message: str = f" [*] Running TEST for function {a_test.__name__}"
            print()
            print(f"{message}", '-' * len(message), sep='\n')

            result = a_test(a_dict)
        except Exception as err:
            print(f'ERROR: {str(err)}')
            flag_test_passed = False
            sys.exit(-1)
        finally:
            status_test: str = 'PASSED' if flag_test_passed is True else 'FAILED'
            message: str = f" [*] TEST on function {a_test.__name__} ended with STATUS = {status_test}"
            print()
            print(f"{message}", '-' * len(message), sep='\n')
        return result
    return wrapper_function

# =============================================================================================== #
# TESTS SECTION                                                                                   #
# =============================================================================================== #

@run_test_decorator
def test_pipeline_util(test_info_dict: dict):

    # Data to let function to be tested
    conf_load_dict = test_info_dict['conf_load_dict']
    conf_preprocess_dict = test_info_dict['conf_preprocess_dict']
    cmd_line_params = test_info_dict['cmd_line_params']
    network_params = test_info_dict['network_params']
    meta_info_project_dict = test_info_dict['meta_info_project_dict']
    main_logger = test_info_dict['main_logger']

    # Load Data.
    run_pipeline(
        conf_load_dict=conf_load_dict,
        conf_preprocess_dict=conf_preprocess_dict,
        cmd_line_params=cmd_line_params,
        network_params=network_params,
        meta_info_project_dict=meta_info_project_dict,
        main_logger=main_logger
    )
    pass

# =============================================================================================== #
# MAIN FUNCTION                                                                                   #
# =============================================================================================== #

def main(cmd_line_params: dict):

    base_dir: str = 'bioinfo_project'
    network_params = read_neural_network_params(cmd_line_params)
    

    print(f"----> Set up analysis environment.")
    logger, meta_info_project_dict =  \
        setup_analysis_environment(
            logger_name=__name__,
            base_dir=base_dir,
            params=cmd_line_params,
            flag_test=True)
    logger.info("\n" + json.dumps(network_params, indent=4))

    
    # ------------------------------------------------------ # 
    # Here - Test pipeline util

    conf_load_dict: dict = {
        'sequence_type': cmd_line_params.sequence_type,
        'path': cmd_line_params.network_parameters,
        'columns_names': [
            'Sequences','Count','Unnamed: 0','Label','Translated_sequences','Protein_length'
        ],
        'train_bins': [1,2,3],
        'val_bins': [4],
        'test_bins': [5],
    }

    conf_preprocess_dict: dict = {
        'padding': 'post',
        'maxlen': network_params['maxlen'],
        'onehot_flag': False,
    }

    pipeline_info_dict : dict = {
        'conf_load_dict': conf_load_dict,
        'conf_preprocess_dict': conf_preprocess_dict,
        'cmd_line_params': cmd_line_params,
        'network_params': network_params,
        'meta_info_project_dict': meta_info_project_dict,
        'main_logger': logger,

    }

    test_pipeline_util(pipeline_info_dict)

    pass

if __name__ == "__main__":

    # Useless rigth now. Just ignore
    dict_images: dict = {
        'loss': {
            'title': 'Training With Validation Loss',
            'fig_name': 'train_val_loss',
            'fig_format': 'png',
            'savefig_flag': True
        },
        'acc': {
            'title': 'Training With Validation Accuracy',
            'fig_name': 'train_val_acc',
            'fig_format': 'png',
            'savefig_flag': True
        },
        'roc_curve': {
            'title': 'Roc Curve',
            'fig_name': 'roc_curve',
            'fig_format': 'png',
            'savefig_flag': True
        },
        'confusion_matrix': {
            'title': 'Confusion Matrix',
            'fig_name': 'confusion_matrix',
            'fig_format': 'png',
            'savefig_flag': True
        }
    }

    cmd_line_params, _ = get_parsed_params()

    main(cmd_line_params)
    pass