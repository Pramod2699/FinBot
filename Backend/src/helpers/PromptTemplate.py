class PromptTemplate:
    def __init__(self, logger):
        self.__loggerObj = logger
    
    def summarization_prompt(self, data: str) -> str:
        """Generates a prompt for summarizing based on the provided data.
        Args:
            data (str): The data information scraped from web.
        Returns:
            str: A formatted prompt used for similarity search in faiss db.
        """
        self.__loggerObj.info("Summarization prompt called")
        summarizationPrompt = f"""
            Summarize the given content into 150–250 words for vector embeddings.

Focus on:
- Loan scheme name & purpose
- Key features, benefits, interest rates, tenure, concessions, fees
- Eligibility (salaried, self-employed, NRIs, PIOs, etc.)
- Required documents
- Loan types offered
- Application process, EMI, prepayment rules

Write factually, without marketing language.
Avoid repetition. Make it semantically dense.

CONTENT:
{data}"""
        return summarizationPrompt
    
    def reply_prompt(self,context,question):

        prompt = f"""You are a knowledgeable assistant specializing in banking products, specifically loans offered by Maharashtra Bank. 
A user will ask you questions related to these loans.

Use the following context to answer the question accurately:
{context}

Instructions:
- Provide concise, user-friendly answers in plain text only.
- Avoid extra formatting like JSON, tables, or bullet points; just return a readable string.
- Include numeric values (like interest rates, EMI) clearly with units.
- If the information is missing or unclear in the context, respond: 
  "I’m sorry, I don’t have the latest details on that, please check with Maharashtra Bank directly."
- Maintain a professional and helpful tone.

User Question:
{question}

Answer strictly as a text string.
"""
        return prompt