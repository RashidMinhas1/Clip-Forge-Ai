-- RLS Policies for Clip Forge AI

-- Enable RLS on all user-owned tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE clips ENABLE ROW LEVEL SECURITY;
ALTER TABLE render_jobs ENABLE ROW LEVEL SECURITY;

-- 1. Profiles Policies
-- Users can read their own profile
CREATE POLICY "Users can view own profile"
ON profiles FOR SELECT
USING ( auth.uid() = id );

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING ( auth.uid() = id );

-- 2. Projects Policies
CREATE POLICY "Users can view own projects"
ON projects FOR SELECT
USING ( auth.uid() = user_id );

CREATE POLICY "Users can create own projects"
ON projects FOR INSERT
WITH CHECK ( auth.uid() = user_id );

CREATE POLICY "Users can update own projects"
ON projects FOR UPDATE
USING ( auth.uid() = user_id );

CREATE POLICY "Users can delete own projects"
ON projects FOR DELETE
USING ( auth.uid() = user_id );

-- 3. Project Sources Policies
CREATE POLICY "Users can view own sources"
ON project_sources FOR SELECT
USING ( auth.uid() = user_id );

CREATE POLICY "Users can insert own sources"
ON project_sources FOR INSERT
WITH CHECK ( auth.uid() = user_id );

CREATE POLICY "Users can update own sources"
ON project_sources FOR UPDATE
USING ( auth.uid() = user_id );

CREATE POLICY "Users can delete own sources"
ON project_sources FOR DELETE
USING ( auth.uid() = user_id );

-- 4. Clips Policies
CREATE POLICY "Users can view own clips"
ON clips FOR SELECT
USING ( auth.uid() = user_id );

CREATE POLICY "Users can insert own clips"
ON clips FOR INSERT
WITH CHECK ( auth.uid() = user_id );

CREATE POLICY "Users can update own clips"
ON clips FOR UPDATE
USING ( auth.uid() = user_id );

CREATE POLICY "Users can delete own clips"
ON clips FOR DELETE
USING ( auth.uid() = user_id );

-- 5. Render Jobs Policies
CREATE POLICY "Users can view own render jobs"
ON render_jobs FOR SELECT
USING ( auth.uid() = user_id );

CREATE POLICY "Users can insert own render jobs"
ON render_jobs FOR INSERT
WITH CHECK ( auth.uid() = user_id );

CREATE POLICY "Users can update own render jobs"
ON render_jobs FOR UPDATE
USING ( auth.uid() = user_id );

CREATE POLICY "Users can delete own render jobs"
ON render_jobs FOR DELETE
USING ( auth.uid() = user_id );
