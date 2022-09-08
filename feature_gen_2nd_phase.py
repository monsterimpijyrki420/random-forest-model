import feature_gen_initial as og
from pandas import read_csv
from csv import DictWriter

#filename = 'final_test_data.csv'
raw_features = ["label","timestamp.y","usage_time","date","datetime","category"]

#recurring_features = ['label', 'category', 'usage_time'] #add application name
starting_fieldnames = ['label', 'category', 'usage_time', 'hour_of_the_day', 'is_weekend']#, 'time_since_last_app']


def first_row_adder(line, current_label): #ds, index, timestamp
    """
    Creates the row, adds the target category's instances data
    """

    #checks that there is a instance before this
    """
    if index > 0:

        #checks that we are dealing with the same participant
        previous_label = ds.loc[index-1]['label']
        if current_label == previous_label:
            previous_timestamp = ds.loc[index-1]['timestamp.y']
            time_since_last_app = ( float(timestamp) - float(previous_timestamp) ) /1000
        else:
            time_since_last_app = 0

    else:
        time_since_last_app = 0
    """
    
    #fills the data
    row = {}
    row['label'] = current_label
    row['category'] = line['category']
    row['usage_time'] = int(line['usage_time'])
    #row['time_since_last_app'] = int(time_since_last_app)
    row['hour_of_the_day'] = og.hour_finder(line, 'datetime')
    row['is_weekend'] = og.weekend_finder(line, 'date')

    return row


def instances_adder(ds, og_index, new_index, position, row):
    """
    adds the new instances to the row or smth
    """
    line = ds.loc[new_index]

    row['category_{}'.format(position)] = line['category']
    row['usage_time_{}'.format(position)] = int(line['usage_time'])

    #Checks if its the first instance by a participant
    if new_index > 0: #1? 
        original_time = float(ds.iloc[og_index]['timestamp.y'])
        current_time = float(line['timestamp.y'])
        time_since_original_app = ( original_time - current_time ) /1000
        row['time_since_original_app_{}'.format(position)] = int(time_since_original_app)
    else:
        row['time_since_original_app_{}'.format(position)] = 0

    row['hour_of_the_day_{}'.format(position)] = og.hour_finder(line, 'datetime')
    row['is_weekend_{}'.format(position)] = og.weekend_finder(line, 'date')
    return row


def empty_feature_filler(row, n_instances):
    """
    used with time frame approach
    fills the empty features if necessary
    """
    intances_already = len(row) / 5 - 1
    extra_instances = n_instances - intances_already
    for n in range(int(extra_instances)):
        division = n_instances - n
        row['category_{}'.format(division)] = 'NOT_AVAILABLE'
        #row['usage_time_{}'.format(division)] = -1 #testaa vaik kaikkea
        #row['time_since_original_app_{}'.format(division)] = -1
        #row['hour_of_the_day_{}'.format(division)] = -1 #?
        #row['is_weekend_{}'.format(division)] = -1
    return row


def row_generator(ds, index, line, n_instances, timeframe=-1):
    """
    creates the new row with the features
    if timeframe is not given, set amount of n_instances will be used
    """
    label = line['label']
    timestamp = line['timestamp.y']
    row = first_row_adder(line, label)

    for n in range(n_instances):
        position = n + 1
        new_index = index - position
        if new_index < 0:
            break

        #checks the id is still the same
        if ds.loc[new_index]['label'] != label:
            break

        #checks, if timeframe has been passed
        if timestamp > ds.loc[new_index]['timestamp.y'] + timeframe and timeframe > 0:
            break

        row = instances_adder(ds, index, new_index, position, row)

    #fills empty features
    if timeframe > 0:
        row = empty_feature_filler(row, n_instances)
    #print(row)
    return row


def write_data(ds, n_instances, filename, timeframe=-1):
    #creates the fieldnames
    fieldnames = starting_fieldnames
    for n in range(n_instances):
        new_fields = ['category_{}'.format(n+1), 'usage_time_{}'.format(n+1), 'time_since_original_app_{}'.format(n+1)]
        new_fields = new_fields + ['hour_of_the_day_{}'.format(n+1), 'is_weekend_{}'.format(n+1)]
        fieldnames = fieldnames + new_fields

    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for index, line in ds.iterrows():
            row = row_generator(ds, index, line, n_instances, timeframe)
            writer.writerow(row)


def main():
    dataset = read_csv('app_with_category.csv', low_memory=False, encoding='ANSI')

    #takes only the relevant features
    dataset = dataset.loc[:, raw_features]#.values

    #removes any instances, where category is other
    dataset = dataset.loc[dataset['category']!='OTHER'].reset_index(drop=True)

    #for testing purposes
    #dataset = dataset.loc[dataset['label']=='P1'].reset_index(drop=True)

    amount_of_instances = [1, 2, 5, 10, 20]

    for n in amount_of_instances:
        filename = "final_test_data_{}{}.csv".format(n, 'instances')
        write_data(dataset, n, filename)

    timeframes = [60, 120, 300, 600, 1200]
    instances_in_tf = [41, 52, 80, 148]

    iterator = 0
    for n_ins in instances_in_tf:
        filename = "final_test_data_v2_{}{}.csv".format(timeframes[iterator], 'seconds')
        write_data(dataset, n_ins, filename, timeframes[iterator]*1000)
        iterator = iterator + 1


if __name__ == "__main__":
    main()
