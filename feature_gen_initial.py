from pandas import read_csv
from csv import DictWriter
import datetime

filename = 'algorithm_test_data.csv'
raw_features = ["label","timestamp.y","application_name","usage_time","date","datetime","category"]

recurring_features = ['label', 'category', 'application_name', 'usage_time']
fieldnames = recurring_features + ['hour_of_the_day', 'is_weekend', 'last_category', 'time_since_last_app']


def reset_saved_data(label='P1'):
    """
    Resets the saved data dictionary
    Useful when the persons changes
    """
    saved_data = {
        "label": label,
        "last_category": "NA",
        "timestamp": 0
    }
    return saved_data


def saved_data_updater(line, saved_data):
    """
    Updates the 'saved_data' -dictionary
    Returns the 'saved_data' -dictionary
    """
    category = line['category']
    saved_data["last_category"] = category
    saved_data["timestamp"] = line['timestamp.y']

    return saved_data 


def weekend_finder(line, feature):
    """
    Finds if a date (in a format YYYY-MM-DD) is on Friday, Saturday or Sunday
    """
    info = line[feature].split('-')
    date = datetime.datetime(int(info[0]), int(info[1]), int(info[2])).weekday()
    if date > 3:
        return 1
    else:
        return 0


def hour_finder(line, feature):
    """
    Takes line and the feature that respesent date+time
    date+time has to be in a format of 'YYYY-MM-DD HH:MM:SS'
    Returns hour of the day
    """
    info = line[feature].split(' ')
    info = info[1].split(':')
    hour = int(info[0])
    return hour


def row_maker(line, saved_data):

    last_category = saved_data["last_category"]
    if last_category == "NA":
        time_since_last_app = 0
    else:
        time_since_last_app = (float(line['timestamp.y']) - float(saved_data["timestamp"]) ) / 1000
    
    row = {}
    for f in recurring_features:
        row[f] = line[f]
    row['last_category'] = last_category
    row['hour_of_the_day'] = hour_finder(line, 'datetime')
    row['time_since_last_app'] = time_since_last_app
    row['is_weekend'] = weekend_finder(line, 'date')

    return row


def data_writer(writer, line, saved_data, row_maker):
    row = row_maker(line, saved_data)
    writer.writerow(row)
    return saved_data_updater(line, saved_data)


def main():
    #reads the data
    dataset = read_csv(filename, low_memory=False, encoding='ANSI')

    #takes only the relevant features
    dataset = dataset.loc[:, raw_features]#.values

    #removes any instances, where category is other
    dataset = dataset.loc[dataset['category']!='OTHER']

    #writing
    with open('app_with_category.csv', 'w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        #writes the new datafile
        saved_data = reset_saved_data()
        for index, line in dataset.iterrows():

            #checks, if participant has changed, resets the data if necessary
            new_label = line["label"]
            if saved_data["label"] != new_label:
                saved_data = reset_saved_data(new_label)

            #writes the data
            saved_data = data_writer(writer, line, saved_data, row_maker)


if __name__ == "__main__":
    main()
