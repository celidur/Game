import pickle

with open('language/language.txt', 'rb') as file:
    file = pickle.Unpickler(file)
    language = file.load()

print(language)