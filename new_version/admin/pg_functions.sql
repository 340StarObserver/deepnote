-- < insert a note >
-- involved tables :
-- 	1. dp_note.note_base
-- 	2. dp_note.note_text
create or replace function addnote(
	p_note_id 	uuid,
	p_usr_nick 	varchar(32),
	p_title 		varchar(128),
	p_tags 		varchar(64),
	p_refs 		text,
	p_feel 		text
	) returns void as $$
begin
	insert into note_base (note_id, usr_nick) values (p_note_id, p_usr_nick);
	insert into note_text (note_id, title, tags, refs, feel, textunite) values (
		p_note_id, p_title, p_tags, p_refs, p_feel,
		setweight(to_tsvector('chinese', p_title), 'A') || 
		setweight(to_tsvector('chinese', p_tags) , 'A') || 
		setweight(to_tsvector('chinese', p_refs) , 'C') || 
		setweight(to_tsvector('chinese', p_feel) , 'B')
	);
end;
$$ language plpgsql;
