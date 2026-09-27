from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SentimentRequest(BaseModel):
    sentences: list[str]


positive_words = [
    "love", "loved", "loving",
    "like", "liked", "likes",
    "great", "good", "better", "best",
    "excellent", "amazing", "awesome",
    "wonderful", "fantastic", "perfect",
    "happy", "happier", "happiness",
    "enjoy", "enjoyed", "enjoying",
    "pleased", "satisfied",
    "beautiful", "brilliant",
    "helpful", "useful",
    "success", "successful",
    "win", "won", "winning",
    "excited", "exciting",
    "fun", "nice", "positive",
    "recommend", "recommended",
    "impressive", "incredible",
    "thank", "thanks", "grateful"
]

negative_words = [
    "hate", "hated", "hating",
    "bad", "worse", "worst",
    "terrible", "awful", "horrible",
    "sad", "unhappy",
    "angry", "anger",
    "disappointed", "disappointing",
    "disappointment",
    "poor", "boring", "bored",
    "fail", "failed", "failure",
    "problem", "problems",
    "broken", "damage", "damaged",
    "wrong", "error", "errors",
    "difficult", "hard",
    "annoying", "annoyed",
    "frustrated", "frustrating",
    "useless", "waste",
    "negative", "pain", "painful",
    "sadly", "unfortunately",
    "complaint", "complaints",
    "refund", "scam"
]


def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

    # Handle common negative phrases
    negative_phrases = [
        "don't like",
        "do not like",
        "doesn't like",
        "didn't like",
        "did not like",
        "don't love",
        "do not love",
        "doesn't love",
        "didn't love",
        "did not love",
        "not happy",
        "not good",
        "not great",
        "not satisfied",
        "not enjoyable"
    ]

    for phrase in negative_phrases:
        if phrase in text:
            return "sad"

    positive_count = sum(
        1 for word in positive_words
        if word in text
    )

    negative_count = sum(
        1 for word in negative_words
        if word in text
    )

    if positive_count > negative_count:
        return "happy"

    if negative_count > positive_count:
        return "sad"

    return "neutral"


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": analyze_sentiment(sentence)
        })

    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)