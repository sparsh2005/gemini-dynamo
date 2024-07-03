from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware

from services.genai import (
    YoutubeProcessor,
    GeminiProcessor
)

class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl
    # advanced settings

app=FastAPI()

#configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai_processor = GeminiProcessor(
        model_name = "gemini-pro",
        project = "gemini-explorer-422106"
    )

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):
    #doing the analysis
    processor = YoutubeProcessor(genai_processor = genai_processor)
    result = processor.retrieve_youtube_documents(str(request.youtube_link), verbose=True)

    #summary = genai_processor.generate_document_summary(result, verbose=True)
    
    #find key concepts
    key_concepts_list = processor.find_key_concepts(result, verbose=True)

    return {
        "key_concepts": key_concepts_list
    }
