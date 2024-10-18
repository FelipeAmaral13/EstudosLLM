import os
import hashlib
import json
import requests.exceptions
import time
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class YouTubeVideoSummarizer:
    def __init__(self, url_video: str, query_user: str, model_class: str, model_params: dict = None):
        """
        Inicializa a classe de processamento de vídeo.

        :param url_video: URL do vídeo no YouTube
        :param query_user: Consulta fornecida pelo usuário para resumo
        :param model_class: Tipo de modelo para ser utilizado ("hf_hub", "openai", "ollama")
        :param model_params: Parâmetros adicionais para o modelo de linguagem
        """
        self.url_video = url_video
        self.query_user = query_user
        self.model_class = model_class
        self.model_params = model_params or {}
        logger.info(f"Inicializando YouTubeVideoSummarizer com URL: {url_video}, Modelo: {model_class}")

    def create_model(self, model_name: str, temperature: float = 0.1):
        logger.info(f"Criando modelo: {model_name} com temperatura: {temperature}")
        models = {
            "hf_hub": lambda: HuggingFaceHub(
                repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
                model_kwargs={
                    **{
                        "temperature": temperature,
                        "return_full_text": False,
                        "max_new_tokens": 1024,
                    },
                    **self.model_params
                }
            ),
            "openai": lambda: ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature),
            "ollama": lambda: self.create_ollama_model(temperature)
        }
        
        try:
            return models[model_name]()
        except KeyError:
            logger.error(f"Modelo inválido fornecido: {model_name}")
            raise ValueError(f"Invalid model_class: {model_name}")
    
    def create_ollama_model(self, temperature: float):
        from langchain_community.llms import ChatOllama
        return ChatOllama(model="phi3", temperature=temperature)

    def create_prompt_template(self) -> ChatPromptTemplate:
        logger.info("Criando template de prompt para o modelo.")
        system_prompt = "Você é um assistente virtual prestativo e deve responder a uma consulta com base na transcrição de um vídeo, que será fornecida abaixo."
        user_prompt = "Consulta: {consulta}\nTranscrição: {transcricao}"

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

    def get_cache_path(self) -> str:
        hash_url = hashlib.md5(self.url_video.encode()).hexdigest()
        cache_path = f"cache/{hash_url}.json"
        logger.info(f"Caminho do cache gerado: {cache_path}")
        return cache_path

    def get_video_info(self, language: list = ["pt", "pt-BR", "en"], translation: str = None):
        cache_path = self.get_cache_path()

        if os.path.exists(cache_path):
            logger.info(f"Cache encontrado para o vídeo: {cache_path}")
            with open(cache_path, "r") as cache_file:
                data = json.load(cache_file)
                return data["transcript"], data["metadata"]

        logger.info(f"Baixando transcrição do vídeo: {self.url_video}")
        video_loader = YoutubeLoader.from_youtube_url(
            self.url_video,
            add_video_info=True,
            language=language,
            translation=translation,
        )
        infos = video_loader.load()[0]

        logger.info("Transcrição obtida com sucesso, salvando em cache.")
        os.makedirs("cache", exist_ok=True)
        with open(cache_path, "w") as cache_file:
            json.dump({"transcript": infos.page_content, "metadata": infos.metadata}, cache_file)

        return infos.page_content, infos.metadata

    def interpret_video(self, language: list = ["pt"], translation: str = None):
        try:
            logger.info("Iniciando interpretação do vídeo.")
            start_time = time.time()
            transcript, metadata = self.get_video_info(language, translation)
            duration = time.time() - start_time
            logger.info(f"Transcrição concluída em {duration:.2f} segundos.")

            logger.info("Invocando o modelo para gerar o resumo.")
            chain = self.create_prompt_template() | self.create_model(self.model_class) | StrOutputParser()
            result = chain.invoke({"transcricao": transcript, "consulta": self.query_user})
            logger.info("Resumo gerado com sucesso.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao acessar o YouTube: {e}")
        except ValueError as e:
            logger.error(f"Erro no modelo ou parâmetros fornecidos: {e}")
        except Exception as e:
            logger.error(f"Erro ao processar o vídeo: {e}")
