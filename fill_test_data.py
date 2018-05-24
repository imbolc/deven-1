import json
from pathlib import Path
import requests

import settings


PATH = Path(__file__).resolve().with_name('data')
URL = f'http://{settings.HOST}:{settings.PORT}'


def yield_data():
    if not PATH.is_dir():
        return
    for path in PATH.iterdir():
        if path.is_file() and path.name.endswith('.json'):
            yield path


r = requests.delete(f'{URL}/level3')
r.raise_for_status()
added = 0
for path in yield_data():
    print(f'Processing: {path}')
    docs = json.loads(path.read_text())
    for doc in docs:
        r = requests.post(f'{URL}/level3', json=doc)
        r.raise_for_status()
        print(r.json())
        added += 1


if not added:
    print(f'Put json files into `{PATH}` folder')
else:
    print(f'Added {added} documents')
