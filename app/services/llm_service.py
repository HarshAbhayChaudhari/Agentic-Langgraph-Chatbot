import os
from typing import Optional
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self, model_name: str = "llama3-8b-8192"):
        """
        Initialize LLM service with Groq
        
        Args:
            model_name: Name of the Groq model to use
        """
        self.model_name = model_name
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """
        Initialize the LLM with Groq
        """
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise Exception("GROQ_API_KEY not found in environment variables")
            
            self.llm = ChatGroq(
                groq_api_key=api_key,
                model_name=self.model_name
            )
            
            print(f"LLM initialized with model: {self.model_name}")
            
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            raise
    
    def generate_answer(self, query: str, context: str) -> str:
        """
        Generate an answer based on the query and context
        
        Args:
            query: User's question
            context: Relevant context from WhatsApp messages
            
        Returns:
            Generated answer
        """
        if not self.llm:
            raise Exception("LLM not initialized")
        
        try:
            # Create system prompt
            system_prompt = """You are a helpful assistant that answers questions based on WhatsApp chat messages. 
            Use only the information provided in the context to answer the user's question. 
            If the context doesn't contain enough information to answer the question, say so.
            Be conversational and helpful in your responses."""
            
            # Create user prompt
            user_prompt = f"""Based on the following WhatsApp messages, please answer this question: {query}

Context (WhatsApp messages):
{context}

Answer:"""
            
            # Generate response
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return response.content
            
        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"
    
    def generate_summary(self, messages: list) -> str:
        """
        Generate a summary of WhatsApp messages
        
        Args:
            messages: List of WhatsApp messages
            
        Returns:
            Generated summary
        """
        if not self.llm:
            raise Exception("LLM not initialized")
        
        try:
            # Create context from messages
            context = "\n".join(messages)
            
            system_prompt = """You are a helpful assistant that summarizes WhatsApp conversations. 
            Provide a concise and informative summary of the conversation."""
            
            user_prompt = f"""Please provide a summary of the following WhatsApp conversation:

{context}

Summary:"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return response.content
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return f"I'm sorry, I encountered an error while generating the summary: {str(e)}"
    
    def extract_keywords(self, text: str) -> list:
        """
        Extract keywords from text
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of keywords
        """
        if not self.llm:
            raise Exception("LLM not initialized")
        
        try:
            system_prompt = """You are a helpful assistant that extracts keywords from text. 
            Return only a comma-separated list of relevant keywords."""
            
            user_prompt = f"""Extract the most important keywords from this text:

{text}

Keywords:"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse keywords from response
            keywords_text = response.content.strip()
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            
            return keywords
            
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return [] 