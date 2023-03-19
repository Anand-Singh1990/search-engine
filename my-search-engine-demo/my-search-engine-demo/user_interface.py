import os
import re
from creds import cred
from azure.core.credentials import AzureKeyCredential
import itertools
import requests
from PIL import Image
import base64
import streamlit as st

def paginator(label, articles, articles_per_page=10, on_sidebar=True):
    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    articles = list(articles)
    n_pages = (len(articles) - 1) // articles_per_page + 1
    page_format_func = lambda i: f"Results {i*10} to {i*10 +10 -1}"
    page_number = location.selectbox(
        label, range(n_pages), format_func=page_format_func
    )

    # Iterate over the articles in the page to let the user display them.
    min_index = page_number * articles_per_page
    max_index = min_index + articles_per_page

    return itertools.islice(enumerate(articles), min_index, max_index)


# def get_download_results_href(response, search_text):
#     """Generates a hyperlink allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """

#     document = "title;date;body\n"
#     for result in response.get("value"):
#         title = re.sub(";", "", result["title"])
#         date = re.sub(";", "", str(result["timestamp"]))
#         body = re.sub(";", "", result["body"])
#         body = re.sub("\n", "", body)
#         body = body + "\n"
#         line = ";".join([title, date, body])
#         document = document + line

#     camelcase = "_".join(search_text.split())
#     csv = document
#     b64 = base64.b64encode(
#         csv.encode()
#     ).decode()  # some strings <-> bytes conversions necessary here
#     href = f'<a download="{camelcase}.csv" href="data:file/csv;base64,{b64}">Download results</a>'
#     return href


# Title
st.markdown(
    "<h1 style='text-align: center; '>Vedic search engine</h1>",
    unsafe_allow_html=True,
)
#st.markdown("<h2 style='text-align: center; '>OM</h2>", unsafe_allow_html=True)

# Logo
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monk2.png")
robeco_logo = Image.open(logo_path)
st.image(robeco_logo, use_column_width=True, width = 500 )

# Search bar
search_query = st.text_input(
    label="", value="", max_chars=None, key=None, type="default", help="Enter your search query here"
)

# Search API
index_name = "vedic-index"
endpoint = cred.get("ACS_ENDPOINT")
credential = cred.get("ACS_API_KEY")
headers = {
    "Content-Type": "application/json",
    "api-key": credential,
}
search_url = f"{endpoint}/indexes/{index_name}/docs/search?api-version=2020-06-30"

search_body = {
    "count": True,
    "search": search_query,
    "searchFields": "english_trans, context",
    "searchMode": "all",
    "select": "source, title, hindi_trans, english_trans",
    "top": 100,
}


if search_query != "":
    response = requests.post(search_url, headers=headers, json=search_body).json()

    record_list = []
    _ = [
        record_list.append(
            {
                "source":record["source"],
                "title": record["title"], 
                "hindi_trans": record["hindi_trans"], 
                "english_trans": record["english_trans"],
                "context": record["context"],
            })
        for record in response.get("value")
    ]

    if record_list:
        st.write(f'Search results ({response.get("@odata.count")}):')

        if response.get('@odata.count') > 100:
            shown_results = 100
        else:
            shown_results = response.get('@odata.count')


        for i, record in paginator(
            f"Select results (showing {shown_results} of {response.get('@odata.count')} results)",
            record_list,
        ):  
            st.write("**Search result:** %s." % (i+1))
            st.write("**Source** : %s" % (record["source"]))
            with st.expander("**Meaning in Hindi**"):
                st.write("%s" % (record["hindi_trans"]))
            with st.expander("**Meaning in English**"):
                st.write("%s" % str((record["english_trans"])))
            with st.expander("**Context**"):
                st.write("%s" % (record["context"]))

        # st.sidebar.markdown(
        #     get_download_results_href(response, search_query), unsafe_allow_html=True
        # )
        
    else:
        st.write(f"No Search results, please try again with different keywords")

