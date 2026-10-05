import {nodeDb} from './node-db';
export function db(){return nodeDb();}
export function secrets(){return process.env as Record<string,string>;}
export const hex=(b:ArrayBuffer)=>Array.from(new Uint8Array(b)).map(x=>x.toString(16).padStart(2,'0')).join('');
export async function digest(s:string){return hex(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)));}
export async function password(p:string,s:string){const k=await crypto.subtle.importKey('raw',new TextEncoder().encode(p),'PBKDF2',false,['deriveBits']);return hex(await crypto.subtle.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:new TextEncoder().encode(s),iterations:100000},k,256));}
export async function hmac(s:string,key:string){const k=await crypto.subtle.importKey('raw',new TextEncoder().encode(key),{name:'HMAC',hash:'SHA-256'},false,['sign']);return hex(await crypto.subtle.sign('HMAC',k,new TextEncoder().encode(s)));}
export function equal(a:string,b:string){let d=a.length^b.length;for(let i=0;i<Math.max(a.length,b.length);i++)d|=(a.charCodeAt(i)||0)^(b.charCodeAt(i)||0);return d===0;}
export async function user(req:Request){const t=req.headers.get('cookie')?.match(/(?:^|;\s*)play_session=([^;]+)/)?.[1];if(!t)return null;return db().prepare('SELECT u.id,u.name,u.email FROM users u JOIN sessions s ON u.id=s.user_id WHERE s.token=? AND s.expires>?').bind(await digest(t),Date.now()).first<{id:string,name:string,email:string}>();}
export async function entitled(id:string){return !!await db().prepare("SELECT id FROM orders WHERE user_id=? AND status='paid' AND (expires IS NULL OR expires>?) LIMIT 1").bind(id,Date.now()).first();}
export function guard(req:Request){const o=req.headers.get('origin');if(o&&new URL(o).host!==req.headers.get('host'))throw new Error('Please submit from this website.');}
export async function throttle(key:string){const now=Date.now();await db().prepare('INSERT INTO attempts(key,count,expires) VALUES(?,1,?) ON CONFLICT(key) DO UPDATE SET count=CASE WHEN expires<? THEN 1 ELSE count+1 END,expires=CASE WHEN expires<? THEN excluded.expires ELSE expires END').bind(key,now+900000,now,now).run();const r=await db().prepare('SELECT count FROM attempts WHERE key=?').bind(key).first<{count:number}>();if(r&&r.count>15)throw new Error('Too many attempts. Please try again in 15 minutes.');}
