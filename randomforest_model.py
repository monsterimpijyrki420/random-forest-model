from pandas import read_csv
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier


def read_data(filename, target, features, encoding='latin1', participant_id=-1):
    """
    Takes csv-file, target feature name and list of other features
    Allows an option to only select data from on participant
    Returns the feature sets (X) and the target set (y)
    """
    dataset = read_csv(filename, encoding = encoding)

    if participant_id != -1:
        dataset = dataset.loc[dataset['label']==participant_id].reset_index(drop=True)

    y = dataset[target].values
    X = dataset.loc[:, features].values

    #changes the string values to floats
    for i in range(len(features)):
        X[:,i] = LabelEncoder().fit_transform(X[:,i])

    return X, y


def get_features(n_instances, fieldnames):
    for n in range(n_instances):
        new_fields = ['category_{}'.format(n+1), 'usage_time_{}'.format(n+1), 'time_since_original_app_{}'.format(n+1)]
        new_fields = new_fields + ['hour_of_the_day_{}'.format(n+1), 'is_weekend_{}'.format(n+1)]
        fieldnames = fieldnames + new_fields
    return fieldnames


def cross_validate(filename, clf, target, starting_fieldnames, max_instances, cv=10, participant_id=-1):
    features = get_features(max_instances, starting_fieldnames)
    X, y = read_data(filename, target, features, participant_id=participant_id)
    scores = cross_val_score(clf, X, y, cv=cv)
    return sum(scores) / len(scores)


def test_instance_data(clf, target, features, n_instances, filename, cv=10):
    """
    used with set amount of instances approach
    filename means the file which scores are saved
    """
    datafile = "final_test_data_{}instances.csv".format(n_instances)
    score = cross_validate(datafile, clf, target, features, n_instances, cv=cv)

    info = "{} instances: {}\n".format(n_instances, score)
    print(info)
    file = open(filename, "a")
    file.write(info)
    file.close()


def test_time_data(clf, target, features, n_instances, timeframe, filename, cv=10):
    """
    used with timeframe approach
    filename means the file which scores are saved
    """
    datafile = "final_test_data_v2_{}seconds.csv".format(timeframe)
    score = cross_validate(datafile, clf, target, features, n_instances, cv=cv)

    info = "{} seconds: {}\n".format(timeframe, score)
    print(info)
    file = open(filename, "a")
    file.write(info)
    file.close()


def get_participant_ids(filename, encoding='latin1'):
    """
    Reads the file, returns list of every unique participant 
    """
    dataset = read_csv(filename, encoding = encoding)
    participant_ids = dataset['label'].unique()
    return participant_ids


#These dont take into consideration of different lengths. Is that a problem?
def individual_scoring_4_instances(clf, target, features, n_instances, filename, cv=10):
    datafile = "final_test_data_{}instances.csv".format(n_instances)
    participants = get_participant_ids(datafile)

    total_score = 0
    for id in participants:
        new_score = cross_validate(datafile, clf, target, features, n_instances, cv=cv, participant_id=id)
        print(new_score)
        total_score = total_score + new_score
    score = total_score / len(participants)
    
    info = "{} instances: {}\n".format(n_instances, score)
    print(info)
    file = open(filename, "a")
    file.write(info)
    file.close()


def individual_scoring_4_seconds(clf, target, features, n_instances, timeframe, filename, cv=10):
    #datafile = "final_test_data_v2_{}seconds.csv".format(timeframe)
    datafile = "final_test_data_v3_{}seconds.csv".format(timeframe)
    participants = get_participant_ids(datafile)

    total_score = 0
    for id in participants:
        new_score = cross_validate(datafile, clf, target, features, n_instances, cv=cv, participant_id=id)
        print(new_score)
        total_score = total_score + new_score
    score = total_score / len(participants)
    
    info = "{} seconds: {}\n".format(timeframe, score)
    print(info)
    file = open(filename, "a")
    file.write(info)
    file.close()



def main():
    target = 'category'
    starting_fieldnames = ['usage_time', 'hour_of_the_day', 'is_weekend']#, 'time_since_last_app']
    n_instances_list = [1, 2, 5, 10, 20]
    n_instances_list = []
    timeframe_list = [(41, 60), (52, 120), (80, 300), (99, 600), (148, 1200)]
    timeframe_list = [(41, 60)]

    instance_file = 'instance_scores_final.txt'
    second_file = 'second_scores_final.txt'
    ind_instance_file = 'ind_instance_scores.txt'
    ind_second_file = 'ind_second_scores.txt'

    clf = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=0)

    for n_ins in n_instances_list:
        test_instance_data(clf, target, starting_fieldnames, n_ins, instance_file)
    
    for time in timeframe_list:
        test_time_data(clf, target, starting_fieldnames, time[0], time[1], second_file)

    #for n_ins in n_instances_list:
    #    individual_scoring_4_instances(clf, target, starting_fieldnames, n_ins, ind_instance_file, cv=10)
    
    for time in timeframe_list:
        individual_scoring_4_seconds(clf, target, starting_fieldnames, time[0], time[1], ind_second_file, cv=10)


if __name__ == "__main__":
    main()
