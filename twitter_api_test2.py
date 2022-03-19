API_KEY = "X2acrIZ9rgXYMfZmgrnBh849b"

API_KEY_SECRET = "5CDmzIJpCwY7AXMM5fzTk4X3cUhT24vUL6epeI8lo4kDLdsE2i"

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFPsZQEAAAAAybHGRAqBWOwo9%2FpxJU9PMILgzGw%3DuNA1HciHqpNEAW3DEGWYNxhPHtfIOl9316lGW2bGQfusuVLofC"
client_id = "23456851"
#
# #
# # from pytwitter import Api
# from pytwitter import Api
# #
# api = Api(bearer_token= BEARER_TOKEN , consumer_key=API_KEY, consumer_secret=API_KEY_SECRET, oauth_flow=True)
# # #
#
# # print(api.get_oauth2_authorize_url())
# print(api.get_authorize_url())
#
# k = str(api.get_authorize_url())
#
#
# # api.generate_access_token("{}&oauth_verifier=oauth_verifier".format(k))
#
# #
# # # api.generate_access_token("https://api.twitter.com/oauth/authorize?oauth_token=szXEdgAAAAABZexTAAABfx5Ji9s")
# api = Api(client_id=client_id, oauth_flow=True)
# #
# url, code_verifier, _ = api.get_oauth2_authorize_url()
#
# # #
# print(url, code_verifier)
# #
# # # code_verifier = "UVvPirHOm6Whpqma722Wo8AFuDADU1sowjxFO1aSdc1FCH3CTMeh4g"
# #
#
# url = url
# k = api.generate_oauth2_access_token(url, code_verifier)
#
# # print(k)


# from pytwitter import StreamApi
# stream_api = StreamApi(bearer_token=BEARER_TOKEN)

# stream_api = StreamApi(consumer_key=API_KEY, consumer_secret=API_KEY_SECRET)

from pytwitter import StreamApi


bearer_token = BEARER_TOKEN


class MySearchStream(StreamApi):
    def on_tweet(self, tweet):
        print(tweet)


if __name__ == "__main__":
    # Application should be
    stream = MySearchStream(bearer_token=bearer_token, consumer_key=API_KEY, consumer_secret=API_KEY_SECRET)

    # create new rules
    add_rules = {
        "add": [
            {"value": "cat has:media", "tag": "cats with media"},
            {"value": "cat has:media -grumpy", "tag": "happy cats with media"},
        ]
    }

    # validate rules
    stream.manage_rules(rules=add_rules, dry_run=True)

    # create rules
    # Rules remain after creating them, check them using stream.get_rules(return_json=True)
    stream.manage_rules(rules=add_rules)
    # Response(data=[StreamRule(id='1370406958721732610', value='cat has:media -grumpy'), StreamRule(id='1370406958721732609', value='cat has:media')])

    # get tweets
    k = stream.search_stream()
    print(k)