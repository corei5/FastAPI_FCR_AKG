import pandas as pd

def create_url_from_argument(Claim_df,Argument_df,claim_index):

    claim_wasQuotedFrom_full_url_list = []
    claim_id = Claim_df["id.1"][claim_index]
    argument_wasQuotedFrom_id_for_claim = Argument_df[Argument_df['hasClaim_marge'].str.contains(claim_id, na=False)]['schema:about{URIRef}']

    for i in range(0, len(argument_wasQuotedFrom_id_for_claim), 1):
        argument_wasQuotedFrom_id_for_claim_url = argument_wasQuotedFrom_id_for_claim[i].split(":")[1]
        claim_wasQuotedFrom_full_url = 'https://covidontheweb.inria.fr/describe/?url=' + 'http%3A%2F%2Fns.inria.fr%2Fcovid19%2F' + str(argument_wasQuotedFrom_id_for_claim_url)

        claim_wasQuotedFrom_full_url_list.append(claim_wasQuotedFrom_full_url)

    return claim_wasQuotedFrom_full_url_list