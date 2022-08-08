import csv
import datetime

num_of_recent_categories = 4

def reset_saved_data(label):
    """
    Resets the saved data dictionary
    Useful when the persons changes
    """
    saved_data = {
        "current_label": label,
        "last_category_used": "NOT_AVAILABLE",
        "most_recent_categories": ["NOT_AVAILABLE"] * num_of_recent_categories,
        "timestamp": 0
    }
    return saved_data


def saved_data_updater(line, saved_data):
    """
    Updates the saved_data dictionary
    """
    category = line['category']
    saved_data["last_category_used"] = category

    del saved_data["most_recent_categories"][0]
    saved_data["most_recent_categories"].append(category)

    saved_data["timestamp"] = line['timestamp.y']

    return saved_data 


def weekend_finder(line):
    """
    Finds if a date (in a format YYYY-MM-DD) is on Friday, Saturday or Sunday
    """
    info = line['date'].split('-')
    date = datetime.datetime(int(info[0]), int(info[1]), int(info[2])).weekday()
    if date > 3:
        return 1
    else:
        return 0


def hour_finder(line):
    info = line['datetime'].split(' ')
    info = info[1].split(':')
    hour = int(info[0])
    return hour


def get_saved_data(line, saved_data):
    time_since_last_app = 0
    last_category = saved_data["last_category_used"]

    last_X_categories = saved_data["most_recent_categories"]
    if "NOT_AVAILABLE" in last_X_categories:
        most_common_category = "NOT_AVAILABLE"
    else:
        most_common_category = max(set(last_X_categories), key=last_X_categories.count)
    
    if saved_data["timestamp"] !=0:
        time_since_last_app = (float(line['timestamp.y']) - float(saved_data["timestamp"]) ) / 1000
    return last_category, most_common_category, int(time_since_last_app)


def new_data_writer(writer, line, saved_data):
    hour = hour_finder(line)
    is_weekend = weekend_finder(line)
    last_c, most_common_c, time_since_last_app = get_saved_data(line, saved_data)

    writer.writerow({'label': line['label'], 'usage_time': line['usage_time'], 'last_category': last_c, 'time_since_last_app': time_since_last_app,'most_used_category_in_5_inst': most_common_c, 'hour_of_the_day': hour, 'is_weekend': is_weekend,'category': line['category'], 'app_name': line['application_name']})


if __name__ == "__main__":
    with open('app_with_category.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('test_data1.csv', 'w', newline='') as csvfile:
            fieldnames = ['label', 'hour_of_the_day', 'usage_time', 'last_category', 'time_since_last_app', 'most_used_category_in_5_inst', 'is_weekend', 'category', 'app_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            saved_data = reset_saved_data('P1')
            while True:
                try:
                    line = reader.__next__()
                    if line['label'] == "P4":
                        break
                except StopIteration:
                    break
                if line['category'] != 'OTHER':
                    if line['label'] != saved_data["current_label"]:
                        saved_data = reset_saved_data(line['label'])
                    new_data_writer(writer, line, saved_data)
                    saved_data = saved_data_updater(line, saved_data)
