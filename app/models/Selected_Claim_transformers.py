import pandas as pd
import numpy as np
from .Claim_index.Selected_Claim_Index_transformers import selected_claim_index
from .Create_URL.Create_url_from_claim import create_url_from_claim
from .Extract_biblo_info.Extract_Biblo_Info import extract_biblo_info


# return Selected Claim
def selected_claim(cosScores, Claim_df, top_k: int):
    listOfSelectedClaimIndex = selected_claim_index(cosScores, top_k)
    listOfSelectedClaimBiblo = []
    for i in range(0, len(listOfSelectedClaimIndex), 1):
        claimWasQuotedFromFullUrl = create_url_from_claim(Claim_df, listOfSelectedClaimIndex[i])
        claimBibloInfo = extract_biblo_info(claimWasQuotedFromFullUrl)
        listOfSelectedClaimBiblo.append(claimBibloInfo)
    return listOfSelectedClaimBiblo


def store_selected_claim(cosScores, Claim_df, threshold: float, search_terms, folder_path):
    selected_claim = []
    selected_claim_similarity = []
    search_text = []
    nx = cosScores.numpy()
    listOfSelectedClaimIndex = np.where(nx >= threshold)[0]
    for i in range(0, len(listOfSelectedClaimIndex), 1):
        selected_claim.append(Claim_df['aif:claimText{Literal}'][listOfSelectedClaimIndex[i]])
        selected_claim_similarity.append(nx[listOfSelectedClaimIndex[i]])
        search_text.append(search_terms)
    data = {'search_terms': search_terms,
            'claim': selected_claim,
            'similarity': selected_claim_similarity}
    # Create DataFrame
    df = pd.DataFrame(data)
    df.to_csv(folder_path + search_terms + ".csv")
    return df
