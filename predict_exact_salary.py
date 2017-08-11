from nba_py import player
import pandas
import numpy
import csv
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC

def get_games_for_name(name):
    with open('adv_stats.csv') as csvfile:
            nbalist = csv.reader(csvfile)
            data = []
            target = []
            i = 0
            for row in nbalist:
                #print row
                if i == 0:
                    i = i + 1
                    continue
                namee =  row[1]
                namee = namee.split("""\\""")[0]
                #print name

                #if len(name.split()) == 2:
                #    fr, lr = name.split(" ")
                #elif len(name.split()) == 3:
                #    fr, lr, tr = name.split(" ")
                #else:
                #    fr, lr, tr, br = name.split(" ")
                #print fr, lr
                #print f,
                #if fr == f:
                #    if lr == l:
                if namee == name:
                    return row[5]
def get_player_stats(name):
    thename = name
    #print name
    #f, l = name.split(" ")
    #pid = player.get_player(first_name=f,last_name=l)
    #ts = player.PlayerGeneralSplits(player_id=pid,season='2016-17').json
    #print ts['resultSets'][1]['headers']
    #ts = ts['resultSets'][0]['rowSet'][0]
    #return ts
    with open('adv_stats.csv') as csvfile:
            nbalist = csv.reader(csvfile)
            data = []
            target = []
            i = 0
            for row in nbalist:
                #print row
                if i == 0:
                    i = i + 1
                    continue
                namee =  row[1]
                namee = namee.split("""\\""")[0]
                #print name

                #if len(name.split()) == 2:
                #    fr, lr = name.split(" ")
                #elif len(name.split()) == 3:
                #    fr, lr, tr = name.split(" ")
                #else:
                #    fr, lr, tr, br = name.split(" ")
                #print fr, lr
                #print f,
                #if fr == f:
                #    if lr == l:
                if namee == name:
                    per =  row[7]
                    #print per
                    ws48 = row[23]
                    bpm = row[27]
                    return [per,ws48,bpm]
            return [0,0,0]

def get_salary_for_name(name):
    df2 = pandas.DataFrame.from_csv('salary.csv')
    f = 0
    for row in df2.iterrows():
        if f==0:
            f = f + 1
            continue
        #salaries[d[1]['Unnamed: 1']] = d[1]['Salary']
        name2  = row[1]['Unnamed: 1']
        name2 = name2.split("""\\""")[0]
        #print name
        #print name2
        if name2 == name:
            salary = row[1]['Salary']
            salary = salary.replace("$", "")
            salary = int(salary)
            return salary
    return "None"
#array =  get_player_stats("Chris Paul")
#Print array
bball = {}

x = ['max','high','medium','lowish','low']
x = numpy.array(x)
bball['target_names'] = x

df = pandas.DataFrame.from_csv('salary.csv')
salaries = {}
target = []
data = []
i = 0
for d in df.iterrows():
    if i==0:
        i = i + 1
        continue
    #salaries[d[1]['Unnamed: 1']] = d[1]['Salary']
    name  = d[1]['Unnamed: 1']
    name = name.split("""\\""")[0]

    salary = d[1]['Salary']
    salary = salary.replace("$", "")
    salary = int(salary)
    #print name
    target.append(salary)
    data.append(get_player_stats(name))


data = numpy.array(data)
target = numpy.array(target)
print data
print target
bball['data'] = data
#print data

bball['target'] = target
#print target
bball['DESCR'] = 'blah'
feature_names = ['PER','WS/48','BPM']
feature_names = numpy.array(feature_names)
bball['feature_names'] = feature_names
x,y = bball['data'], bball['target']

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    def get_prediction(array):
        lm = LinearRegression()
        lm.fit(x,y)
        result = lm.predict(array)
        return result
        #lonzo_list.append(list(result[0]))
    with open('adv_stats.csv') as csvfile:
            nbalist = csv.reader(csvfile)
            i = 0
            for row in nbalist:
                if i == 0:
                    i = i + 1
                    continue
                namee =  row[1]
                #print row[1]
                namee = namee.split("""\\""")[0]

                per =  float(row[7])
                #print per
                ws48 = float(row[23])
                bpm = float(row[27])
                #print namee
                pred = get_prediction([per,ws48,bpm])
                #print namee
                sal = get_salary_for_name(namee)
                donotprint = 0
                if sal == "None":
                    sal = 0
                    donotprint = 1
                diff = int(sal) - int(pred)
                if diff < 0:
                    if donotprint == 0:
                        print namee + " is getting underpaid at " + str(sal) + ", he should be getting paid "  + str(pred)
    #print get_prediction([35.6,0.278,8.0])
    #
    #linSVC = LinearSVC()
    #linSVC.fit(x,y)
    #'7.7','0.015','-4.1
    #result = linSVC._predict_proba_lr()
    #print result

#print df.axes[1].tolist()

#0-4M
#4M-12M
#12M-20M
#20M-28M
#28M-36M