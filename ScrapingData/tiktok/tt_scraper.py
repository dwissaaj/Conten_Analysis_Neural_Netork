from TikTokApi import TikTokApi

api = TikTokApi(custom_verify_fp="verify_da935ac80b4937a1f37596fbaa3b0645")

user = api.user(username='biznethome')

for x in user:
    print(x)