from sklearn.preprocessing import LabelEncoder
from randomforest_model import get_features
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

instances = 2
infofile = "feature_scores.txt"

def get_values(ds, target, features,):
    X = ds.loc[:, features].values
    y = ds[target].values

    #changes the string values to floats
    for i in range(len(features)):
        X[:,i] = LabelEncoder().fit_transform(X[:,i])
    
    return X, y


def write_importance_scores(estimators, feature_names, infofile=infofile):

    file = open(infofile, "a")
    for idx,estimator in enumerate(estimators):
        info = "Features sorted by their score for estimator {}:\n".format(idx)
        print(info)
        file.write(info)

        feature_importances = pd.DataFrame(estimator.feature_importances_, index = feature_names, columns=['importance']).sort_values('importance', ascending=False)# index = diabetes.feature_names, columns=['importance']).sort_values('importance', ascending=False)
        print(feature_importances)
        info = "{}\n".format(feature_importances)
        file.write(info)
    
    file.close()


def main():
    file = "final_test_data_{}instances.csv".format(instances)
    target = 'category'
    starting_fieldnames = ['usage_time', 'hour_of_the_day', 'is_weekend']
    dataset = pd.read_csv(file, encoding = 'latin1')

    features = get_features(instances, starting_fieldnames)
    X, y = get_values(dataset, target, features)

    feature_names = dataset.loc[:, features].columns

    clf = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=0)
    #clf = RandomForestClassifier(n_estimators=20, max_depth=10, random_state=0)
    cv_results = cross_validate(clf, X, y, cv=10, scoring='accuracy', return_estimator=True)

    write_importance_scores(cv_results['estimator'], feature_names)


if __name__ == "__main__":
    main()
