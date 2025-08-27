# 🚀 Servidor MCP Python

Um servidor **Model Context Protocol (MCP)** Python que fornece ferramentas para busca de documentação e pesquisa web.

## ✨ Funcionalidades

- 🔍 **Busca de Documentação**: Suporte para LangChain, OpenAI e LlamaIndex
- 🌐 **Pesquisa Web**: Integração com API Serper para busca na web
- 📄 **Extração de Conteúdo**: Extrai texto de URLs usando BeautifulSoup
- 🖥️ **Múltiplos Transportes**: Suporte para HTTP (localhost) e STDIO
- 🐳 **Containerização**: Docker e Docker Compose configurados
- 📝 **Sistema de Logs**: Logging configurável com rotação de arquivos

## 🛠️ Ferramentas Disponíveis

### `get_docs`
Busca documentação específica de bibliotecas suportadas.

**Parâmetros:**
- `query`: Consulta a ser pesquisada (ex: "Chroma DB")
- `library`: Biblioteca para pesquisa (ex: "langchain", "openai", "llama-index")

**Bibliotecas Suportadas:**
- `langchain`: python.langchain.com/docs
- `llama-index`: docs.llamaindex.ai/en/stable
- `openai`: platform.openai.com/docs

**Exemplo de uso:**
```python
# Buscar documentação sobre Chroma DB no LangChain
result = await get_docs("Chroma DB", "langchain")
```

## 🚀 Início Rápido

### 1. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 2. Configuração
1. Crie um arquivo `.env` na raiz do projeto:
   ```bash
   # Configurações do Servidor MCP
   MCP_SERVER_NAME=mcp-python-server
   MCP_SERVER_VERSION=1.0.0
   MCP_HOST=localhost
   MCP_PORT=8000
   
   # API Serper para busca web
   SERPER_API_KEY=sua_api_key_aqui
   SERPER_URL=https://google.serper.dev/search
   
   # Configurações de Log
   MCP_LOG_LEVEL=INFO
   MCP_LOG_FILE=logs/logs_{datetime.now().strftime('%Y-%m-%d')}.log
   
   # Configurações de Segurança
   MCP_MAX_TOOL_EXECUTION_TIME=30
   MCP_ENABLE_INPUT_VALIDATION=true
   MCP_MAX_INPUT_LENGTH=10000
   ```

### 3. Execução

#### Opção A: Comando Direto
```bash
# Servidor HTTP (localhost:8000)
python main.py --http

# Servidor STDIO (para agentes)
python main.py
```

#### Opção B: Docker
```bash
# Servidor HTTP
docker-compose up mcp-http-server

# Servidor STDIO
docker-compose up mcp-stdio-server

# Ambos os serviços
docker-compose up --build
```

## 🌐 Uso como Servidor HTTP

### Iniciar Servidor
```bash
python main.py --http
```

O servidor estará disponível em `http://localhost:8000`

### Testar Ferramentas
```bash
# Testar busca de documentação
curl -X POST "http://localhost:8000/tools/get_docs" \
  -H "Content-Type: application/json" \
  -d '{"query": "Chroma DB", "library": "langchain"}'
```

## 🔌 Uso com Agentes MCP

### Configuração do Cliente
```python
from mcp.client.stdio import stdio_client

async with stdio_client(["python", "main.py"]) as client:
    # Listar ferramentas disponíveis
    tools = await client.list_tools()
    
    # Executar ferramenta
    result = await client.call_tool("get_docs", {
        "query": "Chroma DB",
        "library": "langchain"
    })
```

### Configuração em Agentes
```yaml
# Exemplo para Claude Desktop
mcpServers:
  python-docs:
    command: python
    args: ["main.py"]
    env:
      SERPER_API_KEY: "sua_api_key"
```

## ⚙️ Configurações

