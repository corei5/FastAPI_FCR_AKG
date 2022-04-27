#return Selected Claim Index
def selected_Claim_Index(document_scores,N_max_elements_list,top_k):
    listOfSelectedClaimIndex = []
    for i in range(0, top_k, 1):
        maxIndex = document_scores.index(N_max_elements_list[i])
        listOfSelectedClaimIndex.append(maxIndex)
    return listOfSelectedClaimIndex