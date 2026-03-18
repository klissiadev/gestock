from decimal import Decimal

def normalize_llm_data(data):
    normalized = []

    for item in data:
        new_item = {}

        for k, v in item.items():

            if isinstance(v, Decimal):
                new_item[k] = float(v)

            elif v is None:
                new_item[k] = 0

            else:
                new_item[k] = v

        normalized.append(new_item)

    return normalized