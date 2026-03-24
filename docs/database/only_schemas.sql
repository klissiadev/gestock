SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA app_ai;
CREATE SCHEMA app_core;
CREATE SCHEMA app_logs;

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA app_ai;
CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA app_core;
CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA app_logs;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA app_ai;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA app_core;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA app_logs;

ALTER DATABASE gestock SET search_path TO app_ai;

CREATE FUNCTION app_core.refresh_stock_view() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY app_core.vw_product;
    REFRESH MATERIALIZED VIEW CONCURRENTLY app_core.mv_movimentacao;
    REFRESH MATERIALIZED VIEW CONCURRENTLY app_core.mv_imports;
    RETURN NULL;
END;
$$;


SET default_table_access_method = heap;

CREATE TABLE app_ai.checkpoint_blobs (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    channel text NOT NULL,
    version text NOT NULL,
    type text NOT NULL,
    blob bytea
);

CREATE TABLE app_ai.checkpoint_migrations (
    v integer NOT NULL
);

CREATE TABLE app_ai.checkpoint_writes (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    task_id text NOT NULL,
    idx integer NOT NULL,
    channel text NOT NULL,
    type text,
    blob bytea NOT NULL,
    task_path text DEFAULT ''::text NOT NULL
);

CREATE TABLE app_ai.checkpoints (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    parent_checkpoint_id text,
    type text,
    checkpoint jsonb NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL
);

CREATE TABLE app_ai.conversation_logs (
    id bigint NOT NULL,
    session_id uuid NOT NULL,
    user_message text NOT NULL,
    bot_response text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);

CREATE SEQUENCE app_ai.conversation_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE app_ai.conversation_logs_id_seq OWNED BY app_ai.conversation_logs.id;

CREATE TABLE app_ai.conversation_sessions (
    session_id uuid NOT NULL,
    title text,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    id_usuario uuid
);

CREATE TABLE app_core.ficha_tecnica (
    produto_final_id integer NOT NULL,
    materia_prima_id integer NOT NULL,
    quantidade_necessaria numeric(10,2) NOT NULL
);

CREATE TABLE app_core.itens_requisicoes (
    id bigint NOT NULL,
    quantidade integer NOT NULL,
    produto_id bigint NOT NULL,
    requisicao_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    prioridade boolean DEFAULT false,
    CONSTRAINT itens_requisicoes_quantidade_check CHECK ((quantidade > 0))
);

ALTER TABLE app_core.itens_requisicoes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_core.itens_requisicoes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE app_core.movimentacoes_entrada (
    id bigint NOT NULL,
    produto_id bigint NOT NULL,
    quantidade integer NOT NULL,
    data_de_compra date NOT NULL,
    preco_de_compra numeric(10,2) NOT NULL,
    fornecedor character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT movimentacoes_entrada_quantidade_check CHECK ((quantidade > 0))
);

