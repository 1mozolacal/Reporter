from . import models
from . import constants


def parse_tuple_enumeration(tuples, key):
    for pair in tuples:
        if pair[0] == key:
            return pair[1]
    return None


# ==================CSV to Model Parsers (start)=======================

def csv_to_model(model_name, csv_row):
    model = parse_tuple_enumeration(
        constants.MODEL_ENUMERATION,
        model_name)
    if model == models.Test:
        test_parser(csv_row)
    elif model == models.TestNumbers:
        test_number_parser(csv_row)
    elif model == models.TestText:
        test_text_parser(csv_row)
    else:
        raise Exception(f"No model found when looking for {model_name}")


def test_parser(csv_row):
    if len(csv_row) < 5:
        raise ValueError("csv row is less than 5")
    _, created = models.Test.objects.update_or_create(
        name=csv_row[0],
        data=csv_row[1],
        data_two=csv_row[2],
        data_three=csv_row[3],
        proper=csv_row[4],
    )


def test_number_parser(csv_row):
    if len(csv_row) < 2:
        raise ValueError("csv row is less than 2")
    _, created = models.TestNumbers.objects.update_or_create(
        data_one=csv_row[0],
        data_two=csv_row[1],
    )


def test_text_parser(csv_row):
    if len(csv_row) < 2:
        raise ValueError("csv row is less than 3")
    _, created = models.TestNumbers.objects.update_or_create(
        data_one=csv_row[0],
        data_two=csv_row[1],
    )

# ===================CSV to Model Parsers (end)========================
