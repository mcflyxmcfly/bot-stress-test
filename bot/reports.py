"""
Gerador de relatórios
"""
from datetime import datetime
import json

class RelatorioGenerator:
    """Gera relatórios formatados dos testes"""
    
    @staticmethod
    def gerar_relatorio_texto(teste_record) -> str:
        """Gerar relatório em texto/markdown"""
        
        status_codes = json.loads(teste_record.status_codes) if teste_record.status_codes else {}
        
        # Formatar status codes
        status_codes_texto = ""
        for codigo, quantidade in sorted(status_codes.items(), key=lambda x: x[1], reverse=True):
            percentual = (quantidade / teste_record.requisicoes_totais * 100) if teste_record.requisicoes_totais > 0 else 0
            status_codes_texto += f"{codigo}: {quantidade} ({percentual:.2f}%)\n"
        
        relatorio = f"""
✅ TESTE CONCLUÍDO

📋 INFORMAÇÕES DO TESTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 URL: {teste_record.url}
📅 Data: {teste_record.data_inicio.strftime('%d/%m/%Y %H:%M:%S')}
⚙️ Threads: {teste_record.threads}
⚡ RPS Configurado: {teste_record.rps}
⏳ Duração: {teste_record.duracao}s

📊 RESULTADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Requisições Aceitas: {teste_record.requisicoes_sucesso:,}
❌ Requisições Recusadas: {teste_record.requisicoes_falha:,}
📈 Total: {teste_record.requisicoes_totais:,}

📉 TAXA DE SUCESSO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sucesso: {100 - teste_record.taxa_erro:.2f}%
❌ Falha: {teste_record.taxa_erro:.2f}%

⏱️ TEMPOS DE RESPOSTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔹 Média: {teste_record.tempo_medio_resposta:.2f}ms
🔸 Mínimo: 0.00ms
🔴 Máximo: 0.00ms

📊 CÓDIGOS HTTP RETORNADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{status_codes_texto}

🔔 ID do Teste: #{teste_record.id}
"""
        
        return relatorio