ALTER TABLE app_core.movimentacoes_entrada ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_core.movimentacoes_entrada_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE app_core.movimentacoes_internas (
    id integer NOT NULL,
    produto_id integer NOT NULL,
    ordem_de_producao character varying(50),
    tipo character varying(20),
    quantidade numeric(12,2) NOT NULL,
    origem character varying(50),
    destino character varying(50),
    data timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE SEQUENCE app_core.movimentacoes_internas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE app_core.movimentacoes_internas_id_seq OWNED BY app_core.movimentacoes_internas.id;

CREATE TABLE app_core.movimentacoes_saida (
    id bigint NOT NULL,
    produto_id bigint NOT NULL,
    quantidade integer NOT NULL,
    data_de_venda date NOT NULL,
    preco_de_venda numeric(10,2) NOT NULL,
    cliente character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT movimentacoes_saida_quantidade_check CHECK ((quantidade > 0))
);

ALTER TABLE app_core.movimentacoes_saida ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_core.movimentacoes_saida_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE app_core.produtos (
    id bigint NOT NULL,
    nome character varying(255) NOT NULL,
    descricao text,
    estoque_minimo integer NOT NULL,
    data_validade date,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    ativo boolean DEFAULT true NOT NULL,
    tipo character varying(20) DEFAULT 'INVALIDO'::character varying NOT NULL,
    CONSTRAINT produtos_status_check CHECK (((tipo)::text = ANY ((ARRAY['MP'::character varying, 'SA'::character varying, 'PA'::character varying, 'INVALIDO'::character varying])::text[])))
);



CREATE MATERIALIZED VIEW app_core.mv_movimentacao AS
 SELECT t.unique_id,
    p.nome AS produto_nome,
    t.quantidade,
    t.data_evento,
    t.valor_unitario,
    t.parceiro_origem,
    t.local_destino,
    t.tipo_movimento,
    t.created_at
   FROM (( SELECT (movimentacoes_entrada.id || '-ENT'::text) AS unique_id,
            movimentacoes_entrada.produto_id,
            movimentacoes_entrada.quantidade,
            movimentacoes_entrada.data_de_compra AS data_evento,
            movimentacoes_entrada.preco_de_compra AS valor_unitario,
            movimentacoes_entrada.fornecedor AS parceiro_origem,
            'ESTOQUE'::character varying AS local_destino,
            'ENTRADA'::text AS tipo_movimento,
            movimentacoes_entrada.created_at
           FROM app_core.movimentacoes_entrada
        UNION ALL
         SELECT (movimentacoes_saida.id || '-SAI'::text),
            movimentacoes_saida.produto_id,
            movimentacoes_saida.quantidade,
            movimentacoes_saida.data_de_venda,
            movimentacoes_saida.preco_de_venda,
            'ESTOQUE'::character varying,
            movimentacoes_saida.cliente,
            'SAIDA'::text,
            movimentacoes_saida.created_at
           FROM app_core.movimentacoes_saida
        UNION ALL
         SELECT (movimentacoes_internas.id || '-INT'::text),
            movimentacoes_internas.produto_id,
            movimentacoes_internas.quantidade,
            movimentacoes_internas.data,
            NULL::numeric,
            movimentacoes_internas.origem,
            movimentacoes_internas.destino,
            'INTERNA'::text,
            movimentacoes_internas.data
           FROM app_core.movimentacoes_internas) t
     JOIN app_core.produtos p ON ((p.id = t.produto_id)))
  WITH NO DATA;



CREATE TABLE app_core.notificacoes (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    severity character varying(30) NOT NULL,
    title character varying(255) NOT NULL,
    message text NOT NULL,
    reference jsonb NOT NULL,
    event_id integer NOT NULL,
    read boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT now(),
    user_id uuid NOT NULL
);


CREATE TABLE app_core.notificacoes_eventos (
    id integer NOT NULL,
    type text NOT NULL,
    context jsonb NOT NULL,
    reference jsonb NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    user_id uuid
);


ALTER TABLE app_core.notificacoes_eventos ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_core.notificacoes_eventos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE SEQUENCE app_core.notificacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE app_core.notificacoes_id_seq OWNED BY app_core.notificacoes.id;

ALTER TABLE app_core.produtos ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_core.produtos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE app_core.requisicoes (
    id bigint NOT NULL,
    titulo character varying(255) NOT NULL,
    observacao text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    user_id uuid NOT NULL
);

ALTER TABLE app_core.requisicoes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_core.requisicoes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE app_core.usuarios (
    nome character varying(255) NOT NULL,
    papel character varying(50) NOT NULL,
    senha_hash bytea NOT NULL,
    email character varying(255) NOT NULL,
    ativo boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    primeiro_acesso boolean DEFAULT true NOT NULL
);

CREATE VIEW app_core.v_movimentacao AS
 SELECT p.nome AS nome_produto,
    me.quantidade,
    me.data_de_compra AS data_movimentacao,
    me.fornecedor AS entidade,
    'entrada'::text AS tipo_movimentacao,
    me.created_at AS adicionado_em
   FROM (app_core.movimentacoes_entrada me
     JOIN app_core.produtos p ON ((me.produto_id = p.id)))
UNION ALL
 SELECT p.nome AS nome_produto,
    ms.quantidade,
    ms.data_de_venda AS data_movimentacao,
    ms.cliente AS entidade,
    'saida'::text AS tipo_movimentacao,
    ms.created_at AS adicionado_em
   FROM (app_core.movimentacoes_saida ms
     JOIN app_core.produtos p ON ((ms.produto_id = p.id)));

CREATE VIEW app_core.v_giro_estoque AS
 SELECT nome_produto,
    sum(
        CASE
            WHEN (tipo_movimentacao = 'entrada'::text) THEN quantidade
            ELSE 0
        END) AS total_entrada,
    sum(
        CASE
            WHEN (tipo_movimentacao = 'saida'::text) THEN quantidade
            ELSE 0
        END) AS total_saida,
    count(*) AS total_movimentacoes
   FROM app_core.v_movimentacao
  GROUP BY nome_produto;

CREATE VIEW app_core.v_produtos AS
 SELECT p.nome AS nome_produto,
    p.descricao,
    p.data_validade,
    p.ativo,
    (((((
        CASE
            WHEN ((p.tipo)::text = 'MP'::text) THEN COALESCE(sum(me.quantidade), (0)::bigint)
            ELSE (0)::bigint
        END)::numeric +
        CASE
            WHEN ((p.tipo)::text = ANY ((ARRAY['SA'::character varying, 'PA'::character varying])::text[])) THEN COALESCE(sum(
            CASE
                WHEN ((mi.tipo)::text = 'PRODUCAO'::text) THEN mi.quantidade
                ELSE NULL::numeric
            END), ((0)::bigint)::numeric)
            ELSE ((0)::bigint)::numeric
        END) -
        CASE
            WHEN ((p.tipo)::text = ANY ((ARRAY['MP'::character varying, 'SA'::character varying])::text[])) THEN COALESCE(sum(
            CASE
                WHEN ((mi.tipo)::text = 'CONSUMO'::text) THEN mi.quantidade
                ELSE NULL::numeric
            END), ((0)::bigint)::numeric)
            ELSE ((0)::bigint)::numeric
        END) - (
        CASE
            WHEN ((p.tipo)::text = 'PA'::text) THEN COALESCE(sum(ms.quantidade), (0)::bigint)
            ELSE (0)::bigint
        END)::numeric))::bigint AS estoque_atual,
    p.estoque_minimo,
    p.id,
    p.tipo,
    (((((
        CASE
            WHEN ((p.tipo)::text = 'MP'::text) THEN COALESCE(sum(me.quantidade), (0)::bigint)
            ELSE (0)::bigint
        END)::numeric +
        CASE
            WHEN ((p.tipo)::text = ANY ((ARRAY['SA'::character varying, 'PA'::character varying])::text[])) THEN COALESCE(sum(
            CASE
                WHEN ((mi.tipo)::text = 'PRODUCAO'::text) THEN mi.quantidade
                ELSE NULL::numeric
            END), ((0)::bigint)::numeric)
            ELSE ((0)::bigint)::numeric
        END) -
        CASE
            WHEN ((p.tipo)::text = ANY ((ARRAY['MP'::character varying, 'SA'::character varying])::text[])) THEN COALESCE(sum(
            CASE
                WHEN ((mi.tipo)::text = 'CONSUMO'::text) THEN mi.quantidade
                ELSE NULL::numeric
            END), ((0)::bigint)::numeric)
            ELSE ((0)::bigint)::numeric
        END) - (
        CASE
            WHEN ((p.tipo)::text = 'PA'::text) THEN COALESCE(sum(ms.quantidade), (0)::bigint)
            ELSE (0)::bigint
        END)::numeric) < (p.estoque_minimo)::numeric) AS baixo_estoque,
    (p.data_validade < CURRENT_DATE) AS vencido
   FROM (((app_core.produtos p
     LEFT JOIN app_core.movimentacoes_entrada me ON ((me.produto_id = p.id)))
     LEFT JOIN app_core.movimentacoes_internas mi ON ((mi.produto_id = p.id)))
     LEFT JOIN app_core.movimentacoes_saida ms ON ((ms.produto_id = p.id)))
  GROUP BY p.id, p.tipo, p.nome, p.descricao, p.data_validade, p.ativo, p.estoque_minimo;

CREATE VIEW app_core.v_produtos_custo AS
 WITH entradas AS (
         SELECT movimentacoes_entrada.produto_id,
            sum(movimentacoes_entrada.quantidade) AS total_entrada,
            sum(((movimentacoes_entrada.quantidade)::numeric * movimentacoes_entrada.preco_de_compra)) AS valor_total_entrada
           FROM app_core.movimentacoes_entrada
          GROUP BY movimentacoes_entrada.produto_id
        ), saidas AS (
         SELECT movimentacoes_saida.produto_id,
            sum(movimentacoes_saida.quantidade) AS total_saida
           FROM app_core.movimentacoes_saida
          GROUP BY movimentacoes_saida.produto_id
        )
 SELECT p.id AS produto_id,
    p.nome AS nome_produto,
    (COALESCE(e.total_entrada, (0)::bigint) - COALESCE(s.total_saida, (0)::bigint)) AS estoque_atual,
        CASE
            WHEN ((COALESCE(e.total_entrada, (0)::bigint) - COALESCE(s.total_saida, (0)::bigint)) <= 0) THEN (0)::numeric
            ELSE round((COALESCE(e.valor_total_entrada, (0)::numeric) / (NULLIF(e.total_entrada, 0))::numeric), 2)
        END AS custo_medio,
        CASE
            WHEN ((COALESCE(e.total_entrada, (0)::bigint) - COALESCE(s.total_saida, (0)::bigint)) <= 0) THEN (0)::numeric
            ELSE round((((COALESCE(e.total_entrada, (0)::bigint) - COALESCE(s.total_saida, (0)::bigint)))::numeric * (COALESCE(e.valor_total_entrada, (0)::numeric) / (NULLIF(e.total_entrada, 0))::numeric)), 2)
        END AS valor_total
   FROM ((app_core.produtos p
     LEFT JOIN entradas e ON ((p.id = e.produto_id)))
     LEFT JOIN saidas s ON ((p.id = s.produto_id)));



CREATE VIEW app_core.v_ultima_movimentacao_produto AS
 SELECT nome_produto,
    max(data_movimentacao) AS ultima_movimentacao
   FROM app_core.v_movimentacao
  GROUP BY nome_produto;



CREATE VIEW app_core.vw_anomaly_input AS
 SELECT m.created_at AS date,
    m.produto_id AS item_id,
    m.quantidade AS value,
    m.preco_de_venda AS sell_price,
        CASE
            WHEN ((p.tipo)::text = 'MP'::text) THEN 'FOODS_1'::text
            WHEN ((p.tipo)::text = 'SA'::text) THEN 'FOODS_2'::text
            WHEN ((p.tipo)::text = 'PA'::text) THEN 'HOBBIES_1'::text
            ELSE NULL::text
        END AS category,
        CASE m.cliente
            WHEN 'Tech Solutions'::text THEN 'CA_1'::text
            WHEN 'E-commerce X'::text THEN 'CA_2'::text
            WHEN 'Empresa Corporativa Y'::text THEN 'CA_3'::text
            WHEN 'Comercial Alpha'::text THEN 'CA_4'::text
            WHEN 'Central Eletrônicos'::text THEN 'TX_1'::text
            WHEN 'Mega Informática'::text THEN 'TX_2'::text
            WHEN 'Loja Digital Prime'::text THEN 'TX_3'::text
            WHEN 'Marketplace Z'::text THEN 'WI_1'::text
            WHEN 'Loja Tech Brasil'::text THEN 'WI_2'::text
            WHEN 'Distribuidora Gamer'::text THEN 'WI_3'::text
            ELSE NULL::text
        END AS store
   FROM (app_core.movimentacoes_saida m
     JOIN app_core.produtos p ON ((p.id = m.produto_id)));



CREATE MATERIALIZED VIEW app_core.vw_product AS
 SELECT p.id,
    p.nome,
        CASE p.tipo
            WHEN 'SA'::text THEN 'Semi Acabado'::character varying
            WHEN 'MP'::text THEN 'Matéria Prima'::character varying
            WHEN 'PA'::text THEN 'Produto Acabado'::character varying
            ELSE p.tipo
        END AS tipo,
    p.descricao,
    (((COALESCE(ent.total_entrada, (0)::bigint))::numeric + COALESCE(mov.total_mov, (0)::numeric)) - (COALESCE(sai.total_saida, (0)::bigint))::numeric) AS estoque_atual,
    p.estoque_minimo,
    ((((COALESCE(ent.total_entrada, (0)::bigint))::numeric + COALESCE(mov.total_mov, (0)::numeric)) - (COALESCE(sai.total_saida, (0)::bigint))::numeric) <= (p.estoque_minimo)::numeric) AS baixo_estoque,
    (p.data_validade < CURRENT_DATE) AS vencido,
    p.data_validade,
    p.ativo
   FROM (((app_core.produtos p
     LEFT JOIN ( SELECT movimentacoes_entrada.produto_id,
            sum(movimentacoes_entrada.quantidade) AS total_entrada
           FROM app_core.movimentacoes_entrada
          GROUP BY movimentacoes_entrada.produto_id) ent ON ((p.id = ent.produto_id)))
     LEFT JOIN ( SELECT movimentacoes_internas.produto_id,
            sum(
                CASE
                    WHEN ((movimentacoes_internas.tipo)::text = 'PRODUCAO'::text) THEN movimentacoes_internas.quantidade
                    WHEN ((movimentacoes_internas.tipo)::text = 'CONSUMO'::text) THEN (- movimentacoes_internas.quantidade)
                    ELSE (0)::numeric
                END) AS total_mov
           FROM app_core.movimentacoes_internas
          GROUP BY movimentacoes_internas.produto_id) mov ON ((p.id = mov.produto_id)))
     LEFT JOIN ( SELECT movimentacoes_saida.produto_id,
            sum(movimentacoes_saida.quantidade) AS total_saida
           FROM app_core.movimentacoes_saida
          GROUP BY movimentacoes_saida.produto_id) sai ON ((p.id = sai.produto_id)))
  WITH NO DATA;



CREATE TABLE app_logs.arquivos_importados (
    id integer NOT NULL,
    file_hash text NOT NULL,
    file_name text,
    created_at timestamp without time zone DEFAULT now()
);



CREATE SEQUENCE app_logs.arquivos_importados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE app_logs.arquivos_importados_id_seq OWNED BY app_logs.arquivos_importados.id;



CREATE TABLE app_logs.importacoes (
    id bigint NOT NULL,
    nome_arquivo character varying(255) NOT NULL,
    qntd_registros integer NOT NULL,
    status character varying(15) NOT NULL,
    msg_erro text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    user_id uuid NOT NULL,
    CONSTRAINT importacoes_qntd_registros_check CHECK ((qntd_registros >= 0)),
    CONSTRAINT importacoes_status_check CHECK (((status)::text = ANY (ARRAY[('SUCESSO'::character varying)::text, ('ERRO'::character varying)::text, ('PROCESSANDO'::character varying)::text])))
);



ALTER TABLE app_logs.importacoes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_logs.importacoes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE app_logs.log_emails (
    id bigint NOT NULL,
    destinatario character varying(255) NOT NULL,
    assunto character varying(255),
    corpo text,
    status_envio character varying(20) NOT NULL,
    erro_envio text,
    requisicao_id bigint,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT log_emails_status_envio_check CHECK (((status_envio)::text = ANY (ARRAY[('ENVIADO'::character varying)::text, ('ERRO'::character varying)::text, ('PENDENTE'::character varying)::text])))
);



ALTER TABLE app_logs.log_emails ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_logs.log_emails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE app_logs.log_llm (
    id bigint NOT NULL,
    llm_id bigint,
    tipo_consulta character varying(20) NOT NULL,
    tokens integer NOT NULL,
    tempo_resposta_ms integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT log_llm_tempo_resposta_ms_check CHECK ((tempo_resposta_ms >= 0)),
    CONSTRAINT log_llm_tipo_consulta_check CHECK (((tipo_consulta)::text = ANY (ARRAY[('CHAT'::character varying)::text, ('RAG'::character varying)::text, ('COMPLETION'::character varying)::text]))),
    CONSTRAINT log_llm_tokens_check CHECK ((tokens >= 0))
);



ALTER TABLE app_logs.log_llm ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME app_logs.log_llm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE MATERIALIZED VIEW app_logs.mv_imports AS
 SELECT i.id,
    i.nome_arquivo,
    i.qntd_registros,
    i.status,
    i.msg_erro,
    i.created_at,
    u.nome AS responsavel_por
   FROM (app_logs.importacoes i
     JOIN app_core.usuarios u ON ((i.user_id = u.id)))
  WITH NO DATA;



ALTER TABLE ONLY app_ai.conversation_logs ALTER COLUMN id SET DEFAULT nextval('app_ai.conversation_logs_id_seq'::regclass);



ALTER TABLE ONLY app_core.movimentacoes_internas ALTER COLUMN id SET DEFAULT nextval('app_core.movimentacoes_internas_id_seq'::regclass);



ALTER TABLE ONLY app_core.notificacoes ALTER COLUMN id SET DEFAULT nextval('app_core.notificacoes_id_seq'::regclass);



ALTER TABLE ONLY app_logs.arquivos_importados ALTER COLUMN id SET DEFAULT nextval('app_logs.arquivos_importados_id_seq'::regclass);



ALTER TABLE ONLY app_ai.checkpoint_blobs
    ADD CONSTRAINT checkpoint_blobs_pkey PRIMARY KEY (thread_id, checkpoint_ns, channel, version);



ALTER TABLE ONLY app_ai.checkpoint_migrations
    ADD CONSTRAINT checkpoint_migrations_pkey PRIMARY KEY (v);



ALTER TABLE ONLY app_ai.checkpoint_writes
    ADD CONSTRAINT checkpoint_writes_pkey PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx);



