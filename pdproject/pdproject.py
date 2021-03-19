import re
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
CORPUS_DIR = config['DEFAULT']['CorpusDirectory']
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
if VERBOSE:
    print("Verbose output enabled.")

class Document:
    """
    Object used to store a parsed textfile. Document contains the filename, as well as a list 
    of paragraphs and sentences. Document objects are intended to be stored within the Corpus 
    object.

    __init__(filename: str)

    Methods:
    \tadd_paragraphs(), add_sentences(), info(), print_paragraphs(), print_sentences().
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.paragraphs = []
        self.sentences = []

    def add_paragraphs(self, paragraphs: list):
        """Attaches a list of strings into a Document object's paragraphs list."""
        if type(paragraphs) is list:
            self.paragraphs += paragraphs
        else:
            raise TypeError("Parameter of add_sentences() was {type} and must be of type 'list'.".format(type=type(paragraphs)))

    def add_sentences(self, sentences: list):
        """Attaches a list of strings into a Document object's sentences list."""
        if type(sentences) is list:
            self.sentences += sentences
        else:
            raise TypeError("Parameter of add_sentences() was {type} and must be of type 'list'.".format(type=type(sentences)))

    def info(self):
        """Outputs the filename for a Document object, along with number of paragraphs and sentences."""
        if VERBOSE:
            print("----------------------------------------")
            print("Filename of Document:", self.filename)
            print("# of paragraphs: {num}".format(num=len(self.paragraphs)))
            print("# of sentences: {num}".format(num=len(self.sentences)))
            print("----------------------------------------\n")
        else:
            print("Document '{file}' contains {num_par} paragraph(s) and {num_sen} sentence(s).".format(file=self.filename, num_par=len(self.paragraphs), num_sen=len(self.sentences)))

    def print_paragraphs(self):
        """Prints out all paragraphs contained with a Document object."""
        if len(self.paragraphs) > 0:
            if VERBOSE:
                print("Paragraphs in Document '{filename}':".format(filename=self.filename))
                for i, para in enumerate(self.paragraphs):
                    print("{file}->paragraphs[{i}]: {para}".format(file=self.filename, i=i, para=para))
            else:
                print("Paragraphs in '{filename}': {paragraphs}".format(filename=self.filename, paragraphs=self.paragraphs))
        else:
            print("No paragraphs in '{filename}' to display.".format(filename=self.filename))

    def print_sentences(self):
        """Prints out all sentences contained within a Document object."""
        if len(self.sentences) > 0:
            if VERBOSE:
                print("Sentences in Document '{filename}':".format(filename=self.filename))
                for i, sentence in enumerate(self.sentences):
                    print("{file}->sentence[{i}]: {sentence}".format(file=self.filename, i=i, sentence=sentence))
            else:
                print("Sentences in '{filename}': {sentences}".format(filename=self.filename, sentences=self.sentences))
        else:
            print("No sentences in '{filename}' to display.".format(filename=self.filename))

class Corpus:
    """
    Object used to store a collection of Document objects. Document objects are stored within a 
    dictionary, where the key is the filename of the given Document and the value is the 
    Document object itself.

    Methods:
    \tadd_document(), info(), get_document().
    """
    def __init__(self):
        self.documents = {}

    def add_document(self, filename, document: Document):
        """Adds a Document object to the documents dictionary of the corpus."""
        if type(document) is Document:
            self.documents[filename] = document
        else:
            raise TypeError("Parameter of add_document() was {type} and must be of type 'Document'.".format(type=type(document)))

    def info(self):
        """Outputs number of documents in the corpus along with their dictionary keys."""
        if len(self.documents) > 0:
            if VERBOSE:
                print("----------------------------------------")
                print("# of documents in Corpus: {num}".format(num=len(self.documents)))
                print("Document keys in Corpus: {keys}".format(keys=[*self.documents]))
                print("----------------------------------------\n")
            else:
                print("Corpus contains {documents} document(s): {keys}".format(documents=len(self.documents), keys=[*self.documents]))
        else:
            print("No Document keys in Corpus to display.")

    def get_document(self, filename) -> Document:
        """Returns a Document object from the corpus."""
        return self.documents[filename]

def split_sentences(string) -> list:
    """
    Separates a string into its component sentences and stores each individual sentence 
    into an output list. Any sentence-terminating punctuation is removed from the sentence 
    when stored into the output list.
    """
    sentences = re.split(r'[.?!]\s*', string)
    if sentences[-1]:
        return sentences
    else:
        return sentences[:-1]

def compile_documents() -> list:
    """
    Checks for the existence of .txt files stored within the defined corpus directory and 
    parses those files into Document objects. Each Document object is appended to a list 
    which is returned to the function caller. The returned list can then be used to create 
    a corpus of documents by calling compile_corpus() with the returned list as a parameter.
    
    The corpus directory to be searched is defined within 'config.ini' located at the root 
    of the project directory.

    Intended Usage:
    \tdocuments = compile_documents()

    \tcorpus = compile_corpus(documents)
    """
    documents = []
    for file in os.listdir(CORPUS_DIR):
        if file.lower().endswith(".txt"):
            with open(os.path.join(CORPUS_DIR, file), 'r') as f:
                doc = Document(file)
                raw_text = f.read()
                paragraphs = raw_text.splitlines()
                paragraphs = list(filter(None, paragraphs))
                doc.add_paragraphs(paragraphs)
                sentences = split_sentences(raw_text)
                doc.add_sentences(sentences)
                documents.append(doc)
    return documents

def compile_corpus(documents: list) -> Corpus:
    """
    Compiles a list of Document objects into a Corpus. When this function is called, 
    a new Corpus object is created, populated with Document objects, and then returned to 
    the function caller. The returned Corpus object can then use its methods to access its 
    held Document objects and their methods.

    Intended Usage:
    \tdocuments = compile_documents()

    \tcorpus = compile_corpus(documents)
    """
    corpus = Corpus()
    for document in documents:
        corpus.add_document(document.filename, document)
    return corpus

if __name__ == '__main__':
    documents = compile_documents()
    corpus = compile_corpus(documents)

    # Examples:
    corpus.info() # Display amount of documents in corpus along with their keys.
    doc1 = corpus.get_document('test01.txt') # Get a specific document from the corpus.
    doc1.info() # Display info for that specific document.
    doc1.print_paragraphs() # Show all paragraphs contained in that document.
    doc1.print_sentences() # Show all sentences contained in that document.