import random
import numpy as np
from gensim.models import KeyedVectors
from typing import List, Tuple, Optional

def load_google_word2vec(path: str):

    print("Loading Word2Vec model ...")
    wv = KeyedVectors.load_word2vec_format(path, binary=True)
    print("Model loaded. Vocab size:", len(wv))
    return wv

def get_vector_if_possible(wv: KeyedVectors, token: str) -> Optional[np.ndarray]:

    if token in wv:
        return wv[token]
    # 嘗試以空格拆（處理多詞 phrase）
    parts = token.split()
    vecs = []
    for p in parts:
        if p in wv:
            vecs.append(wv[p])
    if vecs:
        return np.mean(vecs, axis=0)
    return None

def similar_above_threshold(
    target: str,
    candidates: List[str],
    wv: KeyedVectors,
    threshold: float = 0.7
) -> List[Tuple[str, float]]:

    target_vec = get_vector_if_possible(wv, target)
    if target_vec is None:
        return []

    cand_vecs = []
    cand_keys = []
    for c in candidates:
        v = get_vector_if_possible(wv, c)
        if v is not None:
            cand_vecs.append(v)
            cand_keys.append(c)

    if not cand_vecs:
        return []

    mat = np.vstack(cand_vecs)
    mat_norms = np.linalg.norm(mat, axis=1)
    target_norm = np.linalg.norm(target_vec)

    safe = (mat_norms > 0) & (target_norm > 0)
    scores = np.full(len(cand_keys), -1.0)
    if target_norm > 0:
        scores[safe] = (mat[safe] @ target_vec) / (mat_norms[safe] * target_norm)

    # 過濾出大於等於 threshold 的
    results = [(cand_keys[i], float(scores[i])) for i in range(len(cand_keys)) if scores[i] >= threshold]

    # 排序（高到低）
    results.sort(key=lambda x: x[1], reverse=True)
    return results

class vocList:
    def __init__(self):
        self.Level = []
        self.part_of_speech = []
        self.voc = []
        self.translate = []
    
    def append(self, Level, part_of_speech, voc, translate):
        self.Level.append(int(Level))
        self.part_of_speech.append(part_of_speech)
        self.voc.append(voc)
        self.translate.append(translate)
    
    def get(self, index):
        return {"Level": self.Level[index], 
                "part_of_speech": self.part_of_speech[index], 
                "vocabulary": self.voc[index], 
                "translate": self.translate[index]}
    
    def random_by_level(self, target_level):
        indices = [i for i, lvl in enumerate(self.Level) if lvl == target_level]
        if not indices:
            return None
        random_index = random.choice(indices)
        return self.get(random_index)