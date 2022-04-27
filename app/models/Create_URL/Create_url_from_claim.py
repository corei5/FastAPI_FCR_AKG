import pandas as pd

def create_url_from_claim(Claim_df, claim_index):

    claim_wasQuotedFrom_id = Claim_df['prov:wasQuotedFrom{URIRef}'][claim_index]
    prove_marge_id = Claim_df['proves_marge'][claim_index]
    supports_marge_id = Claim_df['supports_marge'][claim_index]
    claim_wasQuotedFrom_url = claim_wasQuotedFrom_id.split(":")[1]

    claim_wasQuotedFrom_full_url = 'https://covidontheweb.inria.fr/describe/?url=' + 'http%3A%2F%2Fns.inria.fr%2Fcovid19%2F' + str(
        claim_wasQuotedFrom_url)

    prove_marge_full_url = 'https://covidontheweb.inria.fr/describe/?url=' + str(prove_marge_id)
    supports_marge_full_url = 'https://covidontheweb.inria.fr/describe/?url=' + str(supports_marge_id)

    return claim_wasQuotedFrom_full_url