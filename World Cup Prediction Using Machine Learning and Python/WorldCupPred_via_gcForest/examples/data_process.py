# This file processes raw data, extract features and
# transform them into machine learning input format


import numpy as np
import csv
import copy


# data of one match
class Match(object):
    def __init__(self, date, home_team, away_team, home_score, away_score,
                 tournament, city, country, neutral):
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.tournament = tournament
        self.city = city
        self.country = country
        self.neutral = neutral

    def winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        elif self.home_score == self.away_score:
            return "neither"
        else:
            return self.away_team

    def loser(self):
        if self.home_score > self.away_score:
            return self.away_team
        elif self.home_score == self.away_score:
            return "neither"
        else:
            return self.home_team


# rank r of the year
def get_year_rank(y, r):
    return rank8d[y][r - 1]


# champion of the year
def champion(y):
    return rank8d[y][0]


# loseTimeSumary of the year, using match list as input
def loseTimeSumary(li):
    r = {}
    r["neither"] = 0
    for i in li:
        r[i.home_team] = 0
        r[i.away_team] = 0
    for i in li:
        r[i.loser()] += 1
    del (r["neither"])
    return r


# country_involved of the year, using match list as input
def country_involved(li):
    r = {}
    for i in li:
        r[i.home_team] = 1
        r[i.away_team] = 1
    return r


# Beater Tree Structure for a specific year
class BeaterTree(object):

    def __init__(self, li):
        self.li = li
        self.time = self.li[-1].date
        self.beater = {}
        self.beatee = {}
        self.build()
        self.feature = {}
        self.special = {"", "neither", "_year"}
        self.datumTable = {}

    def build(self):
        self.beater = {}
        self.beater["neither"] = ""
        for i in self.li:
            self.beater[i.home_team] = ""
            self.beater[i.away_team] = ""
        # later loss record will overwirte earlier ones auto
        for i in self.li:
            self.beater[i.loser()] = i.winner()
        self.beater[champion(year(self.time))] = ""
        del (self.beater["neither"])

        self.beatee = {}
        self.beatee["neither"] = []
        self.beatee[""] = []  # root
        for i in self.li:
            self.beatee[i.home_team] = []
            self.beatee[i.away_team] = []
        for i in self.beater:
            self.beatee[self.beater[i]].append(i)
        del (self.beatee["neither"])

        return

    def show(self):
        print("-" * 40)
        print(self.time)
        for i in self.feature["_year"]:
            print("%s: %s" % (i, self.feature["_year"][i]))

        def show_country(name, depth):
            rank = str(self.feature[name]["rank"]) if "rank" in self.feature[name] else ""
            print("  " * depth + name + " " + rank)
            for i in self.beatee[name]:
                show_country(i, depth + 1)

        show_country("", 0)
        # # old way:
        # for i in self.beatee:
        #     if i != "" and self.beater[i] == "":
        #         show_country(i, 0)
        return

    def analysis(self):

        # init
        self.feature = {}
        self.feature[""] = {}
        self.feature["neither"] = {}
        for i in self.li:
            self.feature[i.home_team] = {}
            self.feature[i.away_team] = {}

        # depth (recursive)
        def get_depth(name, curd):
            self.feature[name]["depth"] = curd
            for i in self.beatee[name]:
                get_depth(i, curd + 1)

        get_depth("", 0)

        # n_children (recursive)
        def get_n_children(name):
            n = 0
            for i in self.beatee[name]:
                n += get_n_children(i) + 1
            self.feature[name]["n_children"] = n
            return n

        get_n_children("")

        # n_country
        n = len(country_involved(self.li))
        self.feature["_year"] = {"n_country": n}
        # print("%s: %s" % (self.time, n))

        # rank
        curY = year(self.time)
        if curY not in rank8d:
            raise ValueError("year mismatch: %s" % self.time)
        for c in range(8):
            # East Germany = German DR
            # Fedral Germany = West Germany = Germany
            # SU = Russia
            # South Korea = Korea Republic
            v = rank8d[curY][c]
            if v not in self.feature:
                print("country name mismatch: %s %s" %
                      (curY, v))
            else:
                self.feature[v]["rank"] = c + 1

        for c in self.feature:
            if c in self.special or "rank" in self.feature[c]:
                pass
            else:
                self.feature[c]["rank"] = (9 + self.feature["_year"]["n_country"]) / 2

        pass

    # sumarize features into datumTable
    def transform(self):
        # transform feature into a datum table
        # {train: [_year<n_country>, *country<appear?, rank, relative_rank
        # , depth, n_children>], test:  country_id}
        n_dim_per_country = 5
        self.datumTable = {"train": [], "test": []}
        year_feature = list(self.feature["_year"].values())
        dif = n_dim_per_country - len(year_feature)
        if dif < 0:
            raise ValueError("dim per country violation")
        year_feature += [0] * dif
        self.datumTable["train"].append(year_feature)

        for i in get_country_name:
            if i in self.feature:
                cur = [1, self.feature[i]["rank"],
                       self.feature[i]["rank"] / self.feature["_year"]["n_country"],
                       self.feature[i]["depth"],
                       self.feature[i]["n_children"]]
                if len(cur) != n_dim_per_country:
                    raise ValueError("dim per country violation")
                self.datumTable["train"].append(cur)
            else:
                self.datumTable["train"].append([0] * n_dim_per_country)
        self.datumTable["test"] = get_country_id[get_year_rank(year(self.time), 1)]
        return


