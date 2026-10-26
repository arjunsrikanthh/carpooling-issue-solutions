#!/usr/bin/env python3
"""Verify a prepared app with disposable Docker databases. Never use existing volumes."""
from pathlib import Path
import json,os,secrets,shutil,subprocess,sys,tempfile,time

def run(args,cwd=None,env=None,capture=False,check=True):
    p=subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None)
    if check and p.returncode: raise RuntimeError(f'Command failed ({p.returncode}): {args[0]} {args[1] if len(args)>1 else ""}')
    return p

def main():
    if len(sys.argv)!=3:raise RuntimeError('Usage: test-integration.py ISSUE CHECKOUT')
    issue,checkout=sys.argv[1],Path(sys.argv[2]).resolve();app=checkout/'campuspool'
    context=os.environ.get('DOCKER_CONTEXT')
    docker=['docker']+(['--context',context] if context else [])
    if run(docker+['info'],capture=True,check=False).returncode:
        raise RuntimeError('Start Docker Desktop, or set DOCKER_CONTEXT to your running Docker context, then retry verification.')
    project='campuspool-check-'+secrets.token_hex(5)
    with tempfile.TemporaryDirectory(prefix=project+'-') as tmp:
        compose=Path(tmp)/'compose.json'
        config={'name':project,'services':{
          'mysql':{'image':'mysql:8.4','environment':{'MYSQL_DATABASE':'campuspool','MYSQL_USER':'campuspool','MYSQL_PASSWORD':'local-test-only','MYSQL_ROOT_PASSWORD':'local-root-only'},'command':['--skip-log-bin','--default-time-zone=+00:00'],'ports':['127.0.0.1::3306'],'healthcheck':{'test':['CMD','mysqladmin','ping','-h','127.0.0.1'],'interval':'2s','timeout':'3s','retries':60}},
          'mongo':{'image':'mongo:8.0','ports':['127.0.0.1::27017'],'healthcheck':{'test':['CMD','mongosh','--quiet','--eval','db.adminCommand({ping:1}).ok'],'interval':'2s','timeout':'3s','retries':60}}
        }}
        compose.write_text(json.dumps(config));cmd=docker+['compose','-f',str(compose)]
        try:
            run(cmd+['up','-d','--wait','--wait-timeout','180'])
            sql_port=run(cmd+['port','mysql','3306'],capture=True).stdout.strip().rsplit(':',1)[1]
            mongo_port=run(cmd+['port','mongo','27017'],capture=True).stdout.strip().rsplit(':',1)[1]
            env={**os.environ,'DATABASE_URL':f'mysql://campuspool:local-test-only@127.0.0.1:{sql_port}/campuspool','MIGRATION_DATABASE_URL':f'mysql://root:local-root-only@127.0.0.1:{sql_port}/campuspool','MONGODB_URI':f'mongodb://127.0.0.1:{mongo_port}','MONGODB_DB':'campuspool','SESSION_SECRET':secrets.token_hex(32),'APP_ORIGIN':'http://127.0.0.1:3000','DEMO_PASSWORD':'TestOnlyPassword123!','RUN_CAMPUSPOOL_INTEGRATION':'1'}
            for script in ['db:migrate','db:migrate','db:seed']:run(['npm','run',script],app,env)
            run(['npm','test','--','--exclude','tests/http.e2e.test.ts'],app,env)
            required=['tests/http.e2e.test.ts','src/app/api/bookings/route.ts','src/app/api/offers/route.ts','src/app/api/vehicles/route.ts','src/app/api/cancellations/route.ts','src/app/api/activity/route.ts']
            if all((app/f).is_file() for f in required):run(['npm','run','test:http'],app,env)
            else:print('Full cross-feature HTTP journey requires the remaining feature PRs. Available SQL/Mongo integration tests passed.')
        except BaseException:
            run(cmd+['logs','--tail','25'],check=False)
            raise
        finally:run(cmd+['down','--volumes','--remove-orphans'],check=False)
    print(f'Issue {issue}: isolated database verification passed.')

if __name__=='__main__':
    try:main()
    except Exception as error:print(f'test-integration: {error}',file=sys.stderr);sys.exit(1)
