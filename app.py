from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

# Allow requests from the assignment evaluator/browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: list[str]


def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower().strip()

    # Common negative phrases
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
        "not enjoyable",
        "not excellent",
        "not amazing",
        "not wonderful",
        "not useful",
        "not helpful",
    ]

    for phrase in negative_phrases:
        if phrase in text:
            return "sad"

    # Use TextBlob for general sentiment analysis
    polarity = TextBlob(sentence).sentiment.polarity

    if polarity > 0.1:
        return "happy"

    elif polarity < -0.1:
        return "sad"

    else:
        return "neutral"


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": analyze_sentiment(sentence)
        })

    return {
        "results": results
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )