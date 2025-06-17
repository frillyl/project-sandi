import nltk
import numpy as np
import networkx as nx
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

nltk.download("punkt")
nltk.download("stopwords")

STOP_WORDS = list(set(stopwords.words("indonesian")).union(stopwords.words("english")))

def clean_text(text):
    # Hapus bagian penutup/formal/irrelevan
    text = re.sub(r'NIP\.\s*\d+', '', text)
    text = re.sub(r'mailto:\S+', '', text)
    text = re.sub(r'\[Halaman.*?\]', '', text)
    return text.strip()

def summarize_text(text, ratio=0.3):
    IMPORTANT_PATTERNS = [
        "perihal", "dalam rangka", "kami mohon", "mohon", "diminta",
        "dapat dikirim", "diharapkan", "tanggal", "terima kasih",
        "kepada", "Yth", "data", "struktur", "pelatihan", "jumlah", "email"
    ]
    
    def sentence_importance(sentence, index):
        score = 0

        # Frasa penting
        score += sum(1 for pat in IMPORTANT_PATTERNS if pat.lower() in sentence.lower())

        # Mengandung angka (misalnya tanggal/tenggat/jumlah)
        score += len(re.findall(r'\d+', sentence)) * 0.5

        # Kalimat awal dokumen cenderung penting
        if index == 0:
            score += 2
        elif index <= 2:
            score += 1

        return score
    
    text = clean_text(text)
    sentences = sent_tokenize(text)
    total_sentences = len(sentences)

    if total_sentences <= 1:
        return text  # terlalu pendek
    
    if "perihal" in text.lower() and total_sentences <= 15:
        ratio = 0.6
    elif total_sentences <= 5:
        ratio = 0.9
    elif total_sentences <= 10:
        ratio = 0.6
    else:
        ratio = min(ratio, 0.3)

    # Hitung jumlah kalimat yang akan diringkas (minimal 1)
    num_sentences = max(1, int(total_sentences * ratio))
    
    vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)
    
    combined_scores = [
        (scores[i] + 0.1 * sentence_importance(sent, i), sent)
        for i, sent in enumerate(sentences)
    ]
    
    ranked_sentences = sorted(combined_scores, reverse=True)
    selected_sentences = [sent for _, sent in ranked_sentences[:num_sentences]]
    
    ordered_summary = [s for s in sentences if s in selected_sentences]

    # stop_words = set(stopwords.words("indonesian")).union(stopwords.words("english"))
    # sentence_vectors = []

    # for sentence in sentences:
    #     words = [w.lower() for w in word_tokenize(sentence) if w not in stop_words and w not in string.punctuation]
    #     vector = [0] * 10000
    #     for w in words:
    #         vector[hash(w) % 10000] += 1
    #     sentence_vectors.append(vector)

    # sim_matrix = cosine_similarity(sentence_vectors)
    # scores = np.sum(sim_matrix, axis=1)

    # # Ambil kalimat dengan skor tertinggi sebanyak num_sentences
    # top_indices = np.argsort(scores)[-num_sentences:]
    # ranked_sentences = [sentences[i] for i in sorted(top_indices)]
    
    return " ".join(ordered_summary)
