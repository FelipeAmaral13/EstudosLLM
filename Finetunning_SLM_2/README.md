# 📚 Fine-Tuning de Modelos de Linguagem

Este repositório contém um notebook Jupyter para realizar **fine-tuning** de modelos de linguagem, incluindo todas as etapas necessárias para preparação dos dados, configuração do modelo, treinamento e avaliação.

---

## Funcionalidades
- **Pré-processamento de dados** para adequação ao formato de treinamento.
- **Configuração de parâmetros** de fine-tuning (taxa de aprendizado, batch size, épocas, etc.).
- **Treinamento supervisionado** utilizando modelos base.
- **Avaliação e métricas** de desempenho.
- **Exportação do modelo treinado** para uso posterior.

---

## Tecnologias Utilizadas
- [Python 3.x](https://www.python.org/)
- [Jupyter Notebook](https://jupyter.org/)
- [Transformers - Hugging Face](https://huggingface.co/transformers/)
- [Datasets - Hugging Face](https://huggingface.co/docs/datasets/)
- [PyTorch](https://pytorch.org/)
- [Pandas](https://pandas.pydata.org/)

---

## Estrutura do Projeto
```
.
├── fine_tunning.ipynb   # Notebook principal com todo o processo
└── README.md            # Documentação do projeto
```

---

## Instalação

Clone este repositório e instale as dependências:
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
pip install -r requirements.txt
```

---

## Como Executar

1. Abra o Jupyter Notebook:
```bash
jupyter notebook
```
2. Carregue o arquivo `fine_tunning.ipynb`.
3. Execute as células em ordem para realizar o treinamento.

---

## Exemplo de Uso
```python
from transformers import pipeline

modelo = pipeline("text-classification", model="caminho/do/modelo")
resultado = modelo("Este é um exemplo de frase.")
print(resultado)
```

---

## Resultados
Ao final do processo, o notebook gera:
- Métricas de desempenho (accuracy, f1-score, etc.)
- Modelo salvo para uso posterior
- Logs de treinamento

---

## Contribuindo
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Minha nova feature'`).
4. Faça um push (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
