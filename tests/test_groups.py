import hashlib
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from wechat_mac_export.messages import collect_messages, write_export
from wechat_mac_export.cli import _parser

class GroupExportTests(unittest.TestCase):
    def test_selection_members_and_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with closing(sqlite3.connect(root / 'contact.db')) as db, db:
                db.executescript("CREATE TABLE contact(username TEXT, local_type INTEGER, remark TEXT, nick_name TEXT); CREATE TABLE chat_room(username TEXT);")
                db.executemany("INSERT INTO contact VALUES (?, ?, ?, ?)", [('g@chatroom',2,None,'合成群'), ('other@chatroom',2,None,'合成群'), ('member',1,None,'合成成员')])
            with closing(sqlite3.connect(root / 'message_0.db')) as db, db:
                db.execute('CREATE TABLE Name2Id(user_name TEXT)')
                db.executemany('INSERT INTO Name2Id VALUES (?)', [('owner',),('member',),('g@chatroom',),('peer',)])
                for cid in ['g@chatroom','peer']:
                    table = 'Msg_' + hashlib.md5(cid.encode()).hexdigest()
                    db.execute(f'CREATE TABLE {table}(local_id,server_id,create_time,local_type,real_sender_id,message_content)')
                    db.executemany(f'INSERT INTO {table} VALUES (?,?,?,?,?,?)', [(1,1,1700000000,1,1,'本人'),(2,2,1700000001,1,2,'成员'),(3,3,1700000002,1,999,'未知')])
            args=(root,'owner',root/'contact.db')
            self.assertEqual(set(collect_messages(*args)[0]), {'peer'})
            self.assertEqual(set(collect_messages(*args,include_groups=True)[0]), {'peer','g@chatroom'})
            with self.assertRaises(ValueError): collect_messages(*args,group_selectors=('合成群',))
            chats, unresolved=collect_messages(*args,group_selectors=('g@chatroom',))
            rows=chats['g@chatroom'][1]
            self.assertEqual([r['sender'] for r in rows], ['me','them','unknown'])
            self.assertEqual(rows[1]['sender_name'], '合成成员')
            out=root/'out';out.mkdir();write_export(out,chats,unresolved)
            entry=json.loads((out/'导出清单.json').read_text())['conversations'][0]
            self.assertEqual(entry['chat_type'],'group');self.assertTrue(entry['code'].startswith('G'))
            parsed=_parser().parse_args(['export','--snapshot','s','--key-file','k','--output','o','--group','合成群'])
            self.assertEqual(parsed.group,['合成群'])
