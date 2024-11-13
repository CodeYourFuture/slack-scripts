import csv
import os
import sys

import slack

from dotenv import load_dotenv

# To get email addresses you need a fully fledged oauth app with the users:read.email scope.
# Just using a `slack auth token` token won't fetch email addresses.
# Setting these up is annoying. Create an app in the workspace, set up the following scopes, and install it to the workspace. Then fetch the User OAuth Token from the app's settings.
# Required scopes:
# * channels:read
# * users:read
# * users:read.email
def print_channel_emails(client: slack.WebClient, channel_id: str):
    channel_name = client.conversations_info(channel=channel_id)["channel"]["name"]
    for user in client.conversations_members(channel=channel_id)["members"]:
        user_info = client.users_info(user=user).data["user"]

        display_name = user_info.get("name", "UNKNOWN")
        real_name = user_info.get("real_name", "UNKNOWN")
        email = user_info["profile"].get("email", "UNKNOWN")

        writer = csv.writer(sys.stdout)
        writer.writerow([channel_name, real_name, display_name, email])


def main(channel_ids):
    # Fetch from the User OAuth Token box in https://api.slack.com/apps/A080QLL46BC/oauth
    client = slack.WebClient(token=os.environ["SLACK_API_BOT_TOKEN"])

    for channel_id in channel_ids:
        print_channel_emails(client, channel_id)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} channel-id...", file=sys.stderr)
        sys.exit(1)

    load_dotenv()

    main(sys.argv[1:])
