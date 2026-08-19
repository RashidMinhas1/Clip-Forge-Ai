import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://epcxaiztuvgwrafrkouu.supabase.co';
const supabaseKey = 'sb_publishable_b-t3eoQ7swaAyXWDn_Skew_Kf4ojZ2z';
const supabase = createClient(supabaseUrl, supabaseKey);

async function run() {
    console.log("Signing in...");
    let { data, error } = await supabase.auth.signInWithPassword({ email: 'testuser@example.com', password: 'password123' });
    if (error) {
        console.log("SignIn failed, trying SignUp...", error.message);
        const res = await supabase.auth.signUp({ email: 'testuser@example.com', password: 'password123' });
        data = res.data;
        error = res.error;
    }
    if (error) { console.error("Auth Error:", error); return; }
    
    const token = data.session?.access_token;
    console.log("Got token length:", token?.length);
    
    console.log("Fetching from backend...");
    const backendRes = await fetch('http://127.0.0.1:8000/api/v1/projects', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    console.log("Backend status:", backendRes.status);
    console.log("Backend response:", await backendRes.text());
}
run();
