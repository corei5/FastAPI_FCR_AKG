from sklearn.metrics.pairwise import linear_kernel
from .Claim_index.Selected_Claim_Index_vectorizer import selected_Claim_Index
from .Claim_index.List_Of_Selected_Claim_vectorizer import List_Of_Selected_Claim
from .Data_processing.N_max_elements import n_max_elements

#return N Claim
def Selected_Claim(vectorizer, search_term, Claim_df, top_k: int):
    doc_vectors = vectorizer.fit_transform([search_term] + Claim_df['dbpedia_spotlight_entities'])
    # Calculate similarity
    cosine_similarities = linear_kernel(doc_vectors[0:1], doc_vectors).flatten()
    document_scores = [item.item() for item in cosine_similarities[1:]]
    N_max_elements_list = n_max_elements(document_scores, top_k)
    listOfSelectedClaimIndex = selected_Claim_Index(document_scores, N_max_elements_list, top_k)
    listOfSelectedClaim = List_Of_Selected_Claim(Claim_df,listOfSelectedClaimIndex)
    return listOfSelectedClaim