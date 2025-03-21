#Set up the tools
<ol>
<li>run setup.sh</li>
<li>open config.py, replace USERNAME, TOKEN(jenkins api token), REPO_ROOT_PATH with your own one</li>
<li>add <code>alias deploysb="[path_to_the_file]/deploy_sandbox_server.py</code> in your .zshrc file, source .zshrc</li>
</ol>

#How to get a jenkins token
<ol>
<li>Click your name on jenkins website (on the top right corner)</li>
<li>Click Configure in the left bar</li>
<li>Click Add new Token on the API Token section</li>
</ol>

#Usage:
you can run <code>deploysb --help</code> to see details, and here are some basic examples:
<ol>
<li>deploy current repo with current branch:<br> 
<code>deploysb</code></li>
<li>deploy current repo with given branch:<br> 
<code>deploysb --branch test-branch</code></li>
<li>deploy given repo with given branch:<br> 
<code>deploysb --branch test-branch --app bryo --branch master</code></li>
<li>deploy current repo with current branch, and slack someone(no need to mention yourself here, your will always be mentioned):<br> 
<code>deploysb --slack alia,zhenguo,xin</code></li>
</ol>
