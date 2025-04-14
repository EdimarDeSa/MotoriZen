from enum import StrEnum


class ModelsDescriptionTexts(StrEnum):
    # Timestamps
    CREATED_AT = "Data de criação do registro."
    UPDATED_AT = "Data da última atualização do registro."
    DELETED_AT = "Data de desativação/remoção do registro (soft delete)."

    # Paginação/Filtros
    PAGE = "Número da página solicitada (começando em 1)."
    PER_PAGE = "Número de registros por página."
    SORT_BY = "Campo para ordenação dos resultados."
    SORT_ORDER = "Direção da ordenação (asc/desc)."
    TIME_FRAME = "Período de tempo para filtro (formato: YYYY-MM-DD/YYYY-MM-DD)."
    QUERY_FILTERS = "Filtros aplicados na consulta."
    QUERY_OPTIONS = "Opções adicionais de consulta disponíveis."
    TOTAL_RESULTS = "Total number of results in this dataset."
    TOTAL_PAGES = "Total pages existing in the server."
    RANGE_START = "Start point for results in this field."
    RANGE_END = "End point for results in this field."
    FIRST_INDEX = "First index in this page."
    LAST_INDEX = "Last index in this page."
    METADATA = "Metadata for this page and query."
    RESULTS = "Results contained in this dataset."

    # Autenticação
    ACCESS_TOKEN = "Token de acesso para autenticação."
    REFRESH_TOKEN = "Token para renovação do acesso."
    TOKEN_TYPE = "Tipo do token (ex: Bearer)."
    EXPIRES_IN = "Tempo em segundos até a expiração do token de acesso."
    REFRESH_EXPIRES_IN = "Tempo em segundos até a expiração do refresh token."
    SESSION_STATE = "Estado atual da sessão."
    NOT_BEFORE_POLICY = "Tempo em segundos até que o token se torne válido."
    SCOPE = "Escopos de permissão concedidos."

    # Veículos
    VEHICLE_ID = "ID único do veículo."
    VEHICLE_IDS = "Vehicle ids to be returned. If not provided, all vehicles will be returned."
    VEHICLE_CD = "Código de identificação do veículo."
    VEHICLE_MODEL = "Modelo do veículo."
    VEHICLE_YEAR = "Ano de fabricação do veículo."
    VEHICLE_COLOR = "Cor do veículo."
    LICENSE_PLATE = "Placa do veículo (formato: ABC-1234)."
    RENAVAM = "Número do RENAVAM do veículo."
    ODOMETER = "Quilometragem atual do veículo (em km)."
    IS_ACTIVE = "Indica se o veículo está ativo (true/false)."
    VEHICLE_DATA = "New vehicle data after update."
    TOTAL_VEHICLES = "Total number OF vehicle selected for this query."

    # Marcas
    ID_BRAND = "ID único da marca."
    CD_BRAND = "Código de identificação da marca."
    BRAND_NAME = "Nome da marca do veículo."

    # Combustível
    ID_FUEL_TYPE = "ID único do tipo de combustível."
    CD_FUEL_TYPE = "Código do tipo de combustível."
    FUEL_TYPE_NAME = "Nome do tipo de combustível (ex: Gasolina, Etanol)."
    FUEL_CAPACITY = "Capacidade do tanque de combustível (em litros)."
    MEAN_CONSUMPTION = "Consumo médio de combustível (km/l)."

    # Registros
    REGISTER_ID = "ID único do registro."
    REGISTER_DATE = "Data do registro (formato: YYYY-MM-DD)."
    DISTANCE = "Distância percorrida (em km)."
    WORKING_TIME = "Tempo de trabalho/operação (formato: HH:MM:SS)."
    NUMBER_OF_TRIPS = "Número de viagens realizadas."
    TOTAL_VALUE = "Valor total associado ao registro."

    # Relatórios
    REPORTS = "Tipos de relatórios solicitados (separados por vírgula)."
    AGGREGATION_INTERVAL = "Intervalo de agregação para relatórios (diário/semanal/mensal)."

    # Usuários
    USER_CD = "Código de identificação do usuário."
    FIRST_NAME = "Primeiro nome do usuário."
    LAST_NAME = "Sobrenome do usuário."
    EMAIL = "E-mail do usuário."
    PASSWORD = "Senha do usuário (hash)."
    BIRTHDATE = "Data de nascimento do usuário (formato: YYYY-MM-DD)."
    AUTH_CD = "Código de autenticação externa."

    # Respostas/Erros
    RESPONSE_CODE = "Código de resposta da operação."
    BASE_DATA = "Dados principais retornados pela API."
    EXCEPTIONS_DATA = "Detalhes dos erros ocorridos."
    EXCEPTIONS_RC = "Código de erro mapeado."
    INVALID_UPDATES_DATA = "Dados de atualização inválidos - forneça pelo menos um campo válido."
    INVALID_REGISTER_DATA = "Dados de registro inválidos - forneça distância e/ou odômetro."
    TOTAL_BYTES = "Total de bytes recebidos na resposta."
    NEW_REGISTRY = "Indica se é um novo registro (true/false)."
    UPDATES = "Lista de atualizações aplicadas."

    # Outros
    UNKNOWN_ERROR = "Erro desconhecido."
    NO_DATA = "Nenhum dado encontrado."
