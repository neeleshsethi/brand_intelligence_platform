"""Base agent class with retry logic and mock mode support."""

from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
import instructor
from openai import OpenAI
from langsmith import traceable
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.config import settings
import json

T = TypeVar('T', bound=BaseModel)


class BaseAgent(Generic[T]):
    """Base agent with structured output, retry logic, and mock mode."""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        response_model: type[T],
        mock_response: Optional[T] = None
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.response_model = response_model
        self.mock_response = mock_response

        # Initialize instructor-patched OpenAI client
        if not settings.MOCK_MODE and settings.OPENAI_API_KEY:
            self.client = instructor.from_openai(
                OpenAI(api_key=settings.OPENAI_API_KEY)
            )
        else:
            self.client = None

    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=settings.RETRY_WAIT_SECONDS, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    @traceable(run_type="llm")
    def _call_llm(self, user_prompt: str) -> T:
        """Call LLM with retry logic and LangSmith tracing."""
        if settings.MOCK_MODE or not self.client:
            if self.mock_response:
                return self.mock_response
            else:
                raise ValueError(f"Mock mode enabled but no mock response provided for {self.name}")

        # Prepare messages for tracing
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Use instructor for structured output
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=self.response_model,
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )

        return response

    @traceable(run_type="chain")
    async def run(self, user_prompt: str) -> T:
        """Run the agent with the given prompt."""
        try:
            result = self._call_llm(user_prompt)
            return result
        except Exception as e:
            print(f"Error in {self.name}: {str(e)}")
            raise

    def format_output(self, output: T) -> dict:
        """Format output as dictionary."""
        return output.model_dump()
