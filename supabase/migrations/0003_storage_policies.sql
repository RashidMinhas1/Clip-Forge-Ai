-- Storage Schema and Policies for Clip Forge AI

-- 1. Create Buckets
INSERT INTO storage.buckets (id, name, public) 
VALUES ('source-videos', 'source-videos', false)
ON CONFLICT (id) DO NOTHING;

INSERT INTO storage.buckets (id, name, public) 
VALUES ('project-assets', 'project-assets', false)
ON CONFLICT (id) DO NOTHING;

INSERT INTO storage.buckets (id, name, public) 
VALUES ('exports', 'exports', false)
ON CONFLICT (id) DO NOTHING;

-- 2. Storage RLS Policies

-- Enable RLS for objects
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- source-videos bucket policies
CREATE POLICY "Users can upload own source-videos"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'source-videos' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view own source-videos"
ON storage.objects FOR SELECT
USING (
    bucket_id = 'source-videos' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update own source-videos"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'source-videos' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own source-videos"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'source-videos' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);


-- project-assets bucket policies
CREATE POLICY "Users can upload own project-assets"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'project-assets' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view own project-assets"
ON storage.objects FOR SELECT
USING (
    bucket_id = 'project-assets' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update own project-assets"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'project-assets' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own project-assets"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'project-assets' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);


-- exports bucket policies
CREATE POLICY "Users can upload own exports"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'exports' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view own exports"
ON storage.objects FOR SELECT
USING (
    bucket_id = 'exports' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update own exports"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'exports' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own exports"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'exports' AND 
    auth.uid()::text = (storage.foldername(name))[1]
);
