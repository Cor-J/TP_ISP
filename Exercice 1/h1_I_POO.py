# -*- coding : utf8 -*

from hashlib import md5
from random import choice
import pickle
from copy import deepcopy  # see in code
from itertools import product  # compute a matrix of each combination ex : ('a','b'),('c') => (a,c),(b,c)
from datetime import datetime


class Result:
    """Class to store sentence, corresponding hash, and eventually # corresponding bytes"""
    reference = None # constant for the class

    def __init__(self, sentence=''):
        self.sentence = str(sentence)
        self.hash = md5(sentence.encode('utf8')).hexdigest() if sentence else None
        self.nb_matching_bytes = self._set_nb_matching_bytes() if sentence else 0

    def __str__(self):
        """Methode executed when str() is called"""
        return f"{self.sentence}\n{self.hash}\n{self.nb_matching_bytes}"

    def __eq__(self, other): # method called when result == other
        if isinstance(other, Result):
            return self.hash == other.hash
        else:
            return False

    @classmethod
    def set_reference_sentence(cls, sentence):
        cls.reference = Result(sentence)

    def _set_nb_matching_bytes(self):
        """Compute number of matching bytes on hash"""
        if self.reference is None or self.hash is None:
            return 0

        nb_matching_bytes = 0
        for ptr in range(0, len(Result.reference.hash), 2):  # compare 2char per 2 char
            if Result.reference.hash[ptr:ptr + 2] == self.hash[ptr:ptr + 2]:
                nb_matching_bytes += 1
            else:
                return nb_matching_bytes
        return nb_matching_bytes

    def save_result_2textfile(self, file='h1_I.txt', mode='w'):
        with open(file, mode) as f:
            f.write(str(self)+'\n')

    @classmethod
    def load_from_textfile(cls, file='h1_I.txt'):
        try:
            with open(file, 'r', encoding='utf8') as f:
                raw_text = [line.replace('\n','') for line in f.readlines()]
        except FileNotFoundError:
            return Result()
        else:
            r = Result()  # TODO make less ugly (update constructor? but nonsense)
            r.sentence = raw_text[0]
            r.hash = raw_text[1]
            r.nb_matching_bytes = int(raw_text[2])
            return r


