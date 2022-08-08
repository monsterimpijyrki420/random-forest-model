from pandas import read_csv
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier


def read_data(filename, target, features, encoding='latin1'):
    """
    Takes csv-file, target feature name and list of other features
    Returns the feature sets (X) and the target set (y)
    """
    dataset = read_csv(filename, encoding = encoding)

    y = dataset[target].values
    X = dataset.loc[:, features].values

    #changes the string values to floats
    for i in range(len(features)):
        X[:,i] = LabelEncoder().fit_transform(X[:,i])

    return X, y


if __name__ == "__main__":
    target = 'category'
    features = ['hour_of_the_day','usage_time','last_category','time_since_last_app','most_used_category_in_5_inst', 'is_weekend']

    X, y = read_data("test_data0.csv", target, features)
    clf = RandomForestClassifier(n_estimators=75, max_depth=10, random_state=0)

    scores = cross_val_score(clf, X, y,  cv=8)
    avg = sum(scores) / len(scores)
    print(avg)
