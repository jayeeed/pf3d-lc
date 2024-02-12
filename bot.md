# page_bot

## verify_token

```bash
https://8988-103-92-204-0.ngrok-free.app/webhook?hub.mode=subscribe&hub.verify_token=mytoken&hub.challenge=702365780
```

## page_id

```bash
123427088284797 [me]
```

## recipient_id

```bash
7073515559329750
```

## convo_id

```bash
t_7144392195656788
```

## access_token_page(no exp.)

```bash
EAA1LsR3ZAS6wBOz4ppgrwtbuv3N0WGdOrccmpLPwKVhESPvNyg1AmZBlZCZCbehZAHPRt2NcVJcuq1ENggAT3xBG5dLYyrS0AitcGnUBPYbDTPUvf1Kbr1r2kBxiUyaZCVrG4vNeZC2UpjsCQkeEFT6kyxYHFMhSwDKlRpd9Ux3GZAiRWuWzsHykOo3hompXuRLRnGascuNoz4ZB7ohIZD
```

## check_status

```bash
curl -i -X GET "https://graph.facebook.com/me?access_token=EAA1LsR3ZAS6wBOz4ppgrwtbuv3N0WGdOrccmpLPwKVhESPvNyg1AmZBlZCZCbehZAHPRt2NcVJcuq1ENggAT3xBG5dLYyrS0AitcGnUBPYbDTPUvf1Kbr1r2kBxiUyaZCVrG4vNeZC2UpjsCQkeEFT6kyxYHFMhSwDKlRpd9Ux3GZAiRWuWzsHykOo3hompXuRLRnGascuNoz4ZB7ohIZD"
```

## list_convos

```bash
curl -i -X GET "https://graph.facebook.com/v19.0/me/conversations?access_token=EAA1LsR3ZAS6wBOz4ppgrwtbuv3N0WGdOrccmpLPwKVhESPvNyg1AmZBlZCZCbehZAHPRt2NcVJcuq1ENggAT3xBG5dLYyrS0AitcGnUBPYbDTPUvf1Kbr1r2kBxiUyaZCVrG4vNeZC2UpjsCQkeEFT6kyxYHFMhSwDKlRpd9Ux3GZAiRWuWzsHykOo3hompXuRLRnGascuNoz4ZB7ohIZD"
```

## send_message

```bash
curl -X POST -H "Content-Type: application/json" -d '{
"recipient": "{id:7073515559329750}",
"message": {
"text": "hi"
},
"messaging_type": "RESPONSE"
}' "https://graph.facebook.com/v19.0/me/messages?access_token=EAA1LsR3ZAS6wBOz4ppgrwtbuv3N0WGdOrccmpLPwKVhESPvNyg1AmZBlZCZCbehZAHPRt2NcVJcuq1ENggAT3xBG5dLYyrS0AitcGnUBPYbDTPUvf1Kbr1r2kBxiUyaZCVrG4vNeZC2UpjsCQkeEFT6kyxYHFMhSwDKlRpd9Ux3GZAiRWuWzsHykOo3hompXuRLRnGascuNoz4ZB7ohIZD"
```
