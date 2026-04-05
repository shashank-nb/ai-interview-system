from textblob import TextBlob

def analyze_answer(answer):

    analysis = TextBlob(answer)

    sentiment = analysis.sentiment.polarity
    score = round((sentiment + 1) * 50, 2)

    word_count = len(answer.split())

    if word_count < 10:
        feedback = "Answer is too short"
    elif word_count < 20:
        feedback = "Average explanation"
    else:
        feedback = "Excellent explanation"

    return score, feedback