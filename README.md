# 邮局订报管理系统
## 功能支持
+ 订报功能
+ 报刊管理
+ 用户管理
+ 订单统计
+ 三级用户权限

## 使用方法
1. 将papermamnagment.sql文件导入数据库
2. 打开papermanagment项目，修改secrets.toml文件的星号为自己root用户的密码。如有需要也可以修改root为其他用户
3. papermanagment文件夹为项目文件夹。在项目文件夹的下终端输入 streamlit run app.py ‘

## ToDo
+ 使用加密算法对密码明文进行加密，在数据库中存储密文
