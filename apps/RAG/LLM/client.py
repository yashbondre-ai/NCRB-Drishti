"""
Groq LLM client service.

Reads the Groq API key from Django settings.

Provides:
    - GroqLLMService.generate_answer(context, question)
"""

import logging

from django.conf import settings
from groq import Groq

from .prompt import build_rag_prompt

logger = logging.getLogger(__name__)


class GroqLLMService:
    """Wrapper around the Groq API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or getattr(settings, "GROQ_API_KEY", "") or ""

        if not self.api_key:
            logger.error("Groq API Key Found: No")
            raise ValueError(
                "Groq API key is missing. "
                "Set GROQ_API_KEY in your .env file."
            )

        logger.info("Groq API Key Found: Yes")

        self.model = getattr(
            settings,
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

        try:
            self.client = Groq(api_key=self.api_key)
            logger.info("Groq Client Created Successfully")
        except Exception as exc:
            logger.exception("Failed to create Groq client.")
            raise ValueError(
                f"Groq client initialization failed: {exc}"
            ) from exc

    def generate_answer(self, context: str, question: str) -> str:
        """Generate an answer using Groq."""

        prompt = build_rag_prompt(
            context=context,
            question=question,
        )

        logger.info("Sending request to Groq...")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.2,
                max_tokens=1024,
            )

        except Exception as exc:
            logger.exception("Groq request failed.")
            raise ValueError(
                f"Groq request failed: {exc}"
            ) from exc

        answer = ""

        if (
            response
            and response.choices
            and response.choices[0].message
        ):
            answer = response.choices[0].message.content or ""

        logger.info(
            "Response received. Length: %d characters",
            len(answer),
        )

        if not answer:
            logger.warning("Groq returned an empty response.")
            raise ValueError(
                "Groq returned an empty response."
            )

        return answer