import requests
import pandas as pd


CLIENT_ID = '<client_id>'
SECRET_KEY = '<XXXXXXXXXXX>'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {'grant_type': 'password',
        'username': 'kingsman021',
        'password': '<password>'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/news/hot",
                   headers=headers, params={'limit' : '30', 'after': 'latest_post'}) #latestpostid has to be kept manually


df = pd.DataFrame()
for post in res.json()['data']['children']:
    # append relevant data to dataframe
    df = df.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)
df
latest_post = post['kind'] + '_' + post['data']['id']
#post['data']['id']
#post['data'].keys() to find the labels available in the json file.