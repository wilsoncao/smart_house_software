=======================================================
                         开始
=======================================================
首先，小Q第一次接入电脑时访问拒绝，没有权限，解决方法如下：
把55-qrobot.rules文件放到目录 /etc/udev/rules.d

=================================================================
                         安装依赖库步骤
=================================================================
打开新立得软件，找下面的依赖库，若没安装就标记安装
(也可以同去终端apt-get install (下面括号内的软件包名称) 去安装依赖库)
1.libusb (libusb-1.0.0)

=========================================================
                        编译与安装
=========================================================
进入主目录后,执行以下命令
>>>mkdir build     新建build目录
>>>cd build        进入build目录
>>>cmake ..        生成MakeFile
>>>make            构建项目

======================================================================
                                  注意
======================================================================
关于GetHeadPosition函数，使用者最好自己测一下，看看能得到的头部位置的范围