ALTER TABLE ONLY app_ai.checkpoints
    ADD CONSTRAINT checkpoints_pkey PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id);



ALTER TABLE ONLY app_ai.conversation_logs
    ADD CONSTRAINT conversation_logs_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_ai.conversation_sessions
    ADD CONSTRAINT conversation_sessions_pkey PRIMARY KEY (session_id);



ALTER TABLE ONLY app_core.ficha_tecnica
    ADD CONSTRAINT ficha_tecnica_pkey PRIMARY KEY (produto_final_id, materia_prima_id);



ALTER TABLE ONLY app_core.itens_requisicoes
    ADD CONSTRAINT itens_requisicoes_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.itens_requisicoes
    ADD CONSTRAINT itens_requisicoes_requisicao_id_produto_id_key UNIQUE (requisicao_id, produto_id);



ALTER TABLE ONLY app_core.movimentacoes_entrada
    ADD CONSTRAINT movimentacoes_entrada_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.movimentacoes_internas
    ADD CONSTRAINT movimentacoes_internas_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.movimentacoes_saida
    ADD CONSTRAINT movimentacoes_saida_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.notificacoes_eventos
    ADD CONSTRAINT notificacoes_eventos_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.requisicoes
    ADD CONSTRAINT requisicoes_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_core.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);