# synonym from https://justenglish.me/2014/04/18/synonyms-for-the-96-most-commonly-used-words-in-english/
# good, bad, tell, big, old, look, interesting, boring, few, beautiful, colorname
synonyms = [
            ['bad','evil', 'immoral', 'wicked', 'corrupt', 'sinful', 'depraved', 'rotten', 'contaminated', 'spoiled', 'tainted', 'harmful', 'injurious', 'unfavorable', 'defective', 'inferior', 'imperfect', 'substandard', 'faulty', 'improper', 'inappropriate', 'unsuitable', 'disagreeable', 'unpleasant', 'cross', 'nasty', 'unfriendly', 'irascible', 'horrible', 'atrocious', 'outrageous', 'scandalous', 'infamous', 'wrong', 'noxious', 'sinister', 'putrid', 'snide', 'deplorable', 'dismal', 'gross', 'heinous', 'nefarious', 'base', 'obnoxious', 'detestable', 'despicable', 'contemptible', 'foul', 'rank', 'ghastly', 'execrable'],
            ['beautiful','pretty', 'lovely', 'handsome', 'attractive', 'gorgeous', 'dazzling', 'splendid', 'magnificent', 'comely', 'fair', 'ravishing', 'graceful', 'elegant', 'fine', 'exquisite', 'aesthetic', 'pleasing', 'shapely', 'delicate', 'stunning', 'glorious', 'heavenly', 'resplendent', 'radiant', 'glowing', 'blooming', 'sparkling'],
            ['big', 'enormous', 'huge', 'immense', 'gigantic', 'vast', 'colossal', 'gargantuan', 'large', 'sizable', 'grand', 'great', 'tall', 'substantial', 'mammoth', 'astronomical', 'ample', 'broad', 'expansive', 'spacious', 'stout', 'tremendous', 'titanic', 'mountainous'],
            ['boring', 'tiring„ tiresome', 'uninteresting', 'slow', 'dumb', 'stupid', 'unimaginative', 'lifeless', 'dead', 'insensible', 'tedious', 'wearisome', 'listless', 'expressionless', 'plain', 'monotonous', 'humdrum', 'dreary'],
            ['cloudy blue', 'dark pastel green', 'dust', 'electric lime', 'fresh green', 'light eggplant', 'nasty green', 'really light blue', 'tea', 'warm purple', 'yellowish tan', 'cement', 'dark grass green', 'dusty teal', 'grey teal', 'macaroni and cheese', 'pinkish tan', 'spruce', 'strong blue', 'toxic green', 'windows blue', 'blue blue', 'blue with a hint of purple', 'booger', 'bright sea green', 'dark green blue', 'deep turquoise', 'green teal', 'strong pink', 'bland', 'deep aqua', 'lavender pink', 'light moss green', 'light seafoam green', 'olive yellow', 'pig pink', 'deep lilac', 'desert', 'dusty lavender', 'purpley grey', 'purply', 'candy pink', 'light pastel green', 'boring green', 'kiwi green', 'light grey green', 'orange pink', 'tea green', 'very light brown', 'egg shell', 'eggplant purple', 'powder pink', 'reddish grey', 'baby shit brown', 'liliac', 'stormy blue', 'ugly brown', 'custard', 'darkish pink', 'deep brown', 'greenish beige', 'manilla', 'off blue', 'battleship grey', 'browny green', 'bruise', 'kelley green', 'sickly yellow', 'sunny yellow', 'azul', 'darkgreen', 'green/yellow', 'lichen', 'light light green', 'pale gold', 'sun yellow', 'tan green', 'burple', 'butterscotch', 'toupe', 'dark cream', 'indian red', 'light lavendar', 'poison green', 'baby puke green', 'bright yellow green', 'charcoal grey', 'squash', 'cinnamon', 'light pea green', 'radioactive green', 'raw sienna', 'baby purple', 'cocoa', 'light royal blue', 'orangeish', 'rust brown', 'sand brown', 'swamp', 'tealish green', 'burnt siena', 'camo', 'dusk blue', 'fern', 'old rose', 'pale light green', 'peachy pink', 'rosy pink', 'light bluish green', 'light bright green', 'light neon green', 'light seafoam', 'tiffany blue', 'washed out green', 'browny orange', 'nice blue', 'sapphire', 'greyish teal', 'orangey yellow', 'parchment', 'straw', 'very dark brown', 'terracota', 'ugly blue', 'clear blue', 'creme', 'foam green', 'grey/green', 'light gold', 'seafoam blue', 'topaz', 'violet pink', 'wintergreen', 'yellow tan', 'dark fuchsia', 'indigo blue', 'light yellowish green', 'pale magenta', 'rich purple', 'sunflower yellow', 'green/blue', 'leather', 'racing green', 'vivid purple', 'dark royal blue', 'hazel', 'muted pink', 'booger green', 'canary', 'cool grey', 'dark taupe', 'darkish purple', 'true green', 'coral pink', 'dark sage', 'dark slate blue', 'flat blue', 'mushroom', 'rich blue', 'dirty purple', 'greenblue', 'icky green', 'light khaki', 'warm blue', 'dark hot pink', 'deep sea blue', 'carmine', 'dark yellow green', 'pale peach', 'plum purple', 'golden rod', 'neon red', 'old pink', 'very pale blue', 'blood orange', 'grapefruit', 'sand yellow', 'clay brown', 'dark blue grey', 'flat green', 'light green blue', 'warm pink', 'dodger blue', 'gross green', 'ice', 'metallic blue', 'pale salmon', 'sap green', 'algae', 'bluey grey', 'greeny grey', 'highlighter green', 'light light blue', 'light mint', 'raw umber', 'vivid blue', 'deep lavender', 'dull teal', 'light greenish blue', 'mud green', 'pinky', 'red wine', 'shit green', 'tan brown', 'darkblue', 'rosa', 'lipstick', 'pale mauve', 'claret', 'dandelion', 'orangered', 'poop green', 'ruby', 'dark', 'greenish turquoise', 'pastel red', 'piss yellow', 'bright cyan', 'dark coral', 'algae green', 'darkish red', 'reddy brown', 'blush pink', 'camouflage green', 'lawn green', 'putty', 'vibrant blue', 'dark sand', 'purple/blue', 'saffron', 'twilight', 'warm brown', 'bluegrey', 'bubble gum pink', 'duck egg blue', 'greenish cyan', 'petrol', 'royal', 'butter', 'dusty orange', 'off yellow', 'pale olive green', 'orangish', 'leaf', 'light blue grey', 'dried blood', 'lightish purple', 'rusty red', 'lavender blue', 'light grass green', 'light mint green', 'sunflower', 'velvet', 'brick orange', 'lightish red', 'pure blue', 'twilight blue', 'violet red', 'yellowy brown', 'carnation', 'muddy yellow', 'dark seafoam green', 'deep rose', 'dusty red', 'grey/blue', 'lemon lime', 'purple/pink', 'brown yellow', 'purple brown', 'wisteria', 'banana yellow', 'lipstick red', 'water blue', 'brown grey', 'vibrant purple', 'baby green', 'barf green', 'eggshell blue', 'sandy yellow', 'cool green', 'pale', 'blue/grey', 'hot magenta', 'greyblue', 'purpley', 'baby shit green', 'brownish pink', 'dark aquamarine', 'diarrhea', 'light mustard', 'pale sky blue', 'turtle green', 'bright olive', 'dark grey blue', 'greeny brown', 'lemon green', 'light periwinkle', 'seaweed green', 'sunshine yellow', 'ugly purple', 'medium pink', 'puke brown', 'very light pink', 'viridian', 'bile', 'faded yellow', 'very pale green', 'vibrant green', 'bright lime', 'spearmint', 'light aquamarine', 'light sage', 'yellowgreen', 'baby poo', 'dark seafoam', 'deep teal', 'heather', 'rust orange', 'dirty blue', 'fern green', 'bright lilac', 'weird green', 'peacock blue', 'avocado green', 'faded orange', 'grape purple', 'hot green', 'lime yellow', 'mango', 'shamrock', 'bubblegum', 'purplish brown', 'vomit yellow', 'pale cyan', 'key lime', 'tomato red', 'lightgreen', 'merlot', 'night blue', 'purpleish pink', 'apple', 'baby poop green', 'green apple', 'heliotrope', 'yellow/green', 'almost black', 'cool blue', 'leafy green', 'mustard brown', 'dusk', 'dull brown', 'frog green', 'vivid green', 'bright light green', 'fluro green', 'kiwi', 'seaweed', 'navy green', 'ultramarine blue', 'iris', 'pastel orange', 'yellowish orange', 'perrywinkle', 'tealish', 'dark plum', 'pear', 'pinkish orange', 'midnight purple', 'light urple', 'dark mint', 'greenish tan', 'light burgundy', 'turquoise blue', 'ugly pink', 'sandy', 'electric pink', 'muted purple', 'mid green', 'greyish', 'neon yellow', 'banana', 'carnation pink', 'tomato', 'sea', 'muddy brown', 'turquoise green', 'buff', 'fawn', 'muted blue', 'pale rose', 'dark mint green', 'amethyst', 'blue/green', 'chestnut', 'sick green', 'pea', 'rusty orange', 'stone', 'rose red', 'pale aqua', 'deep orange', 'earth', 'mossy green', 'grassy green', 'pale lime green', 'light grey blue', 'pale grey', 'asparagus', 'blueberry', 'purple red', 'pale lime', 'greenish teal', 'caramel', 'deep magenta', 'light peach', 'milk chocolate', 'ocher', 'off green', 'purply pink', 'lightblue', 'dusky blue', 'golden', 'light beige', 'butter yellow', 'dusky purple', 'french blue', 'ugly yellow', 'greeny yellow', 'orangish red', 'shamrock green', 'orangish brown', 'tree green', 'deep violet', 'gunmetal', 'blue/purple', 'cherry', 'sandy brown', 'warm grey', 'dark indigo', 'midnight', 'bluey green', 'grey pink', 'soft purple', 'blood', 'brown red', 'medium grey', 'berry', 'poo', 'purpley pink', 'light salmon', 'snot', 'easter purple', 'light yellow green', 'dark navy blue', 'drab', 'light rose', 'rouge', 'purplish red', 'slime green', 'baby poop', 'irish green', 'pink/purple', 'dark navy', 'greeny blue', 'light plum', 'pinkish grey', 'dirty orange', 'rust red', 'pale lilac', 'orangey red', 'primary blue', 'kermit green', 'brownish purple', 'murky green', 'wheat', 'very dark purple', 'bottle green', 'watermelon', 'deep sky blue', 'fire engine red', 'yellow ochre', 'pumpkin orange', 'pale olive', 'light lilac', 'lightish green', 'carolina blue', 'mulberry', 'shocking pink', 'auburn', 'bright lime green', 'celadon', 'pinkish brown', 'poo brown', 'bright sky blue', 'celery', 'dirt brown', 'strawberry', 'dark lime', 'copper', 'medium brown', 'muted green', "robin's egg", 'bright aqua', 'bright lavender', 'ivory', 'very light purple', 'light navy', 'pink red', 'olive brown', 'poop brown', 'mustard green', 'ocean green', 'very dark blue', 'dusty green', 'light navy blue', 'minty green', 'adobe', 'barney', 'jade green', 'bright light blue', 'light lime', 'dark khaki', 'orange yellow', 'ocre', 'maize', 'faded pink', 'british racing green', 'sandstone', 'mud brown', 'light sea green', 'robin egg blue', 'aqua marine', 'dark sea green', 'soft pink', 'orangey brown', 'cherry red', 'burnt yellow', 'brownish grey', 'camel', 'purplish grey', 'marine', 'greyish pink', 'pale turquoise', 'pastel yellow', 'bluey purple', 'canary yellow', 'faded red', 'sepia', 'coffee', 'bright magenta', 'mocha', 'ecru', 'purpleish', 'cranberry', 'darkish green', 'brown orange', 'dusky rose', 'melon', 'sickly green', 'silver', 'purply blue', 'purpleish blue', 'hospital green', 'shit brown', 'mid blue', 'amber', 'easter green', 'soft blue', 'cerulean blue', 'golden brown', 'bright turquoise', 'red pink', 'red purple', 'greyish brown', 'vermillion', 'russet', 'steel grey', 'lighter purple', 'bright violet', 'prussian blue', 'slate green', 'dirty pink', 'dark blue green', 'pine', 'yellowy green', 'dark gold', 'bluish', 'darkish blue', 'dull red', 'pinky red', 'bronze', 'pale teal', 'military green', 'barbie pink', 'bubblegum pink', 'pea soup green', 'dark mustard', 'shit', 'medium purple', 'very dark green', 'dirt', 'dusky pink', 'red violet', 'lemon yellow', 'pistachio', 'dull yellow', 'dark lime green', 'denim blue', 'teal blue', 'lightish blue', 'purpley blue', 'light indigo', 'swamp green', 'brown green', 'dark maroon', 'hot purple', 'dark forest green', 'faded blue', 'drab green', 'light lime green', 'snot green', 'yellowish', 'light blue green', 'bordeaux', 'light mauve', 'ocean', 'marigold', 'muddy green', 'dull orange', 'steel', 'electric purple', 'fluorescent green', 'yellowish brown', 'blush', 'soft green', 'bright orange', 'lemon', 'purple grey', 'acid green', 'pale lavender', 'violet blue', 'light forest green', 'burnt red', 'khaki green', 'cerise', 'faded purple', 'apricot', 'dark olive green', 'grey brown', 'green grey', 'true blue', 'pale violet', 'periwinkle blue', 'light sky blue', 'blurple', 'green brown', 'bluegreen', 'bright teal', 'brownish yellow', 'pea soup', 'forest', 'barney purple', 'ultramarine', 'purplish', 'puke yellow', 'bluish grey', 'dark periwinkle', 'dark lilac', 'reddish', 'light maroon', 'dusty purple', 'terra cotta', 'avocado', 'marine blue', 'teal green', 'slate grey', 'lighter green', 'electric green', 'dusty blue', 'golden yellow', 'bright yellow', 'light lavender', 'umber', 'poop', 'dark peach', 'jungle green', 'eggshell', 'denim', 'yellow brown', 'dull purple', 'chocolate brown', 'wine red', 'neon blue', 'dirty green', 'light tan', 'ice blue', 'cadet blue', 'dark mauve', 'very light blue', 'grey purple', 'pastel pink', 'very light green', 'dark sky blue', 'evergreen', 'dull pink', 'aubergine', 'mahogany', 'reddish orange', 'deep green', 'vomit green', 'purple pink', 'dusty pink', 'faded green', 'camo green', 'pinky purple', 'pink purple', 'brownish red', 'dark rose', 'mud', 'brownish', 'emerald green', 'pale brown', 'dull blue', 'burnt umber', 'medium green', 'clay', 'light aqua', 'light olive green', 'brownish orange', 'dark aqua', 'purplish pink', 'dark salmon', 'greenish grey', 'jade', 'ugly green', 'dark beige', 'emerald', 'pale red', 'light magenta', 'sky', 'light cyan', 'yellow orange', 'reddish purple', 'reddish pink', 'orchid', 'dirty yellow', 'orange red', 'deep red', 'orange brown', 'cobalt blue', 'neon pink', 'rose pink', 'greyish purple', 'raspberry', 'aqua green', 'salmon pink', 'tangerine', 'brownish green', 'red brown', 'greenish brown', 'pumpkin', 'pine green', 'charcoal', 'baby pink', 'cornflower', 'blue violet', 'chocolate', 'greyish green', 'scarlet', 'green yellow', 'dark olive', 'sienna', 'pastel purple', 'terracotta', 'aqua blue', 'sage green', 'blood red', 'deep pink', 'grass', 'moss', 'pastel blue', 'bluish green', 'green blue', 'dark tan', 'greenish blue', 'pale orange', 'vomit', 'forrest green', 'dark lavender', 'dark violet', 'purple blue', 'dark cyan', 'olive drab', 'pinkish', 'cobalt', 'neon purple', 'light turquoise', 'apple green', 'dull green', 'wine', 'powder blue', 'off white', 'electric blue', 'dark turquoise', 'blue purple', 'azure', 'bright red\t#ff000dpinkish red', 'cornflower blue', 'light olive', 'grape', 'greyish blue', 'purplish blue', 'yellowish green', 'greenish yellow', 'medium blue', 'dusty rose', 'light violet', 'midnight blue', 'bluish purple', 'red orange', 'dark magenta', 'greenish', 'ocean blue', 'coral', 'cream', 'reddish brown', 'burnt sienna', 'brick', 'sage', 'grey green', 'white', "robin's egg blue", 'moss green', 'steel blue', 'eggplant', 'light yellow', 'leaf green', 'light grey', 'puke', 'pinkish purple', 'sea blue', 'pale purple', 'slate blue', 'blue grey', 'hunter green', 'fuchsia', 'crimson', 'pale yellow', 'ochre', 'mustard yellow', 'light red', 'cerulean', 'pale pink', 'deep blue', 'rust', 'light teal', 'slate', 'goldenrod', 'dark yellow', 'dark grey', 'army green', 'grey blue', 'seafoam', 'puce', 'spring green', 'dark orange', 'sand', 'pastel green', 'mint', 'light orange', 'bright pink', 'chartreuse', 'deep purple', 'dark brown', 'taupe', 'pea green', 'puke green', 'kelly green', 'seafoam green', 'blue green', 'khaki', 'burgundy', 'dark teal', 'brick red', 'royal purple', 'plum', 'mint green', 'gold', 'baby blue', 'yellow green', 'bright purple', 'dark red', 'pale blue', 'grass green', 'navy', 'aquamarine', 'burnt orange', 'neon green', 'bright blue', 'rose', 'light pink', 'mustard', 'indigo', 'lime', 'sea green', 'periwinkle', 'dark pink', 'olive green', 'peach', 'pale green', 'light brown', 'hot pink', 'black', 'lilac', 'navy blue', 'royal blue', 'beige', 'salmon', 'olive', 'maroon', 'bright green', 'dark purple', 'mauve', 'forest green', 'aqua', 'cyan', 'tan', 'dark blue', 'lavender', 'turquoise', 'dark green', 'violet', 'light purple', 'lime green', 'grey', 'sky blue', 'yellow', 'magenta', 'light green', 'orange', 'teal', 'light blue', 'red', 'brown', 'pink', 'blue', 'green', 'purple'],
            ['few','a lot of', 'some'],
            #['get', 'acquire', 'obtain', 'secure', 'procure', 'gain', 'fetch', 'find', 'scoe', 'accumulate', 'win', 'earn', 'rep', 'catch', 'net', 'bag', 'derive', 'collect', 'gather', 'glean', 'pick up', 'accept', 'come by', 'regain', 'salvage'],
            ['good', 'excellent', 'fine', 'superior', 'wonderful', 'marvelous', 'qualified', 'suited', 'suitable', 'apt', 'proper', 'capable', 'generous', 'kindly', 'friendly', 'gracious', 'obliging', 'pleasant', 'agreeable', 'pleasurable', 'satisfactory', 'well-behaved', 'obedient', 'honorable', 'reliable', 'trustworthy', 'safe', 'favorable', 'profitable', 'advantageous', 'righteous', 'expedient', 'helpful', 'valid', 'genuine', 'ample', 'salubrious', 'estimable', 'beneficial', 'splendid', 'great', 'noble', 'worthy', 'first-rate', 'top-notch', 'grand', 'sterling', 'superb', 'respectable', 'edifying'],
            ['interesting', ' fascinating', 'engaging', 'sharp', 'keen', 'bright', 'intelligent', 'animated', 'spirited', 'attractive', 'inviting', 'intriguing', 'provocative', 'though-provoking', 'challenging', 'inspiring', 'involving', 'moving', 'titillating', 'tantalizing', 'exciting', 'entertaining', 'piquant', 'lively', 'racy', 'spicy', 'engrossing', 'absorbing', 'consuming', 'gripping', 'arresting', 'enthralling', 'spellbinding', 'curious', 'captivating', 'enchanting', 'bewitching', 'appealing'],
            ['look', ' gaze', 'see', 'glance', 'watch', 'survey', 'study', 'seek', 'search for', 'peek', 'peep', 'glimpse', 'stare', 'contemplate', 'examine', 'gape', 'ogle', 'scrutinize', 'inspect', 'leer', 'behold', 'observe', 'view', 'witness', 'perceive', 'spy', 'sight', 'notice', 'recognize', 'peer', 'eye', 'gawk', 'peruse', 'explore'],
            ['old', 'feeble', 'frail', 'ancient', 'weak', 'aged', 'used', 'worn', 'dilapidated', 'ragged', 'faded', 'broken-down', 'former', 'old-fashioned', 'outmoded', 'passe', 'veteran', 'mature', 'venerable', 'primitive', 'traditional', 'archaic', 'conventional', 'customary', 'stale', 'musty', 'obsolete', 'extinct'],
            ['tell', 'say', 'inform', 'notify', 'advise', 'relate', 'recount', 'narrate', 'explain', 'reveal', 'disclose', 'divulge', 'declare', 'command', 'order', 'bid', 'enlighten', 'instruct', 'insist', 'teach', 'train', 'direct', 'issue', 'remark', 'converse', 'speak', 'affirm', 'suppose', 'utter', 'negate', 'express', 'verbalize', 'voice', 'articulate', 'pronounce', 'deliver', 'convey', 'impart', 'assert', 'state', 'allege', 'mutter', 'mumble', 'whisper', 'sigh', 'exclaim', 'yell', 'sing', 'yelp', 'snarl', 'hiss', 'grunt', 'snort', 'roar', 'bellow', 'thunder', 'scream', 'shriek', 'screech', 'squawk', 'whine', 'philosophize', 'stammer', 'stutter', 'lisp', 'drawl', 'jabber', 'protest', 'announce', 'swear', 'vow', 'content', 'assure', 'deny', 'dispute']
            ]


