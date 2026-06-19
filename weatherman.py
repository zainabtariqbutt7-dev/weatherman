import os
import sys
import csv
from datetime import datetime
from calendar import month_name


RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def read_files(folder):
    weather_data = []

    if not os.path.isdir(folder):
        print(f"Error: folder '{folder}' not found.")
        return weather_data

    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    lines = []

                    for line in file:
                        if line.strip() != "":
                            lines.append(line)

            except OSError:
                print(f"Warning: could not read '{file_name}', skipping.")
                continue

            reader = csv.DictReader(lines, skipinitialspace=True)

            for row in reader:
                date_text = row.get("PKT") or row.get("GST")

                if date_text:
                    try:
                        row["date"] = datetime.strptime(date_text, "%Y-%m-%d")
                        weather_data.append(row)
                    except ValueError:
                        pass

    return weather_data


def monthly_data(data, year, month):
    high_temp = None
    low_temp = None
    high_humidity = None

    high_temp_date = None
    low_temp_date = None
    humidity_date = None

    for row in data:
        if row["date"].year == year and row["date"].month == month:
            try:
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
                humidity = int(row.get("Max Humidity"))
            except (TypeError, ValueError):
                continue

            if high_temp is None or max_temp > high_temp:
                high_temp = max_temp
                high_temp_date = row["date"]

            if low_temp is None or min_temp < low_temp:
                low_temp = min_temp
                low_temp_date = row["date"]

            if high_humidity is None or humidity > high_humidity:
                high_humidity = humidity
                humidity_date = row["date"]

    return high_temp, high_temp_date, low_temp, low_temp_date, high_humidity, humidity_date


def yearly_report(data, year):
    final_high_temp = None
    final_low_temp = None
    final_high_humidity = None

    final_high_temp_date = None
    final_low_temp_date = None
    final_humidity_date = None

    for month in range(1, 13):
        high_temp, high_temp_date, low_temp, low_temp_date, high_humidity, humidity_date = monthly_data(data, year, month)

        if high_temp is not None and (final_high_temp is None or high_temp > final_high_temp):
            final_high_temp = high_temp
            final_high_temp_date = high_temp_date

        if low_temp is not None and (final_low_temp is None or low_temp < final_low_temp):
            final_low_temp = low_temp
            final_low_temp_date = low_temp_date

        if high_humidity is not None and (final_high_humidity is None or high_humidity > final_high_humidity):
            final_high_humidity = high_humidity
            final_humidity_date = humidity_date

    if final_high_temp is None:
        print("No data found.")
    else:
        print(f"Highest: {final_high_temp}C on {final_high_temp_date.strftime('%B %d')}")
        print(f"Lowest: {final_low_temp}C on {final_low_temp_date.strftime('%B %d')}")
        print(f"Humid: {final_high_humidity}% on {final_humidity_date.strftime('%B %d')}")


def monthly_average(data, year, month):
    max_sum = 0
    min_sum = 0
    humidity_sum = 0
    count = 0

    for row in data:
        if row["date"].year == year and row["date"].month == month:
            try:
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
                humidity = int(row.get("Mean Humidity"))
            except (TypeError, ValueError):
                continue

            max_sum += max_temp
            min_sum += min_temp
            humidity_sum += humidity
            count += 1

    if count == 0:
        print("No data found.")
    else:
        print(f"Highest Average: {max_sum // count}C")
        print(f"Lowest Average: {min_sum // count}C")
        print(f"Average Humidity: {humidity_sum // count}%")


def monthly_chart(data, year, month):
    print(f"{month_name[month]} {year}")

    found = False

    for row in data:
        if row["date"].year == year and row["date"].month == month:
            try:
                day = row["date"].day
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
            except (TypeError, ValueError):
                continue

            found = True

            print(f"{day:02d} {RED}{'+' * max_temp}{RESET} {max_temp}C")
            print(f"{day:02d} {BLUE}{'+' * min_temp}{RESET} {min_temp}C")

    if not found:
        print("No data found.")


def bonus_chart(data, year, month):
    print(f"{month_name[month]} {year}")

    found = False

    for row in data:
        if row["date"].year == year and row["date"].month == month:
            try:
                day = row["date"].day
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
            except (TypeError, ValueError):
                continue

            found = True

            print(f"{day:02d} {BLUE}{'+' * min_temp}{RED}{'+' * max_temp}{RESET} {min_temp}C - {max_temp}C")

    if not found:
        print("No data found.")


def parse_year(date):
    try:
        return int(date)
    except ValueError:
        print(f"Error: '{date}' is not a valid year.")
        return None


def parse_year_month(date):
    parts = date.split("/")

    if len(parts) != 2:
        print(f"Error: '{date}' is not a valid year/month, expected format YYYY/MM.")
        return None, None

    try:
        year = int(parts[0])
        month = int(parts[1])
    except ValueError:
        print(f"Error: '{date}' is not a valid year/month, expected format YYYY/MM.")
        return None, None

    if month < 1 or month > 12:
        print(f"Error: month '{month}' is invalid, must be between 1 and 12.")
        return None, None

    return year, month


def main():
    if len(sys.argv) != 4:
        return

    option = sys.argv[1]
    date = sys.argv[2]
    folder = sys.argv[3]

    data = read_files(folder)

    if len(data) == 0:
        print("No weather data found.")
        return

    if option == "-e":
        year = parse_year(date)

        if year is not None:
            yearly_report(data, year)

    elif option == "-a":
        year, month = parse_year_month(date)

        if year is not None:
            monthly_average(data, year, month)

    elif option == "-c":
        year, month = parse_year_month(date)

        if year is not None:
            monthly_chart(data, year, month)

    elif option == "-b":
        year, month = parse_year_month(date)

        if year is not None:
            bonus_chart(data, year, month)

    else:
        print("Wrong option.")
        print("Use -e, -a, -c, or -b")


main()