import csv
from collections import defaultdict

import pandas as pd


def xls_to_csv(input_file, output_file):
    """
    Convert an Excel file (XLS/XLSX) to a CSV file.

    :param input_file: Path to the input Excel file.
    :param output_file: Path to save the output CSV file.
    """
    try:
        # Load the Excel file
        df = pd.read_excel(input_file, engine="xlrd")

        # Save it as a CSV file
        df.to_csv(output_file, index=False)
        print(f"Conversion successful! CSV file saved at: {output_file}")

    except Exception as e:
        print(f"Error during conversion: {e}")


def merge_cost_type(input_data):
    # Merging process
    result_data = defaultdict(list)  # Use defaultdict to group data by index

    for index, record in input_data.items():
        cost_type = record["cost_type"]
        # Append the record to the appropriate index key as a list of dictionaries
        result_data[cost_type].append(record)
    return result_data


def export_to_csv(result_data, file_name):
    # Export to CSV
    dst_name: str = "./output/" + file_name.split(".")[0] + "_grouped.csv"

    with open(dst_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(["Cost Type", "Date", "Cost Price", "Total Cost Price"])

        # Write rows for each cost_type and its associated records
        for cost_type, records in result_data.items():
            for record in records:
                writer.writerow([cost_type, record["date"], record["real_cost_price"], record["total_cost_price"]])

    print(f"Grouped data has been exported to {dst_name}")
