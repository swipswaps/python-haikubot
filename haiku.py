import os
import time
from slackclient import SlackClient
import json

BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

with open('syllables.json') as fh:
    SYLLABLES = json.load(fh)

def handle_command(potential, channel):
    """
        parse the potential haiku
        if it is a haiku, let the channel it came from know
    """

    print('handling {0}'.format(potential))

    # split up the words and strip common punctuation
    words = [w.rstrip('.').rstrip('?').rstrip('!') for w in
        potential.strip().upper().split()]

    count_syl = 0
    for word in words:
        try:
            count_syl += SYLLABLES[word]
        except KeyError:
            print("""don't know the word {0}""".format(word))
            return

    if count_syl == 17:
        response = """found a haiku! '{0}'""".format(potential)
        print(response)
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    else:
        print('{0} with {1} syllables is not a haiku'.format(
            potential, count_syl))


def parse_slack_output(slack_rtm_output):
    """
        grab slack output on channels we are in.
        filter out non messages, and messages from ourself
        send the rest to handle command
    """

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output:
                if not output.get('type') == 'message':
                    # ignore non messages
                    continue
                elif output.get('user') == BOT_ID:
                    # ignore messages from self
                    continue

                potential = output.get('text') or ''
                if not len(potential):
                    continue
                channel = output.get('channel')
                print('channel {0}, potential {1}'.format(
                    channel, potential))
                return potential, channel
                #if potential and channel:
                #    return potential.split().strip(), channel
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
