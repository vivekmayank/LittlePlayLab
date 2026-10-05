import {DatabaseSync} from 'node:sqlite';
import {mkdirSync,readFileSync,readdirSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
type Value=string|number|null;
let connection:DatabaseSync|undefined;
export function nodeDb(){
 if(!connection){
  const filename=process.env.DATABASE_PATH||resolve(process.cwd(),'data/play-lab.sqlite');mkdirSync(dirname(filename),{recursive:true});
  connection=new DatabaseSync(filename);connection.exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;');
  connection.exec('CREATE TABLE IF NOT EXISTS migrations (name TEXT PRIMARY KEY)');
  const dir=resolve(process.cwd(),'drizzle');
  for(const file of readdirSync(dir).filter(f=>f.endsWith('.sql')).sort()){
   if(!connection.prepare('SELECT name FROM migrations WHERE name=?').get(file)){
    connection.exec('BEGIN IMMEDIATE');
    try{connection.exec(readFileSync(resolve(dir,file),'utf8'));connection.prepare('INSERT INTO migrations(name) VALUES(?)').run(file);connection.exec('COMMIT');}catch(error){connection.exec('ROLLBACK');throw error;}
   }
  }
 }
 const db=connection;
 return {prepare(sql:string){let args:Value[]=[];return {bind(...values:Value[]){args=values;return this;},async first<T=Record<string,unknown>>(){return db.prepare(sql).get(...args) as T|undefined;},async all(){return {results:db.prepare(sql).all(...args)};},async run(){return db.prepare(sql).run(...args);}};}};
}