def save_generator_state(generator):
    with open('generator_state.pkl', 'wb') as f:
        pickle.dump(generator, f)


def get_generator(resume=True):
    """Get the generator state from pickle file
    :return: generator of synonym combinaison"""
    if resume:
        try:
            with open('generator_state.pkl', 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return product(*synonyms)
    else:
        return product(*synonyms)


if __name__ == '__main__':
    timestamp = datetime.now().strftime('%d_%m_%y_%Hh%M') # for logfile
    Result.set_reference_sentence('F*ck you, dear professor!')

    # resuming prgm state
    prod = get_generator()
    # best_result = get_best_result()

    best_result = Result.load_from_textfile()
    print('Search is running ...')
    try:
        for bad, beautiful, big, boring, colorname, few, good, interesting, look, old, tell in prod:
            forged = Result(f"{good.capitalize()} news or {bad} news? I'm gonna {tell} you and let you judge! "
                                f"This {big} {old} course {look}s {choice([interesting, boring])}. "
                                f"The workload seems {big} too. "
                                f"Also {few} people in the class are {beautiful} and {interesting}."
                                f"One guy always wear a {colorname} jacket.")

            if forged.nb_matching_bytes > best_result.nb_matching_bytes:
                forged.save_result_2textfile(f"log_{timestamp}.txt",'a')
                forged.save_result_2textfile()
                if forged == Result.reference:
                    print('Astonishing, we find a full match!, see in file h1_I.txt')
                    exit()

                # Ask user to continue execution or exit the prgm
                while True:
                    print('\n\nSentence:\n', forged.sentence,
                          '\nSentence hash: ', forged.hash,
                          '\nOriginal hash: ', Result.reference.hash,
                          '\nNb of matching bytes: ',  forged.nb_matching_bytes)
                    rep = input('\nDo you  want to continue to try to find another hash? y or n\n'
                                '"n" will the best result into h1_I.txt,'
                                'other results are logged in log_%s\n' % timestamp).lower()
                    if rep == 'y':
                        best_result = deepcopy(forged) # avoid modification of forged impact best_result and reciprocally
                        print('Trying to find a better sentence...')
                        break

                    elif rep == 'n':
                        print('Result was saved in h1_I.txt')
                        exit()
        print('All combination tried')

    finally:
        print('Saving anything')
        best_result.save_result_2textfile()
        save_generator_state(prod)