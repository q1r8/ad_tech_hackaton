import argparse

from pathlib import Path

import pandas as pd

import requests
from preprocessing_data.preprocess_input_data import preprocess_dataframe
import json 

with open('preprocessing_data/city_coords.json', 'r') as f:
    cities_coords = json.load(f)

URL = 'http://10.10.67.145:5010/api/test'
headers = {'Content-type': 'application/json'}


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('Predict segments')
    parser.add_argument('--csv_input', '-ci', help='название csv для предсказывания сегментов')
    parser.add_argument('--csv_output', '-co', help='название csv с предсказанными сегментами')
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    csv_input_path = Path(args.csv_input)
    csv_output_path = Path(args.csv_output)

    if (str(args.csv_input).endswith('.gz')) or (str(args.csv_input).endswith('.gzip')):
        df = pd.read_csv(csv_input_path)
    else:
        df = pd.read_csv(csv_input_path)
    df_for_predicts = preprocess_dataframe(df, cities_coords)

    r = requests.post(URL, data=json.dumps(df_for_predicts.to_dict()), headers=headers)

    df['Segment'] = eval(r.json()['predicts'])
    df.to_csv(csv_output_path, index=False)

