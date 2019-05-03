--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.12
-- Dumped by pg_dump version 10.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: tsm_system_rows; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS tsm_system_rows WITH SCHEMA public;


--
-- Name: EXTENSION tsm_system_rows; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION tsm_system_rows IS 'TABLESAMPLE method which accepts number of rows as a limit';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: amazon_reviews; Type: TABLE; Schema: public; Owner: cs411project
--

CREATE TABLE public.amazon_reviews (
    reviewid integer NOT NULL,
    reviewtext text NOT NULL,
    overall integer NOT NULL
);


ALTER TABLE public.amazon_reviews OWNER TO cs411project;

--
-- Name: amazon_reviews_reviewid_seq; Type: SEQUENCE; Schema: public; Owner: cs411project
--

CREATE SEQUENCE public.amazon_reviews_reviewid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_reviews_reviewid_seq OWNER TO cs411project;

--
-- Name: amazon_reviews_reviewid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs411project
--

ALTER SEQUENCE public.amazon_reviews_reviewid_seq OWNED BY public.amazon_reviews.reviewid;


--
-- Name: crew; Type: TABLE; Schema: public; Owner: cs411project
--

CREATE TABLE public.crew (
    tconst character varying(18),
    directors text,
    writers text
);


ALTER TABLE public.crew OWNER TO cs411project;

--
-- Name: movie_reviews; Type: TABLE; Schema: public; Owner: cs411project
--

CREATE TABLE public.movie_reviews (
    tconst character varying(18),
    reviewid integer
);


ALTER TABLE public.movie_reviews OWNER TO cs411project;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: cs411project
--

CREATE TABLE public.movies (
    tconst character varying(18) NOT NULL,
    titletype character varying(24),
    primarytitle character varying(510),
    originaltitle character varying(510),
    isadult integer,
    startyear integer,
    endyear integer,
    runtimeminutes integer,
    genres character varying(64)
);


ALTER TABLE public.movies OWNER TO cs411project;

--
-- Name: ratings; Type: TABLE; Schema: public; Owner: cs411project
--

CREATE TABLE public.ratings (
    tconst character varying(18),
    averagerating numeric(3,1),
    numvotes integer
);


ALTER TABLE public.ratings OWNER TO cs411project;

--
-- Name: amazon_reviews reviewid; Type: DEFAULT; Schema: public; Owner: cs411project
--

ALTER TABLE ONLY public.amazon_reviews ALTER COLUMN reviewid SET DEFAULT nextval('public.amazon_reviews_reviewid_seq'::regclass);


--
-- Name: amazon_reviews amazon_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: cs411project
--

ALTER TABLE ONLY public.amazon_reviews
    ADD CONSTRAINT amazon_reviews_pkey PRIMARY KEY (reviewid);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: cs411project
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (tconst);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO cs411project;


--
-- PostgreSQL database dump complete
--

