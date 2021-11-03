# Windows Setup

## Downloading

1. First off make a github account at <https://github.com> if you haven't yet
2. Download git from <https://git-scm.com/download/win>
3. Open the exe file that downloads when you open the site
4. Click next till you get to this screen:

![Git installer text editor choose screen](/static/choose_text_editor.png)

5. Choose a text editor other then vim, there are many options, but nano, visual studio code or notepad++(you will need to download these separately first at <https://code.visualstudio.com/download>, <https://notepad-plus-plus.org/downloads> respectively) are good choices

## Git Setup

1. When you download git it will download something called git-bash open it (search for it in the search bar)
2. First set up your details with:

```console
$ git config --global user.email "youremail@email.com"
```

```console
$ git config --global user.email "Your Name"
```

3. Then generate a ssh key for authenticating to github with:

```console
$ ssh-keygen
```

4. To access the key you just created use and copy the output:

```console
$ cat ~/.ssh/id_rsa.pub
```

5. Add the the key to github by going to <https://github.com/settings/ssh/new> and pasting it into the key input box

## Getting the Project

1. Go back to git bash and execute these commands:

```console
$ cd ~
```

```console
$ mkdir dev
```

```console
$ cd dev
```

```console
$ git clone git@github.com:gabydinnerdavid/face.git
```

2. Now you can open the project with your favorite editor/ide and contribute

## Using git to synchronize

1. When are you are finished making a change to the code then you can commit all your changes with:

```console
$ git stage -A
$ git commit -a -m "your change"
```

2. To add your changes to the remote repository you are going to use (you need to be a contributer to do this so send me your github username):

```console
$ git push origin master
```

3. When you want to sync your local code with the remote repository you are going to use (note you have to commit all your changes before you can do this):

```console
$ git pull origin master
```
