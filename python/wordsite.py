import enchant,json,sys,random,MySQLdb
from itertools import permutations

db = MySQLdb.connect(host="localhost", user="root", passwd="XTC980326", db="sr")
cur = db.cursor()

def solve(word):
	dictionary = enchant.Dict("en_US")
	results = []
	string = word.lower()
	word_list = list(set(''.join(p) for p in permutations(string)))
	for i in xrange(len(word_list)):
		if (dictionary.check(word_list[i])):
			results.append(word_list[i])
	for word in results:
		count = wordSearch(word)
		if count == 0:
			quiz = createQuiz(word)
			addWord(word,quiz)
	return json.dumps(results)

def createQuiz(word):
	quiz = ''.join(random.sample(word,len(word)))
	return quiz

def addWord(word, quiz):
	sql = "INSERT INTO `wordbank` (`word`, `quiz`) VALUES (%s, %s)"
	cur.execute(sql, (word, quiz))
	db.commit()

def printWordList():
	cur.execute("SELECT * FROM wordbank")
	db.commit()
	for words in cur.fetchall():
		print words[0]

def wordSearch(word):
	sql = "SELECT * FROM `wordbank` WHERE `word` LIKE '%s'" % (word)
	x = cur.execute(sql)
	return x

if __name__ == "__main__":
	print solve(sys.argv[1])

	