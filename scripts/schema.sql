/* Create DDBB schema: */
create table execute (id INTEGER PRIMARY KEY AUTOINCREMENT, class TEXT, action TEXT, value TEXT, extra TEXT, command TEXT);
create table config (id INTEGER PRIMARY KEY AUTOINCREMENT, json TEXT);
