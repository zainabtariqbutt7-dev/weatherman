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

    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                lines = []

                for line in file:
                    if line.strip() != "":
                        lines.append(line)

                reader = csv.DictReader(lines, skipinitialspace=True)

                for row in reader:
                    date_text = row.get("PKT") or row.get("GST")

                    if date_text:
                        try:
                            row["date"] = datetime.strptime(date_text, "%Y-%m-%d")
                            weather_data.append(row)
                        except:
                            pass

    return weather_data


def yearly_report(data, year):
    high_temp = None
    low_temp = None
    high_humidity = None

    high_temp_date = None
    low_temp_date = None
    humidity_date = None

    for row in data:
        if row["date"].year == year:
            try:
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
                humidity = int(row.get("Max Humidity"))
            except:
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

    if high_temp is None:
        print("No data found.")
    else:
        print(f"Highest: {high_temp}C on {high_temp_date.strftime('%B %d')}")
        print(f"Lowest: {low_temp}C on {low_temp_date.strftime('%B %d')}")
        print(f"Humid: {high_humidity}% on {humidity_date.strftime('%B %d')}")


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
            except:
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
            found = True

            try:
                day = row["date"].day
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
            except:
                continue

            print(f"{day:02d} {RED}{'+' * max_temp}{RESET} {max_temp}C")
            print(f"{day:02d} {BLUE}{'+' * min_temp}{RESET} {min_temp}C")

    if not found:
        print("No data found.")


def bonus_chart(data, year, month):
    print(f"{month_name[month]} {year}")

    found = False

    for row in data:
        if row["date"].year == year and row["date"].month == month:
            found = True

            try:
                day = row["date"].day
                max_temp = int(row.get("Max TemperatureC"))
                min_temp = int(row.get("Min TemperatureC"))
            except:
                continue

            print(f"{day:02d} {BLUE}{'+' * min_temp}{RED}{'+' * max_temp}{RESET} {min_temp}C - {max_temp}C")

    if not found:
        print("No data found.")


def main():
    if len(sys.argv) < 4:
        print("Wrong command.")
        return
    option = sys.argv[1]
    date = sys.argv[2]
    folder = sys.argv[3]

    data = read_files(folder)

    if option == "-e":
        yearly_report(data, int(date))

    elif option == "-a":
        year, month = date.split("/")
        monthly_average(data, int(year), int(month))

    elif option == "-c":
        year, month = date.split("/")
        monthly_chart(data, int(year), int(month))

    elif option == "-b":
        year, month = date.split("/")
        bonus_chart(data, int(year), int(month))

    else:
        print("Wrong option.")


main()