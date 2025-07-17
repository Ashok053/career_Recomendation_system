# resume_parser/apps/models/trie_keyword_extractor.py

from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, phrase: str):
        node = self.root
        for token in phrase.lower().split():
            node = node.children[token]
        node.is_end = True

    def search(self, words: list, start: int) -> (bool, int):
        node = self.root
        length = 0
        for i in range(start, len(words)):
            token = words[i]
            if token in node.children:
                node = node.children[token]
                length += 1
                if node.is_end:
                    return True, length
            else:
                break
        return False, 0

def build_trie_from_skill_list(skill_list):
    trie = Trie()
    for skill in skill_list:
        trie.insert(skill)
    return trie

def extract_tech_keywords(text: str, trie: Trie):
    words = text.lower().split()
    found = set()
    i = 0
    while i < len(words):
        matched, length = trie.search(words, i)
        if matched:
            phrase = ' '.join(words[i:i+length])
            found.add(phrase)
            i += length
        else:
            i += 1
    return sorted(found)
