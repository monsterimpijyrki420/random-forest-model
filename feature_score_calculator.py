import re

filename = "feature_scores.txt"


def preprocess_file(filename=filename):
    file = open(filename, "r")
    text = file.read()
    text = text.split("\n")

    #takes the scores, removes the headers
    info_list = []
    for line in text:
        try:
            first_char = line[0]
            if not (first_char == "F" or first_char == " "):
                line = re.sub(' +', ' ', line)
                info_list.append(line)
        except IndexError:
            pass
    
    return info_list

def give_averages(infolist):
    scores = {}

    for line in infolist:
        feature, value = line.split()
        value = float(value)
        try:
            index = scores[feature][1]
            new_index = index + 1

            new_value = (scores[feature][0]*index + value) /  new_index
            scores[feature] = (new_value, index+1)
        except KeyError:
            scores[feature] = (value, 1)

    return scores


def main():
    score_list = preprocess_file()
    scores = give_averages(score_list)
    
    for name in scores:
        print(name, scores[name][0])

if __name__ == "__main__":
    main()
