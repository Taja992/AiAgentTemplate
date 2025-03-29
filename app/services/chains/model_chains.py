from typing import List, Dict, Any, Optional
import asyncio
from functools import partial

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOllama

from app.services.chains.base import BaseChain
from app.models.schemas import Message
from app.utils.logger import get_logger

logger = get_logger(__name__)

class CodeLlamaChain(BaseChain):
    """Chain for CodeLlama that enforces programming-focused responses."""

    async def run(
            self,
            messages: List[Message],
            model: str,
            temperature: float = 0.7,
            max_tokens: int = 1000,
            **kwargs
    ) -> Dict[str, Any]:
        # Prompt template to follow
        system_message = """You are a programming assistant that ONLY provides code examples, explanations of programming concepts, 
        or direct answers to technical questions. If asked about non-programming topics, politely explain that 
        you can only assist with programming-related queries."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        model_name = model.split(":", 1)[1] if ":" in model else model


        # Create the LangChain LLM
        llm = ChatOllama(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Create and run the chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Convert messages to history format
        history = [{"role": msg.role, "content": msg.content} for msg in messages[:-1]]

        # Get the last user message as input
        input_message = next ((msg.content for msg in reversed(messages) if msg.role.lower() == "user" ), "")

        try:
            # Run in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(chain.invoke, {"history": history, "input": input_message})
            )

            return {
                "content": response,
                "model": model,
                "usage": {}
            }
        except Exception as e:
            logger.error(f"Error in CodeLlamaChain: {str(e)}")
            raise