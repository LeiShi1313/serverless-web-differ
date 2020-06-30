<p align="center">
    <h2 align="center">Serverless Web Differ</h2>
</p>

<p align="center">一个基于<a href="http://serverless.com/">Serverless</a>，<a href="https://aws.amazon.com/lambda/">AWS Lambda</a>，<a href="https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md">Headless Chrome</a> 和<a href="https://selenium-python.readthedocs.io/">Selenium</a>，运行在云端的浏览器。</p>

<p align="center">
    <b><a href="#能做什么">能做什么</a></b>
    |
    <b><a href="#环境准备">环境准备</a></b>
    |
    <b><a href="#配置">配置</a></b>
    |
    <b><a href="#部署">部署</a></b>
</p>

## 能做什么

- 在无需自己部署的服务器的云上运行无头浏览器.
- 浏览网页并且通过xpath提取页面元素并与预设值比较.
- 如有不同发送推送通知.

## 环境准备

0. 首先你需要一个AWS账号，和具有lambda权限的`aws_access_key_id`和`aws_secret_access_key`。如果你还没有账号，可以去[这里](https://portal.aws.amazon.com/billing/signup#/start)注册一个账号，然后看[这儿](https://docs.aws.amazon.com/zh_cn/general/latest/gr/managing-aws-access-keys.html)来取得访问密钥。
1. 安装[node](https://nodejs.org/)，并确认`npm`能成功运行。
2. 安装Serverless: `npm install -g serverless`
3. 配置serverless使用aws的密钥：`sls config credentials -p aws -k aws_access_key_id -s aws_secret_access_key`
4. Clone这个仓库：`git clone https://github.com/LeiShi1313/serverless-web-differ.git`
5. 安装依赖：`cd serverless-web-differ && npm install`

## 配置

在部署前有很多东西可以配置，你可以参考仓库里的`config.yml`以及`config.yml.example`文件，下面是各个配置项的解释：

- `events`: 这是定义这个小程序运行频率的地方，具体可以参考[这里(英文)](https://serverless.com/framework/docs/providers/aws/events/schedule/)或者[这里(中文)](https://docs.aws.amazon.com/zh_cn/AmazonCloudWatch/latest/events/ScheduledEvents.html)。大部分时候，你可以简单地写成：`- schedule: rate(1 hour)`或者`- schedule: cron(0 * * * ? *)`，这俩都是每小时跑一次的意思。
- `server_chan`/`sendgrid`/`ifttt`/`pushbullet`: 设置推送的方式，现在只支持这4种，你也可以在`notify.py`自己添加自己喜欢的方式，大部分时候就是一个简单的POST。在`config.yml.example`里有怎么设置的各种key的解释，也可以通过设置环境变量的方式来设置这些推送方式的访问密钥。
- `websites`: 这是最主要的配置部分。你可以在`websites`设置多个项目，每个都包含一个`url`和`xpath`，分别对应你要监控的网页和网页上页面元素对应的xpath。你要是不知道怎么获取xpath，用chrome打开对应的网页，在你想要监控变化的页面元素上邮件->审查元素->在对应html上邮件复制->复制xpath就好了。`original`就是你要监控的页面元素的初始值。

## 部署

得益于serverless，部署非常简单：
```
sls deploy
```
就可以了:tada::tada::tada:
