Weather Man Assignment

This is a Python command-line project that reads weather data files and generates different weather reports.

1. Yearly Report
This command shows:
Highest temperature and date
Lowest temperature and date
Most humid day and humidity
python weatherman.py -e 2005 data_weather/lahore_weather

2. Monthly Average Report
This command shows:
Average highest temperature
Average lowest temperature
Average humidity
python weatherman.py -a 2005/6 data_weather/lahore_weather

3. Monthly Bar Chart
This command shows highest and lowest temperature using colored bar charts.
python weatherman.py -c 2005/6 data_weather/lahore_weather

4. Bonus Chart
This command shows highest and lowest temperature on the same line.
python weatherman.py -b 2005/6 data_weather/lahore_weather