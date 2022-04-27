from .Claim_index.Selected_Claim_Index_transformers import selected_claim_index
from .Create_URL.Create_url_from_claim import create_url_from_claim
from .Extract_biblo_info.Extract_Biblo_Info import extract_biblo_info

#return Selected Claim
def selected_claim(cosScores,Claim_df,top_k: int):
    listOfSelectedClaimIndex = selected_claim_index(cosScores, top_k)
    listOfSelectedClaim = []
    for i in range(0, len(listOfSelectedClaimIndex), 1):
        claimWasQuotedFromFullUrl = create_url_from_claim(Claim_df,listOfSelectedClaimIndex[i])
        claimBibloInfo = extract_biblo_info(claimWasQuotedFromFullUrl)
        listOfSelectedClaim.append(claimBibloInfo)
    return listOfSelectedClaim