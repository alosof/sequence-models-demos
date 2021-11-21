from datetime import date, timedelta
from itertools import product, chain
from pathlib import Path
from random import randint, choice
from typing import List, Tuple

import click
import pandas as pd


@click.command()
@click.option('--start-date', type=click.DateTime(formats=["%d-%m-%Y"]), default='01-01-1800')
@click.option('--end-date', type=click.DateTime(formats=["%d-%m-%Y"]), default='31-12-2050')
@click.option('--train-size', type=int, default=10000)
@click.option('--test-size', type=int, default=15000)
@click.option('--output-directory', type=Path, default=Path(__file__).parent)
def create_datasets(start_date: date, end_date: date, train_size: int, test_size: int, output_directory: Path) -> None:
    generated_dataset = generate_date_pairs(start_date=start_date,
                                            end_date=end_date,
                                            size=train_size + test_size,
                                            input_formats=get_input_date_formats(),
                                            target_format='%d-%m-%Y')
    train_dataset = generated_dataset[:train_size]
    test_dataset = generated_dataset[train_size:]
    save(train_dataset, output_directory / 'train_dates.csv')
    save(test_dataset, output_directory / 'test_dates.csv')


def generate_date_pairs(start_date: date, end_date: date, size: int, input_formats: List[str],
                        target_format: str) -> List[Tuple[str, str]]:
    unique_random_dates = set()
    while len(unique_random_dates) < size:
        random_date = get_random_date(start_date, end_date)
        unique_random_dates.add(random_date)
    return [
        (random_date.strftime(choice(input_formats)), random_date.strftime(target_format))
        for random_date in unique_random_dates
    ]


def get_input_date_formats() -> List[str]:
    day_name_formats = ['', '%A ', '%A, ', '%a ', '%a. ']
    day_formats = ['%d']
    month_formats = ['-%m-', '/%m/', '.%m.', ' %m ', ' %B ', ' %b ', ' %b. ']
    year_formats = ['%Y']

    return [''.join(parts)
            for parts in chain(product(day_name_formats, day_formats, month_formats, year_formats),
                               product(day_name_formats, year_formats, month_formats, day_formats))]


def get_random_date(start_date: date, end_date: date) -> date:
    date_range = (end_date - start_date).days
    return start_date + timedelta(days=randint(0, date_range))


def save(dataset: List[Tuple[str, str]], output_file: Path) -> None:
    dataframe = pd.DataFrame(columns=['input', 'target'], data=dataset)
    dataframe.to_csv(output_file, header=True, index=False, sep=';')


if __name__ == '__main__':
    create_datasets()
