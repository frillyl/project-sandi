from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models import HasilOCR
from utils.text_cleaning import clean_text

import re

def remove_template_sections(text: str) -> str:
    headings = [
        "LATAR BELAKANG", "TUJUAN", "WAKTU DAN TEMPAT", "TANGGAL", "TEMPAT",
        "PESERTA", "NARASUMBER", "RANGKAIAN ACARA", "KESIMPULAN",
        "NOMOR AGENDA", "TANGGAL TERIMA", "NOMOR SURAT", "TANGGAL SURAT",
        "ASAL SURAT", "PERIHAL", "ISI RINGKAS", "DITERUSKAN KEPADA YTH",
        "INSTRUKSI/DISPOSISI", "CATATAN", "TANGGAL DISPOSISI",
        "PENJABAT PENDISPOSISI", "KEPADA", "DARI", "NOMOR", "LAMPIRAN",
        "HARI, TANGGAL", "WAKTU", "AGENDA", "SIFAT"
    ]
    for heading in headings:
        pattern = rf'(?im)^\s*{heading}\s*:?\s*'
        text = re.sub(pattern, '', text)
    return text

def get_recommendations(db: Session, doc_id: int, top_n: int = 5, min_score: float = 0.3):
    documents = db.query(HasilOCR).all()

    # corpus = [doc.hasil_ocr for doc in documents]
    ids = [doc.id for doc in documents]

    if doc_id not in ids:
        return []

    processed_docs = []
    for doc in documents:
        raw_text = f"{doc.judul} {doc.judul} {doc.judul} {doc.hasil_ocr}"  # bobot judul
        no_template = remove_template_sections(raw_text)
        cleaned = clean_text(no_template)  # pakai modul kamu
        processed_docs.append(cleaned)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_docs)
    cosine_sim = cosine_similarity(tfidf_matrix)

    idx = ids.index(doc_id)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx]  # hilangkan dirinya sendiri

    filtered_scores = [s for s in sim_scores if s[1] >= min_score]

    recommendations = [
        {
            "id": ids[i],
            "judul": documents[i].judul,
            "similarity": float(score),
            "preview": processed_docs[i][:200]
        }
        for i, score in filtered_scores[:top_n]
    ]

    return recommendations
