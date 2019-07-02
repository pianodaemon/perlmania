---
--- New catalog tables and values
---

CREATE TABLE public.adjudications (
    id integer NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL
);

CREATE TABLE public.fundings (
    id integer NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL
);

INSERT INTO adjudications(id, title, description)
    VALUES (1, 'Licitación Pública', ''),
           (2, 'Adjudicación Directa', ''),
           (3, 'Invitación Restringida', '');

INSERT INTO fundings(id, title, description)
    VALUES (1, 'Federal', ''), (2, 'Estatal', '');

ALTER TABLE public.contracts ADD COLUMN adjudication integer;
ALTER TABLE public.contracts ADD COLUMN funding integer;
ALTER TABLE public.contracts ADD COLUMN program integer;

CREATE OR REPLACE FUNCTION public.alter_contract(
    _contract_id integer,
    _number character varying,
    _title character varying,
    _description text,
    _provider integer,
    _delivery_stage integer,
    _adjudication integer,
    _funding integer,
    _program integer,
    _initial_contracted_amount double precision,
    _kickoff date,
    _ending date,
    _down_payment date,
    _down_payment_amount double precision,
    _ext_agreement date,
    _ext_agreement_amount double precision,
    _final_contracted_amount double precision,
    _total_amount_paid double precision,
    _outstanding_down_payment double precision,
    _inceptor_uuid character varying
) RETURNS record
LANGUAGE plpgsql
AS $$

DECLARE

    current_moment timestamp with time zone = now();
    coincidences integer := 0;
    latter_id integer := 0;

    -- dump of errors
    rmsg text;

BEGIN

    CASE

        WHEN _contract_id = 0 THEN

            INSERT INTO contracts (
                number,
                title,
                description ,
                provider,
                delivery_stage,
                adjudication,
                funding,
                program,
                initial_contracted_amount,
                kickoff,
                ending,
                down_payment,
                down_payment_amount,
                ext_agreement,
                ext_agreement_amount,
                final_contracted_amount,
                total_amount_paid,
                outstanding_down_payment,
                inceptor_uuid,
                inception_time,
                touch_latter_time
            ) VALUES (
                _number,
                _title,
                _description,
                _provider,
                _delivery_stage,
                _adjudication,
                _funding,
                _program,
                _initial_contracted_amount,
                _kickoff,
                _ending,
                _down_payment,
                _down_payment_amount,
                _ext_agreement,
                _ext_agreement_amount,
                _final_contracted_amount,
                _total_amount_paid,
                _outstanding_down_payment,
                _inceptor_uuid,
                current_moment,
                current_moment		
            ) RETURNING id INTO latter_id;

        WHEN _contract_id > 0 THEN

            -- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            -- STARTS - Validates contract id
            --
            -- JUSTIFICATION: Because UPDATE statement does not issue
            -- any exception if nothing was updated.
            -- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            SELECT count(id)
            FROM contracts INTO coincidences
            WHERE not blocked AND id = _contract_id;

            IF not coincidences = 1 THEN
                RAISE EXCEPTION 'contract identifier % does not exist', _contract_id;
            END IF;
            -- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            -- ENDS - Validate contract id
            -- :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

            UPDATE contracts
            SET number = _number, title  = _title, description = _description,
                provider = _provider, delivery_stage = _delivery_stage,
                adjudication = _adjudication, funding = _funding, program = _program,
                initial_contracted_amount = _initial_contracted_amount,
                kickoff = _kickoff, ending = _ending, down_payment = _down_payment,
                down_payment_amount = _down_payment_amount,
                ext_agreement = _ext_agreement,
                ext_agreement_amount = _ext_agreement_amount,
                final_contracted_amount = _final_contracted_amount,
                total_amount_paid = _total_amount_paid,
                outstanding_down_payment = _outstanding_down_payment,
                touch_latter_time = current_moment
            WHERE id = _contract_id;

            -- Upon edition we return contract id as latter id
            latter_id = _contract_id;

        ELSE
            RAISE EXCEPTION 'negative contract identifier % is unsupported', _contract_id;

    END CASE;

    return ( latter_id::integer, ''::text );

    EXCEPTION
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS rmsg = MESSAGE_TEXT;
            return ( -1::integer, rmsg::text );

END;
$$;
