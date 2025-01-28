from datetime import datetime, timedelta

from extract_data.isracart.main import extract_isracart_data
from extract_data.isracart.utils import utils


if __name__ == "__main__":
    # utils.extract_diff_fields("extract_data/isracart/output/grouped.csv", "extract_data/isracart/data/Export_1_01_2025.xls.csv")
    current_month = datetime.now().month
    start_date = datetime.strptime(f"01/12/2024", "%d/%m/%Y")
    end_date = datetime.strptime(f"20/01/2025", "%d/%m/%Y")
    # end_date = start_date + timedelta(weeks=5)
    extract_isracart_data(start_date, end_date)

    print("Done!")
