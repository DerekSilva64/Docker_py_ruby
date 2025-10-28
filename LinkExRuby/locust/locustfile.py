from locust import HttpUser, task, between
from urllib.parse import quote

class LinkExtractorUser(HttpUser):
    
    def on_start(self):
        # Lista de 10 URLs diferentes para testar
        self.test_urls = [
            "https://www.wikipedia.org",
            "https://github.com",
            "https://www.python.org",
            "https://www.microsoft.com",
            "https://www.reddit.com",
            "https://www.coursera.org",
            "https://www.nodejs.org",
            "https://www.mozilla.org",
            "https://www.docker.com",
            "https://www.kubernetes.io"
        ]
        self.current_url_index = 0
    
    @task
    def test_link_extractor_sequence(self):
        # Pega a próxima URL da sequência
        url = self.test_urls[self.current_url_index]
        
        # Codifica a URL de forma segura usando urllib
        encoded_url = quote(url, safe='')
        
        # Faz a requisição e registra metadados extras para melhor análise
        with self.client.get(
            f"/?url={encoded_url}",
            name=f"Extract Links: {url}",  # Nome amigável no relatório
            catch_response=True
        ) as response:
            # Validação básica da resposta
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
        
        # Avança para a próxima URL, voltando ao início se necessário
        self.current_url_index = (self.current_url_index + 1) % len(self.test_urls)