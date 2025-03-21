
### glower
A tool box for glow developers

1. change `user` and `host` in `glower/init.sh` to your own user and host.
2. add `[[ -f path/to/glower/init.sh ]] && source path/to/glower/init.sh` to your `.bashrc` or `.zshrc` to enable the command `glower`.
3. then you get a command line tool called sbt, change name as your want in init.sh

### How to use
see tools help
```
sbt -h
sbt deploy -h
sbt run -h
use <TAB> to auto complete
```

### convenient way: deploy a single python file to sandbox 
sbt deploy your/path/to/glow/server/bryo/file_your_want_to_deploy.py --service bryo-www

### convenient way: run a single python file on sandbox
sbt run your/path/to/your/python/file.py

### convenient way: avoid mocking context every time, use /test dir for example
sbt run your/path/to/test/test_user.py --upload-parent (must be used with --upload-parent to upload base.py)
#### run a single function in test_user.py
sbt run your/path/to/test/test_user.py test_example

### deploy_sandbox_server
This is another tool written by Alias, deploy entire service to sandbox. See its readme for more info. Consult Alia if has problem in usage.
