import requests
import openpyxl
from io import BytesIO

def load_data(api_url: str):
    try:
        response = requests.get(api_url, timeout=60)
        response.raise_for_status()
        data = BytesIO(response.content)
        workbook = openpyxl.load_workbook(data)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(dict(zip(headers, row)))
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None
    except openpyxl.utils.exceptions.InvalidFileException as e:
        print(f"An error occurred while opening the Excel file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    API_URL = "https://analitika.woysa.club/images/panel/json/download/niches.php?skip=0&price_min=0&price_max=1060225&up_vy_min=0&up_vy_max=108682515&up_vy_pr_min=0&up_vy_pr_max=2900&sum_min=1000&sum_max=82432725&feedbacks_min=0&feedbacks_max=32767&trend=false&sort=sum_sale&sort_dir=-1&id_cat=10000"
    data = load_data(API_URL)
    if data:
        print(data)
    else:
        print("Failed to load data.")

if __name__ == "__main__":
    main()