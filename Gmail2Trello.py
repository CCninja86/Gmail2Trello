import gmail
import trolly
from tqdm import tqdm

print "Logging into Gmail..."
gmail = gmail.login("[gmail address]", "[gmail password]")

if gmail.logged_in:
    print "Done!"
    print "Fetching emails..."
    messages = gmail.inbox().mail(unread=True)

    if len(messages) > 0:
        print "Adding cards to Trello..."

        for i in tqdm(range(len(messages))):
            messages[i].fetch()

            email_subject = messages[i].subject
            email_body = messages[i].body

            trello_client = trolly.client.Client('[Trello API Key]', '[Trello OAuth Key]')

            for board in trello_client.get_boards():
                board_info = board.get_board_information()
                board_name = board_info["name"].encode("utf-8")

                if board_name == "[Board to add card to]":
                    for list in board.get_lists():
                        list_info = list.get_list_information()
                        list_name = list_info["name"].encode("utf-8")
                        list_id = list_info["id"].encode("utf-8")

                        if list_info["name"] == "[List to add card to]":
                            list.add_card({'name': email_subject, 'desc': email_body, 'idList': list_id})
                            messages[i].read()
                            messages[i].archive()
    else:
        print "No new bug reports"
else:
    print "Failed to log into Gmail"