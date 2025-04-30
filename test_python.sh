#!/bin/bash

# Caminhos base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${BASE_DIR}/backend/src"
TEST_MODULE="tests"
GENERATE_SCRIPT="utils/generate_fake_data.py"
CLEANER_MODULE="tests.utils.cleaner"

# Nome do arquivo a ser testado (pode ser um regex)
# Exemplo: "test_001_users.py" ou "test_001*.py"
FILE_TO_TEST="test_004*.py"

# Outras configurações
FULL_TEST_PATH="${TEST_MODULE}/${FILE_TO_TEST}"
MESSAGE="Iniciando testes ${FILE_TO_TEST}"
LINE_WIDTH=120
BORDER_CHAR="="
SIDE_BORDER="###"

# Limpa a tela
clear

# Função para imprimir uma linha de borda
print_border() {
  printf "${SIDE_BORDER}"
  printf '%*s' "${LINE_WIDTH}" '' | tr ' ' "${BORDER_CHAR}"
  printf "${SIDE_BORDER}\n"
}

# Função para imprimir uma linha em branco com borda lateral
print_frame() {
  printf "${SIDE_BORDER}"
  printf '%*s' "${LINE_WIDTH}" ''
  printf "${SIDE_BORDER}\n"
}

# Função para imprimir a mensagem centralizada
print_centered_message() {
  local msg_len=${#MESSAGE}
  local pad=$(((LINE_WIDTH - msg_len) / 2))
  local extra=$((LINE_WIDTH - msg_len - pad))
  printf "${SIDE_BORDER}"
  printf '%*s%s%*s' "$pad" '' "$MESSAGE" "$extra" ''
  printf "${SIDE_BORDER}\n"
}

# Cabeçalho formatado
echo ""
print_border
print_frame
print_centered_message
print_frame
print_border
echo ""

# Executa os testes
pushd "${SRC_DIR}" > /dev/null

echo "🔧 Gerando dados fake..."
python "${TEST_MODULE}/${GENERATE_SCRIPT}"

echo "🧪 Executando testes..."
pytest -vvvs --disable-warnings -p no:warnings --durations=0 ${FULL_TEST_PATH}

echo "🧹 Limpando dados..."
python -m "${CLEANER_MODULE}" > /dev/null

popd > /dev/null

echo -e "\n✅ Finalizado!"
