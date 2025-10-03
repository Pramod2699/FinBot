from src.utils.Logger import Logger
from src.config.ConfigHelper import ConfigHelper
from src.helpers.PromptTemplate import PromptTemplate
from src.helpers.OpenAIHelper import AIHelper
from src.models.FaissClient import FaissClient
import time

class AnswerGenerator:
    def __init__(self):
        self.__config = ConfigHelper().config
        self.__loggerObj = Logger()
        self.prompt = PromptTemplate(self.__loggerObj)
        self.ai = AIHelper(self.__loggerObj, self.__config)
        self.faiss = FaissClient(self.__loggerObj,self.__config)

    def generate_answer(
        self,
        query: str
    ) -> str:
        """Generates an answer for the given query.

        Args:
            query (str): The query string.

        Returns:
            str: The generated answer.
        """

        self.__loggerObj.info("Generate Answer called")
        start_time = time.perf_counter()  # <-- START TIMER
        self.__loggerObj.critical("query: " + str(query))
        response = None
        # chat_history_formatted = "\n".join(
        #     [single_chat for single_chat in chat_history]
        # )
        # self.logger.info("Chat History formated")
        # t1 = time.perf_counter()

        retrived_data = self.faiss.similarity_search(query)
        t1 = time.perf_counter()
        self.__loggerObj.info(f"Faiss Search Time: {time.perf_counter() - t1:.2f}s")

        if retrived_data == []:
            response = "It seems like I didn't quite catch that. Could you please rephrase your question or ask in a slightly different way? I'm here to help and want to make sure I understand you correctly."
            self.__loggerObj.critical("Unable to retrive data from vector store")
        else:
            context = "\n\n".join(retrived_data.values())
            response = self.ai.genrate_from_prompt(self.__config['openai']['models']['answer_relevancy'],prompt=self.prompt.reply_prompt(context,query))
            t2 = time.perf_counter()
            self.__loggerObj.info(f"Answer Generation Time: {time.perf_counter() - t2:.2f}s")

        total_time = time.perf_counter() - start_time
        self.__loggerObj.info((f"Total generate_answer Time: {total_time:.2f}s"))
        return response


