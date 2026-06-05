"""
Cloud / Internet LLM Provider Adapters — EXTENSION POINT

This module is a placeholder for future cloud-based LLM providers.
When ready, add new ProviderAdapter subclasses here and register
them in the ADAPTER_TYPES dict in `llm` (the main CLI script).

Example structure for a future provider:

    class OpenAiCloudAdapter(ProviderAdapter):
        \"\"\"OpenAI API. Requires API key in provider config.\"\"\"
        def models_path(self) -> str: return "/v1/models"
        def chat_path(self) -> str: return "/v1/chat/completions"
        def is_stream_sse(self) -> bool: return True

        def parse_model_list(self, raw: dict) -> List[str]:
            return [m["id"] for m in raw.get("data", [])]

        def parse_chunk(self, chunk: dict) -> str:
            return chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")

Registration in `llm`:

    # In the ADAPTER_TYPES dict, add:
    #   "openai-api": OpenAiCloudAdapter,
    #   "anthropic": AnthropicAdapter,

Provider config in ~/.llm_config.json:

    {
      "providers": {
        "openai-api": {
          "type": "openai",             # matches ADAPTER_TYPES key
          "base_url": "https://api.openai.com/v1",
          "api_key": "sk-...",          # or use env var / secrets
          "models": [
            {"id": "gpt-4o", "name": "GPT-4o"}
          ]
        }
      }
    }

The LoggingProxy in `llm` automatically wraps all adapters with:
- Auth header injection (via Proxy)
- Request/response logging
- Rate limiting / retry (future)
"""

# When implementing cloud providers, uncomment and extend:
# from .llm import ProviderAdapter  # if split into package
# Or copy the ProviderAdapter ABC here and register in ADAPTER_TYPES.