ALTER TABLE ONLY app_core.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_logs.arquivos_importados
    ADD CONSTRAINT arquivos_importados_file_hash_key UNIQUE (file_hash);



ALTER TABLE ONLY app_logs.arquivos_importados
    ADD CONSTRAINT arquivos_importados_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_logs.importacoes
    ADD CONSTRAINT importacoes_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_logs.log_emails
    ADD CONSTRAINT log_emails_pkey PRIMARY KEY (id);



ALTER TABLE ONLY app_logs.log_llm
    ADD CONSTRAINT log_llm_pkey PRIMARY KEY (id);



CREATE INDEX checkpoint_blobs_thread_id_idx ON app_ai.checkpoint_blobs USING btree (thread_id);



CREATE INDEX checkpoint_writes_thread_id_idx ON app_ai.checkpoint_writes USING btree (thread_id);



CREATE INDEX checkpoints_thread_id_idx ON app_ai.checkpoints USING btree (thread_id);



CREATE INDEX idx_conversation_logs_session ON app_ai.conversation_logs USING btree (session_id, created_at);



CREATE INDEX idx_conversation_sessions_updated_at ON app_ai.conversation_sessions USING btree (updated_at DESC);



CREATE INDEX idx_itens_requisicoes_produto ON app_core.itens_requisicoes USING btree (produto_id);



