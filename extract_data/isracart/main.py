import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from extract_data.isracart.utils.utils import xls_to_csv, merge_cost_type, export_to_csv

DATE_INDEX = 0
COST_TYPE_INDEX = 1
TOTAL_COST_PRICE_INDEX = 2
COST_PRICE_INDEX = 4

# Add one month to the current time
now_time: datetime = datetime.now()
next_week: datetime = now_time + timedelta(weeks=1)


def extract_isracart_data(
    start_date: datetime = now_time,
    end_date: datetime = next_week,
):
    try:
        # Collect all .xls files in the folder
        base_path: Path = Path(os.getcwd()) / "extract_data" / "isracart"
        main_data_folder: Path = base_path / "data"
        xls_files = [f for f in os.listdir(main_data_folder) if f.endswith(".xls")]

        # Print the names of the .xls files and read them
        result_data = {}

        for file in xls_files:
            file_path = os.path.join(main_data_folder, file)
            csv_file = f"{main_data_folder}/{file}.csv"
            xls_to_csv(file_path, csv_file)

            try:
                df = pd.read_csv(csv_file)

                # Iterate over each row
                for index, row in df.iterrows():
                    # Check if the first column contains a valid date
                    try:
                        # Adjust 'Unnamed: 0' to the actual column name or index if necessary
                        first_column_value = row.iloc[DATE_INDEX]
                        third_column_value = row.iloc[COST_TYPE_INDEX]

                        if isinstance(first_column_value, str):
                            first_column_value = first_column_value.strip()

                        # Check if it is a date
                        valid_date = datetime.strptime(
                            str(first_column_value), "%d/%m/%Y"
                        )

                        # Check if the third column is a float
                        total_cost_price = float(row.iloc[TOTAL_COST_PRICE_INDEX])
                        real_cost_price = float(row.iloc[COST_PRICE_INDEX])

                        if total_cost_price == real_cost_price:
                            total_cost_price = ""

                        # If it is a date, process the row
                        if start_date <= valid_date <= end_date:
                            result_data[index] = {
                                "date": valid_date,
                                "cost_type": third_column_value,
                                "real_cost_price": real_cost_price,
                                "total_cost_price": total_cost_price,
                            }
                    except Exception as e:
                        # If not a date, skip
                        continue
            except Exception as e:
                print(f"Could not read {file}: {e}")
        merge_result = merge_cost_type(result_data)
        export_to_csv(merge_result)
    except Exception as e:
        print("Error:", e)
