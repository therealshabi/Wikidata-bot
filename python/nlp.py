import nltk

query_properties = []

def parts_of_speech(corpus):
    "returns named entity chunks in a given text"
    sentences = nltk.sent_tokenize(corpus)
    tokenized = [nltk.word_tokenize(sentence) for sentence in sentences]
    pos_tags = [nltk.pos_tag(sentence) for sentence in tokenized]
    print(pos_tags[0])
    for name, tag in pos_tags[0]:
        if tag == 'NN':
            query_properties.append(name)
    print(query_properties)
    chunked_sents = nltk.ne_chunk_sents(pos_tags, binary=True)
    return chunked_sents


def find_entities(corpus):
    chunks = parts_of_speech(corpus)

    def traverse(tree):

        entity_names = []

        if hasattr(tree, 'label') and tree.label:
            if tree.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in tree]))
            else:
                for child in tree:
                    entity_names.extend(traverse(child))

        return entity_names

    named_entities = []

    for chunk in chunks:

        entities = sorted(list(set([word for tree in chunk
                                    for word in traverse(tree)])))
        for e in entities:
            if e not in named_entities:
                named_entities.append(e)
    return named_entities