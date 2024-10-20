-- Database: Synthesis_mod_AI

-- DROP DATABASE "Synthesis_mod_AI";

CREATE DATABASE "Synthesis_mod_AI"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
-- Table: public.Base_links

-- DROP TABLE public."Base_links";

CREATE TABLE public."Base_links"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "SRC_LINK" bigint,
    "DIST_LINK" bigint,
    "RULE" text COLLATE pg_catalog."default",
    "NOTES" text COLLATE pg_catalog."default",
    CONSTRAINT "Base_links_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Base_links"
    OWNER to postgres;
	
-- Table: public.Base_model

-- DROP TABLE public."Base_model";

CREATE TABLE public."Base_model"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "BASE_ID" bigint,
    "MODEL_TYPE" text COLLATE pg_catalog."default",
    "SRC_ID" text COLLATE pg_catalog."default",
    "NAME" text COLLATE pg_catalog."default",
    "BASE_PARENT_ID" text COLLATE pg_catalog."default",
    "LEVEL_NUM" bigint,
    "NODE_TYPE" text COLLATE pg_catalog."default",
    "PARENT_ID" text COLLATE pg_catalog."default",
    CONSTRAINT "Base_model_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Base_model"
    OWNER to postgres;
-- Index: Base_model_index

-- DROP INDEX public."Base_model_index";

CREATE INDEX "Base_model_index"
    ON public."Base_model" USING btree
    ("MODEL_TYPE" COLLATE pg_catalog."default" bpchar_pattern_ops ASC NULLS LAST, "NODE_TYPE" COLLATE pg_catalog."default" bpchar_pattern_ops ASC NULLS LAST)
    TABLESPACE pg_default;
	
-- Table: public.Facts

-- DROP TABLE public."Facts";

CREATE TABLE public."Facts"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "FACT_STATE" text COLLATE pg_catalog."default",
    "MODEL_TYPE" text COLLATE pg_catalog."default",
    "NODE_TYPE" text COLLATE pg_catalog."default",
    "NAME" text COLLATE pg_catalog."default",
    "PARENT_ID" text COLLATE pg_catalog."default",
    "LEVEL_NUM" bigint,
    "FACT_ID" text COLLATE pg_catalog."default",
    CONSTRAINT "Facts_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Facts"
    OWNER to postgres;
-- Index: Facts_index

-- DROP INDEX public."Facts_index";

CREATE INDEX "Facts_index"
    ON public."Facts" USING btree
    ("MODEL_TYPE" COLLATE pg_catalog."default" bpchar_pattern_ops ASC NULLS LAST, "NODE_TYPE" COLLATE pg_catalog."default" bpchar_pattern_ops ASC NULLS LAST)
    TABLESPACE pg_default;
	
-- Table: public.Req

-- DROP TABLE public."Req";

CREATE TABLE public."Req"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "MODEL_TYPE" text COLLATE pg_catalog."default",
    "NODE_TYPE" text COLLATE pg_catalog."default",
    "NAME" text COLLATE pg_catalog."default",
    "SRC_ID" text COLLATE pg_catalog."default",
    "PARENT_ID" text COLLATE pg_catalog."default",
    "LEVEL_NUM" bigint,
    CONSTRAINT "Req_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Req"
    OWNER to postgres;
	
-- Table: public.Req_links

-- DROP TABLE public."Req_links";

CREATE TABLE public."Req_links"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "SRC_LINK" bigint,
    "DIST_LINK" bigint,
    "RULE" text COLLATE pg_catalog."default",
    "NOTES" text COLLATE pg_catalog."default",
    CONSTRAINT "Req_links_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Req_links"
    OWNER to postgres;
	
-- Table: public.Req_model

-- DROP TABLE public."Req_model";

CREATE TABLE public."Req_model"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "BASE_ID" bigint,
    "MODEL_TYPE" text COLLATE pg_catalog."default",
    "SRC_ID" text COLLATE pg_catalog."default",
    "NAME" text COLLATE pg_catalog."default",
    "BASE_PARENT_ID" text COLLATE pg_catalog."default",
    "LEVEL_NUM" bigint,
    "NODE_TYPE" text COLLATE pg_catalog."default",
    "PARENT_ID" text COLLATE pg_catalog."default",
    CONSTRAINT "Req_model_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Req_model"
    OWNER to postgres;
	
-- Table: public.Temp_table

-- DROP TABLE public."Temp_table";

CREATE TABLE public."Temp_table"
(
    "BASE_ID" bigint,
    "PARENT_ID" text COLLATE pg_catalog."default",
    "SRC_ID" text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public."Temp_table"
    OWNER to postgres;
	
-- Table: public.Temp_table2

-- DROP TABLE public."Temp_table2";

CREATE TABLE public."Temp_table2"
(
    "BASE_ID" bigint,
    "PARENT_ID" text COLLATE pg_catalog."default",
    "SRC_ID" text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public."Temp_table2"
    OWNER to postgres;
	
-- Table: public.Facts_processed

-- DROP TABLE public."Facts_processed";

CREATE TABLE IF NOT EXISTS public."Facts_processed"
(
    "ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "FACT_ID" text COLLATE pg_catalog."default",
    "LEVEL_NUM" bigint,
    "isAchieved" bigint,
    "CONTROL_DATE" timestamp with time zone,
    CONSTRAINT "Facts_processed_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE public."Facts_processed"
    OWNER to postgres;