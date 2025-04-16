# 🚗 MotoriZen – Controle de Ganhos, KM e Consumo para Motoristas
MotoriZen é uma solução completa para motoristas de aplicativos como Uber e 99, facilitando o acompanhamento de ganhos, despesas, quilômetros rodados, consumo de combustível e muito mais. Com uma interface intuitiva e funcionalidades úteis, o app ajuda você a maximizar seus lucros e controlar seu desempenho diário.

## ⚙️ Funcionalidades Principais
- Acompanhamento de Ganhos: Registre corridas e monitoramento de ganhos por dia, semana ou mês.
- Controle de KM Rodados: Mantenha o controle da quilometragem para otimizar seus trajetos e planejar manutenções.
- Gestão de Combustível: Registre abastecimentos e acompanhe o consumo médio para economizar combustível.
- Relatórios Detalhados: Visualize gráficos e relatórios com resumo de ganhos, custos e eficiência.
- Alertas e Lembretes: Notificações personalizáveis para troca de óleo, revisão ou controle de despesas.

## 🛠️ Tecnologias Utilizadas
<!-- - Frontend: [HTML, CSS, JS, JQuery] -->
- Backend: [Python, FastAPI, SqlAlchemy, Keycloak]
- Banco de Dados: [PostgreSQL, Redis]

## 🚀 Como Executar o Projeto
Clone o repositório:
``` bash
# Clonar repositório
git clone https://github.com/EdimarDeSa/MotoriZen.git
cd MotoriZen
```

Instale as dependências:
``` bash
# Poetry
poetry shell
poetry install
```

``` bash
# Pip
pip install -r requeriments.txt
```

``` bash
# Docker
docker-compose up
```

Criando arquivo .env e definindo configurações:
``` bash
touch .env
cat <<EOF > .env
DB_DIALECT="postgresql"
DB_USER="postgres"
DB_PASSWORD="P455W0rD!#"
DB_IP="localhost"
DB_PORT="5432"
DB_NAME="postgres"

DEBUG_MODE=1
EOF
```

Inicie o projeto:
```bash
# Poetry
poetry run fastapi dev
📱 Screenshots (Em breve)
Acompanhe as primeiras telas e exemplos visuais de uso em nossa próxima atualização.
```

### 📋 Roadmap
- Implementação de calculo para ganho/KM
- Implementação de calculo para consumo de combustível / R$ ganho
- Implementação de cálculo de lucro líquido
- Exportação de relatórios em PDF/Excel
- Modo offline para registrar dados sem internet
- Integração com Google Maps para rotas e trajetos

### 🎯 Contribuições
Sinta-se à vontade para abrir issues e enviar pull requests. Toda ajuda é bem-vinda!