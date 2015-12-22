##Yahoo Finance Stock Price
从Yahoo Finance上获取当前股票成交价,写入mysql.
###需要
MySQLdb
###说明
####配置
在config.json里填写mysql的用户名和密码.
####Mysql
会自动创建stock_data数据库和stock_price表.
####多线程
多线程抓取
###使用
python multi_yahoo.py
###结果
```
# symbol, last_price
'AAOI', '17'
'AAON', '22.85'
'AAPC', '10.1'
'AAPL', '107.33'
'AAVL', '9.69'
'AAWW', '41.38'
.....
.....
```