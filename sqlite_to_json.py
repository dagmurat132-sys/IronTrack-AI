"""Read-only conversion of legacy IronTrack SQLite data to mobile JSON backup.
Usage: py sqlite_to_json.py "C:\\path\\irontrack.db"
Never changes the original database.
"""
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DAYS = ('Pazartesi', 'Salı')

def convert(db_path):
    path = Path(db_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    # Read-only connection guarantees no edits to the user's database.
    with sqlite3.connect(f'file:{path.as_posix()}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {'exercises', 'sessions', 'sets'}.issubset(tables):
            raise ValueError('Bu dosya IronTrack veritabanı değil.')
        exercises = []
        for e in db.execute('SELECT * FROM exercises'):
            exercises.append({'id': str(e['id']), 'name': e['name'], 'group': e['muscle_group'], 'targets': [int(e['rep_max'] or 12)] * 3})
        plans = {day: [] for day in DAYS}
        if 'day_plan' in tables:
            for p in db.execute('SELECT day,exercise_id FROM day_plan ORDER BY day,position'):
                if p['day'] in plans:
                    plans[p['day']].append(str(p['exercise_id']))
        else:
            for day in DAYS:
                plans[day] = [x['id'] for x in exercises]
        if 'set_targets' in tables:
            for t in db.execute('SELECT exercise_id,set_number,target_reps FROM set_targets'):
                ex = next((x for x in exercises if x['id'] == str(t['exercise_id'])), None)
                if ex and 1 <= t['set_number'] <= 3:
                    ex['targets'][t['set_number']-1] = int(t['target_reps'])
        sessions = []
        for s in db.execute('SELECT * FROM sessions ORDER BY session_date,id'):
            sets = []
            for t in db.execute('SELECT * FROM sets WHERE session_id=? ORDER BY id', (s['id'],)):
                ex = next((x for x in exercises if x['id'] == str(t['exercise_id'])), None)
                n = int(t['set_number'])
                sets.append({'exerciseId': str(t['exercise_id']), 'number': n, 'kg': float(t['weight']), 'reps': int(t['reps']), 'rir': t['rir'], 'target': ex['targets'][n-1] if ex and 1 <= n <= 3 else 12})
            if sets:
                sessions.append({'id': str(s['id']), 'date': s['session_date'], 'day': s['workout_name'] if s['workout_name'] in DAYS else 'Pazartesi', 'created': s['created_at'] or datetime.now().isoformat(), 'sets': sets})
        return {'version': 3, 'exercises': exercises, 'plans': plans, 'sessions': sessions, 'drafts': {}, 'lastSaved': {}}

def main():
    if len(sys.argv) != 2:
        print('Kullanım: py sqlite_to_json.py "C:\\...\\irontrack.db"')
        return 2
    try:
        result = convert(sys.argv[1])
        output = Path.cwd() / 'irontrack-eski-kayitlar.json'
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'JSON hazır: {output} | {len(result["sessions"])} antrenman')
        return 0
    except Exception as e:
        print(f'Hata: {e}')
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
