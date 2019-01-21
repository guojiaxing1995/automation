# automation
自动化测试平台

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过vue element + python flask实现前后端分离的自动化测试平台，并配套辅助小程序工具。目前完成接口测试部分，包含功能：接口测试、定时任务、用例批量执行、查看执行报告和查询用例执行记录。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;项目目前已经上线 PC端：https://automation.guojiaxing.red/ &nbsp;小程序端：![自动化测试助手]<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/wei-mini.jpg" width="100"/>

## PC端
#### 接口测试
![接口测试](https://github.com/guojiaxing1995/automation/blob/master/github_img/接口测试.jpg)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;一个类似postman的接口请求功能。输入url、data、header和预期结果进行接口访问，如果预期结果在接口返回中则认为通过，反之失败。注：所有标点符号必须是英文，目前只支持json返回格式的接口，所以请不要请求百度ㄟ(≧◇≦)ㄏ。

#### 批量执行
![批量执行](https://github.com/guojiaxing1995/automation/blob/master/github_img/批量执行1.jpg)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;左边列表为项目列表，选择项目右边表格会刷新对应的用例。点击运行按钮批量执行一个项目的用例。用例与用例之间如果有依赖关系，则会先执行被依赖的用例。此外还支持用例的增删改查和通过excel表格批量导入的功能。

![批量执行](https://github.com/guojiaxing1995/automation/blob/master/github_img/批量执行2.jpg)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;对于依赖用例的数据处理，提供了如图中的3种处理方法。默认处理，不需要填写处理语句，系统会将当前接口返回的每一对key-value值以键值对存储；获取key值保存，系统通过填写的key获取当前用例接口返回的value值，并给其一个新的key值保存起来，例如(key,new_key);正则表达式，通过python正则表达式匹配接口返回中第一个符合的值并为其指定一个key保存起来，例如(正则，key)。在data中可以通过$key$来获取已经运行过的接口的处理数据。

![批量执行](https://github.com/guojiaxing1995/automation/blob/master/github_img/批量执行3.jpg)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;执行完毕后，点击一条用例会弹出这条用例的详细信息。

#### 定时任务
![定时任务](https://github.com/guojiaxing1995/automation/blob/master/github_img/定时任务.jpg)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;以项目为单位设置定时任务，系统会在设定的时间自动批量执行该项目的用例，执行完毕后会给维护人和填写的抄送人邮箱发送报告邮件。除此之外支持定时任务的删除和修改。

#### 执行报告
![执行报告](https://github.com/guojiaxing1995/automation/blob/master/github_img/执行报告.jpg)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;以项目为单位展示本周执行结果折线图和当日执行结果饼图。

#### 记录查询
![记录查询](https://github.com/guojiaxing1995/automation/blob/master/github_img/记录查询.jpg)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;条件查询所有批量执行过的所有记录。

## 小程序端
自动化测试工具。PC端自动化测试平台的辅助工具。可一键执行批量测试，也可方便的查看用例详情，执行结果和执行报告。


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/1.jpg" width="260"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/2.jpg" width="260"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/3.jpg" width="260" />


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/4.jpg" width="260"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/5.jpg" width="260"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/guojiaxing1995/automation/blob/master/github_img/6.jpg" width="260" />


方便快速查看，前端（PC、小程序）未作账户体系，但后端flask已经实现，具体可查看代码。
