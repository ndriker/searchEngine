class Posting:
    def __init__(self, doc_id, freq_counts, position):
        self.doc_id = doc_id
        self.freq_counts = freq_counts
        self.position = position

    def get_id(self):
        return self.doc_id

    def get_freq(self):
        return self.freq_counts

    def __str__(self):
        return f'{self.doc_id},{self.freq_counts},{self.position}'