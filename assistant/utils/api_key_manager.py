import os
import sys
import json
from assistant.logger import GLOBAL_LOGGER as log
from assistant.exception.custom_exception import AssistantException as ProductAssistantException

class ApiKeyMgr:
    required_keys = [
        "GOOGLE_API_KEY",
        "GROQ_API_KEY"]
    
    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("API_KEYS")

        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise Exception("API_KEYS must be a JSON object")
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse API_KEYS: {e}")
        
        for key in self.required_keys:
            if not self.api_keys.get(key):
                value = os.getenv(key)
                if not value:
                    raise Exception(f"Missing required API key: {key}")
                self.api_keys[key] = value
                log.info(f"Loaded {key} from individual env var")

        missing = [a for a in self.REQUIRED_KEYS if not self.api_keys.get(a)]

        if missing:
            log.error("Missing required API keys", missing_keys=missing)
            raise ProductAssistantException("Missing API keys", sys)
        
        log.info("API keys loaded", keys={k: v[:6] + "..." for k, v in self.api_keys.items()})

    def get(self, key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val