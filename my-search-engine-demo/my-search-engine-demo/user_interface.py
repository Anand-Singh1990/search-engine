import os
import re

from azure.core.credentials import AzureKeyCredential
import itertools
import requests
from PIL import Image
import base64
import streamlit as st

# https://gist.github.com/treuille/2ce0acb6697f205e44e3e0f576e810b7
def paginator(label, articles, articles_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of article.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    article : Iterator[Any]
        The articles to display in the paginator.
    articles_per_page: int
        The number of articles to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.
        
    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the article on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

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


def get_download_results_href(response, search_text):
    """Generates a hyperlink allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """

    document = "title;date;body\n"
    for result in response.get("value"):
        title = re.sub(";", "", result["title"])
        date = re.sub(";", "", str(result["timestamp"]))
        body = re.sub(";", "", result["body"])
        body = re.sub("\n", "", body)
        body = body + "\n"
        line = ";".join([title, date, body])
        document = document + line

    camelcase = "_".join(search_text.split())
    csv = document
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a download="{camelcase}.csv" href="data:file/csv;base64,{b64}">Download results</a>'
    return href


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
endpoint = os.environ["ACS_ENDPOINT"]
credential = os.environ["ACS_API_KEY"]
headers = {
    "Content-Type": "application/json",
    "api-key": credential,
}
search_url = f"{endpoint}/indexes/{index_name}/docs/search?api-version=2020-06-30"

search_body = {
    "count": True,
    "search": search_query,
    "searchFields": "title",
    "searchMode": "all",
    "select": "source, title, body, timestamp",
    "top": 100,
}


if search_query != "":
    response = requests.post(search_url, headers=headers, json=search_body).json()

    record_list = []
    _ = [
        record_list.append({"source":record["source"], "title": record["title"], "body": record["body"], "timestamp": record["timestamp"]})
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
            st.write("**Shlok** : %s" % (record["source"]))
            with st.expander("**Meaning in English**"):
                st.write("%s" % (record["title"]))
            with st.expander("**Source**"):
                st.write("%s" % str((record["timestamp"])))
            with st.expander("**Context**"):
                st.write("%s" % (record["body"]))

        st.sidebar.markdown(
            get_download_results_href(response, search_query), unsafe_allow_html=True
        )
        
    else:
        st.write(f"No Search results, please try again with different keywords")

