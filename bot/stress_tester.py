"""
Motor de testes de stress
"""
import aiohttp
import asyncio
import time
from urllib.parse import urlparse
from typing import Tuple, Dict
import statistics

class StressTester:
    """Classe para executar testes de stress/carga"""
    
    def __init__(self, url: str, threads: int, rps: int, duracao: int):
        self.url = url
        self.threads = threads
        self.rps = rps
        self.duracao = duracao
        self.resultados = {
            'requisicoes_totais': 0,
            'requisicoes_sucesso': 0,
            'requisicoes_falha': 0,
            'status_codes': {},
            'tempos_resposta': [],
            'erros': []
        }
    
    def validar_url(self) -> Tuple[bool, str]:
        """Validar se a URL é válida"""
        try:
            resultado = urlparse(self.url)
            if not all([resultado.scheme, resultado.netloc]):
                return False, "URL inválida. Deve incluir http:// ou https://"
            if resultado.scheme not in ['http', 'https']:
                return False, "Apenas HTTP e HTTPS são suportados"
            return True, "URL válida"
        except Exception as e:
            return False, f"Erro ao validar URL: {str(e)}"
    
    async def executar_teste(self) -> Tuple[bool, str]:
        """Executar o teste de stress"""
        try:
            # Calcular intervalo entre requisições
            intervalo = 1.0 / self.rps if self.rps > 0 else 0
            tempo_inicio = time.time()
            
            # Criar tarefas assincronamente
            tarefas = []
            contador = 0
            
            async with aiohttp.ClientSession() as session:
                while time.time() - tempo_inicio < self.duracao:
                    # Criar requisições até atingir o RPS
                    for _ in range(self.threads):
                        if time.time() - tempo_inicio >= self.duracao:
                            break
                        
                        tarefa = self._fazer_requisicao(session, contador)
                        tarefas.append(tarefa)
                        contador += 1
                    
                    # Aguardar intervalo antes de próximo lote
                    await asyncio.sleep(intervalo)
                    
                    # Processar tarefas em lotes
                    if len(tarefas) >= 50:
                        await asyncio.gather(*tarefas, return_exceptions=True)
                        tarefas = []
                
                # Processar tarefas restantes
                if tarefas:
                    await asyncio.gather(*tarefas, return_exceptions=True)
            
            return True, "Teste concluído com sucesso"
        
        except Exception as e:
            return False, f"Erro ao executar teste: {str(e)}"
    
    async def _fazer_requisicao(self, session: aiohttp.ClientSession, index: int):
        """Fazer uma requisição HTTP"""
        try:
            inicio = time.time()
            
            async with session.get(self.url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                tempo_resposta = (time.time() - inicio) * 1000  # em millisegundos
                
                self.resultados['requisicoes_totais'] += 1
                
                # Registrar status code
                status = response.status
                self.resultados['status_codes'][status] = self.resultados['status_codes'].get(status, 0) + 1
                
                # Contar sucesso/falha
                if 200 <= status < 400:
                    self.resultados['requisicoes_sucesso'] += 1
                else:
                    self.resultados['requisicoes_falha'] += 1
                
                # Registrar tempo de resposta
                self.resultados['tempos_resposta'].append(tempo_resposta)
        
        except asyncio.TimeoutError:
            self.resultados['requisicoes_totais'] += 1
            self.resultados['requisicoes_falha'] += 1
            self.resultados['status_codes']['TIMEOUT'] = self.resultados['status_codes'].get('TIMEOUT', 0) + 1
            self.resultados['erros'].append('Timeout')
        
        except aiohttp.ClientConnectorError as e:
            self.resultados['requisicoes_totais'] += 1
            self.resultados['requisicoes_falha'] += 1
            self.resultados['status_codes']['CONN_ERROR'] = self.resultados['status_codes'].get('CONN_ERROR', 0) + 1
            self.resultados['erros'].append(f'Erro de conexão: {str(e)}')
        
        except Exception as e:
            self.resultados['requisicoes_totais'] += 1
            self.resultados['requisicoes_falha'] += 1
            self.resultados['status_codes']['ERROR'] = self.resultados['status_codes'].get('ERROR', 0) + 1
            self.resultados['erros'].append(f'Erro: {str(e)}')
    
    def obter_relatorio(self) -> Dict:
        """Obter relatório dos resultados"""
        total = self.resultados['requisicoes_totais']
        
        if total == 0:
            return {
                'requisicoes_totais': 0,
                'requisicoes_sucesso': 0,
                'requisicoes_falha': 0,
                'tempo_medio_ms': 0,
                'tempo_minimo_ms': 0,
                'tempo_maximo_ms': 0,
                'taxa_sucesso_percentual': 0,
                'taxa_erro_percentual': 0,
                'status_codes': {}
            }
        
        tempos = self.resultados['tempos_resposta']
        tempo_medio = statistics.mean(tempos) if tempos else 0
        tempo_minimo = min(tempos) if tempos else 0
        tempo_maximo = max(tempos) if tempos else 0
        
        taxa_sucesso = (self.resultados['requisicoes_sucesso'] / total) * 100
        taxa_erro = (self.resultados['requisicoes_falha'] / total) * 100
        
        return {
            'requisicoes_totais': total,
            'requisicoes_sucesso': self.resultados['requisicoes_sucesso'],
            'requisicoes_falha': self.resultados['requisicoes_falha'],
            'tempo_medio_ms': round(tempo_medio, 2),
            'tempo_minimo_ms': round(tempo_minimo, 2),
            'tempo_maximo_ms': round(tempo_maximo, 2),
            'taxa_sucesso_percentual': round(taxa_sucesso, 2),
            'taxa_erro_percentual': round(taxa_erro, 2),
            'status_codes': self.resultados['status_codes']
        }
