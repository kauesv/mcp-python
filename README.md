# 🚀 Servidor MCP Python

Um servidor **Model Context Protocol (MCP)** Python que fornece ferramentas para busca de documentação e pesquisa web.

## ✨ Funcionalidades

- 🔍 **Busca de Documentação**: Suporte para LangChain, OpenAI e LlamaIndex
- 🌐 **Pesquisa Web**: Integração com API Serper para busca na web
- 📄 **Extração de Conteúdo**: Extrai texto de URLs
- 🖥️ **Múltiplos Transportes**: Suporte para HTTP (localhost) e STDIO
- 🐳 **Containerização**: Docker e Docker Compose configurados

## 🛠️ Ferramentas Disponíveis

### `get_docs`
Busca documentação específica de bibliotecas suportadas.

**Parâmetros:**
- `query`: Consulta a ser pesquisada (ex: "Chroma DB")
- `library`: Biblioteca para pesquisa (ex: "langchain", "openai", "llama-index")

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
1. Copie o arquivo de exemplo:
   ```bash
   cp config.env.example .env
   ```
2. Configure sua API key do Serper no arquivo `.env`:
   ```bash
   SERPER_API_KEY=sua_api_key_aqui
   ```

### 3. Execução

#### Opção A: Script Interativo (Recomendado)
```bash
python start_server.py
```

#### Opção B: Comando Direto
```bash
# Servidor HTTP (localhost:8000)
python main.py --http

# Servidor STDIO (para agentes)
python main.py
```

#### Opção C: Docker
```bash
docker-compose up --build
```

## 🌐 Uso como Servidor HTTP

### Iniciar Servidor
```bash
python main.py --http
```

### Acessar API
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **OpenAPI Schema**: http://localhost:8000/openapi.json

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
| `MCP_HOST` | Host para servidor HTTP | `localhost` |
| `MCP_PORT` | Porta para servidor HTTP | `8000` |
| `SERPER_API_KEY` | API Key do Serper | - |
| `MCP_LOG_LEVEL` | Nível de log | `INFO` |

### Configurações de Ferramentas
- **Tempo máximo de execução**: 30 segundos
- **Validação de entrada**: Habilitada
- **Tamanho máximo de entrada**: 10.000 caracteres
- **Cache de recursos**: Habilitado

## 🐳 Docker

### Construir Imagem
```bash
docker build -t mcp-python-server .
```

### Executar Container
```bash
docker run -p 8000:8000 --env-file config.env mcp-python-server
```

### Docker Compose
```bash
docker-compose up --build
```

## 📁 Estrutura do Projeto

```
mcp-python/
├── app/
│   ├── logging.py          # Sistema de logs
│   ├── settings.py         # Configurações
│   ├── tools/              # Ferramentas MCP
│   │   └── get_docs.py     # Ferramenta de busca de docs
│   └── services/           # Serviços de negócio
│       ├── search_web.py   # Busca web
│       └── fetch_url.py    # Extração de conteúdo
├── main.py                 # Ponto de entrada
├── start_server.py         # Script de inicialização
├── config.env              # Configurações de ambiente
├── requirements.txt        # Dependências Python
├── Dockerfile             # Imagem Docker
└── docker-compose.yml     # Orquestração Docker
```

## 🔧 Desenvolvimento

### Instalar Dependências de Desenvolvimento
```bash
pip install -r requirements.txt
```

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
Configure `SERPER_API_KEY` no arquivo `config.env`

### Erro: "Porta já em uso"
Altere `MCP_PORT` no arquivo `config.env` ou pare outros serviços na porta 8000

### Erro: "Permissão negada" (Docker)
```bash
sudo docker-compose up --build
```

## 📚 Recursos Adicionais

- [Documentação MCP](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [API Serper](https://serper.dev/)

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