# check code consistancy
def check():
    # 2002 in JP & NK, other world cups all have same year and country
    # for i in range(1, len(matches)):
    #     if (matches[i].date.split('/', 1)[0] == matches[i - 1].date.split('/', 1)[0]) != (
    #             matches[i].country == matches[i - 1].country):
    #         print(i, matches[i].date.split('/', 1)[0], matches[i - 1].date.split('/', 1)[0], matches[i].country,
    #               matches[i - 1].country)

    # # champion check
    # for i in m_y:
    #     print(i[-1].date, champion(year(i[-1].date)))

    # # n_game
    # for g in m_y:
    #     print(len(g))

    # # lose time
    # for g in m_y:
    #     print(g[-1].date)
    #     li = loseTimeSumary(g)
    #     for i in li:
    #         if li[i] == 0:
    #             print("  %s: %s" % (i, li[i]))

    pass


# get year from date formated like 2018/7/20
def year(s):
    return s.split('/', 1)[0]


# main
if __name__ == "__main__":
    print("Data Processing initialized...")
    # readin match
    matches = []
    reader = csv.reader(open("data.csv"))
    for m in reader:
        matches.append(Match(*m))
    matches = matches[1:]

    # sort by year
    m_y = []
    curY = ""
    curG = []
    for i in matches:
        if year(i.date) == curY:
            curG.append(i)
        else:
            m_y.append(curG)
            curG = [i]
            curY = year(i.date)
    m_y.append(curG)
    m_y = m_y[1:]

    # readin rank feature
    reader = csv.reader(open("rank8x.csv"))
    rank8 = list(reader)
    rank8 = rank8[1:]
    rank8d = {}
    for i in rank8:
        rank8d[i[0]] = i[1:]

    check()

    # bulid a beater tree:
    beaterForest = []
    for g in m_y:
        beaterForest.append(BeaterTree(g))

    # extract feature:
    for t in beaterForest:
        t.analysis()
        t.show()

    # map countries to country_id
    promising_country_set = set()
    other_country_set = set()
    promising_rank = 1  # allow 1 to 8 (1: gcforest don't allow class not appeared)
    for g in rank8d.values():
        for i in range(promising_rank):
            promising_country_set.add(g[i])

    for i in matches:
        if i.home_team not in promising_country_set:
            other_country_set.add(i.home_team)
        if i.away_team not in promising_country_set:
            other_country_set.add(i.away_team)

    promising_country_list = sorted([*promising_country_set])
    other_country_list = sorted([*other_country_set])
    get_country_name = promising_country_list + other_country_list

    get_country_id = {}
    for i in range(len(get_country_name)):
        get_country_id[get_country_name[i]] = i

    if len(get_country_id) != len(get_country_name):
        raise ValueError("Internalogos Error")

    n_promising_country = len(promising_country_list)

    print("n_promising_country: %s" % n_promising_country)

    for i in range(len(promising_country_list)):
        print("%s %s" % (i, promising_country_list[i]))

    # transform to datum table
    for i in beaterForest:
        i.transform()

    # form standard training data and testing data (# skip 2018)
    n_previous_session_used = 5  # -1, -2, -3
    n_sessions = len(beaterForest)
    X = []
    y = []
    for targeted_session in range(n_previous_session_used, n_sessions + 1):
        if targeted_session != n_sessions:
            y.append(beaterForest[targeted_session].datumTable["test"])
        curX = []
        for curS in range(targeted_session - n_previous_session_used, targeted_session):
            curX.append(beaterForest[curS].datumTable["train"])
        X.append(curX)

    # # check
    # print([*map(get_country_name.__getitem__, y)])

    X_train = X[:-1]
    X_test = copy.deepcopy(X[-1:])
    y_train = y
    y_test = copy.deepcopy(y[-1:])  # meaningless until 2022

    # rotation
    default_rotate_time = n_promising_country - 1
    rotate_time = default_rotate_time
    n_train_base = len(X_train)
    for i in range(n_train_base):
        rotate_base = copy.deepcopy(X_train[i])
        curY = y_train[i]
        # rotate
        for r in range(rotate_time):  # rotate time
            for j in range(n_previous_session_used):  # for each previous session
                tmp = copy.deepcopy(rotate_base[j][n_promising_country])
                for k in range(n_promising_country, 1, -1):
                    rotate_base[j][k] = copy.deepcopy(rotate_base[j][k - 1])
                rotate_base[j][1] = tmp
            X_train.append(copy.deepcopy(rotate_base))
            curY = curY + 1 if curY < n_promising_country - 1 else 0
            y_train.append(curY)


    # check is li2 a right shift rotation from li1
    def check_rotate(li1, li2, beg, end):
        def equal(a1, a2):
            if isinstance(a1, list):
                if isinstance(a2, list):
                    if len(a1) == len(a2):
                        for i in range(len(a1)):
                            if not equal(a1[i], a2[i]):
                                return False
                        return True
                    return False
                return False
            if isinstance(a2, list):
                return False
            return a1 == a2

        if len(li1) != len(li2):
            raise ValueError
        for i in range(len(li1)):
            for j in range(beg + 1, end):
                if not equal(li2[i][j], li1[i][j - 1]):
                    raise ValueError
            if not equal(li2[i][beg], li1[i][end - 1]):
                raise ValueError


    for i in range(n_train_base):
        # print(i)
        beg = n_train_base + i * rotate_time
        check_rotate(X_train[i], X_train[beg], 1, n_promising_country + 1)
        for j in [beg + x for x in range(1, rotate_time)]:
            # print(j)
            check_rotate(X_train[j - 1], X_train[j], 1, n_promising_country + 1)

    print([*map(get_country_name.__getitem__, y_train)][:15])

    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    X_train = X_train[:, np.newaxis, :, :]
    X_test = X_test[:, np.newaxis, :, :]

    np.save("X_train", X_train)
    np.save("X_test", X_test)
    np.save("y_train", y_train)
    np.save("y_test", y_test)

    # load check

    X_train = np.load("X_train.npy")
    X_test = np.load("X_test.npy")
    y_train = np.load("y_train.npy")
    y_test = np.load("y_test.npy")

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    print("Data Generation completed. 0 exception raised.")
pass
