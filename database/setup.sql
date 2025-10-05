--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Debian 15.1-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cybernews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cybernews (
    id bigserial primary key,
    source text,
    url text,
    title text,
    date text,
    recorded bigint,
    details text,
    html text
);


ALTER TABLE public.cybernews OWNER TO postgres;

--
-- Data for Name: cybernews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cybernews (id, source, url, title, date, recorded, details, html) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

