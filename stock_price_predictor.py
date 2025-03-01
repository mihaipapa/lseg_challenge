import os
import argparse
import random
import re
import traceback
from datetime import datetime, timedelta

import pandas as pd

from vars import input_folder, csv_regex_pattern, output_folder


def check_value(value):
    """
    Function to check if the input value is within bounds
    :param value: The value to check
    :return: Exception or the value
    """
    ivalue = int(value)
    if ivalue not in range(1, 3):
        raise argparse.ArgumentTypeError(f"{value} is an invalid value, choose between 1 and 2")
    return ivalue


parser = argparse.ArgumentParser()
parser.add_argument('file_number', type=check_value,
                    help="Number of files to be processed from each stock exchange folder")
args = parser.parse_args()
no_files = int(args.file_number)


def get_all_files(directory=input_folder, number_of_files=2):
    """
    Function to return the file structure of the input files.
    :param directory: Directory to search in
    :param number_of_files: Number of files to add to the list
    :return: A list of files from the directories
    """
    regex_check = re.compile(csv_regex_pattern)
    all_files = []
    for (root, folder_list, file_list) in os.walk(directory):
        if len(file_list) == 0:
            continue
        # removing Windows style separators as they were giving me some problems with creating directories
        root = root.replace("\\", "/")
        for index in range(min(len(file_list), number_of_files)):
            filename = file_list[index]
            # only adding csv files to the list, checking it with a regex
            if regex_check.match(filename):
                all_files.append(f"{root}/{filename}")
    return all_files


def return_data_points(filename: str) -> pd.DataFrame:
    """
    A function that returns 10 consecutive data point from a random index
    :param filename: Filename to extract from
    :return: The 10 datapoints in a pandas dataframe
    """
    try:
        col_names = ['Stock', 'Timestamp', 'Value']
        df = pd.read_csv(filename, header=None, names=col_names,
                         dtype={"Stock": str, "Timestamp": str, "Value": float})
    except IOError:
        print("There was a problem opening the file")
        traceback.print_exc()
        exit(-1)
    random_index = random.randint(0, len(df) - 10)
    sliced_df = df.iloc[random_index:random_index + 10].reset_index(drop=True)
    return sliced_df


def predict_next_values(filename: str):
    """
    Function that writes the output of the prediction algorithm into csv files.
    :param filename:
    """
    df = return_data_points(filename)

    last_date = datetime.strptime(df.iloc[-1]['Timestamp'], "%d-%m-%Y")
    stock = df['Stock'][0]

    second_highest = df.sort_values(by="Value").iloc[[-2]]
    df = pd.concat([df, second_highest]).reset_index(drop=True)
    df.loc[len(df) - 1, "Timestamp"] = (last_date + timedelta(days=1)).strftime("%d-%m-%Y")

    second_to_last_value = df.iloc[-2]['Value']
    last_value = df.iloc[-1]['Value']
    middle_value = min(second_to_last_value, last_value) + abs(second_to_last_value - last_value) / 2
    df.loc[len(df)] = [stock, (last_date + timedelta(days=2)).strftime("%d-%m-%Y"), middle_value]

    second_to_last_value = df.iloc[-2]['Value']
    last_value = df.iloc[-1]['Value']
    middle_value = min(second_to_last_value, last_value) + abs(second_to_last_value - last_value) / 4
    df.loc[len(df)] = [stock, (last_date + timedelta(days=3)).strftime("%d-%m-%Y"), middle_value]

    os.makedirs("/".join(filename.split("/")[:-1]).replace(input_folder, output_folder), exist_ok=True)
    df['Value'] = df['Value'].apply(lambda x: round(x, 2))
    df.to_csv(filename.replace(input_folder, output_folder), index=False, header=False)


try:
    filenames = get_all_files(number_of_files=no_files)
    for file in filenames:
        predict_next_values(file)
except:
    traceback.print_exc()
    exit(-1)
