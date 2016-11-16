from HoverSpace.models import TAGS_COLLECTION

class Tag(object):
	def __init__(self, tagname):
		self.tagname = tagname
		self.addTag()

	def addTag(self):
		try:
			TAGS_COLLECTION.insert_one({'_id': self.tagname, 'quesID': []})
		except:
			pass

class TagMethods(object):
    def __init__(self, quesID, tags=[]):
        self.quesID = str(quesID)
        self.tags = tags

    def addQuestion(self):
        for tag in self.tags:
            TAGS_COLLECTION.find_one_and_update({'_id': tag}, {'$addToSet': {'quesID': self.quesID}})

class TagQuestion(object):
	def __init__(self, tag):
		self.tag = tag

	def getQuestions(self):
		return TAGS_COLLECTION.find_one({'_id': self.tag})['quesID']