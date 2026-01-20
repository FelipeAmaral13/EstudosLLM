import re

class Guardrail:
    """
    Guardrail especializado em Cibersegurança:
    - Mascara Identificadores Pessoais (PII).
    - Detecta e mascara segredos técnicos (Tokens/Hashes).
    - Valida se a resposta final contém uma ação de mitigação clara.
    """

    def __init__(self):
        # Padrões para identificar dados sensíveis em logs e relatórios
        self.security_patterns = {
            "IP_INTERNO": re.compile(r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}"),
            "HASH_SHA256": re.compile(r"\b[A-Fa-f0-9]{64}\b"),
            "AUTH_TOKEN": re.compile(r"bearer\s[a-zA-Z0-9\-\._~\+/]+=*", re.IGNORECASE)
        }

    def validate_output(self, output: str, user_name: str) -> str:
        """
        Valida o relatório final do SOC antes de exibir ao analista humano.
        """
        
        # 1. Mascaramento de PII (Nome do Colaborador)
        if user_name and user_name.strip():
            name_pattern = re.compile(re.escape(user_name), re.IGNORECASE)
            output = name_pattern.sub("[USUARIO_CONFIDENCIAL]", output)

        # 2. Mascaramento de Infraestrutura e Segredos Técnicos
        # Protege IPs internos da rede contra exposição indevida
        output = self.security_patterns["IP_INTERNO"].sub("[IP_REDE_INTERNA]", output)
        
        # Remove hashes de arquivos ou tokens de autenticação que possam estar no log bruto
        output = self.security_patterns["HASH_SHA256"].sub("[FILE_HASH_REDACTED]", output)
        output = self.security_patterns["AUTH_TOKEN"].sub("[AUTH_TOKEN_REDACTED]", output)

        # 3. Guardrail de Conformidade: Verifica se há uma recomendação clara
        # No SOC, precisamos de ações diretas: BLOQUEAR, ISOLAR ou FALSO POSITIVO
        acoes_validas = ["BLOQUEAR ACESSO", "ISOLAR MAQUINA", "FALSO POSITIVO"]
        
        if not any(acao in output.upper() for acao in acoes_validas):
            output += (
                "\n\n⚠️ [GUARDRAIL ALERT]: O relatório não especificou uma ação de mitigação padrão "
                "(BLOQUEAR ACESSO, ISOLAR MAQUINA ou FALSO POSITIVO). "
                "Revisão urgente necessária pelo Nível 2."
            )
            
        return output