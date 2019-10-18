# -*- coding: utf-8 -*-

import math
import csv
import copy

AGE_GRANULARITY = 10


def reidentify_patient(record_hospital):
    gender = record_hospital['gender']
    age = record_hospital['age']
    zipcode = record_hospital['zipcode']
    # TODO Find the matching record in voters that has the same gender,age and zipcode
    # TODO If exactly one match found, re-identification is successful, set success_ variable to True; otherwise to False
    # TODO Save the matching voting record in a variable called record_voter

    success_ = False # TODO DELETE THIS LINE
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
    #TODO implement this method using the provided VGH
    # result = ...

    result = '*' # TODO DELETE THIS LINE
    return result


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
    # TODO implement this method
    # k = ...

    k = -1 # TODO DELETE THIS LINE
    return k


def compute_distortion(levels, max_levels):
    assert len(max_levels) == len(levels)
    # TODO implement this method
    # d = ...

    d = -1 # TODO DELETE THIS LINE
    return d


if __name__ == '__main__':

    with open('voters.txt') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        voters_records = [record for record in reader]
    # for record in voters_records:
    #    print(record['name'], record['gender'], record['age'], record['zipcode'])

    with open('hospital_records.txt') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        hospital_records = [record for record in reader]

    # Question 1

    # TODO print a list of all successfully re-identified patients with their name and disease

    # TODO print the successful re-identification rate as a percent


    # Questions 2 -> 6

    k_target = 5

    level_gender_max = -1 # TODO Use the VGH to replace with the correct value
    level_age_max =  -1 # TODO Use the VGH to replace with the correct value
    level_zipcode_max = -1  # TODO Use the VGH to replace with the correct value

    # TODO Compute each possible generalization of hospital_records and pick the optimal one as described in the exercise

    # TODO Set variables opt_level_gender, opt_level_age, opt_level_zipcode with the found optimal generalization levels
    # TODO Set variable distortion_opt with the distorsion value of the optimal generalization
    # TODO Set variable k_opt with the k-anonimity value of the optimal generalization

    # TODO Uncomment the following two lines
#    params_opt = (opt_level_gender, opt_level_age, opt_level_zipcode)
#    print('Optimal scheme (targeted k=%d): levels(gender,age,zipcode)=%s, distortion=%.2f, k=%d' % (k_target, str(params_opt), distortion_opt, k_opt))

