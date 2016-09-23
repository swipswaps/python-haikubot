# python-haikubot

a python 3 slack haiku detetor for nate

basic bot logic almost entirely from starterbot: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

basic hakiu logic and the syllables file from toby:  http://www.metaltoad.com/blog/writing-haiku-detecting-bot-slack

toby's bot is more advanced, but this is less work to get running

# howto

1. install/set up python3.  I recommend using a virtualenv but you don't have to
2. install the requirements: pip install -r requirements.txt
3. Set BOT_ID and SLACK_BOT_TOKEN as environent variables.  The page for starterbot has good instructions if you dont know how
4. run the bot: python3 haiku.py
5. the bot will watch channels it has access to.  if it finds a haiku, it will let the channel know

