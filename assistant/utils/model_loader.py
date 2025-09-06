import os
import sys
import asyncio
from dotenv import load_dotenv
from assistant.utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from assistant.logger import GLOBAL_LOGGER as log
from assistant.exception.custom_exception import ProductAssistantException
from api_key_manager import ApiKeyMgr
from langchain.chat_models import ChatOpenAI

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
        
    def load_llm(self):
        """
        Load and return the configured LLM model.
        """
        llm_block = self.config["llm"]
        provider_key = os.getenv("LLM_PROVIDER", "google")

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider=provider_key)
            raise ValueError(f"LLM provider '{provider_key}' not found in config")

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)
    
        log.info("Loading LLM", provider=provider, model=model_name)

        match provider:
            case "google":
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY"),
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            case "groq":
                return ChatGroq(
                    model=model_name,
                    api_key=self.api_key_mgr.get("GROQ_API_KEY"), #type: ignore
                    temperature=temperature,
                )           
            case "openai":
                return ChatOpenAI(
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    openai_api_key=self.api_key_mgr.get("OPENAI_API_KEY")
                )
            case _:
                log.error("Unsupported LLM provider", provider=provider)
                raise ValueError(f"Unsupported LLM provider: {provider}")

            