CREATE UNIQUE INDEX idx_unique_mv_id ON app_core.mv_movimentacao USING btree (unique_id);



CREATE INDEX idx_usuarios_ativo ON app_core.usuarios USING btree (ativo);



CREATE UNIQUE INDEX idx_vw_product_unique_id ON app_core.vw_product USING btree (id);



CREATE INDEX idx_importacoes_created_at ON app_logs.importacoes USING btree (created_at);



CREATE INDEX idx_log_emails_created_at ON app_logs.log_emails USING btree (created_at);



CREATE INDEX idx_log_llm_created_at ON app_logs.log_llm USING btree (created_at);



CREATE UNIQUE INDEX idx_mv_imports_id ON app_logs.mv_imports USING btree (id);



CREATE INDEX idx_mv_imports_user_file ON app_logs.mv_imports USING btree (responsavel_por, nome_arquivo);



CREATE TRIGGER trg_refresh_view_entrada AFTER INSERT OR DELETE OR UPDATE ON app_core.movimentacoes_entrada FOR EACH STATEMENT EXECUTE FUNCTION app_core.refresh_stock_view();



CREATE TRIGGER trg_refresh_view_product AFTER INSERT OR DELETE OR UPDATE ON app_core.produtos FOR EACH STATEMENT EXECUTE FUNCTION app_core.refresh_stock_view();



