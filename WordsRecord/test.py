from wordsrecord import WordsRecord

if __name__ == "__main__":
    nested_dict = {'a': {'b': {'c': [12, 23]}}}
    print(nested_dict.values())
    print(WordsRecord.get_deep_meaning(nested_dict))

    print(WordsRecord.search_meaning("account"))
