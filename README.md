# HoverSpace

## Configuration Instructions

1. **Fork** the repository and clone it locally

2. Install [pip](http://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3)

3. Install [virtualenv](http://www.howopensource.com/2011/05/installation-of-virtualenv-in-linux/)

4. Install [docker](https://docs.docker.com/engine/installation/linux/ubuntulinux/)

5. **Pull MongoDB** using `docker pull mongod`.

6. Create **mongo instance** using `docker run --name mongo -p 27017:27017 -d mongo`

7. Create **virtual environment** using `virtualenv env` and then **activate** it using `source env/bin/activate`

8. Install **dependencies** using `pip install -r requirements.txt`  

9. Set environment variables using `export` command  
    `export APP_SETTINGS="config.DevelopmentConfig"`

10. **deactivate** virtual environment by using `deactivate`  
 Reactivate your virtualenv using `source env/bin/activate`


## Contributing

1. Create your **_branch_**: `git checkout -b my-new-feature`

2. **_Commit_** your changes: `git commit -m 'Add some feature'`

3. **_Push_** to the branch: `git push origin my-new-feature`

4. Send a **Pull Request**

5. **_Enjoy!_**

## Resources
 * [Pymongo](http://api.mongodb.com/python/current/index.html)
