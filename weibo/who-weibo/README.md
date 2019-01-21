
## 简介
 
**使用 weibo 图片 url 找出发图人 ID**

1. 例如链接

    ```plain
    http://wx1.sinaimg.cn/mw690/9d0d09abgy1fj0wcs7aewj20ij0sn12y.jpg
    ```
    
    提取文件名`9d0d09abgy1fj0wcs7aewj20ij0sn12y`，前8位`9d0d09ab`用**16进制**转换下变为`2634877355`，就是用户 uid

2. 如果是`005`、`006`开头的就用**62进制**转换

    ```plain
    http://wx1.sinaimg.cn/mw690/006r2HqOgy1fj7dxg3zuxj30p02a1wry.jpg
    ```
    
    P.S. 为什么出现这个应该是发现 8 位 16 进制存不下了

## Ref

1. https://www.v2ex.com/t/388152
2. https://gist.github.com/zh-h/c5adc0dc4f0b96b00040aab9b8df93e6

