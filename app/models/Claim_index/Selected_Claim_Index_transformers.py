import numpy as np

#return Selected Claim Index
def selected_claim_index(cosScores,top_k: int):
    listOfSelectedClaimIndex = []
    topResults = np.argpartition(-cosScores, range(top_k))[0:top_k]
    for idx in topResults[0:top_k]:
        listOfSelectedClaimIndex.append(int(idx))
    return listOfSelectedClaimIndex