from pandas import read_csv
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression


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


def score_writer(clf, X, y, filename):
    scores = cross_val_score(clf, X, y,  cv=10)
    avg_score = sum(scores) / len(scores)
    file = open(filename, "a")
    file.write("{}: {}\n".format(clf, avg_score))
    file.close()


def main():
    datafile = 'algorithm_test_data.csv'
    target = 'category'
    features = ['hour_of_the_day','usage_time','last_category','time_since_last_app', 'is_weekend']

    X, y = read_data(datafile, target, features)

    #creating the classifiers
    RF = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
    J48 = DecisionTreeClassifier(max_depth=7, random_state=0)
    KNN = KNeighborsClassifier(n_neighbors=300, p=1)
    MLP = MLPClassifier()
    LR3 = LogisticRegression(solver='sag', max_iter=100)
    #SVM = SVC()
    list_of_clfs = [RF, J48, KNN, MLP]

    #resets the txt file
    filename = 'test_scores.txt'
    file = open(filename, "w")
    file.close()

    #rating the classifiers
    for clf in list_of_clfs:
        score_writer(clf, X, y, filename)


if __name__ == "__main__":
    main()