CREATE TRIGGER trg_refresh_view_saida AFTER INSERT OR DELETE OR UPDATE ON app_core.movimentacoes_saida FOR EACH STATEMENT EXECUTE FUNCTION app_core.refresh_stock_view();



ALTER TABLE ONLY app_ai.conversation_logs
    ADD CONSTRAINT fk_session FOREIGN KEY (session_id) REFERENCES app_ai.conversation_sessions(session_id) ON DELETE CASCADE;



ALTER TABLE ONLY app_ai.conversation_sessions
    ADD CONSTRAINT id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES app_core.usuarios(id);



ALTER TABLE ONLY app_core.ficha_tecnica
    ADD CONSTRAINT ficha_tecnica_materia_prima_id_fkey FOREIGN KEY (materia_prima_id) REFERENCES app_core.produtos(id);



ALTER TABLE ONLY app_core.ficha_tecnica
    ADD CONSTRAINT ficha_tecnica_produto_final_id_fkey FOREIGN KEY (produto_final_id) REFERENCES app_core.produtos(id);



ALTER TABLE ONLY app_core.notificacoes
    ADD CONSTRAINT fk_notificacoes_evento FOREIGN KEY (event_id) REFERENCES app_core.notificacoes_eventos(id) ON DELETE CASCADE;



