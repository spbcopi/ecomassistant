import os
import sys
from dotenv import load_dotenv
from assistant.utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from assistant.logger import GLOBAL_LOGGER as log
from assistant.exception.custom_exception import ProductAssistantException
import asyncio
from api_key_manager import ApiKeyMgr

class ModelLoader:
    """
    Loads embedding models and LLMs based on config and environment.
    """
    def __init__(self):
        if os.getenv("ENV", "local").lower() != "production":
            load_dotenv()
            log.info("Running in LOCAL mode: .env loaded")
        else:
            log.info("Running in PRODUCTION mode")

        self.api_key_mgr = ApiKeyMgr()
        self.config = load_config()
        log.info("YAML config loaded", config_keys=list(self.config.keys()))
    
    def load_embedding_model(self):
        """
        Load and return embedding model from Google Generative AI.
        """
        try:
            model_name = self.config["embedding_model"]["model_name"]
            log.info("Loading embedding model", model=model_name)

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())

            return GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY")
            )
        except Exception as e:
            log.error("Failed to get embedding model config", error=str(e))
            raise ProductAssistantException("Invalid embedding model config", sys)