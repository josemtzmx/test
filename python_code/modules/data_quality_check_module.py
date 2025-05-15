import pandas as pd
import re
import os

REQUIRED_FIELDS = ['name', 'phone', 'location']
OUTPUT_DIR = 'output'

def clean_phone(phone):
    clean = re.sub(r'[^\d,]', '', str(phone))
    phones = clean.split(',')
    phones = [p for p in phones if p.isdigit()]
    return phones if phones else None

def clean_text(text):
    return re.sub(r'[^\w\s,.-]', '', str(text)) if pd.notnull(text) else text

def run_data_quality_checks(input_file):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(input_file, on_bad_lines='skip')

    valid_records = []
    bad_records = []
    issue_meta = {}

    for i, row in df.iterrows():
        issues = []

        for field in REQUIRED_FIELDS:
            if pd.isnull(row[field]) or str(row[field]).strip() == '':
                issues.append('null')

        cleaned_phones = clean_phone(row['phone'])
        if not cleaned_phones:
            issues.append('invalid_phone')

        row['address'] = clean_text(row.get('address', ''))
        row['reviews_list'] = clean_text(row.get('reviews_list', ''))

        row_dict = row.to_dict()
        row_dict['phone_1'] = cleaned_phones[0] if cleaned_phones else None
        row_dict['phone_2'] = cleaned_phones[1] if cleaned_phones and len(cleaned_phones) > 1 else None

        if issues:
            bad_records.append(row_dict)
            for issue in issues:
                issue_meta.setdefault(issue, []).append(i + 2)
        else:
            valid_records.append(row_dict)

    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    pd.DataFrame(valid_records).to_csv(os.path.join(OUTPUT_DIR, f'{base_filename}.out'), index=False)
    pd.DataFrame(bad_records).to_csv(os.path.join(OUTPUT_DIR, f'{base_filename}.bad'), index=False)
    pd.DataFrame([
        {'type_of_issue': k, 'row_num_list': v} for k, v in issue_meta.items()
    ]).to_csv(os.path.join(OUTPUT_DIR, f'{base_filename}_metadata.csv'), index=False)