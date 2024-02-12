import requests

page_id = '123427088284797'
page_access_token = 'EAA1LsR3ZAS6wBOz4ppgrwtbuv3N0WGdOrccmpLPwKVhESPvNyg1AmZBlZCZCbehZAHPRt2NcVJcuq1ENggAT3xBG5dLYyrS0AitcGnUBPYbDTPUvf1Kbr1r2kBxiUyaZCVrG4vNeZC2UpjsCQkeEFT6kyxYHFMhSwDKlRpd9Ux3GZAiRWuWzsHykOo3hompXuRLRnGascuNoz4ZB7ohIZD'

# get PSID
response = requests.get(
    f'https://graph.facebook.com/{page_id}/conversations?fields=participants&access_token={page_access_token}')

print(response.text)