class Posting:
    def __init__(self, doc_id, freq_counts, position):
        self.doc_id = doc_id
        self.freq_counts = freq_counts
        self.position = position

    def __str__(self):
        return f'doc id is {self.doc_id}, token frequency is {self.freq_counts}, token position is {self.position}'