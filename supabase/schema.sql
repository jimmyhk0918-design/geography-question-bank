create table if not exists public.student_progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  bank_id text not null,
  progress jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, bank_id)
);

alter table public.student_progress enable row level security;

drop policy if exists "Students can read their own progress" on public.student_progress;
create policy "Students can read their own progress"
on public.student_progress
for select
using (auth.uid() = user_id);

drop policy if exists "Students can insert their own progress" on public.student_progress;
create policy "Students can insert their own progress"
on public.student_progress
for insert
with check (auth.uid() = user_id);

drop policy if exists "Students can update their own progress" on public.student_progress;
create policy "Students can update their own progress"
on public.student_progress
for update
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

drop policy if exists "Students can delete their own progress" on public.student_progress;
create policy "Students can delete their own progress"
on public.student_progress
for delete
using (auth.uid() = user_id);

create index if not exists student_progress_updated_at_idx
on public.student_progress (updated_at desc);
