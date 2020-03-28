
(env) [scfan@fdm baiduyun]$ 
(env) [scfan@fdm baiduyun]$ diff level3.txt  a
1c1
< https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=RF4dg&url=rZ77gBdjtsPwguXYUH/epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m=
---
> https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=dC8mW&url=rZ77gBdjtsPwguXYUH/epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m=
(env) [scfan@fdm baiduyun]$ env3
(env36) [scfan@fdm baiduyun]$ ipython
Python 3.6.8 (default, Aug  7 2019, 17:28:10) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.10.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]:                                                                                                                                                                                                                                                                                             

In [1]: !cat level3.txt                                                                                                                                                                                                                                                                             
https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=RF4dg&url=rZ77gBdjtsPwguXYUH/epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m=

In [2]: !cat a                                                                                                                                                                                                                                                                                      
https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=dC8mW&url=rZ77gBdjtsPwguXYUH/epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m=

In [3]: import difflib                                                                                                                                                                                                                                                                              

In [4]: url1 = "https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=RF4dg&url=rZ77gBdjtsPwguXYUH
   ...: /epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m="                                                                                                                                                          

In [5]: url2 = "https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=dC8mW&url=rZ77gBdjtsPwguXYUH
   ...: /epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m="                                                                                                                                                          

In [6]: d=difflib.Differ()                                                                                                                                                                                                                                                                          

In [7]: diff=d.compare(url1.splitlines(),url2.splitlines())                                                                                                                                                                                                                                         

In [8]: diff                                                                                                                                                                                                                                                                                        
Out[8]: <generator object Differ.compare at 0x7fada722c888>

In [9]: print('\n'.join(list(diff)))                                                                                                                                                                                                                                                                
- https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=RF4dg&url=rZ77gBdjtsPwguXYUH/epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m=
?                                                                                                                                                                                                                                                         ^^^^^

+ https://www.pansoso.com/url/?t=rZP7jBd0ttbwneXQUGDeu1U2hjK7fMxIySu/DVCdvlmtbftKF/%2B2EvBZ5QVQ4t40VeyGV7tgzOPJKb8gULe%2BWq17%2B1oX8LYN8H/lB1Dc3hxVKYYwu1LMSskqvyVQj75ZrW37Shf/thLwWeXOULXeAFWthjG7acxPySq/LlC5vlStV/tcF0y2VfBt5VNQtN4xVZCGMrtQzH3Jkg==&a=dC8mW&url=rZ77gBdjtsPwguXYUH/epVV1hra7h8zgya2/1FBuvtitg/vaF3S23PCc5c1QI96lVTSG47uqzKvJvb/7UEK%2B/q3F%2B8AXfbbB8LTlqFAc3stVNoacu5rMl8m4v4BQcA==&dx=rcf7vxdV&m=
?     


