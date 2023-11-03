import csv
import itertools
import os
import re

import pypdf

expense_pattern = re.compile(
    r"(\bJan\b|\bFeb\b|\bMar\b|\bApr\b|\bMay\b|\bJun\b|\bJul\b|\bAug\b|\bSep\b|\bOct\b|\bNov\b|\bDec\b) (\d{1,2}), (\d{4}) (.+?) \$(\d{1,3}(?:,\d{3})*\.\d{2})"
)


# Function to parse a page string and extract expense items
def parse_expenses(page_string):
    # Find all matches in the page string
    matches = expense_pattern.findall(page_string)
    # Extract the expense items
    expenses = [
        {
            "Date": "{} {}, {}".format(m[0], m[1], m[2]),
            "Description": m[3].strip(),
            "Amount": m[4],
        }
        for m in matches
    ]
    return expenses


def write_to_csv(expenses, filename):
    # Check if file exists to determine if we need to write headers
    write_header = not os.path.isfile(filename)

    with open(filename, "a", newline="") as csvfile:
        fieldnames = ["Date", "Description", "Amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()  # Write header if file didn't exist

        for expense in expenses:
            writer.writerow(expense)


def main():
    FILE_PATH = "/PATH/credit_card.pdf"
    OUT_FILE_PATH = "/PATH/expenses.csv"
    pdf_reader = pypdf.PdfReader(FILE_PATH)
    all_expenses = []
    for page in pdf_reader.pages:
        all_expenses.extend(parse_expenses(page.extract_text()))
    write_to_csv(all_expenses, OUT_FILE_PATH)


if __name__ == "__main__":
    main()
