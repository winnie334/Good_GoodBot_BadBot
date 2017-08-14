import praw, requests
from bs4 import BeautifulSoup
from praw.exceptions import APIException

database = 'https://goodbot-badbot.herokuapp.com/all_filter'


def checkforcomments(bot):
	p = open('threads_replied_to.txt', 'r')
	posts_replied_to = [line.rstrip('\n') for line in p]  # fill the list with earlier submissions to prevent doubles
	p.close()
	print("Got submission id's.")
	newcomments = bot.subreddit('all').stream.comments()
	for comment in newcomments:
		if 'good bot' in comment.body.lower():
			if not comment.is_root and comment.parent().author is not None:
				parentAuthor = comment.parent().author.name
				sub = comment.subreddit.display_name
				if parentAuthor == 'GoodBot_BadBot':
					print('we got one! Found in ' + sub)
					print('http://reddit.com' + comment.permalink())
					if comment.submission.id not in posts_replied_to:
						replytocomment(comment)
					else:
						print('sadly, we already replied in this thread.')
				else:
					print('author here was ' + parentAuthor + ' found in ' + sub)


def replytocomment(comment):
	votecount = getscore()
	print('replying...')
	try:
		# I know the following could be written better
		lastnumber = str(votecount)[-1]
		if lastnumber in ["4", "5", "6", "7", "8", "9", "0"]:
			end = 'th'
		elif lastnumber == "1":
			end = 'st'
		elif lastnumber == "2":
			end = 'nd'
		else:
			end = 'rd'
		message = 'You are the ' + str(votecount) + '^' + end + ' user calling /u/GoodBot_BadBot a good bot!'
		if comment.subreddit.display_name == 'me_irl':
			message += '\n\n I mean me too thanks'
		else:
			message += ' He definitely is awesome.'
		comment.reply(message)
	except APIException:
		print('aww, couldnt reply :(')
		return

	print('I replied! (count = ' + str(votecount) + ')')
	with open('threads_replied_to.txt', 'a') as t:
		t.write(comment.submission.id + '\n')


def getscore():
	sc = requests.get(database).text
	soup = BeautifulSoup(sc, 'html.parser')
	ref = soup.find('a', {'href': 'https://www.reddit.com/user/GoodBot_BadBot'})
	score = ref.find_next('td')
	goodBotVotes = score.find_next('td')
	return goodBotVotes.text


if __name__ == '__main__':
	print('logging in...')
	with open('creds.txt', 'r') as f:
		password = f.readline()

	reddit = praw.Reddit(
		user_agent='Takes it one level further -- answers to people calling /u/GoodBot_BadBot a good bot.',
		client_id='7pMF08wOH7A9hQ',
		client_secret='uid4R2XTiXroIPzhdWmnf-ok_AI',
		username='Good_GoodBot_BadBot',
		password=password)
	print('logged in.')
	checkforcomments(reddit)
