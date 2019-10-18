# -*- coding: utf-8 -*-

import math
import csv
import copy
from itertools import product

AGE_GRANULARITY = 10

def get_records_from_csv(filepath):
    with open(filepath,'r',newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        return [record for record in reader]


def reidentify_patient(record_hospital, voters_list):
    gender = record_hospital['gender']
    age = record_hospital['age']
    zipcode = record_hospital['zipcode']
    # TODO Verify why result show 85% instead of 87%
    # Find the matching record in voters that has the same gender,age and zipcode
    # If exactly one match found, re-identification is successful, set success_ variable to True; otherwise to False
    # Save the matching voting record in a variable called record_voter
    success_ = False
    record_voter = None
    for voter in voters_list:
        if voter['gender'] == gender and voter['age'] == age and voter['zipcode'] == zipcode:
            if record_voter is None:
                record_voter = voter
                success_ = True
            else:
                success_ = False

    if success_:
        return True, record_voter['name'] + ': ' + record_hospital['condition']
    else:
        return False, ''


def generalize_gender(gender: str, level: int):
    assert (type(level) is int and level >= 0)
    assert (gender in ['male', 'female'])

    if level == 0:
        return gender
    else:
        return '*'


def generalize_age(age: int, level: int):
    assert (type(level) is int and level >= 0)
    assert (type(age) is int and age > 0)

    if level == 0:
        return age
    elif 0 < level < 3:
        granularity = AGE_GRANULARITY * level
        age_ = granularity * math.floor(age / granularity)
        return '[%d-%d[' % (age_, age_ + granularity)
    else:
        return '*'


def generalize_zipcode(zipcode: str, level: int):
    assert (type(level) is int and level >= 0)
    assert type(zipcode) is str
    # implement this method using the provided VGH
    if len(zipcode)<= level:
        return '*' * len(zipcode)
    else:
        return zipcode[0:len(zipcode) - level] + '*'*level



def generalize_record(record, level_gender, level_age, level_zipcode):
    record_ = copy.deepcopy(record)
    record_['gender'] = generalize_gender(record['gender'], level_gender)
    record_['age'] = generalize_age(int(record['age']), level_age)
    record_['zipcode'] = generalize_zipcode(record['zipcode'], level_zipcode)
    return record_


def generalize_database(records, level_gender, level_age, level_zipcode):
    # This method generalizes the entire hospital_records
    return [generalize_record(record, level_gender, level_age, level_zipcode) for record in records]


def compute_anonymity_level(records, quasi_identifiers):
    # implement this method
    k = {}
    for line in records:
        qi_vals = tuple(line[qi] for qi in quasi_identifiers)
        if qi_vals not in k:
            k[qi_vals] = 1
        else:
            k[qi_vals] += 1
    return min(k.values())


def compute_distortion(levels, max_levels):
    assert len(max_levels) == len(levels)
    return sum([lq/lq_max for lq, lq_max in zip(levels, max_levels)])/len(levels)


if __name__ == '__main__':

    voters_list = get_records_from_csv('voters.txt')
    hospital_list = get_records_from_csv('hospital_records.txt')

    # Question 1

    # print a list of all successfully re-identified patients with their name and disease
    reidentified = []
    for hospital_record in hospital_list:
        sucess, record =  reidentify_patient(hospital_record, voters_list)
        if sucess:
            reidentified.append(record)

    print(reidentified)
    # print the successful re-identification rate as a percent
    print(len(reidentified)/(len(hospital_list))*100) # len(hospital) = # ligne - header

    # Questions 2 -> 6
    # Question 3
    Gen_hospital_list = generalize_database(hospital_list, 1, 1, 2)
    print(Gen_hospital_list[1])

    # Question 4
    print('Q4 - k anonymity reagrdings to quasi-identifiers', compute_anonymity_level(hospital_list, ['gender', 'age', 'zipcode']))

    # Question 5
    print('Q5 - distorsion of [1,1,2], [1,3,4]', compute_distortion([1,1,2], [1,3,4]))

    # Question 6
    # Compute each possible generalization of hospital_records and pick the optimal one as described in the exercise
    level_gender_max = 1
    level_age_max = 3
    level_zipcode_max = 4
    opt_level_age, opt_level_gender, opt_level_zipcode = 0,0,0
    levels_combination = product([0, 1], [0, 1, 2, 3], [0, 1, 2, 3, 4])  # (gender, age, zipcode)
    k_target = 13
    distortion_opt, k_opt = 1, 0 # 1 is worse distorsion, 0 just to set a useless value
    for gender_level, age_level, zipcode_level in levels_combination:
        geneZ = generalize_database(hospital_list, gender_level, age_level, zipcode_level)
        k_anon = compute_anonymity_level(geneZ, ['age', 'gender', 'zipcode'])
        dist = compute_distortion((gender_level, age_level, zipcode_level),
                                  (level_gender_max, level_age_max, level_zipcode_max))
        if k_anon >= k_target and dist < distortion_opt:  # select levels if anonymyzation is better than the actuals levels and with less distorsion
            opt_level_age, opt_level_gender, opt_level_zipcode = age_level, gender_level, zipcode_level
            distortion_opt, k_opt = dist, k_anon


    # TODO Set variables opt_level_gender, opt_level_age, opt_level_zipcode with the found optimal generalization levels
    # TODO Set variable distortion_opt with the distorsion value of the optimal generalization
    # TODO Set variable k_opt with the k-anonimity value of the optimal generalization

    # TODO Uncomment the following two lines
    params_opt = (opt_level_gender, opt_level_age, opt_level_zipcode)
    s = 'Optimal scheme (targeted k=%d): levels(gender,age,zipcode)=%s, distortion=%.2f, k=%d' % (k_target, str(params_opt), distortion_opt, k_opt)
    print(s)
    with open('h2.txt','w') as f:
        f.write(s)
        print('writen')