ALTER TABLE ONLY app_core.movimentacoes_internas
    ADD CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES app_core.produtos(id) ON DELETE RESTRICT;



ALTER TABLE ONLY app_core.itens_requisicoes
    ADD CONSTRAINT itens_requisicoes_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES app_core.produtos(id) ON DELETE RESTRICT;



ALTER TABLE ONLY app_core.itens_requisicoes
    ADD CONSTRAINT itens_requisicoes_requisicao_id_fkey FOREIGN KEY (requisicao_id) REFERENCES app_core.requisicoes(id) ON DELETE RESTRICT;



ALTER TABLE ONLY app_core.movimentacoes_entrada
    ADD CONSTRAINT movimentacoes_entrada_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES app_core.produtos(id) ON DELETE RESTRICT;



ALTER TABLE ONLY app_core.movimentacoes_saida
    ADD CONSTRAINT movimentacoes_saida_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES app_core.produtos(id) ON DELETE RESTRICT;



ALTER TABLE ONLY app_core.requisicoes
    ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES app_core.usuarios(id);



ALTER TABLE ONLY app_core.notificacoes
    ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES app_core.usuarios(id);



ALTER TABLE ONLY app_logs.log_emails
    ADD CONSTRAINT log_emails_requisicao_id_fkey FOREIGN KEY (requisicao_id) REFERENCES app_core.requisicoes(id) ON DELETE SET NULL;



ALTER TABLE ONLY app_logs.importacoes
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES app_core.usuarios(id);



