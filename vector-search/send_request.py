
import urllib,json
import urllib.parse
import google.auth.transport.requests
import google.oauth2.id_token
CONVERTER_FUNCTION_URL="https://vector-search-fzsubm6qeq-uc.a.run.app"
def make_authorized_get_request(endpoint, audience, params):
    # Add the parameters to the endpoint URL
    url = endpoint+"/query" + '?' + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    # Parse the JSON response
    data = json.loads(response.read())
    return data 
params={"query":"black jeans"}
response=make_authorized_get_request(CONVERTER_FUNCTION_URL,CONVERTER_FUNCTION_URL, params)
print(response)