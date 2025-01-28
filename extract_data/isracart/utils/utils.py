import os
import csv
from collections import defaultdict
from pathlib import Path

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

    except Exception as e:
        print(f"Error during conversion: {e}")


def define_cost_level(cost):
    if cost >= 1000:
        return "***Very High***"
    if cost >= 200:
        return "*High*"
    elif cost >= 100:
        return "Medium"
    else:
        return "Low"


def merge_cost_type(input_data):
    # Merging process
    result_data = defaultdict(list)  # Use defaultdict to group data by index

    for index, record in input_data.items():
        cost_type = record["cost_type"]
        # Append the record to the appropriate index key as a list of dictionaries
        result_data[cost_type].append(record)
    return result_data


def sort_by_level_and_cost(summarize):
    cost_level_order = {
        "***Very High***": 1,
        "*High*": 2,
        "Medium": 3,
        "Low": 4
    }

    # Sort the list by cost level (high to low) and cost_per_type (high to low)
    summarize.sort(
        key=lambda x: (cost_level_order[x["cost_level"]], -x["cost_per_type"]),
        reverse=False  # Sort first by cost level and then by cost_per_type descending
    )
    return summarize


def export_to_csv(result_data):
    # Export to CSV
    base_path = Path(os.getcwd()) / "extract_data" / "isracart"
    base_path.mkdir(parents=True, exist_ok=True)  # Ensure the directories exist

    dst_name = base_path / "output" / "grouped.csv"
    dst_name.parent.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

    with open(dst_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(
            ["Cost Type", "Date", "Cost Price", "Total Cost Price", "Index"]
        )

        # Initialize variables
        costs_sum = 0
        index = 1
        summarize = []

        # Write rows for each cost_type and its associated records
        for cost_type, records in result_data.items():
            cost_per_type = sum(record["real_cost_price"] for record in records)
            for record in records:
                writer.writerow(
                    [
                        cost_type,
                        record["date"],
                        record["real_cost_price"],
                        record["total_cost_price"],
                        index,
                    ]
                )
                index += 1
                costs_sum += record["real_cost_price"]
            summarize.append(
                {
                    "cost_type": cost_type,
                    "cost_per_type": cost_per_type,
                    "cost_level": define_cost_level(cost_per_type),
                }
            )

        # Write summarize section
        writer.writerow([])  # Add an empty line for separation
        writer.writerow(["Summarized Costs"])  # Add a header for summaries

        summarize = sort_by_level_and_cost(summarize)

        for entry in summarize:
            writer.writerow(
                [
                    entry["cost_type"],
                    "",
                    entry["cost_per_type"],
                    entry["cost_level"],
                    "",
                ]
            )

        # Write total cost summary
        writer.writerow([])
        writer.writerow(["Total Costs", "", "", costs_sum])


def extract_diff_fields(origin_csv, result_csv):
    # Load the CSV files
    origin_df = pd.read_csv(origin_csv)
    result_df = pd.read_csv(result_csv)

    # Initialize dictionaries to count occurrences
    origin_dict = {}
    result_dict = {}

    # Iterate through origin_df and count occurrences
    for row in origin_df.itertuples():  # index=False excludes the row index
        row = list(row)
        key = row[0]  # Adjust column index as needed
        if key in origin_dict:
            origin_dict[key] += 1
        else:
            origin_dict[key] = 1

    # Iterate through result_df and count occurrences
    for row in result_df.itertuples(index=False):  # index=False excludes the row index
        key = row[1]  # Adjust column index as needed
        if key in result_dict:
            result_dict[key] += 1
        else:
            result_dict[key] = 1

    # Compare dictionaries
    added_keys = {
        key: result_dict[key] for key in result_dict if key not in origin_dict
    }
    removed_keys = {
        key: origin_dict[key] for key in origin_dict if key not in result_dict
    }
    changed_keys = {
        key: (origin_dict[key], result_dict[key])
        for key in origin_dict
        if key in result_dict and origin_dict[key] != result_dict[key]
    }

    print(f"Added keys: {added_keys}")
    print(f"Removed keys: {removed_keys}")
    print(f"Changed keys: {changed_keys}")
