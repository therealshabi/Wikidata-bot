import nltk


# pos tagging using NLTK
def parts_of_speech(query_sentence, query_properties):
    sentences = nltk.sent_tokenize(query_sentence)
    tokenized = [nltk.word_tokenize(sentence) for sentence in sentences]
    pos_tags = [nltk.pos_tag(sentence) for sentence in tokenized]
    print(pos_tags[0])

    # extracting query properties i.e. common nouns from the query sentence which is tagged as NN by POS tagger
    for name, tag in pos_tags[0]:
        if tag == 'NN':
            # for handling queries like head-of-government which would be queries as a singular head of government
            name = name.split("-")
            name = " ".join(name)
            query_properties.append(name)
    print(query_properties)
    chunked_sents = nltk.ne_chunk_sents(pos_tags, binary=True)
    return chunked_sents


def find_entities(corpus):
    query_properties = []
    chunks = parts_of_speech(corpus, query_properties)

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
    return named_entities, query_properties
