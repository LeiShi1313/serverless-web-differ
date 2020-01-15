<p align="center">
    <h2 align="center">Serverless Web Differ</h2>
</p>

<p align="center">A serverless web browser which crawls websites and compares pages by schedule, with <a href="http://serverless.com/">Serverless</a>, <a href="https://aws.amazon.com/lambda/">AWS Lambda</a>, <a href="https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md">Headless Chrome</a> and <a href="https://selenium-python.readthedocs.io/">Selenium</a>!</p>

<p align="center">
    <b><a href="#what-it-can-do">What it can do</a></b>
    |
    <b><a href="#prerequisites">Prerequisites</a></b>
    |
    <b><a href="#configuration">Configuration</a></b>
    |
    <b><a href="#deploy">Deploy</a></b>
</p>

## What it can do

- Runs headless chrome in a serverless environement.
- Finds web elements with xpath and compares it.
- Send notifications/emails if something has changed.

## Prerequisites

0. You need to have a aws account, `aws_access_key_id` and `aws_secret_access_key`. If you don't an account yet, go to [here](https://portal.aws.amazon.com/billing/signup#/start) to sign up for one, and then follow the instructions [here](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/) to get the key_id and access key.
1. Install [node](https://nodejs.org/en/download/) and make sure `npm` is available in your path.
2. Install docker from [here](https://docs.docker.com/install/).
3. Install Serverless: `npm install -g serverless`
4. Configure serverless with aws, using the `aws_access_key_id` and `aws_secret_access_key` from step 0: `sls config credentials -p aws -k aws_access_key_id -s aws_secret_access_key`
5. Clone this project: `git clone https://github.com/LeiShi1313/serverless-web-differ.git`
6. Install the dependencies: `cd serverless-web-differ && npm install`

## Configuration

There are couple of things you need to configure before actually make the function running in the cloud. First you need to create a file called `config.yml` and copy/paste everything from `config.yml.example`. Inside the `config.yml`:

- `events`: This is the place you can define what is the frequency the function runs, you can read more from [here](https://serverless.com/framework/docs/providers/aws/events/schedule/). But most of the time, you want one entry like `- schedule: rate(1 hour)` or `- schedule: cron(0 * * * ? *)`, which both means run the function every hour.
- `server_chan`/`sendgrid`/`ifttt`: There are the pre-defined ways to notify you if something has changed on the websites you interested. You can read the comments to find out how to get the security keys.
- `websites`: This is the main configuration part. `websites` can have multiple entries, and each one represents a website you want to periodically check. `url` and `xpath` is easy to understand, if you don't know how to get the xpath, try search `xpath [THE BROWSER YOU ARE USING]`, you should be able to find a lot of informations. For `original`, actually it can be absent if you are expecting a web element will appear, otherwise the function will compare the EXACT text from `original` and the web element of the web page by `xpath`.

## Deploy

This is simple, when everything is all set, run:
```
sls deploy
```
and :tada::tada::tada:

## TODO

- [ ] For each `website`, deploy a lambda function instead of visiting all websites in one function.
- [ ] Make `notify.py` another lambda function.
- [ ] Add more ways to notify.
- [ ] Maybe move `notify.py` to another project and make a submodule here?
- [ ] Provide a headerless chrome docker image
- [ ] Options for other cloud provider: Google Cloud, Aliyun, etc