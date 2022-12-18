from pandas import read_csv

raw_features = ["label","timestamp.y","category"]

def instances_in_timeframe(ds, timeframe, line, index):
    """
    n_inst = 0
    while True:
        index = index - 1
        last_timestamp = ds.loc[index]()
    """

    label = line['label']
    timestamp = line['timestamp.y']

    #this went through the whole list multiple times -> really slow
    """
    #checks id
    #ds = ds.loc[ds['label'] == line['label']]

    #takes only smaller timestamp values
    #ds = ds.loc[ds['timestamp.y'] < timestamp]

    #checks the timeframe
    #ds = ds.loc[ds['timestamp.y'] >= (timestamp - timeframe)]
    """

    counter = 0
    while True:
        index = index - 1
        if index < 0:
            break

        #checks label
        new_label = ds.loc[index]['label']
        if label != new_label:
            break

        #checks timestamp
        new_timestamp = ds.loc[index]['timestamp.y']
        if timestamp > new_timestamp + timeframe:
            break

        counter = counter + 1

    return counter
    #return len(ds)


def max_instances_in_timeframe(ds, timeframe):
    """
    takes dataset and timeframe in seconds
    returns the max instances that were recorded in that timeframe
    """
    max_instances = 0
    for index, line in ds.iterrows():
        new_instances = instances_in_timeframe(ds, timeframe*1000, line, index)

        if max_instances < new_instances:
            max_instances = new_instances

    return max_instances


def instances_writer(ds, timelist, filename):

    #resets the file
    #file = open(filename, "w")
    #file.close()

    for timeframe in timelist:
        max_inst = max_instances_in_timeframe(ds, timeframe)
        file = open(filename, "a")
        file.write("{}s: {}\n".format(timeframe, max_inst))
        file.close()
        #print(timeframe)


def main():
    dataset = read_csv('app_with_category.csv', low_memory=False, encoding='ANSI')

    #takes only the relevant features
    dataset = dataset.loc[:, raw_features]#.values

    #removes any instances, where category is other
    dataset = dataset.loc[dataset['category']!='OTHER'].reset_index(drop=True)

    #dataset = dataset.loc[dataset['label']=='P92'].reset_index(drop=True)

    timeframes = [60, 120, 300, 1200]
    timeframes = [600]
    instances_file = 'max_instances_in_timeframe.txt'
    instances_writer(dataset, timeframes, instances_file)


if __name__ == "__main__":
    main()