### Variáveis de Ambiente
| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `MCP_SERVER_NAME` | Nome do servidor | `mcp-python-server` |
| `MCP_SERVER_VERSION` | Versão do servidor | `1.0.0` |
| `MCP_HOST` | Host para servidor HTTP | `localhost` |
| `MCP_PORT` | Porta para servidor HTTP | `8000` |
| `SERPER_API_KEY` | API Key do Serper | - |
| `SERPER_URL` | URL da API Serper | `https://google.serper.dev/search` |
| `MCP_LOG_LEVEL` | Nível de log | `INFO` |
| `MCP_LOG_FILE` | Arquivo de log | `logs/logs_{date}.log` |
| `MCP_MAX_TOOL_EXECUTION_TIME` | Tempo máximo de execução (s) | `30` |
| `MCP_ENABLE_INPUT_VALIDATION` | Validação de entrada | `true` |
| `MCP_MAX_INPUT_LENGTH` | Tamanho máximo de entrada | `10000` |

### Configurações de Ferramentas
- **Tempo máximo de execução**: 30 segundos
- **Validação de entrada**: Habilitada
- **Tamanho máximo de entrada**: 10.000 caracteres
- **Cache de recursos**: Habilitado
- **Tamanho máximo de recursos**: 1MB

## 🐳 Docker

### Construir Imagem
```bash
docker build -t mcp-python-server .
```

### Executar Container
```bash
# Servidor HTTP
docker run -p 8000:8000 --env-file .env mcp-python-server

# Servidor STDIO
docker run --env-file .env mcp-python-server python main.py
```

### Docker Compose
```bash
# Servidor HTTP na porta 8000
docker-compose up mcp-http-server

# Servidor STDIO
docker-compose up mcp-stdio-server

# Ambos os serviços
docker-compose up --build
```

## 📁 Estrutura do Projeto

```
mcp-python/
├── app/
│   ├── logging.py          # Sistema de logs configurável
│   ├── settings.py         # Configurações e variáveis de ambiente
│   ├── tools/              # Ferramentas MCP
│   │   └── get_docs.py     # Ferramenta de busca de documentação
│   └── services/           # Serviços de negócio
│       ├── search_web.py   # Busca web via API Serper
│       └── fetch_url.py    # Extração de conteúdo HTML
├── data/                   # Dados e recursos
│   └── docs/              # Documentação local
├── logs/                   # Arquivos de log
├── main.py                 # Ponto de entrada principal
├── requirements.txt        # Dependências Python
├── Dockerfile             # Imagem Docker
└── docker-compose.yml     # Orquestração Docker
```

## 🔧 Desenvolvimento

### Instalar Dependências de Desenvolvimento
```bash
pip install -r requirements.txt
```

### Dependências Principais
- `mcp[cli]`: Framework MCP para Python
- `python-dotenv`: Gerenciamento de variáveis de ambiente
- `httpx`: Cliente HTTP assíncrono
- `beautifulsoup4`: Parser HTML para extração de conteúdo

### Executar Testes
```bash
# TODO: Adicionar testes
python -m pytest
```

### Formatação de Código
```bash
# TODO: Adicionar black, isort
black .
isort .
```

## 🚨 Solução de Problemas

### Erro: "Dependência não encontrada"
```bash
pip install -r requirements.txt
```

### Erro: "API Key do Serper não configurada"
Configure `SERPER_API_KEY` no arquivo `.env`

### Erro: "Porta já em uso"
Altere `MCP_PORT` no arquivo `.env` ou pare outros serviços na porta 8000

### Erro: "Permissão negada" (Docker)
```bash
sudo docker-compose up --build
```

### Erro: "Timeout na busca web"
- Verifique sua conexão com a internet
- Confirme se a API key do Serper está válida
- Aumente `MCP_MAX_TOOL_EXECUTION_TIME` se necessário

## 📚 Recursos Adicionais

- [Documentação MCP](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [API Serper](https://serper.dev/)
- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/)
- [httpx](https://www.python-httpx.org/)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique as [Issues](https://github.com/seu-usuario/mcp-python/issues)
2. Crie uma nova issue com detalhes do problema
3. Inclua logs e informações do ambiente

---

**Desenvolvido com ❤️ usando Python e MCP**
