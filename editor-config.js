/* ============================================================
   Built for Wonder — Editor cloud config
   ------------------------------------------------------------
   Paste your Supabase project URL + anon (public) key below to
   turn on cloud sync. Until you do, the editor runs in LOCAL
   mode (edits/notes stay in that one browser).

   These are PUBLIC values (the anon key is meant to ship in the
   browser). Access is controlled by the table policies you set
   up in SUPABASE-SETUP.md — treat the editor URL itself as the
   "password": only share it with people you want editing.
   ============================================================ */
window.EDITOR_CONFIG = {
  supabaseUrl:     "",   // e.g. "https://abcdxyz.supabase.co"
  supabaseAnonKey: ""    // the "anon public" key from Supabase → Settings → API
};
