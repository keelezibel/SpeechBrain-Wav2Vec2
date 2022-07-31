"""
Downloads and creates data manifest files for IEMOCAP
(https://paperswithcode.com/dataset/iemocap).

Authors:
 * Mirco Ravanelli, 2021
 * Modified by Pierre-Yves Yanni, 2021
 * Abdel Heba, 2021
 * Yingzhi Wang, 2022
"""

import os
import sys
import re
import json
import random
import logging
from glob import glob
from speechbrain.dataio.dataio import read_audio

logger = logging.getLogger(__name__)
SAMPLERATE = 16000


def prepare_data(
    data_original,
    save_json_train,
    save_json_valid,
    save_json_test,
    split_ratio=[80, 10, 10],
    seed=12,
):
    """
    Prepares the json files for the IEMOCAP dataset.

    Arguments
    ---------
    data_original : str
        Path to the folder where the original IEMOCAP dataset is stored.
    save_json_train : str
        Path where the train data specification file will be saved.
    save_json_valid : str
        Path where the validation data specification file will be saved.
    save_json_test : str
        Path where the test data specification file will be saved.
    split_ratio: list
        List composed of three integers that sets split ratios for train,
        valid, and test sets, respecively.
        For instance split_ratio=[80, 10, 10] will assign 80% of the sentences
        to training, 10% for validation, and 10% for test.
    seed : int
        Seed for reproducibility
    """

    # setting seeds for reproducible code.
    random.seed(seed)

    # Check if this phase is already done (if so, skip it)
    if skip(save_json_train, save_json_valid, save_json_test):
        logger.info("Preparation completed in previous run, skipping.")
        return

    # Map emotions to wavs
    emo_dict = transform_data(data_original)

    # List files and create manifest from list
    logger.info(f"Creating {save_json_train}, {save_json_valid}, and {save_json_test}")

    data_split = split_sets(emo_dict, split_ratio)

    # Creating json files
    create_json(data_split["train"], save_json_train)
    create_json(data_split["valid"], save_json_valid)
    create_json(data_split["test"], save_json_test)


def create_json(wav_list, json_file):
    """
    Creates the json file given a list of wav information.

    Arguments
    ---------
    wav_list : list of list
        The list of wav information (path, label, gender).
    json_file : str
        The path of the output json file
    """

    json_dict = {}
    for obj in wav_list:
        wav_file = obj
        emo = os.path.dirname(obj).split(os.path.sep)[-1]
        # Read the signal (to retrieve duration in seconds)
        signal = read_audio(wav_file)
        duration = signal.shape[0] / SAMPLERATE

        # Create entry for this utterance
        json_dict[wav_file] = {
            "wav": wav_file,
            "length": duration,
            "emo": emo,
        }

    # Writing the dictionary to the json file
    with open(json_file, mode="w") as json_f:
        json.dump(json_dict, json_f, indent=2)

    logger.info(f"{json_file} successfully created!")


def skip(*filenames):
    """
    Detects if the data preparation has been already done.
    If the preparation has been done, we can skip it.

    Returns
    -------
    bool
        if True, the preparation phase can be skipped.
        if False, it must be done.
    """
    for filename in filenames:
        if not os.path.isfile(filename):
            return False
    return True


def split_sets(emo_dict, split_ratio):
    """Randomly splits the wav list into training, validation, and test lists.

    Arguments
    ---------
    emo_dict : list
        a dictionary of emotions and its corresponding audio information
    split_ratio: list
        List composed of three integers that sets split ratios for train,
        valid, and test sets, respectively.
        For instance split_ratio=[80, 10, 10] will assign 80% of the sentences
        to training, 10% for validation, and 10% for test.

    Returns
    ------
    dictionary containing train, valid, and test splits.
    """

    wav_list = []
    for key in emo_dict.keys():
        wav_list.extend(emo_dict[key])

    # Random shuffle of the list
    random.shuffle(wav_list)
    tot_split = sum(split_ratio)
    tot_snts = len(wav_list)
    data_split = {}
    splits = ["train", "valid"]

    for i, split in enumerate(splits):
        n_snts = int(tot_snts * split_ratio[i] / tot_split)
        data_split[split] = wav_list[0:n_snts]
        del wav_list[0:n_snts]
    data_split["test"] = wav_list

    return data_split


def transform_data(path_loadData):
    """
    Create a dictionary that maps emotions and corresponding wavs

    Arguments
    ---------
    path_loadData : str
        Path to the folder where the original dataset is stored.
    """

    emotions = os.listdir(path_loadData)
    emo_dict = {str(emo): [] for emo in emotions if emo != "README.md"}

    for emo in emotions:
        emo_files = os.listdir(os.path.join(path_loadData, emo))
        emo_dir = os.path.join(path_loadData, emo)
        emo_dict[emo] = [os.path.join(emo_dir, file) for file in emo_files]

    return emo_dict
