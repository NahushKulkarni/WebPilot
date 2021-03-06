import re
from transformers import pipeline

ExclusionTable = ["able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldnt", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", "furthermore", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "just", "keep", "keeps", "kept", "kg", "km", "know", "known", "knows", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now",
                  "nowhere", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "que", "quickly", "quite", "qv", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "zero"]

TopLevelThreshold = 50


def parse(crawlResults):
    textualData = crawlResults['headings'] + crawlResults['text']

    pageDiscription = ""
    if len(crawlResults['meta']) > 0:
        pageDiscription = crawlResults['meta'][0]

    mediaData = crawlResults['images'] + \
        crawlResults['videos'] + crawlResults['audios'] + \
        crawlResults['documents']

    Summary = ""
    textLength = len(crawlResults['text'])
    if textLength in range(1000, 10000):
        Summary = Summarize(crawlResults['text'])

    textOccurance = OccuranceTable(textualData)

    for ET in ExclusionTable:
        if ET in textOccurance:
            textOccurance.pop(ET)

    textOccurance = sorted(textOccurance.items(),
                           key=lambda x: x[1], reverse=True)
    textOccurance = textOccurance[:TopLevelThreshold]

    return {'URL': crawlResults['url'], 'Description': pageDiscription, 'pageTitle': crawlResults['title'], 'OccuranceTable': textOccurance, 'MediaURLs': mediaData, 'ContactURLs': crawlResults['contacts'], 'Summary': Summary}


def RemovePunctuation(text, exceptions=None):
    punctuations = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    if exceptions == None:
        return text.translate(str.maketrans('', '', punctuations))
    else:
        for e in exceptions:
            punctuations = punctuations.replace(e, '')
        return text.translate(str.maketrans('', '', punctuations))


def RemoveHTMLEntities(text):
    return re.sub(r'&#(\d+);', lambda x: chr(int(x.group(1))), text)


def OccuranceTable(textualData):
    Occurance = {}
    for entry in textualData:
        entry = entry.lower()
        entry = RemoveHTMLEntities(entry)
        entry = RemovePunctuation(entry)
        for word in entry.split():
            if len(word) == 1:
                continue
            if word in Occurance:
                Occurance[word] += 1
            else:
                Occurance[word] = 1
    return Occurance


def Summarize(text):
    text = ' '.join(text)
    text = RemoveHTMLEntities(text)

    summarizer = pipeline(
        'summarization', model="t5-small", device="0")
    summary = summarizer(text, max_length=1000,
                         min_length=100, do_sample=False)[0]['summary_text']
    summary = summary.replace(' .', '.')
    summary = '. '.join(
        map(lambda s: s.strip().capitalize(), summary.split('. ')))

    return summary
