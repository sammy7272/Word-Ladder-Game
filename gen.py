import random

def is_one_letter_different(word1, word2):
    """Check if two words differ by exactly one letter."""
    if len(word1) != len(word2):
        return False
    differences = sum(1 for a, b in zip(word1, word2) if a != b)
    return differences == 1

def find_neighbors(word, word_list):
    """Find all words in the list that differ by one letter."""
    return [w for w in word_list if is_one_letter_different(word, w)]

def filter_connected_words(word_list):
    """Filter words to ensure each word has at least one neighbor."""
    connected_words = set()
    for word in word_list:
        neighbors = find_neighbors(word, word_list)
        if neighbors:
            connected_words.add(word)
    return connected_words

def generate_dictionary():
    """Generate a dictionary of 3-letter, 5-letter, and 7-letter connected words."""
    # Base word lists (you can replace these with your own lists or load from a file)
    three_letter_words = [
        "cat", "dog", "hat", "bat", "bet", "let", "set", "sit", "hit", "hot", 
        "dot", "pot", "pen", "pin", "pig", "big", "bag", "bug", "bud", "but", 
        "cut", "cup", "cap", "car", "bar", "far", "fat", "rat", "mat", "map", 
        "man", "pan", "fan", "fun", "run", "sun", "son", "sin", "win", "wig", 
        "wag", "tag", "tap", "tip", "top", "mop", "mom", "dad", "sad", "mad", 
        "pad", "bad", "bed", "red", "fed", "wed", "wet", "get", "net", "not", 
        "now", "cow", "how", "bow", "boy", "toy", "joy", "job", "jog", "log", 
        "fog", "fig", "dig", "dip", "lip", "lap", "tap"
    ]

    five_letter_words = [
        "apple", "brave", "crane", "dance", "eagle", "flame", "grape", "honey", 
        "image", "jelly", "knight", "lemon", "mango", "olive", "peach", "queen", 
        "river", "snake", "tiger", "urban", "vapor", "whale", "youth", "zebra", 
        "about", "above", "acute", "admit", "adopt", "agree", "alarm", "alert", 
        "allow", "alter", "among", "anger", "angle", "angry", "apart", "apply", 
        "argue", "arise", "armor", "arrow", "aside", "asset", "audio", "avoid", 
        "award", "aware", "beach", "begin", "below", "bench", "birth", "black", 
        "blame", "blank", "blast", "blend", "block", "blood", "board", "boost", 
        "brain", "bread", "break", "breed", "brick", "brief", "bring", "broad", 
        "brush", "build", "burst", "cabin", "cable", "candy", "carry", "catch", 
        "cause", "chain", "chair", "chalk", "charm", "chart", "chase", "cheap", 
        "check", "cheer", "chest", "chief", "child", "civil", "claim", "class", 
        "clean", "clear", "climb", "clock", "close", "cloud", "coach", "coast", 
        "color", "comic", "commit", "common", "coral", "corner", "cotton", "count", 
        "court", "cover", "crash", "cream", "crime", "cross", "crowd", "crown", 
        "curve", "cycle", "daily", "dance", "danger", "dated", "death", "delay", 
        "depth", "diary", "dirty", "discuss", "divide", "doubt", "dozen", "draft", 
        "drama", "dream", "dress", "drift", "drink", "drive", "eager", "early", 
        "earth", "echo", "edge", "effect", "elect", "empty", "enjoy", "enter", 
        "equal", "error", "event", "exact", "exist", "extra", "faith", "fancy", 
        "fault", "favor", "fence", "field", "fight", "final", "focus", "force", 
        "frame", "fresh", "front", "fruit", "funny", "gauge", "ghost", "giant", 
        "glass", "globe", "glory", "grace", "grade", "grain", "grand", "grant", 
        "grass", "grave", "great", "green", "greet", "group", "guard", "guess", 
        "guide", "habit", "happy", "harsh", "heart", "heavy", "hello", "honor", 
        "horse", "hotel", "house", "human", "humor", "ideal", "imply", "index", 
        "inner", "input", "issue", "joint", "judge", "juice", "knock", "known", 
        "label", "labor", "large", "laser", "later", "laugh", "layer", "learn", 
        "least", "leave", "legal", "level", "light", "limit", "local", "logic", 
        "loose", "lower", "lucky", "lunch", "magic", "major", "march", "match", 
        "maybe", "media", "metal", "method", "middle", "minor", "model", "money", 
        "month", "moral", "motor", "mount", "mouse", "mouth", "movie", "music", 
        "naked", "nerve", "never", "night", "noise", "north", "notice", "novel", 
        "nurse", "occur", "ocean", "offer", "often", "order", "other", "outer", 
        "owner", "paint", "panel", "paper", "party", "patch", "pause", "peace", 
        "pedal", "penny", "phase", "phone", "photo", "piano", "pilot", "pitch", 
        "place", "plane", "plant", "plate", "point", "porch", "pound", "power", 
        "press", "price", "pride", "prime", "prize", "proof", "proud", "pulse", 
        "quick", "quiet", "quite", "quote", "radio", "raise", "range", "rapid", 
        "reach", "react", "ready", "refer", "relax", "reply", "right", "robot", 
        "rough", "round", "route", "royal", "rural", "scale", "scene", "scope", 
        "score", "sense", "serve", "shade", "share", "sharp", "sheep", "shelf", 
        "shell", "shift", "shine", "shock", "shoot", "short", "sight", "since", 
        "skill", "sleep", "slide", "small", "smart", "smile", "smoke", "solid", 
        "solve", "sound", "south", "space", "speak", "speed", "spell", "spend", 
        "spill", "split", "sport", "stand", "stare", "start", "state", "steel", 
        "stick", "still", "stone", "store", "storm", "story", "strip", "study", 
        "style", "sugar", "super", "table", "taste", "teach", "thank", "theme", 
        "there", "thick", "thing", "think", "third", "those", "three", "throw", 
        "tight", "tired", "title", "today", "total", "touch", "tough", "tower", 
        "track", "trade", "train", "treat", "trend", "trial", "trust", "twist", 
        "uncle", "under", "union", "until", "usual", "value", "video", "visit", 
        "voice", "waste", "watch", "water", "weigh", "wheel", "where", "which", 
        "while", "white", "whole", "whose", "woman", "world", "worry", "worth", 
        "would", "write", "wrong", "young", "youth"
    ]

    seven_letter_words = [
        "ability", "absence", "academy", "achieve", "acquire", "address", "advance", 
        "advice", "alcohol", "ancient", "analyze", "anxiety", "apology", "approve", 
        "arrange", "article", "athlete", "attempt", "attract", "average", "balance", 
        "balloon", "benefit", "biology", "blanket", "bravery", "breathe", "brilliant", 
        "brother", "buffalo", "cabinet", "capable", "capital", "capture", "careful", 
        "caution", "ceiling", "celebrate", "century", "certain", "chapter", "charity", 
        "chemistry", "classic", "climate", "clothes", "collect", "comfort", "command", 
        "comment", "company", "compare", "compete", "complex", "concern", "conduct", 
        "confirm", "connect", "consent", "consist", "contain", "content", "contest", 
        "context", "control", "convert", "correct", "courage", "curious", "current", 
        "decline", "deliver", "density", "deposit", "despair", "destroy", "develop", 
        "diamond", "discuss", "disease", "display", "disturb", "divorce", "dynamic", 
        "economy", "educate", "electric", "element", "embrace", "emotion", "emperor", 
        "empower", "enforce", "enhance", "enough", "entertain", "envelope", "episode", 
        "evening", "evident", "exactly", "example", "excited", "exclude", "exhibit", 
        "expense", "explain", "explore", "express", "extreme", "factory", "failure", 
        "fashion", "feature", "federal", "fiction", "finally", "finance", "fitness", 
        "forward", "freedom", "frequent", "gallery", "general", "genuine", "gesture", 
        "glacier", "glimpse", "gravity", "grocery", "guarantee", "guidance", "habitat", 
        "harvest", "healthy", "hearing", "history", "holiday", "horizon", "hospital", 
        "humanity", "imagine", "improve", "include", "initial", "inquiry", "inspire", 
        "install", "instant", "intense", "involve", "isolate", "justify", "kingdom", 
        "kitchen", "landing", "leading", "leather", "liberty", "library", "license", 
        "logical", "machine", "magazine", "maintain", "manager", "marriage", "measure", 
        "medical", "meeting", "mention", "message", "million", "minimum", "miracle", 
        "mission", "mixture", "monitor", "morning", "musical", "mystery", "natural", 
        "neglect", "nervous", "network", "neutral", "notable", "nuclear", "obvious", 
        "offense", "opinion", "organic", "organize", "outcome", "outdoor", "outline", 
        "overcome", "package", "painting", "parking", "partner", "passion", "patient", 
        "pattern", "payment", "penalty", "pension", "percent", "perfect", "perform", 
        "perhaps", "persist", "picture", "plastic", "pleasant", "pleasure", "politics", 
        "popular", "portion", "possess", "practice", "prepare", "present", "prevent", 
        "primary", "process", "produce", "program", "project", "promise", "promote", 
        "protect", "protein", "provide", "publish", "purpose", "qualify", "quality", 
        "quarter", "radical", "railway", "realize", "receive", "recover", "reflect", 
        "regular", "release", "relieve", "request", "require", "reserve", "resolve", 
        "respect", "respond", "restore", "revenue", "reverse", "routine", "running", 
        "satisfy", "science", "section", "segment", "serious", "service", "session", 
        "shelter", "silence", "similar", "society", "soldier", "special", "species", 
        "sponsor", "stadium", "standard", "station", "stomach", "storage", "strange", 
        "stretch", "student", "subject", "success", "suggest", "support", "surface", 
        "surprise", "survive", "suspend", "sustain", "symptom", "teacher", "theater", 
        "therapy", "thought", "through", "traffic", "trouble", "typical", "uniform", 
        "unknown", "upgrade", "utility", "variety", "victory", "village", "visible", 
        "visitor", "vitamin"
    ]

    # Combine all words and remove duplicates
    all_words = list(set(three_letter_words + five_letter_words + seven_letter_words))

    # Ensure all words are connected
    connected_words = filter_connected_words(all_words)

    # Convert the set to a list for sampling
    connected_words_list = list(connected_words)

    # Select the first 1000 words from the connected words
    selected_words = connected_words_list[:1000]

    # Save to dictionary.txt
    with open("dictionary.txt", "w") as f:
        for word in selected_words:
            f.write(word + "\n")

    print(f"Generated dictionary.txt with {len(selected_words)} connected words.")

if __name__ == "__main__":
    generate_dictionary()