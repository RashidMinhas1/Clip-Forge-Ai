-- Enable Realtime for render_jobs table

-- First, ensure the publication exists (Supabase creates 'supabase_realtime' by default)
-- Add the render_jobs table to the publication
BEGIN;
  DROP PUBLICATION IF EXISTS supabase_realtime;
  CREATE PUBLICATION supabase_realtime;
COMMIT;

ALTER PUBLICATION supabase_realtime ADD TABLE render_jobs;
