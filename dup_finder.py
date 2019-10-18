#!/usr/bin/python3


import mmh3
import argparse
from bitarray import bitarray
import ruletoken
import xml.etree.ElementTree as et







def getRules(dg):
    """Returns a list of security policies from the supplied device group"""
    pre_rules = dg.findall('pre-rulebase/security/rules/*')
    post_rules = dg.findall('post-rulebase/security/rules/*')
    return pre_rules, post_rules


def ruleCheck(target, donor):
    """Builds bloom filter based on rules in target device group and checks for
    duplicates in the donor ruleset"""
    # Create and initialize bit array
    rule_filter = bitarray(10000000)
    rule_filter.setall(0)
    # Load rule tokens for target DG into bloom filter
    target_rule_dict = {}
    for rule in target:
        token_tuple = ruletoken.genToken(rule)
        token = token_tuple[1]
        target_rule_dict[token_tuple[1]] = token_tuple[0]
        hash_count = 0
        while hash_count < 4:
            hash_result = mmh3.hash(token, hash_count) % 10000000
            rule_filter[hash_result] = 1
            hash_count += 1
    # Check rule tokens for donor DG against bloom filter
    for rule in donor:
        token_tuple = ruletoken.genToken(rule)
        token = token_tuple[1]
        hash_count = 0
        hash_track = 0
        while hash_count < 3:
            hash_result = mmh3.hash(token, hash_count) % 10000000
            if rule_filter[hash_result] == 0:
                break
            else:
                hash_track += 1
                hash_count += 1
        if hash_track == 3:
            print("{} from the donor DG has a possible match with {} in the target DG.".format(rule.attrib['name'], target_rule_dict[token]))
    return






def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--donor', help='Name of the donor device group')
    parser.add_argument('-t', '--target', help='Name of the target device group')
    parser.add_argument('-c', '--config', help='Path to the configuration file')
    args = parser.parse_args()





    # Parse XML config
    config = et.parse(args.config)
    config_root = config.getroot()
    dg_list = config_root.findall('./devices/entry/device-group/*')
    tdg = None
    ddg = None
    for dg in dg_list:
        if dg.attrib['name'] == args.target:
            print('Target match found!!')
            tdg = dg
        elif dg.attrib['name'] == args.donor:
            print('Donor match found!!')
            ddg = dg
    if (tdg or ddg) == None:
        if tdg == None:
            print('Error finding target device group. Please check name and '
                  'try again.')
            exit(1)
        else:
            print('Error finding donor device group. Please check name and '
                  'try again.')
            exit(1)
    # Get lists of Pre and Post rules for both donor and target device groups
    donor_pre, donor_post = getRules(ddg)
    target_pre, target_post = getRules(tdg)
    ruleCheck(target_pre, donor_pre)
    ruleCheck(target_post, donor_post)











if __name__ == "__main__":
    main()