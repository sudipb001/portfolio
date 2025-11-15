-- schema.sql
create table if not exists public.sales (
  id bigserial primary key,
  sale_date date not null,
  region text not null,
  product text not null,
  customer text,
  quantity int not null,
  revenue numeric(12,2) not null,
  created_at timestamptz default now()
);
