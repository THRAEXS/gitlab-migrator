# GitLab Community Edition数据迁移

使用`gitlab-ce` API进行私有仓库数据迁移，从`9.5.4`迁至`12.4.2`。因版本不同，无法使用`gitlab-rake`工具进行`backup`/`restore`。

## 配置

`src/config.py`:

- `SOURCE`: 老版本GitLab地址(端口`80`)与访问令牌

- `TARGET`: 新版本GitLab(`test`/`prod`)地址与访问令牌

## 用法

``` sh
$ python3 src/<users | groups | groups-members>.py [test | prod]
```
